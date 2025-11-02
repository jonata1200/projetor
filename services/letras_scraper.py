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

    def _clean_text(self, lyrics_container_element):
        """Limpa o texto, priorizando o conteúdo de tags <p> como estrofes separadas por \n\n."""
        if not lyrics_container_element:
            return ""

        estrofes_textos = []
        paragraphs = lyrics_container_element.find_all('p', recursive=True)

        if paragraphs:
            for p_tag in paragraphs:
                for br in p_tag.find_all('br'):
                    br.replace_with('\n')
                
                p_text = p_tag.get_text(separator='\n').strip() 
                
                if p_text:
                    linhas_limpas_da_estrofe = [linha.strip() for linha in p_text.split('\n') if linha.strip()]
                    if linhas_limpas_da_estrofe:
                        estrofes_textos.append("\n".join(linhas_limpas_da_estrofe))
            
            full_lyrics = "\n\n".join(estrofes_textos)
        
        else:
            for br in lyrics_container_element.find_all('br'):
                br.replace_with('\n')
            full_lyrics = lyrics_container_element.get_text(separator='\n').strip()
            full_lyrics = re.sub(r'\n\s*\n(\s*\n)*', '\n\n', full_lyrics)

        full_lyrics = re.sub(r'(\n\s*){3,}', '\n\n', full_lyrics.strip())
        
        return full_lyrics.strip()

    def search_music_url(self, artist_name, song_title):
        artist_raw_slug = artist_name.lower().replace(" ", "-")
        title_raw_slug = song_title.lower().replace(" ", "-")
        artist_slug = unidecode(artist_raw_slug)
        title_slug = unidecode(title_raw_slug)
        query = f"{artist_name} {song_title}".replace(" ", "+")
        search_url = f"{self.BASE_URL_SEARCH}/?q={query}"
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
            response = requests.get(search_url, headers=headers, timeout=15)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            song_links = soup.find_all('a', href=True)
            best_match_url = None
            expected_href_part = f"/{artist_slug}/{title_slug}"
            for link in song_links:
                href_lower = link['href'].lower()
                if expected_href_part in href_lower and not href_lower.startswith("http"):
                    best_match_url = self.BASE_URL_SEARCH + link['href']
                    return best_match_url
            for link in song_links:
                href = link['href'].lower()
                link_text = link.get_text().lower()
                if artist_slug in href and title_slug in href and not href.startswith("http") and href.count('/') >= 2:
                    best_match_url = self.BASE_URL_SEARCH + link['href']
                    break 
                elif best_match_url is None and artist_name.lower() in link_text and song_title.lower() in link_text and not href.startswith("http") and href.count('/') >= 2:
                    best_match_url = self.BASE_URL_SEARCH + link['href']
            return best_match_url
        except requests.exceptions.RequestException:
            return None

    def fetch_lyrics_from_url(self, song_url):
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
            response = requests.get(song_url, headers=headers, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            title = "Título Desconhecido"
            artist = "Artista Desconhecido"

            title_tag = soup.find('h1', class_='textStyle-primary')
            if title_tag:
                title = title_tag.get_text(strip=True)
            else:
                old_title_container = soup.find('div', class_='cnt-head_title')
                if old_title_container and old_title_container.find('h1'):
                    title = old_title_container.find('h1').get_text(strip=True)
                else:
                    print(f"AVISO: Título não encontrado com 'h1.textStyle-primary' nem com o seletor antigo em {song_url}")

            artist_tag = soup.find('h2', class_='textStyle-secondary')
            if artist_tag:
                artist_link_inside_h2 = artist_tag.find('a')
                if artist_link_inside_h2:
                    artist = artist_link_inside_h2.get_text(strip=True)
                else:
                    artist = artist_tag.get_text(strip=True)
            else:
                old_title_container = soup.find('div', class_='cnt-head_title')
                if old_title_container and old_title_container.find('h2'):
                    old_artist_h2 = old_title_container.find('h2')
                    old_artist_link = old_artist_h2.find('a')
                    if old_artist_link:
                        artist = old_artist_link.get_text(strip=True)
                    else:
                        artist = old_artist_h2.get_text(strip=True)
                else:
                    print(f"AVISO: Artista não encontrado com 'h2.textStyle-secondary' nem com o seletor antigo em {song_url}")

            lyrics_container = soup.find('div', class_='lyric-original') 
            if not lyrics_container:
                lyrics_container = soup.find('div', class_=['cnt-letra', '歌詞', 'lyric-cnt', 'js-lyric-cnt'])
            
            if lyrics_container:
                lyrics_text = self._clean_text(lyrics_container)
            else:
                lyrics_text = None

            if lyrics_text and lyrics_text.strip():
                return {"title": title, "artist": artist, "lyrics_full": lyrics_text.strip()}
            else:
                return None

        except requests.exceptions.HTTPError as http_err:
            return None
        except requests.exceptions.RequestException as req_err:
            return None
        except Exception as e:
            return None

    def search_and_fetch_lyrics(self, artist_name, song_title):
        song_url = self.search_music_url(artist_name, song_title)
        if song_url:
            return self.fetch_lyrics_from_url(song_url)
        else:
            return None

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