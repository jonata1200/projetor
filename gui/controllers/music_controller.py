import customtkinter as ctk
from tkinter import messagebox
from gui.dialogs import AddEditSongDialog
import threading
import logging
from core.exceptions import MusicDatabaseError, ScraperError, ValidationError
from core.validators import validate_url

logger = logging.getLogger(__name__)

class MusicController:
    """
    Controlador responsável por toda a lógica da aba de Músicas.
    Usa uma abordagem eficiente de esconder/mostrar widgets para a busca.
    """
    def __init__(self, master, view_widgets, music_manager, scraper, on_content_selected_callback, playlist_controller):
        self.master = master
        self.view = view_widgets
        self.manager = music_manager
        self.scraper = scraper
        self.on_content_selected = on_content_selected_callback
        self.playlist_controller = playlist_controller

        self.current_song_id = None
        # self.music_widgets agora armazena o objeto do botão e seu texto original
        self.music_widgets = {} 
        
        self.selected_color = ("gray75", "gray40")
        self.transparent_color = "transparent"

        # Label para quando não houver resultados
        self.no_results_label = ctk.CTkLabel(self.view["scroll_frame"], text="", text_color="gray")

        self._setup_callbacks()
        self.build_music_list() # Cria a lista inicial de botões

    def _setup_callbacks(self):
        """Conecta os widgets da UI aos métodos deste controlador."""
        self.view["search_entry"].bind("<KeyRelease>", self.filter_music_list)
        self.view["btn_add"].configure(command=self.show_add_dialog)
        self.view["btn_edit"].configure(command=self.show_edit_dialog)
        self.view["btn_delete"].configure(command=self.confirm_delete)
        self.view["btn_import"].configure(command=self.show_import_dialog)
        self.view["btn_add_to_playlist"].configure(command=self.add_to_playlist)

    def build_music_list(self):
        """
        Cria todos os widgets de música UMA ÚNICA VEZ e os armazena.
        Isso é chamado apenas ao iniciar ou após adicionar/remover uma música.
        Armazena também a letra completa para permitir busca por trechos da letra.
        """
        # Limpa os widgets antigos
        for widget in self.view["scroll_frame"].winfo_children():
            widget.destroy()
        self.music_widgets.clear()
        
        self.current_song_id = None
        self._update_buttons_state(False)

        all_music = self.manager.get_all_music_titles_with_artists()
        default_text_color = ctk.ThemeManager.theme["CTkLabel"]["text_color"]

        for music_id, display_name in all_music:
            # Busca a música completa para obter a letra
            music = self.manager.get_music_by_id(music_id)
            lyrics_full = music.get('lyrics_full', '').lower() if music else ''
            
            song_button = ctk.CTkButton(
                self.view["scroll_frame"],
                text=display_name,
                fg_color=self.transparent_color,
                text_color=default_text_color,
                anchor="w",
                hover=True,
                command=lambda mid=music_id: self.on_music_select(mid)
            )
            # Armazena o botão, texto do display e letra completa para a busca
            self.music_widgets[music_id] = {
                'widget': song_button, 
                'text': display_name.lower(),
                'lyrics': lyrics_full
            }
            song_button.pack(fill="x", padx=5, pady=2)

        # Recria o label de "nenhum resultado" para garantir que ele exista
        self.no_results_label = ctk.CTkLabel(self.view["scroll_frame"], text="", text_color="gray")

    def filter_music_list(self, event=None):
        """
        Filtra a lista de músicas escondendo/mostrando os widgets existentes.
        Busca tanto no título/artista quanto na letra completa da música.
        Não destrói nem recria nada.
        """
        filter_term = self.view["search_entry"].get().lower().strip()
        found_any = False
        
        # Esconde o label de "nenhum resultado" antes de começar
        self.no_results_label.pack_forget()

        for music_id, data in self.music_widgets.items():
            widget = data['widget']
            display_text = data['text']  # Título - Artista
            lyrics = data.get('lyrics', '')  # Letra completa
            
            # Busca no título/artista OU na letra
            if filter_term in display_text or (filter_term and filter_term in lyrics):
                widget.pack(fill="x", padx=5, pady=2)
                found_any = True
            else:
                widget.pack_forget()

        # Se nenhum item foi encontrado, mostra a mensagem apropriada
        if not found_any:
            label_text = "Nenhuma música encontrada com este termo."
            if not self.music_widgets: # Se o banco de dados está vazio
                label_text = "Nenhuma música na base de dados."
            self.no_results_label.configure(text=label_text)
            self.no_results_label.pack(pady=20, padx=10)

    def on_music_select(self, music_id):
        if self.current_song_id and self.current_song_id in self.music_widgets:
            self.music_widgets[self.current_song_id]['widget'].configure(fg_color=self.transparent_color)
        
        if music_id in self.music_widgets:
            self.music_widgets[music_id]['widget'].configure(fg_color=self.selected_color)
        
        self.current_song_id = music_id
        slides = self.manager.get_lyrics_slides(self.current_song_id)
        self.on_content_selected("music", slides, self.current_song_id)
        self._update_buttons_state(True)
    
    def _update_buttons_state(self, is_song_selected):
        # (Este método permanece o mesmo)
        state = "normal" if is_song_selected else "disabled"
        self.view["btn_edit"].configure(state=state)
        self.view["btn_delete"].configure(state=state)
        self.view["btn_add_to_playlist"].configure(state=state)

    def show_add_dialog(self):
        dialog = AddEditSongDialog(self.master, dialog_title="Adicionar Nova Música")
        song_data = dialog.get_data()
        if song_data:
            try:
                added = self.manager.add_music(song_data["title"], song_data["artist"], song_data["lyrics_full"])
                if added:
                    messagebox.showinfo("Sucesso", "Música adicionada!", parent=self.master)
                    self.build_music_list()
                    self.filter_music_list()
            except ValidationError as e:
                logger.warning(f"Erro de validação ao adicionar música: {e}")
                messagebox.showerror("Erro de Validação", str(e), parent=self.master)
            except MusicDatabaseError as e:
                logger.error("Erro ao adicionar música", exc_info=True)
                messagebox.showerror("Erro ao Salvar",
                                     f"Não foi possível salvar a nova música no arquivo 'music_db.json'.\n"
                                     f"Verifique as permissões de escrita na pasta do programa.\n\n"
                                     f"Detalhes: {str(e)}", 
                                     parent=self.master)

    def show_edit_dialog(self):
        if not self.current_song_id: return
        song = self.manager.get_music_by_id(self.current_song_id)
        if not song: return messagebox.showerror("Erro", "Música não encontrada.", parent=self.master)
        
        dialog = AddEditSongDialog(self.master, dialog_title="Editar Música", song_data=song)
        updated_data = dialog.get_data()
        if updated_data:
            try:
                success = self.manager.edit_music(self.current_song_id, updated_data["title"], updated_data["artist"], updated_data["lyrics_full"])
                if success:
                    messagebox.showinfo("Sucesso", "Música atualizada!", parent=self.master)
                    self.build_music_list()
                    self.filter_music_list()
                    self.on_music_select(self.current_song_id)
            except ValidationError as e:
                logger.warning(f"Erro de validação ao editar música: {e}")
                messagebox.showerror("Erro de Validação", str(e), parent=self.master)
            except MusicDatabaseError as e:
                logger.error("Erro ao editar música", exc_info=True)
                messagebox.showerror("Erro ao Salvar", 
                                     f"Não foi possível salvar as alterações no arquivo 'music_db.json'.\n"
                                     f"Verifique as permissões de escrita.\n\n"
                                     f"Detalhes: {str(e)}", 
                                     parent=self.master)

    def show_import_dialog(self):
        dialog = ctk.CTkInputDialog(text="Digite a URL completa da página da música no Letras.mus.br:", title="Importar Música por URL")
        song_url = dialog.get_input()
        if not song_url or not song_url.strip(): return
        
        # Validar URL antes de processar (Fail Fast)
        try:
            song_url = validate_url(song_url.strip(), allowed_domains=['letras.mus.br'])
        except ValidationError as e:
            logger.warning(f"Erro de validação de URL: {e}")
            messagebox.showerror("URL Inválida", str(e), parent=self.master)
            return
        
        thread = threading.Thread(target=self._threaded_import, args=(song_url,), daemon=True)
        thread.start()
        self.view["btn_import"].configure(state="disabled", text="Importando...")

    def _threaded_import(self, song_url):
        try:
            music_data = self.scraper.fetch_lyrics_from_url(song_url)
            self.master.after(0, self._on_import_finished, music_data)
        except ValidationError as e:
            logger.warning(f"Erro de validação ao importar música de {song_url}: {e}")
            self.master.after(0, self._on_import_finished, None, e)
        except ScraperError as e:
            logger.error(f"Erro ao importar música de {song_url}", exc_info=True)
            self.master.after(0, self._on_import_finished, None, e)
        except Exception as e:
            logger.error(f"Erro inesperado ao importar música de {song_url}", exc_info=True)
            self.master.after(0, self._on_import_finished, None, e)

    def _on_import_finished(self, music_data, error=None):
        self.view["btn_import"].configure(state="normal", text="Importar (URL)")
        if error:
            # --- FEEDBACK DE ERRO ---
            if isinstance(error, ValidationError):
                messagebox.showerror("Erro de Validação", 
                                     f"URL inválida:\n{error}", 
                                     parent=self.master)
            elif isinstance(error, ScraperError):
                messagebox.showerror("Erro de Importação", 
                                     f"Ocorreu um erro ao importar a música:\n{error}", 
                                     parent=self.master)
            else:
                messagebox.showerror("Erro de Importação", 
                                     f"Ocorreu um erro inesperado:\n{error}", 
                                     parent=self.master)
            return
        if music_data and music_data.get("lyrics_full"):
            title, artist = music_data.get("title", "Título Desconhecido"), music_data.get("artist", "Artista Desconhecido")
            if self.manager.is_duplicate(title, artist):
                if not messagebox.askyesno("Música Existente", f"A música '{title}' por '{artist}' já parece existir. Deseja importá-la mesmo assim?", parent=self.master): return
            
            try:
                added_song = self.manager.add_music(title, artist, music_data["lyrics_full"])
                if added_song:
                    messagebox.showinfo("Importação Concluída", f"Música '{added_song['title']}' importada com sucesso!", parent=self.master)
                    self.build_music_list()
                    self.filter_music_list()
            except MusicDatabaseError as e:
                logger.error("Erro ao salvar música importada", exc_info=True)
                messagebox.showerror("Erro ao Salvar", 
                                     f"A música foi importada, mas não foi possível salvá-la no arquivo 'music_db.json'.\n"
                                     f"Verifique as permissões de escrita.\n\n"
                                     f"Detalhes: {str(e)}", 
                                     parent=self.master)
        else:
            messagebox.showwarning("Falha na Importação", "Não foi possível encontrar a letra na URL fornecida. O site pode ter atualizado sua estrutura.", parent=self.master)

    def confirm_delete(self):
        if not self.current_song_id: return
        song = self.manager.get_music_by_id(self.current_song_id)
        if not song: return
        if messagebox.askyesno("Confirmar Exclusão", f"Tem certeza que deseja excluir '{song['title']}'?", icon="warning", parent=self.master):
            try:
                if self.manager.delete_music(self.current_song_id):
                    messagebox.showinfo("Sucesso", "Música excluída.", parent=self.master)
                    self.on_content_selected("music", [], None)
                    self.build_music_list()
                    self.filter_music_list()
            except MusicDatabaseError as e:
                logger.error("Erro ao excluir música", exc_info=True)
                messagebox.showerror("Erro ao Excluir", 
                                     f"Não foi possível salvar as alterações no arquivo 'music_db.json' após a exclusão.\n"
                                     f"A música não foi removida. Verifique as permissões de escrita.\n\n"
                                     f"Detalhes: {str(e)}", 
                                     parent=self.master)
    
    def add_to_playlist(self):
        if self.current_song_id:
            self.playlist_controller.add_music_item(self.current_song_id, self.manager)