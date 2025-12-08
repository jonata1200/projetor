import requests
from bs4 import BeautifulSoup
from typing import Optional, List, Dict
import re
import logging
from core.exceptions import ScraperError, ScraperNetworkError, ScraperParseError, ValidationError
from core.validators import validate_url

logger = logging.getLogger(__name__)

class LetrasScraper:
    BASE_URL_SEARCH = "https://www.letras.mus.br"
    
    # --- SELETORES ATUALIZADOS ---
    # Colocamos os seletores mais recentes e específicos no início da lista.
    TITLE_SELECTORS: List[str] = ['div.title-content h1.textStyle-primary', 'h1.textStyle-primary', 'div.cnt-head_title h1']
    ARTIST_SELECTORS: List[str] = ['div.title-content h2.textStyle-secondary', 'div.song-title a', 'h2.textStyle-secondary a', 'div.cnt-head_title h2 a']
    LYRICS_CONTAINER_SELECTORS: List[str] = ['div.lyric-original', 'div.cnt-letra', 'div.歌詞', 'div.lyric-cnt', 'div.js-lyric-cnt']

    def _find_element_text(self, soup: BeautifulSoup, selectors: List[str]) -> Optional[str]:
        """Tenta encontrar um elemento usando uma lista de seletores e retorna seu texto."""
        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                return element.get_text(strip=True)
        return None

    def _find_element_container(self, soup: BeautifulSoup, selectors: List[str]) -> Optional[BeautifulSoup]:
        """Tenta encontrar um elemento container usando uma lista de seletores."""
        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                return element
        return None

    def _clean_text(self, lyrics_container_element: Optional[BeautifulSoup]) -> str:
        """Limpa o texto, priorizando o conteúdo de tags <p> como estrofes separadas por \n\n."""
        if not lyrics_container_element:
            return ""

        for unwanted in lyrics_container_element.select('.send-lyrics, .translate-lyrics'):
            unwanted.decompose()

        estrofes_textos = []
        paragraphs = lyrics_container_element.find_all('p', recursive=True)

        if paragraphs:
            for p_tag in paragraphs:
                for br in p_tag.find_all('br'):
                    br.replace_with('\n')
                
                p_text = p_tag.get_text(separator='\n').strip() 
                if p_text:
                    linhas_limpas = [linha.strip() for linha in p_text.split('\n') if linha.strip()]
                    if linhas_limpas:
                        estrofes_textos.append("\n".join(linhas_limpas))
            full_lyrics = "\n\n".join(estrofes_textos)
        else:
            for br in lyrics_container_element.find_all('br'):
                br.replace_with('\n')
            full_lyrics = lyrics_container_element.get_text(separator='\n').strip()
            full_lyrics = re.sub(r'\n\s*\n(\s*\n)*', '\n\n', full_lyrics)

        return re.sub(r'(\n\s*){3,}', '\n\n', full_lyrics.strip())

    def fetch_lyrics_from_url(self, song_url: str) -> Dict[str, str]:
        # Fail Fast: Validar URL no início
        song_url = validate_url(song_url, allowed_domains=['letras.mus.br'])
        
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
            response = requests.get(song_url, headers=headers, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            title = self._find_element_text(soup, self.TITLE_SELECTORS) or "Título Desconhecido"
            artist = self._find_element_text(soup, self.ARTIST_SELECTORS) or "Artista Desconhecido"

            lyrics_container = self._find_element_container(soup, self.LYRICS_CONTAINER_SELECTORS)
            
            if lyrics_container:
                lyrics_text = self._clean_text(lyrics_container)
            else:
                logger.warning(f"Scraper não encontrou o container da letra em {song_url}")
                raise ScraperParseError(f"Não foi possível encontrar o container da letra na URL: {song_url}")

            if lyrics_text and lyrics_text.strip():
                return {"title": title, "artist": artist, "lyrics_full": lyrics_text.strip()}
            else:
                logger.warning(f"Scraper encontrou o container mas não conseguiu extrair a letra em {song_url}")
                raise ScraperParseError(f"Não foi possível extrair a letra da música na URL: {song_url}")

        except requests.exceptions.RequestException as req_err:
            logger.error(f"Scraper falhou na requisição para {song_url}", exc_info=True)
            raise ScraperNetworkError(f"Erro de rede ao acessar {song_url}: {req_err}") from req_err
        except ScraperError:
            # Re-levanta exceções de ScraperError (ScraperParseError)
            raise
        except Exception as e:
            logger.error(f"Scraper teve um erro inesperado em {song_url}", exc_info=True)
            raise ScraperError(f"Erro inesperado ao fazer scraping de {song_url}: {e}") from e