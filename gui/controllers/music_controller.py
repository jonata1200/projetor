import customtkinter as ctk
from tkinter import messagebox
from gui.dialogs import AddEditSongDialog

class MusicController:
    """
    Controlador responsável por toda a lógica da aba de Músicas.
    Usa um CTkScrollableFrame e CTkButtons para uma UI consistente.
    """
    def __init__(self, master, view_widgets, music_manager, scraper, on_content_selected_callback):
        self.master = master
        self.view = view_widgets
        self.manager = music_manager
        self.scraper = scraper
        self.on_content_selected = on_content_selected_callback

        self.current_song_id = None
        self.music_widgets = {}
        
        self.selected_color = ("gray75", "gray40")
        self.transparent_color = "transparent"

        self._setup_callbacks()
        self.load_music_list()

    def _setup_callbacks(self):
        """Conecta os widgets da UI aos métodos deste controlador."""
        self.view["search_entry"].bind("<KeyRelease>", self.filter_music_list)
        self.view["btn_add"].configure(command=self.show_add_dialog)
        self.view["btn_edit"].configure(command=self.show_edit_dialog)
        self.view["btn_delete"].configure(command=self.confirm_delete)
        self.view["btn_import"].configure(command=self.show_import_dialog)

    def load_music_list(self, filter_term=None):
        """Limpa o frame e recria os botões das músicas com base no filtro."""
        scroll_frame = self.view["scroll_frame"]
        
        for widget in scroll_frame.winfo_children():
            widget.destroy()
        self.music_widgets.clear()
        
        self.current_song_id = None
        self._update_buttons_state(False)

        all_music = self.manager.get_all_music_titles_with_artists()
        filtered_items = all_music
        if filter_term and filter_term.strip():
            filtered_items = [item for item in all_music if filter_term.lower() in item[1].lower()]

        if not filtered_items:
            label_text = "Nenhuma música encontrada" if filter_term else "Nenhuma música na base de dados"
            no_music_label = ctk.CTkLabel(self.view["scroll_frame"], text=label_text, text_color="gray")
            no_music_label.pack(pady=20, padx=10)
            return

        default_text_color = ("#1A1A1A", "#DCE4EE")

        for music_id, display_name in filtered_items:
            song_button = ctk.CTkButton(
                scroll_frame,
                text=display_name,
                fg_color=self.transparent_color,
                text_color=default_text_color,
                anchor="w",
                hover=True,
                command=lambda mid=music_id: self.on_music_select(mid)
            )
            song_button.pack(fill="x", padx=5, pady=2)
            self.music_widgets[music_id] = song_button

    def filter_music_list(self, event=None):
        """Chamado quando o usuário digita no campo de busca."""
        self.load_music_list(self.view["search_entry"].get())

    def on_music_select(self, music_id):
        """
        Callback executado quando um botão de música é clicado.
        Atualiza a cor de seleção e notifica o PresentationController.
        """
        if self.current_song_id and self.current_song_id in self.music_widgets:
            self.music_widgets[self.current_song_id].configure(fg_color=self.transparent_color)
        
        if music_id in self.music_widgets:
            self.music_widgets[music_id].configure(fg_color=self.selected_color)
        
        self.current_song_id = music_id
        slides = self.manager.get_lyrics_slides(self.current_song_id)
        self.on_content_selected("music", slides, self.current_song_id)
        self._update_buttons_state(True)
    
    def _update_buttons_state(self, is_song_selected):
        """Habilita ou desabilita os botões de 'Editar' e 'Excluir'."""
        state = "normal" if is_song_selected else "disabled"
        self.view["btn_edit"].configure(state=state)
        self.view["btn_delete"].configure(state=state)

    def show_add_dialog(self):
        dialog = AddEditSongDialog(self.master, dialog_title="Adicionar Nova Música")
        song_data = dialog.get_data()
        if song_data:
            added = self.manager.add_music(song_data["title"], song_data["artist"], song_data["lyrics_full"])
            if added:
                messagebox.showinfo("Sucesso", "Música adicionada!", parent=self.master)
                self.load_music_list()
            else:
                messagebox.showerror("Erro", "Falha ao adicionar música.", parent=self.master)

    def show_edit_dialog(self):
        if not self.current_song_id: return
        song = self.manager.get_music_by_id(self.current_song_id)
        if not song: return messagebox.showerror("Erro", "Música não encontrada.", parent=self.master)
        
        dialog = AddEditSongDialog(self.master, dialog_title="Editar Música", song_data=song)
        updated_data = dialog.get_data()
        if updated_data:
            success = self.manager.edit_music(self.current_song_id, updated_data["title"], updated_data["artist"], updated_data["lyrics_full"])
            if success:
                messagebox.showinfo("Sucesso", "Música atualizada!", parent=self.master)
                self.load_music_list(self.view["search_entry"].get())
                self.on_music_select(self.current_song_id)
            else:
                messagebox.showerror("Erro", "Falha ao atualizar música.", parent=self.master)

    def show_import_dialog(self):
        """
        Abre um diálogo para o usuário inserir uma URL completa do Letras.mus.br
        e importa a música a partir dela.
        """
        dialog = ctk.CTkInputDialog(
            text="Digite a URL completa da página da música no Letras.mus.br:",
            title="Importar Música por URL"
        )
        song_url = dialog.get_input()

        if not song_url or not song_url.strip():
            return

        song_url = song_url.strip()

        if not song_url.startswith("https://www.letras.mus.br/"):
            messagebox.showerror("URL Inválida", "Por favor, insira uma URL válida do site Letras.mus.br.", parent=self.master)
            return
        
        btn = self.view["btn_import"]
        btn.configure(state="disabled", text="Importando...")
        self.master.update_idletasks()

        try:
            music_data = self.scraper.fetch_lyrics_from_url(song_url)
            
            if music_data and music_data.get("lyrics_full"):
                title = music_data.get("title", "Título Desconhecido")
                artist = music_data.get("artist", "Artista Desconhecido")

                if self.manager.is_duplicate(title, artist):
                    if not messagebox.askyesno("Música Existente", f"A música '{title}' por '{artist}' já parece existir. Deseja importá-la mesmo assim?"):
                        return

                added_song = self.manager.add_music(title, artist, music_data["lyrics_full"])
                if added_song:
                    messagebox.showinfo("Importação Concluída", f"Música '{added_song['title']}' importada com sucesso!", parent=self.master)
                    self.load_music_list()
                else:
                    messagebox.showerror("Erro de Importação", "Não foi possível salvar a música no banco de dados.", parent=self.master)
            else:
                messagebox.showwarning("Falha na Importação", f"Não foi possível encontrar a letra na URL fornecida.\nVerifique se a URL está correta ou se a página da música ainda existe.", parent=self.master)
        
        except Exception as e:
            messagebox.showerror("Erro Inesperado", f"Ocorreu um erro durante a importação: {e}", parent=self.master)
        
        finally:
            btn.configure(state="normal", text="Importar (URL)")

    def confirm_delete(self):
        if not self.current_song_id: return
        song = self.manager.get_music_by_id(self.current_song_id)
        if not song: return
        
        if messagebox.askyesno("Confirmar Exclusão", f"Tem certeza que deseja excluir '{song['title']}'?", icon="warning", parent=self.master):
            if self.manager.delete_music(self.current_song_id):
                messagebox.showinfo("Sucesso", "Música excluída.", parent=self.master)
                self.on_content_selected("music", [], None)
                self.load_music_list(self.view["search_entry"].get())