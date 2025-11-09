import customtkinter as ctk
from tkinter import messagebox
from gui.dialogs import AddEditSongDialog
import threading

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
            song_button = ctk.CTkButton(
                self.view["scroll_frame"],
                text=display_name,
                fg_color=self.transparent_color,
                text_color=default_text_color,
                anchor="w",
                hover=True,
                command=lambda mid=music_id: self.on_music_select(mid)
            )
            # Armazena o botão e seu texto para a busca
            self.music_widgets[music_id] = {'widget': song_button, 'text': display_name.lower()}
            song_button.pack(fill="x", padx=5, pady=2)

        # Recria o label de "nenhum resultado" para garantir que ele exista
        self.no_results_label = ctk.CTkLabel(self.view["scroll_frame"], text="", text_color="gray")

    def filter_music_list(self, event=None):
        """
        Filtra a lista de músicas escondendo/mostrando os widgets existentes.
        Não destrói nem recria nada.
        """
        filter_term = self.view["search_entry"].get().lower().strip()
        found_any = False
        
        # Esconde o label de "nenhum resultado" antes de começar
        self.no_results_label.pack_forget()

        for music_id, data in self.music_widgets.items():
            widget = data['widget']
            text = data['text']
            
            if filter_term in text:
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
        # (Este método permanece o mesmo)
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
        # Modificado para reconstruir a lista após a ação
        dialog = AddEditSongDialog(self.master, dialog_title="Adicionar Nova Música")
        song_data = dialog.get_data()
        if song_data:
            added = self.manager.add_music(song_data["title"], song_data["artist"], song_data["lyrics_full"])
            if added:
                messagebox.showinfo("Sucesso", "Música adicionada!", parent=self.master)
                self.build_music_list() # Reconstrói a lista de widgets
                self.filter_music_list() # Aplica o filtro atual
            else:
                messagebox.showerror("Erro", "Falha ao adicionar música.", parent=self.master)

    def show_edit_dialog(self):
        # Modificado para reconstruir a lista após a ação
        if not self.current_song_id: return
        song = self.manager.get_music_by_id(self.current_song_id)
        if not song: return messagebox.showerror("Erro", "Música não encontrada.", parent=self.master)
        
        dialog = AddEditSongDialog(self.master, dialog_title="Editar Música", song_data=song)
        updated_data = dialog.get_data()
        if updated_data:
            success = self.manager.edit_music(self.current_song_id, updated_data["title"], updated_data["artist"], updated_data["lyrics_full"])
            if success:
                messagebox.showinfo("Sucesso", "Música atualizada!", parent=self.master)
                self.build_music_list() # Reconstrói a lista de widgets
                self.filter_music_list() # Aplica o filtro atual
                self.on_music_select(self.current_song_id) # Re-seleciona a música
            else:
                messagebox.showerror("Erro", "Falha ao atualizar música.", parent=self.master)

    def show_import_dialog(self):
        # (Este método não precisa ser alterado, apenas a sua função de callback)
        dialog = ctk.CTkInputDialog(text="Digite a URL completa da página da música no Letras.mus.br:", title="Importar Música por URL")
        song_url = dialog.get_input()
        if not song_url or not song_url.strip(): return
        song_url = song_url.strip()
        if not song_url.startswith("https://www.letras.mus.br/"):
            messagebox.showerror("URL Inválida", "Por favor, insira uma URL válida do site Letras.mus.br.", parent=self.master)
            return
        
        thread = threading.Thread(target=self._threaded_import, args=(song_url,), daemon=True)
        thread.start()
        self.view["btn_import"].configure(state="disabled", text="Importando...")

    def _threaded_import(self, song_url):
        # (Este método permanece o mesmo)
        try:
            music_data = self.scraper.fetch_lyrics_from_url(song_url)
            self.master.after(0, self._on_import_finished, music_data)
        except Exception as e:
            self.master.after(0, self._on_import_finished, None, e)

    def _on_import_finished(self, music_data, error=None):
        # Modificado para reconstruir a lista após a ação
        self.view["btn_import"].configure(state="normal", text="Importar (URL)")
        if error:
            messagebox.showerror("Erro Inesperado", f"Ocorreu um erro durante a importação: {error}", parent=self.master)
            return
        if music_data and music_data.get("lyrics_full"):
            title, artist = music_data.get("title", "Título Desconhecido"), music_data.get("artist", "Artista Desconhecido")
            if self.manager.is_duplicate(title, artist):
                if not messagebox.askyesno("Música Existente", f"A música '{title}' por '{artist}' já parece existir. Deseja importá-la mesmo assim?"): return
            added_song = self.manager.add_music(title, artist, music_data["lyrics_full"])
            if added_song:
                messagebox.showinfo("Importação Concluída", f"Música '{added_song['title']}' importada com sucesso!", parent=self.master)
                self.build_music_list() # Reconstrói a lista de widgets
                self.filter_music_list() # Aplica o filtro atual
            else:
                messagebox.showerror("Erro de Importação", "Não foi possível salvar a música no banco de dados.", parent=self.master)
        else:
            messagebox.showwarning("Falha na Importação", "Não foi possível encontrar a letra na URL fornecida.", parent=self.master)

    def confirm_delete(self):
        # Modificado para reconstruir a lista após a ação
        if not self.current_song_id: return
        song = self.manager.get_music_by_id(self.current_song_id)
        if not song: return
        if messagebox.askyesno("Confirmar Exclusão", f"Tem certeza que deseja excluir '{song['title']}'?", icon="warning", parent=self.master):
            if self.manager.delete_music(self.current_song_id):
                messagebox.showinfo("Sucesso", "Música excluída.", parent=self.master)
                self.on_content_selected("music", [], None)
                self.build_music_list() # Reconstrói a lista de widgets
                self.filter_music_list() # Aplica o filtro atual
            else:
                messagebox.showerror("Erro", "Falha ao excluir a música.", parent=self.master)
    
    def add_to_playlist(self):
        # (Este método permanece o mesmo)
        if self.current_song_id:
            self.playlist_controller.add_music_item(self.current_song_id, self.manager)