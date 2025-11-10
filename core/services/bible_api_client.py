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