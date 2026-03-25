import requests
import os
import time

class GitHubClient:
    BASE_URL = "https://api.github.com"

    def __init__(self):
        self.token = os.getenv("GITHUB_TOKEN")
        self.headers = {
            "Accept": "application/vnd.github.v3+json"
        }
        if self.token:
            self.headers["Authorization"] = f"token {self.token}"

    def search_popular_repos(self, language, page=1):
        """Busca repositorios por lenguaje y estrellas."""
        url = f"{self.BASE_URL}/search/repositories"
        params = {
            "q": f"language:{language} stars:>100",
            "sort": "stars",
            "order": "desc",
            "page": page,
            "per_page": 5
        }
        response = requests.get(url, headers=self.headers, params=params)
        
        if response.status_code == 403:
            print("Límite de API alcanzado. Esperando 60 segundos...")
            time.sleep(60)
            return []
            
        return response.json().get("items", [])

    def get_repo_files(self, full_name):
        """Obtiene la lista de archivos de un repositorio (recursivo)."""
        url = f"{self.BASE_URL}/repos/{full_name}/git/trees/HEAD?recursive=1"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.json().get("tree", [])
        return []

    def download_file(self, url):
        """Descarga el contenido de un archivo (Raw)."""
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            import base64
            content_b64 = response.json().get("content", "")
            return base64.b64decode(content_b64).decode('utf-8', errors='ignore')
        return ""