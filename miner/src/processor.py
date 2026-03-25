import ast
import re
import javalang

class CodeProcessor:
    @staticmethod
    def split_name(name):
        """Separa camelCase y snake_case en palabras individuales."""
        parts = name.split('_')
        words = []
        for part in parts:
            camel_parts = re.sub('([A-Z][a-z]+)', r' \1', re.sub('([A-Z]+)', r' \1', part)).split()
            words.extend([w.lower() for w in camel_parts if len(w) > 1])
        return words

    def extract_python_methods(self, code):
        words = []
        try:
            tree = ast.parse(code)
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    if not node.name.startswith('__'):
                        words.extend(self.split_name(node.name))
        except:
            pass
        return words

    def extract_java_methods(self, code):
        words = []
        try:
            tree = javalang.parse.parse(code)
            for path, node in tree.filter(javalang.tree.MethodDeclaration):
                words.extend(self.split_name(node.name))
        except:
            pass
        return words