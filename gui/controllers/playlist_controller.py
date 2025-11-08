import customtkinter as ctk
from tkinter import messagebox

class PlaylistController:
    """
    Controlador para a aba 'Ordem de Culto'. Gerencia a lista de
    itens (músicas e passagens bíblicas) e sua exibição.
    """
    def __init__(self, master, view_widgets, presentation_controller):
        self.master = master
        self.view = view_widgets
        self.presentation_controller = presentation_controller

        self.playlist = []  # A lista de itens. Ex: [{'type': 'music', 'title': '...', 'slides': [...]}, ...]
        self.selected_index = -1
        self.item_widgets = []

        self.selected_color = ("gray75", "gray40")
        self.transparent_color = "transparent"

        self._setup_callbacks()

    def _setup_callbacks(self):
        """Conecta os botões de gerenciamento da playlist."""
        self.view["btn_remove"].configure(command=self.remove_selected_item)
        self.view["btn_up"].configure(command=lambda: self.move_selected_item(-1))
        self.view["btn_down"].configure(command=lambda: self.move_selected_item(1))
        self.view["btn_clear"].configure(command=self.clear_playlist)

    def add_music_item(self, music_id, music_manager):
        """Adiciona uma música à playlist."""
        if not music_id:
            messagebox.showwarning("Nenhuma Música", "Selecione uma música para adicionar.", parent=self.master)
            return
        
        music = music_manager.get_music_by_id(music_id)
        if music:
            item = {
                "type": "music",
                "title": f"{music['title']} - {music['artist']}",
                "slides": music['slides']
            }
            self.playlist.append(item)
            self._render_playlist()
            messagebox.showinfo("Sucesso", f"'{item['title']}' adicionada à Ordem de Culto.", parent=self.master)

    def add_bible_item(self, slides, title):
        """Adiciona uma passagem bíblica à playlist."""
        if not slides or "Nenhum versículo encontrado" in slides[0]:
            messagebox.showwarning("Nenhum Versículo", "Carregue versículos válidos para adicionar.", parent=self.master)
            return
            
        item = {
            "type": "bible",
            "title": title,
            "slides": slides
        }
        self.playlist.append(item)
        self._render_playlist()
        messagebox.showinfo("Sucesso", f"'{item['title']}' adicionada à Ordem de Culto.", parent=self.master)
    
    def _render_playlist(self):
        """Limpa e redesenha a lista de itens da playlist na UI."""
        scroll_frame = self.view["scroll_frame"]
        for widget in scroll_frame.winfo_children():
            widget.destroy()
        self.item_widgets.clear()
        
        self.selected_index = -1
        self._update_buttons_state()

        if not self.playlist:
            no_items_label = ctk.CTkLabel(scroll_frame, text="Nenhum item na Ordem de Culto", text_color="gray")
            no_items_label.pack(pady=20, padx=10)
            return

        default_text_color = ctk.ThemeManager.theme["CTkLabel"]["text_color"]

        for i, item in enumerate(self.playlist):
            icon = "🎵" if item['type'] == 'music' else "📖"
            display_text = f"{i + 1}. {icon} {item['title']}"
            
            item_button = ctk.CTkButton(
                scroll_frame,
                text=display_text,
                fg_color=self.transparent_color,
                text_color=default_text_color,
                anchor="w",
                hover=True,
                command=lambda index=i: self.on_item_select(index)
            )
            item_button.pack(fill="x", padx=5, pady=2)
            self.item_widgets.append(item_button)

    def on_item_select(self, index):
        """Chamado quando um item da playlist é clicado."""
        if self.selected_index != -1 and self.selected_index < len(self.item_widgets):
            self.item_widgets[self.selected_index].configure(fg_color=self.transparent_color)

        self.selected_index = index
        self.item_widgets[self.selected_index].configure(fg_color=self.selected_color)
        
        selected_item = self.playlist[self.selected_index]
        self.presentation_controller.load_content(
            selected_item['type'],
            selected_item['slides']
        )
        self._update_buttons_state()
        
    def remove_selected_item(self):
        if self.selected_index == -1: return
        
        item_title = self.playlist[self.selected_index]['title']
        if messagebox.askyesno("Confirmar", f"Tem certeza que deseja remover '{item_title}' da lista?"):
            del self.playlist[self.selected_index]
            self.presentation_controller.clear_projection_content()
            self._render_playlist()
            
    def move_selected_item(self, direction):
        if self.selected_index == -1: return
        
        new_index = self.selected_index + direction
        if 0 <= new_index < len(self.playlist):
            # Troca os itens de lugar
            item = self.playlist.pop(self.selected_index)
            self.playlist.insert(new_index, item)
            
            # Atualiza a UI e a seleção
            self._render_playlist()
            self.on_item_select(new_index)

    def clear_playlist(self):
        if not self.playlist: return
        if messagebox.askyesno("Confirmar", "Tem certeza que deseja limpar toda a Ordem de Culto?"):
            self.playlist.clear()
            self.presentation_controller.clear_projection_content()
            self._render_playlist()

    def _update_buttons_state(self):
        """Habilita ou desabilita os botões de gerenciamento."""
        is_item_selected = self.selected_index != -1
        state = "normal" if is_item_selected else "disabled"
        
        self.view["btn_remove"].configure(state=state)
        self.view["btn_up"].configure(state=state)
        self.view["btn_down"].configure(state=state)