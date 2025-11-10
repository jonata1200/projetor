import json
import os
import uuid
# --- IMPORTAÇÃO MODIFICADA ---
from core.paths import MUSIC_DB_PATH

class MusicManager:
    def __init__(self):
        self.music_database = []
        self.load_music_db()

    def _generate_slides_from_lyrics(self, lyrics_full):
        if not lyrics_full:
            return []
        slides = [slide.strip() for slide in lyrics_full.strip().split('\n\n') if slide.strip()]
        return slides

    def load_music_db(self):
        try:
            if os.path.exists(MUSIC_DB_PATH):
                with open(MUSIC_DB_PATH, 'r', encoding='utf-8') as f:
                    self.music_database = json.load(f)
                    for music in self.music_database:
                        if 'slides' not in music or not music['slides']:
                            music.get('lyrics_full', '')
            else:
                self.music_database = []
        except (json.JSONDecodeError, IOError) as e:
            print(f"Erro ao carregar o banco de dados de músicas: {e}")
            self.music_database = []
        return self.music_database

    def save_music_db(self):
        try:
            # Garante que o diretório 'data' exista
            os.makedirs(os.path.dirname(MUSIC_DB_PATH), exist_ok=True)
            with open(MUSIC_DB_PATH, 'w', encoding='utf-8') as f:
                json.dump(self.music_database, f, ensure_ascii=False, indent=2)
            return True
        except IOError as e:
            print(f"Erro ao salvar o banco de dados de músicas: {e}")
            return False

    def is_duplicate(self, title, artist):
        """
        Verifica se uma música com o mesmo título e artista já existe.
        A verificação não diferencia maiúsculas de minúsculas e ignora espaços extras.
        """
        title_lower = title.lower().strip()
        artist_lower = artist.lower().strip()
        for music in self.music_database:
            if music.get('title', '').lower().strip() == title_lower and \
               music.get('artist', '').lower().strip() == artist_lower:
                return True
        return False

    def get_all_music_titles_with_artists(self):
        sorted_music = sorted(self.music_database, key=lambda x: x.get('title', '').lower())
        return [(music.get('id', ''), f"{music.get('title', 'N/A')} - {music.get('artist', 'N/A')}")
                for music in sorted_music]

    def get_music_by_id(self, music_id):
        for music in self.music_database:
            if music.get('id') == music_id:
                return music
        return None

    def get_lyrics_slides(self, music_id):
        music = self.get_music_by_id(music_id)
        if music and 'slides' in music:
            return music['slides']
        return []

    def add_music(self, title, artist, lyrics_full):
        if not title or not artist or not lyrics_full:
            return None
        new_id = str(uuid.uuid4())
        slides = self._generate_slides_from_lyrics(lyrics_full)
        new_music = {
            "id": new_id,
            "title": title.strip(),
            "artist": artist.strip(),
            "lyrics_full": lyrics_full.strip(),
            "slides": slides
        }
        self.music_database.append(new_music)
        if self.save_music_db():
            return new_music
        else:
            # Se salvar falhar, remove a música que foi adicionada apenas na memória.
            self.music_database.pop() 
            return None

    def edit_music(self, song_id, new_title, new_artist, new_lyrics_full):
        if not all([song_id, new_title, new_artist, new_lyrics_full]):
            return False

        for music in self.music_database:
            if music.get('id') == song_id:
                music['title'] = new_title.strip()
                music['artist'] = new_artist.strip()
                music['lyrics_full'] = new_lyrics_full.strip()
                music['slides'] = self._generate_slides_from_lyrics(new_lyrics_full)
                return self.save_music_db()
        return False

    def delete_music(self, song_id):
        if not song_id:
            return False
        
        # Faz um backup do estado atual caso o salvamento falhe
        original_database = [dict(d) for d in self.music_database]
        
        original_length = len(self.music_database)
        self.music_database = [music for music in self.music_database if music.get('id') != song_id]
        
        if len(self.music_database) < original_length:
            if self.save_music_db():
                return True
            else:
                # Se salvar falhou, restaura o banco de dados em memória para o estado anterior.
                self.music_database = original_database
                return False
        return False # Retorna False se o song_id não foi encontrado