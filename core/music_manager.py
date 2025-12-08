import uuid
import logging
from typing import Dict, Optional, List, Tuple
# --- IMPORTAÇÃO MODIFICADA ---
from pathlib import Path
from core.paths import MUSIC_DB_PATH
from core.exceptions import MusicDatabaseError, ValidationError
from core.validators import validate_string
from core.utils.file_utils import save_json_file, load_json_file

logger = logging.getLogger(__name__)

class MusicManager:
    """
    Gerenciador do banco de dados de músicas.
    
    Responsável por todas as operações CRUD (Create, Read, Update, Delete)
    relacionadas a músicas. Utiliza índices O(1) para busca eficiente.
    
    Attributes:
        music_database: Lista de todas as músicas armazenadas
        _music_index: Índice mapeando ID → música (busca O(1))
        _title_artist_index: Índice mapeando (title, artist) → ID (duplicata O(1))
    """
    def __init__(self) -> None:
        """
        Inicializa o MusicManager e carrega o banco de dados.
        
        Constrói os índices de busca O(1) após carregar os dados.
        """
        self.music_database: List[Dict] = []
        # Índices para busca O(1)
        self._music_index: Dict[str, Dict] = {}  # ID → música
        self._title_artist_index: Dict[Tuple[str, str], str] = {}  # (title, artist) → ID
        self.load_music_db()

    def _generate_slides_from_lyrics(self, lyrics_full: str) -> List[str]:
        if not lyrics_full:
            return []
        slides = [slide.strip() for slide in lyrics_full.strip().split('\n\n') if slide.strip()]
        return slides

    def _rebuild_indexes(self) -> None:
        """
        Reconstrói os índices de busca O(1) a partir do banco de dados.
        
        Constrói:
        - _music_index: mapeia ID da música → objeto música
        - _title_artist_index: mapeia (title, artist) normalizado → ID da música
        """
        self._music_index.clear()
        self._title_artist_index.clear()
        
        for music in self.music_database:
            music_id = music.get('id')
            if not music_id:
                logger.warning("Música sem ID encontrada no banco de dados")
                continue
            
            # Índice ID → música
            self._music_index[music_id] = music
            
            # Índice (title, artist) → ID
            title = music.get('title', '').lower().strip()
            artist = music.get('artist', '').lower().strip()
            if title and artist:
                key = (title, artist)
                # Se já existe, loga aviso (duplicata no banco)
                if key in self._title_artist_index and self._title_artist_index[key] != music_id:
                    logger.warning(f"Duplicata encontrada no banco: '{title}' por '{artist}'")
                self._title_artist_index[key] = music_id

    def load_music_db(self) -> List[Dict]:
        self.music_database = load_json_file(Path(MUSIC_DB_PATH), default=[])
        
        # Garantir que slides existam para músicas antigas
        for music in self.music_database:
            if 'slides' not in music or not music['slides']:
                music.get('lyrics_full', '')
        
        # Reconstruir índices após carregar
        self._rebuild_indexes()
        
        return self.music_database

    def save_music_db(self) -> bool:
        save_json_file(Path(MUSIC_DB_PATH), self.music_database, ensure_ascii=False)
        return True

    def is_duplicate(self, title: str, artist: str) -> bool:
        """
        Verifica se uma música com o mesmo título e artista já existe.
        A verificação não diferencia maiúsculas de minúsculas e ignora espaços extras.
        
        Usa índice O(1) para busca eficiente.
        
        Args:
            title: Título da música
            artist: Artista da música
        
        Returns:
            bool: True se já existe uma música com mesmo título e artista
        """
        key = (title.lower().strip(), artist.lower().strip())
        return key in self._title_artist_index

    def get_all_music_titles_with_artists(self) -> List[Tuple[str, str]]:
        sorted_music = sorted(self.music_database, key=lambda x: x.get('title', '').lower())
        return [(music.get('id', ''), f"{music.get('title', 'N/A')} - {music.get('artist', 'N/A')}")
                for music in sorted_music]

    def get_music_by_id(self, music_id: str) -> Optional[Dict]:
        """
        Busca uma música pelo ID usando índice O(1).
        
        Args:
            music_id: ID da música a buscar
        
        Returns:
            Dict com dados da música ou None se não encontrada
        """
        return self._music_index.get(music_id)

    def get_lyrics_slides(self, music_id: str) -> List[str]:
        music = self.get_music_by_id(music_id)
        if music and 'slides' in music:
            return music['slides']
        return []

    def add_music(self, title: str, artist: str, lyrics_full: str) -> Optional[Dict]:
        # Fail Fast: Validar entradas no início
        title = validate_string(title, "título", min_length=1)
        artist = validate_string(artist, "artista", min_length=1)
        lyrics_full = validate_string(lyrics_full, "letra completa", min_length=1)
        
        new_id = str(uuid.uuid4())
        slides = self._generate_slides_from_lyrics(lyrics_full)
        new_music = {
            "id": new_id,
            "title": title,
            "artist": artist,
            "lyrics_full": lyrics_full,
            "slides": slides
        }
        self.music_database.append(new_music)
        
        # Atualizar índices incrementalmente (O(1))
        self._music_index[new_id] = new_music
        key = (title.lower().strip(), artist.lower().strip())
        self._title_artist_index[key] = new_id
        
        try:
            self.save_music_db()
            return new_music
        except MusicDatabaseError:
            # Se salvar falhar, remove a música que foi adicionada apenas na memória.
            self.music_database.pop()
            # Remover dos índices também
            del self._music_index[new_id]
            if key in self._title_artist_index:
                del self._title_artist_index[key]
            raise

    def edit_music(self, song_id: str, new_title: str, new_artist: str, new_lyrics_full: str) -> bool:
        # Fail Fast: Validar entradas no início
        if not song_id:
            raise ValidationError("ID da música não pode estar vazio")
        
        new_title = validate_string(new_title, "título", min_length=1)
        new_artist = validate_string(new_artist, "artista", min_length=1)
        new_lyrics_full = validate_string(new_lyrics_full, "letra completa", min_length=1)

        music = self._music_index.get(song_id)
        if not music:
            return False
        
        # Remover índice antigo se título/artista mudaram
        old_title = music.get('title', '').lower().strip()
        old_artist = music.get('artist', '').lower().strip()
        old_key = (old_title, old_artist)
        if old_key in self._title_artist_index:
            del self._title_artist_index[old_key]
        
        # Atualizar música
        music['title'] = new_title
        music['artist'] = new_artist
        music['lyrics_full'] = new_lyrics_full
        music['slides'] = self._generate_slides_from_lyrics(new_lyrics_full)
        
        # Atualizar índice novo
        new_key = (new_title.lower().strip(), new_artist.lower().strip())
        self._title_artist_index[new_key] = song_id
        
        self.save_music_db()  # Levanta exceção se falhar
        return True

    def delete_music(self, song_id: str) -> bool:
        if not song_id:
            return False
        
        music = self._music_index.get(song_id)
        if not music:
            return False
        
        # Faz um backup do estado atual caso o salvamento falhe
        original_database = [dict(d) for d in self.music_database]
        original_music_index = self._music_index.copy()
        original_title_artist_index = self._title_artist_index.copy()
        
        # Remover da lista
        self.music_database = [m for m in self.music_database if m.get('id') != song_id]
        
        # Remover dos índices
        if song_id in self._music_index:
            del self._music_index[song_id]
        
        title = music.get('title', '').lower().strip()
        artist = music.get('artist', '').lower().strip()
        key = (title, artist)
        if key in self._title_artist_index:
            del self._title_artist_index[key]
        
        try:
            self.save_music_db()  # Levanta exceção se falhar
            return True
        except MusicDatabaseError:
            # Se salvar falhou, restaura o banco de dados e índices para o estado anterior.
            self.music_database = original_database
            self._music_index = original_music_index
            self._title_artist_index = original_title_artist_index
            raise