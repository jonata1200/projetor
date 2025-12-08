import requests
import os
from typing import Dict, List, Optional, Any
from dotenv import load_dotenv
import json
import logging
from core.exceptions import BibleAPIError

load_dotenv()

logger = logging.getLogger(__name__)

class BibleAPIClient:
    BASE_URL = "https://www.abibliadigital.com.br/api"

    def __init__(self, token: Optional[str] = None) -> None:
        self.token: Optional[str] = token or os.getenv("BIBLE_API_TOKEN")
        if not self.token:
            logger.warning("Token da API da Bíblia Digital não configurado. Algumas funcionalidades podem ser limitadas.")

    def _make_request(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Any:
        headers = {}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        
        response = None
        try:
            response = requests.get(f"{self.BASE_URL}{endpoint}", headers=headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            status_code = response.status_code if response is not None else None
            logger.error(
                f"Erro na API da Bíblia - endpoint: {endpoint}, params: {params}, status: {status_code}",
                exc_info=True
            )
            raise BibleAPIError(f"Erro ao fazer requisição para {endpoint}: {e}") from e
        except json.JSONDecodeError as e:
            response_text = response.text if response is not None else "Nenhuma resposta recebida"
            logger.error(
                f"Erro ao decodificar JSON da API da Bíblia - endpoint: {endpoint}, resposta: {response_text}",
                exc_info=True
            )
            raise BibleAPIError(f"Erro ao decodificar resposta JSON da API: {e}") from e

    def get_versions(self) -> List[Dict[str, str]]:
        """Retorna uma lista de versões disponíveis."""
        return [
            {"version": "nvi", "name": "Nova Versão Internacional"},
            {"version": "acf", "name": "Almeida Corrigida Fiel"}
        ]

    def get_books(self, version_abbrev: str = "nvi") -> List[Dict[str, Any]]:
        data = self._make_request("/books")
        return [{"abbrev": book.get("abbrev", {}).get("pt", book.get("name").lower()[:3]), 
                 "name": book.get("name"),
                 "chapters": book.get("chapters"),
                 "testament": book.get("testament")} 
                for book in data]

    def get_chapter_verses(self, version_abbrev: str, book_abbrev: str, chapter_number: int) -> List[Dict[str, Any]]:
        endpoint = f"/verses/{version_abbrev}/{book_abbrev}/{chapter_number}"
        data = self._make_request(endpoint)
        if data and "verses" in data:
            return data["verses"]
        return []