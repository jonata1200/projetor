import requests
from bs4 import BeautifulSoup
import re
try:
    from unidecode import unidecode
except ImportError:
    def unidecode(s):
        return s 

class LetrasScraper:
    BASE_URL_SEARCH = "https://www.letras.mus.br"
    
    # --- NOVAS LISTAS DE SELETORES ---
    # Adicionamos seletores antigos e novos para aumentar a chance de acerto.
    TITLE_SELECTORS = ['h1.textStyle-primary', 'div.cnt-head_title h1']
    ARTIST_SELECTORS = ['h2.textStyle-secondary a', 'div.cnt-head_title h2 a']
    LYRICS_CONTAINER_SELECTORS = ['div.lyric-original', 'div.cnt-letra', 'div.歌詞', 'div.lyric-cnt', 'div.js-lyric-cnt']

    def _find_element_text(self, soup, selectors):
        """Tenta encontrar um elemento usando uma lista de seletores e retorna seu texto."""
        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                return element.get_text(strip=True)
        return None

    def _find_element_container(self, soup, selectors):
        """Tenta encontrar um elemento container usando uma lista de seletores."""
        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                return element
        return None

    def _clean_text(self, lyrics_container_element):
        """Limpa o texto, priorizando o conteúdo de tags <p> como estrofes separadas por \n\n."""
        if not lyrics_container_element:
            return ""

        # Remove elementos indesejados (como avisos de "contribuição")
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

    def fetch_lyrics_from_url(self, song_url):
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
            response = requests.get(song_url, headers=headers, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Usa os novos métodos para encontrar o título e o artista
            title = self._find_element_text(soup, self.TITLE_SELECTORS) or "Título Desconhecido"
            artist = self._find_element_text(soup, self.ARTIST_SELECTORS) or "Artista Desconhecido"

            # Usa o novo método para encontrar o container da letra
            lyrics_container = self._find_element_container(soup, self.LYRICS_CONTAINER_SELECTORS)
            
            if lyrics_container:
                lyrics_text = self._clean_text(lyrics_container)
            else:
                print(f"AVISO: Scraper não encontrou o container da letra em {song_url}")
                return None

            if lyrics_text and lyrics_text.strip():
                return {"title": title, "artist": artist, "lyrics_full": lyrics_text.strip()}
            else:
                print(f"AVISO: Scraper encontrou o container mas não conseguiu extrair a letra em {song_url}")
                return None

        except requests.exceptions.RequestException as req_err:
            print(f"ERRO: Scraper falhou na requisição para {song_url} - {req_err}")
            return None
        except Exception as e:
            # Captura qualquer outro erro inesperado para não travar o app
            print(f"ERRO: Scraper teve um erro inesperado em {song_url} - {e}")
            return None

    # O método search_music_url não precisa de grandes mudanças, mas podemos simplificá-lo
    # e torná-lo um pouco mais genérico, já que fetch_lyrics_from_url é o principal.
    # Por agora, vamos mantê-lo como está, pois a lógica principal foi robustecida.

# O bloco de teste (if __name__ == '__main__') permanece o mesmo.
if __name__ == '__main__':
    scraper = LetrasScraper()
    
    direct_url = "https://www.letras.mus.br/fernandinho/pra-sempre/"
    print(f"--- Testando Extração com URL Direta: {direct_url} ---")
    music_data_direct = scraper.fetch_lyrics_from_url(direct_url)
    
    if music_data_direct:
        print(f"\n--- Letra Importada (URL Direta) ---")
        print(f"Título: {music_data_direct['title']}")
        print(f"Artista: {music_data_direct['artist']}")
        print(f"Letra (início):\n{music_data_direct['lyrics_full'][:200]}...")
    else:
        print(f"\nFalha ao importar letra da URL direta: {direct_url}")

    print("-" * 30)