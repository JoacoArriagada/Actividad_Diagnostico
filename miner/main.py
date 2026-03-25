import time
import os
from src.github_client import GitHubClient
from src.processor import CodeProcessor
from src.database import DatabaseManager
from dotenv import load_dotenv

load_dotenv()

def main():
    print("Iniciando Miner de nombres de métodos...")
    
    client = GitHubClient()
    processor = CodeProcessor()
    db = DatabaseManager()
    
    current_page = 1
    languages = ["Python", "Java"]

    while True:
        for lang in languages:
            print(f"Buscando repositorios populares en {lang} (Página {current_page})...")
            repos = client.search_popular_repos(lang, page=current_page)
            
            for repo in repos:
                repo_name = repo["full_name"]
                print(f"Procesando: {repo_name}")
                
                files = client.get_repo_files(repo_name)
                target_ext = ".py" if lang == "Python" else ".java"
                filtered_files = [f for f in files if f["path"].endswith(target_ext)][:10]

                for f in filtered_files:
                    content = client.download_file(f["url"])
                    if content:
                        if lang == "Python":
                            words = processor.extract_python_methods(content)
                        else:
                            words = processor.extract_java_methods(content)
                        
                        db.save_words(words)
                
                time.sleep(2)
        
        current_page += 1
        print("Ciclo de página completado")

if __name__ == "__main__":
    main()