import requests
import os
from dotenv import load_dotenv
import json

load_dotenv()

class BibleAPIClient:
    BASE_URL = "https://www.abibliadigital.com.br/api"

    def __init__(self, token=None):
        self.token = token or os.getenv("BIBLE_API_TOKEN")
        if not self.token:
            print("AVISO: Token da API da Bíblia Digital não configurado. Algumas funcionalidades podem ser limitadas.")

    def search_verses(self, version_abbrev, term):
        """
        Busca por versículos que contenham o termo fornecido.
        A API requer que o corpo da requisição seja um JSON, incluindo a versão.
        """
        # CORREÇÃO 1: A URL é fixa e não contém a versão.
        endpoint = "/verses/search"
        
        # CORREÇÃO 2: A versão é adicionada ao corpo (payload) da requisição.
        payload = {
            "version": version_abbrev,
            "search": term
        }
        
        headers = {
            "Content-Type": "application/json"
        }
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"

        response = None
        try:
            response = requests.post(f"{self.BASE_URL}{endpoint}", headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()
            return data.get("verses", [])
        except requests.exceptions.RequestException as e:
            if response is not None and response.status_code == 404:
                print(f"ERRO na API da Bíblia (busca): URL não encontrada - {e}")
            else:
                print(f"Erro na API da Bíblia (busca): {e}")
            return None
        except json.JSONDecodeError:
            response_text = response.text if response is not None else "Nenhuma resposta recebida"
            print(f"Erro ao decodificar JSON da API da Bíblia (busca). Resposta: {response_text}")
            return None

    def _make_request(self, endpoint, params=None):
        headers = {}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        
        response = None
        try:
            response = requests.get(f"{self.BASE_URL}{endpoint}", headers=headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Erro na API da Bíblia: {e}")
            return None
        except json.JSONDecodeError:
            response_text = response.text if response is not None else "Nenhuma resposta recebida"
            print(f"Erro ao decodificar JSON da API da Bíblia. Resposta: {response_text}")
            return None

    def get_versions(self):
        """Retorna uma lista de versões disponíveis."""
        return [
            {"version": "nvi", "name": "Nova Versão Internacional"},
            {"version": "acf", "name": "Almeida Corrigida Fiel"}
        ]

    def get_books(self, version_abbrev="nvi"):
        data = self._make_request("/books")
        if data:
            return [{"abbrev": book.get("abbrev", {}).get("pt", book.get("name").lower()[:3]), 
                     "name": book.get("name"),
                     "chapters": book.get("chapters"),
                     "testament": book.get("testament")} 
                    for book in data]
        return []

    def get_chapter_verses(self, version_abbrev, book_abbrev, chapter_number):
        endpoint = f"/verses/{version_abbrev}/{book_abbrev}/{chapter_number}"
        data = self._make_request(endpoint)
        if data and "verses" in data:
            return data["verses"] 
        return []

if __name__ == '__main__':
    client = BibleAPIClient()

    versions = client.get_versions()
    if versions:
        for v in versions:
            print(f"{v['name']} ({v['version']})")

    books = client.get_books()
    if books:
        for i, book in enumerate(books[:5]): 
            print(f"{book['name']} ({book['abbrev']['pt'] if isinstance(book['abbrev'], dict) else book['abbrev']}) - Capítulos: {book['chapters']}")
    
    if books:
        selected_book_abbrev = books[0]['abbrev']['pt'] if isinstance(books[0]['abbrev'], dict) else books[0]['abbrev'] 
        selected_version = "nvi"
        chapter = 1
        print(f"\n--- Versículos de {selected_book_abbrev.upper()} Cap. {chapter} ({selected_version.upper()}) ---")
        verses = client.get_chapter_verses(selected_version, selected_book_abbrev, chapter)
        if verses:
            for verse in verses[:3]: 
                print(f"{verse['number']}. {verse['text']}")
        else:
            print("Nenhum versículo encontrado ou erro na API.")
    else:
        print("Não foi possível carregar os livros para testar os versículos.")