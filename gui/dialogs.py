import customtkinter as ctk
from screeninfo import get_monitors
from tkinter import messagebox
from tkinter.colorchooser import askcolor

# =============================================================================
# Diálogo para Adicionar/Editar Músicas
# =============================================================================

class AddEditSongDialog(ctk.CTkToplevel):
    """
    Janela de diálogo para criar uma nova música ou editar uma existente.
    """
    def __init__(self, master, dialog_title="Nova Música", song_data=None):
        super().__init__(master)
        self.transient(master) 
        self.grab_set()        
        self.title(dialog_title)
        
        self.geometry("550x650") 
        self.resizable(True, True)

        self.result = None 

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1) 

        # Widgets de entrada
        ctk.CTkLabel(self, text="Título:").grid(row=0, column=0, padx=10, pady=(20,5), sticky="w")
        self.title_entry = ctk.CTkEntry(self, width=400)
        self.title_entry.grid(row=0, column=1, padx=10, pady=(20,5), sticky="ew")

        ctk.CTkLabel(self, text="Artista:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.artist_entry = ctk.CTkEntry(self, width=400)
        self.artist_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        ctk.CTkLabel(self, text="Letra Completa:").grid(row=2, column=0, padx=10, pady=(10,0), sticky="nw")
        self.lyrics_textbox = ctk.CTkTextbox(self, wrap="word", font=ctk.CTkFont(size=14))
        self.lyrics_textbox.grid(row=2, column=1, padx=10, pady=(10,5), sticky="nsew")

        # Botões de ação
        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.grid(row=3, column=0, columnspan=2, pady=(10,20), sticky="ew")
        button_frame.grid_columnconfigure((0, 3), weight=1)

        self.save_button = ctk.CTkButton(button_frame, text="Salvar", command=self.on_save, width=100)
        self.save_button.grid(row=0, column=1, padx=10)

        self.cancel_button = ctk.CTkButton(button_frame, text="Cancelar", command=self.on_cancel, fg_color="gray50", hover_color="gray60", width=100)
        self.cancel_button.grid(row=0, column=2, padx=10)

        # Preenche os campos se estiver editando
        if song_data:
            self.title_entry.insert(0, song_data.get("title", ""))
            self.artist_entry.insert(0, song_data.get("artist", ""))
            self.lyrics_textbox.insert("1.0", song_data.get("lyrics_full", ""))
        
        self.title_entry.focus_set()
        self.protocol("WM_DELETE_WINDOW", self.on_cancel)
        self.after(50, self._center_window)

    def on_save(self):
        title = self.title_entry.get().strip()
        artist = self.artist_entry.get().strip()
        lyrics_full = self.lyrics_textbox.get("1.0", "end-1c").strip() 
        if not all([title, artist, lyrics_full]):
            messagebox.showwarning("Campos Vazios", "Título, Artista e Letra não podem estar vazios.", parent=self)
            return
        self.result = { "title": title, "artist": artist, "lyrics_full": lyrics_full }
        self.destroy()

    def on_cancel(self):
        self.result = None
        self.destroy()

    def get_data(self):
        """Espera a janela fechar e retorna os dados inseridos pelo usuário."""
        self.master.wait_window(self)
        return self.result

    def _center_window(self):
        """Centraliza a janela de diálogo na janela mestre."""
        try:
            self.update_idletasks()
            master_x, master_y = self.master.winfo_x(), self.master.winfo_y()
            master_w, master_h = self.master.winfo_width(), self.master.winfo_height()
            dialog_w, dialog_h = self.winfo_width(), self.winfo_height()
            x = master_x + (master_w - dialog_w) // 2
            y = master_y + (master_h - dialog_h) // 2
            self.geometry(f"+{x}+{y}")
        except Exception as e:
            print(f"Erro ao centralizar AddEditSongDialog: {e}")


# =============================================================================
# Diálogo de Configurações
# =============================================================================

class SettingsDialog(ctk.CTkToplevel):
    """
    Janela de diálogo para configurar as opções de projeção.
    """
    def __init__(self, master, config_manager):
        super().__init__(master)
        self.master_app = master 
        self.config_manager = config_manager
        
        self.transient(master)
        self.grab_set()
        self.title("Configurações")
        self.geometry("550x640")
        self.resizable(False, False)

        main_settings_frame = ctk.CTkFrame(self)
        main_settings_frame.pack(pady=10, padx=10, fill="both", expand=True)

        self._create_projection_settings_tab(main_settings_frame)
        
        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.pack(side="bottom", fill="x", pady=(5,15), padx=10)
        button_frame.grid_columnconfigure((0, 3), weight=1)

        self.save_button = ctk.CTkButton(button_frame, text="Salvar", command=self.on_save, width=140)
        self.save_button.grid(row=0, column=1, padx=5, pady=5)

        self.cancel_button = ctk.CTkButton(button_frame, text="Cancelar", command=self.destroy, fg_color="gray50", hover_color="gray60", width=100)
        self.cancel_button.grid(row=0, column=2, padx=5, pady=5)

        self.protocol("WM_DELETE_WINDOW", self.destroy) 
        self.after(50, self._center_window)
        self.focus_force()

    def _create_projection_settings_tab(self, tab_frame):
        tab_frame.grid_columnconfigure(1, weight=1)

        # --- Monitor para Projeção ---
        ctk.CTkLabel(tab_frame, text="Monitor para Projeção:").grid(row=0, column=0, padx=10, pady=(20,5), sticky="w")
        self.monitor_display_list = ["Automático (Recomendado)"]
        self.monitor_map_for_saving = {"Automático (Recomendado)": ""} 
        try:
            for i, m in enumerate(get_monitors()):
                display_name = f"Monitor {i}: {m.name or f'({m.width}x{m.height})'}{' (Primário)' if m.is_primary else ''}"
                self.monitor_display_list.append(display_name)
                self.monitor_map_for_saving[display_name] = str(i)
        except Exception as e:
            print(f"Erro ao listar monitores: {e}")
        self.selected_monitor_var = ctk.StringVar()
        current_idx = self.config_manager.get_setting('Display', 'projection_monitor_index', '')
        current_name = next((name for name, idx in self.monitor_map_for_saving.items() if idx == current_idx), "Automático (Recomendado)")
        self.selected_monitor_var.set(current_name)
        self.monitor_optionmenu = ctk.CTkOptionMenu(tab_frame, variable=self.selected_monitor_var, values=self.monitor_display_list, width=300, dynamic_resizing=False)
        self.monitor_optionmenu.grid(row=0, column=1, padx=10, pady=(20,5), sticky="ew")
        ctk.CTkLabel(tab_frame, text="Automático tentará o 2º monitor não primário,\n senão o primário.", font=ctk.CTkFont(size=10)).grid(row=1, column=1, padx=10, pady=(0,10), sticky="w")
        
        ctk.CTkFrame(tab_frame, height=2, fg_color="gray50").grid(row=2, column=0, columnspan=2, pady=15, sticky="ew")

        # --- Opções de Aparência ---
        ctk.CTkLabel(tab_frame, text="Tamanho da Fonte:").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.font_size_var = ctk.StringVar(value=self.config_manager.get_setting('Projection', 'font_size', '60'))
        self.font_size_entry = ctk.CTkEntry(tab_frame, textvariable=self.font_size_var)
        self.font_size_entry.grid(row=3, column=1, padx=10, pady=5, sticky="ew")

        ctk.CTkLabel(tab_frame, text="Cor da Fonte:").grid(row=4, column=0, padx=10, pady=5, sticky="w")
        font_color_frame = ctk.CTkFrame(tab_frame, fg_color="transparent")
        font_color_frame.grid(row=4, column=1, padx=10, pady=5, sticky="ew")
        font_color_frame.grid_columnconfigure(0, weight=1)
        self.font_color_var = ctk.StringVar(value=self.config_manager.get_setting('Projection', 'font_color', 'white'))
        self.font_color_entry = ctk.CTkEntry(font_color_frame, textvariable=self.font_color_var)
        self.font_color_entry.grid(row=0, column=0, sticky="ew")
        ctk.CTkButton(font_color_frame, text="Escolher...", width=80, command=lambda: self._pick_color(self.font_color_var)).grid(row=0, column=1, padx=(10,0))
        
        ctk.CTkLabel(tab_frame, text="Cor de Fundo:").grid(row=5, column=0, padx=10, pady=5, sticky="w")
        bg_color_frame = ctk.CTkFrame(tab_frame, fg_color="transparent")
        bg_color_frame.grid(row=5, column=1, padx=10, pady=5, sticky="ew")
        bg_color_frame.grid_columnconfigure(0, weight=1)
        self.bg_color_var = ctk.StringVar(value=self.config_manager.get_setting('Projection', 'bg_color', 'black'))
        self.bg_color_entry = ctk.CTkEntry(bg_color_frame, textvariable=self.bg_color_var)
        self.bg_color_entry.grid(row=0, column=0, sticky="ew")
        ctk.CTkButton(bg_color_frame, text="Escolher...", width=80, command=lambda: self._pick_color(self.bg_color_var)).grid(row=0, column=1, padx=(10,0))
        
        ctk.CTkLabel(tab_frame, text="Use o botão 'Escolher' ou digite um nome de cor\n em inglês (ex: white) ou código hex (ex: #FFFFFF).", font=ctk.CTkFont(size=10)).grid(row=6, column=1, padx=10, pady=(0,10), sticky="w")

        ctk.CTkFrame(tab_frame, height=2, fg_color="gray50").grid(row=7, column=0, columnspan=2, pady=15, sticky="ew")

        # --- Animação de Fundo ---
        ctk.CTkLabel(tab_frame, text="Animação de Fundo:").grid(row=8, column=0, padx=10, pady=5, sticky="w")
        self.animation_options = ["Nenhuma", "Neve", "Partículas Flutuantes"]
        self.animation_var = ctk.StringVar(value=self.config_manager.get_setting('Projection', 'animation_type', 'Neve'))
        self.animation_optionmenu = ctk.CTkOptionMenu(tab_frame, variable=self.animation_var, values=self.animation_options)
        self.animation_optionmenu.grid(row=8, column=1, padx=10, pady=5, sticky="ew")
        
        ctk.CTkLabel(tab_frame, text="Cor da Animação:").grid(row=9, column=0, padx=10, pady=5, sticky="w")
        anim_color_frame = ctk.CTkFrame(tab_frame, fg_color="transparent")
        anim_color_frame.grid(row=9, column=1, padx=10, pady=5, sticky="ew")
        anim_color_frame.grid_columnconfigure(0, weight=1)
        self.anim_color_var = ctk.StringVar(value=self.config_manager.get_setting('Projection', 'animation_color', 'white'))
        self.anim_color_entry = ctk.CTkEntry(anim_color_frame, textvariable=self.anim_color_var)
        self.anim_color_entry.grid(row=0, column=0, sticky="ew")
        ctk.CTkButton(anim_color_frame, text="Escolher...", width=80, command=lambda: self._pick_color(self.anim_color_var)).grid(row=0, column=1, padx=(10,0))

    def on_save(self):
        # Monitor
        monitor_index_to_save = self.monitor_map_for_saving.get(self.selected_monitor_var.get(), "") 
        self.config_manager.set_setting('Display', 'projection_monitor_index', monitor_index_to_save)
        
        # Fonte
        font_size_val = self.font_size_entry.get()
        if not (font_size_val.isdigit() and int(font_size_val) > 0):
            messagebox.showwarning("Valor Inválido", "O tamanho da fonte deve ser um número inteiro positivo.", parent=self)
            self.font_size_entry.focus(); return
        self.config_manager.set_setting('Projection', 'font_size', font_size_val)
        
        # Cores e Animação
        self.config_manager.set_setting('Projection', 'font_color', self.font_color_entry.get().strip())
        self.config_manager.set_setting('Projection', 'bg_color', self.bg_color_entry.get().strip())
        self.config_manager.set_setting('Projection', 'animation_type', self.animation_var.get())
        self.config_manager.set_setting('Projection', 'animation_color', self.anim_color_var.get().strip())
        
        messagebox.showinfo("Configurações Salvas", 
                            "As configurações foram salvas.\n\n"
                            "As novas configurações serão aplicadas na próxima vez\n"
                            "que a janela de projeção for aberta.",
                            parent=self)
        self.destroy()

    def _pick_color(self, string_var_to_update):
        """Abre o seletor de cores e atualiza a StringVar com o resultado."""
        color_info = askcolor(parent=self)
        if color_info and color_info[1]:
            string_var_to_update.set(color_info[1])

    def _center_window(self):
        """Centraliza a janela de diálogo na janela mestre."""
        self.after(20, self._do_center) 

    def _do_center(self):
        try:
            self.update_idletasks() 
            master_x, master_y = self.master.winfo_x(), self.master.winfo_y()
            master_w, master_h = self.master.winfo_width(), self.master.winfo_height()
            dialog_w, dialog_h = self.winfo_width(), self.winfo_height()
            if dialog_w <= 1: self.after(50, self._do_center); return
            x = master_x + (master_w - dialog_w) // 2
            y = master_y + (master_h - dialog_h) // 2
            self.geometry(f"+{x}+{y}")
        except Exception: pass


# =============================================================================
# Diálogo de Ajuda de Atalhos
# =============================================================================

class ShortcutsHelpDialog(ctk.CTkToplevel):
    """
    Janela de diálogo que exibe uma lista dos atalhos de teclado.
    """
    def __init__(self, master):
        super().__init__(master)
        
        self.transient(master)
        self.grab_set()
        self.title("Atalhos do Teclado")
        self.geometry("400x240")
        self.resizable(False, False)

        shortcuts = [
            ("Seta Direita", "Avançar para o Próximo Slide"),
            ("Seta Esquerda", "Voltar para o Slide Anterior"),
            ("C", "Limpar Conteúdo da Projeção"),
            ("Esc", "Fechar Janela de Projeção")
        ]

        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True, padx=15, pady=15)
        main_frame.grid_columnconfigure(1, weight=1)

        header_font = ctk.CTkFont(weight="bold")
        ctk.CTkLabel(main_frame, text="Atalho", font=header_font).grid(row=0, column=0, sticky="w", padx=(0, 20))
        ctk.CTkLabel(main_frame, text="Ação", font=header_font).grid(row=0, column=1, sticky="w")
        
        ctk.CTkFrame(main_frame, height=2, fg_color="gray50").grid(row=1, column=0, columnspan=2, pady=(5, 10), sticky="ew")

        for i, (key, description) in enumerate(shortcuts):
            row = i + 2
            ctk.CTkLabel(main_frame, text=key).grid(row=row, column=0, sticky="w", pady=2)
            ctk.CTkLabel(main_frame, text=description).grid(row=row, column=1, sticky="w", pady=2)

        close_button = ctk.CTkButton(self, text="Fechar", command=self.destroy)
        close_button.pack(pady=(0, 15))
        
        self.after(50, self.lift)