import customtkinter as ctk
import speech_recognition as sr
from screeninfo import get_monitors
from tkinter import messagebox

class AddEditSongDialog(ctk.CTkToplevel):
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

        ctk.CTkLabel(self, text="Título:").grid(row=0, column=0, padx=10, pady=(20,5), sticky="w")
        self.title_entry = ctk.CTkEntry(self, width=400)
        self.title_entry.grid(row=0, column=1, padx=10, pady=(20,5), sticky="ew")

        ctk.CTkLabel(self, text="Artista:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.artist_entry = ctk.CTkEntry(self, width=400)
        self.artist_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        lyrics_label = ctk.CTkLabel(self, text="Letra Completa:")
        lyrics_label.grid(row=2, column=0, padx=10, pady=(10,0), sticky="nw") 
        self.lyrics_textbox = ctk.CTkTextbox(self, wrap="word", font=ctk.CTkFont(size=14))
        self.lyrics_textbox.grid(row=2, column=1, padx=10, pady=(10,5), sticky="nsew")

        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.grid(row=3, column=0, columnspan=2, pady=(10,20), sticky="ew")
        button_frame.grid_columnconfigure(0, weight=1); button_frame.grid_columnconfigure(1, weight=0) 
        button_frame.grid_columnconfigure(2, weight=0); button_frame.grid_columnconfigure(3, weight=1) 

        self.save_button = ctk.CTkButton(button_frame, text="Salvar", command=self.on_save, width=100)
        self.save_button.grid(row=0, column=1, padx=10)

        self.cancel_button = ctk.CTkButton(button_frame, text="Cancelar", command=self.on_cancel, fg_color="gray50", hover_color="gray60", width=100)
        self.cancel_button.grid(row=0, column=2, padx=10)

        if song_data:
            self.title_entry.insert(0, song_data.get("title", ""))
            self.artist_entry.insert(0, song_data.get("artist", ""))
            self.lyrics_textbox.insert("1.0", song_data.get("lyrics_full", ""))
        
        self.title_entry.focus_set()
        self.protocol("WM_DELETE_WINDOW", self.on_cancel)
        self.after(50, self._center_window_on_master)

    def on_save(self):
        title = self.title_entry.get().strip()
        artist = self.artist_entry.get().strip()
        lyrics_full = self.lyrics_textbox.get("1.0", "end-1c").strip() 
        if not title or not artist or not lyrics_full:
            messagebox.showwarning("Campos Vazios", "Título, Artista e Letra não podem estar vazios.", parent=self)
            return
        self.result = { "title": title, "artist": artist, "lyrics_full": lyrics_full }
        self.destroy()

    def on_cancel(self):
        self.result = None
        self.destroy()

    def get_data(self):
        self.master.wait_window(self)
        return self.result

    def _center_window_on_master(self):
        """Agenda a centralização real após um pequeno delay."""
        self.after(20, self._do_center)

    def _do_center(self):
        """Realiza a centralização do diálogo na janela mestre."""
        try:
            self.update_idletasks()
            
            if not self.master or not self.master.winfo_exists() or not self.winfo_exists():
                return

            master_x = self.master.winfo_x()
            master_y = self.master.winfo_y()
            master_width = self.master.winfo_width()
            master_height = self.master.winfo_height()

            dialog_width = self.winfo_width()
            dialog_height = self.winfo_height()

            if dialog_width <= 1 or dialog_height <= 1:
                self.after(50, self._do_center) 
                return

            x = master_x + (master_width - dialog_width) // 2
            y = master_y + (master_height - dialog_height) // 2
            
            screen_width = self.winfo_screenwidth()
            screen_height = self.winfo_screenheight()
            x = max(0, min(x, screen_width - dialog_width))
            y = max(0, min(y, screen_height - dialog_height))
            
            self.geometry(f"+{x}+{y}")
        except Exception as e:
            print(f"Erro ao tentar centralizar AddEditSongDialog: {e}")
            pass


class SettingsDialog(ctk.CTkToplevel):
    def __init__(self, master, config_manager):
        super().__init__(master)
        self.master_app = master 
        self.config_manager = config_manager
        
        self.transient(master)
        self.grab_set()
        self.title("Configurações do Projetor IA")
        self.geometry("550x420") # <-- Note a altura
        self.resizable(False, False)

        self.tab_view = ctk.CTkTabview(self, width=530)
        self.tab_view.pack(pady=10, padx=10, fill="both", expand=True)
        
        self.audio_tab = self.tab_view.add("Áudio (Modo IA)")
        self.projection_tab = self.tab_view.add("Projeção")

        self._create_audio_settings_tab(self.audio_tab)
        self._create_projection_settings_tab(self.projection_tab)
        
        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.pack(side="bottom", fill="x", pady=(5,15), padx=10)
        button_frame.grid_columnconfigure((0, 3), weight=1)

        self.save_button = ctk.CTkButton(button_frame, text="Salvar e Aplicar", command=self.on_save, width=140)
        self.save_button.grid(row=0, column=1, padx=5, pady=5)

        self.cancel_button = ctk.CTkButton(button_frame, text="Cancelar", command=self.destroy, fg_color="gray50", hover_color="gray60", width=100)
        self.cancel_button.grid(row=0, column=2, padx=5, pady=5)

        self.protocol("WM_DELETE_WINDOW", self.destroy) 
        self.after(50, self._center_window_on_master)
        self.focus_force()

    def _create_audio_settings_tab(self, tab_frame):
        tab_frame.grid_columnconfigure(1, weight=1)
        ctk.CTkLabel(tab_frame, text="Dispositivo de Entrada (Mic):").grid(row=0, column=0, padx=10, pady=(20,5), sticky="w")
        
        self.mic_names_full = ["Padrão do Sistema"] 
        self.mic_indices_map = {"Padrão do Sistema": ""} 
        
        if sr:
            try:
                available_mics = sr.Microphone.list_microphone_names()
                for i, name in enumerate(available_mics):
                    display_name = f"{i}: {name[:60]}"
                    self.mic_names_full.append(display_name)
                    self.mic_indices_map[display_name] = str(i)
            except Exception as e:
                print(f"Erro ao listar microfones em SettingsDialog: {e}")
                self.mic_names_full.append("Erro ao listar microfones")
        else:
            self.mic_names_full.append("SpeechRecognition não disponível")

        self.selected_mic_var = ctk.StringVar()
        current_mic_index_str = self.config_manager.get_setting('Audio', 'input_device_index', '')
        
        current_mic_display_name = "Padrão do Sistema"
        if current_mic_index_str:
            for display_name, index_str_map in self.mic_indices_map.items():
                if index_str_map == current_mic_index_str:
                    current_mic_display_name = display_name
                    break
        self.selected_mic_var.set(current_mic_display_name)

        self.mic_optionmenu = ctk.CTkOptionMenu(tab_frame, variable=self.selected_mic_var, values=self.mic_names_full, width=300, dynamic_resizing=False)
        self.mic_optionmenu.grid(row=0, column=1, padx=10, pady=(20,5), sticky="ew")

        ctk.CTkLabel(tab_frame, text="Limiar de Energia (Ruído):").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.energy_threshold_var = ctk.StringVar(value=self.config_manager.get_setting('Audio', 'energy_threshold', '3000'))
        self.energy_entry = ctk.CTkEntry(tab_frame, textvariable=self.energy_threshold_var)
        self.energy_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
        ctk.CTkLabel(tab_frame, text="(Ex: 300-8000. Menor = mais sensível)", font=ctk.CTkFont(size=10)).grid(row=2, column=1, padx=10, pady=(0,10), sticky="w")

    def _create_projection_settings_tab(self, tab_frame):
        tab_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(tab_frame, text="Monitor para Projeção:").grid(row=0, column=0, padx=10, pady=(20,5), sticky="w")

        self.monitor_display_list = ["Automático (Recomendado)"]
        self.monitor_map_for_saving = {"Automático (Recomendado)": ""} 
        
        try:
            monitors = get_monitors()
            if monitors:
                for i, m in enumerate(monitors):
                    display_name = f"Monitor {i}: {m.name if m.name else f'({m.width}x{m.height})'}"
                    if m.is_primary: display_name += " (Primário)"
                    self.monitor_display_list.append(display_name)
                    self.monitor_map_for_saving[display_name] = str(i)
            else:
                self.monitor_display_list.append("Nenhum monitor detectado por screeninfo")
        except Exception as e:
            print(f"Erro ao listar monitores para configurações: {e}")
            self.monitor_display_list.append("Erro ao listar monitores")

        self.selected_monitor_var = ctk.StringVar()
        current_proj_monitor_idx_str = self.config_manager.get_setting('Display', 'projection_monitor_index', '')

        current_monitor_display_name = "Automático (Recomendado)"
        if current_proj_monitor_idx_str:
            for display_name, index_str_map in self.monitor_map_for_saving.items():
                if index_str_map == current_proj_monitor_idx_str:
                    current_monitor_display_name = display_name
                    break
        self.selected_monitor_var.set(current_monitor_display_name)

        self.monitor_optionmenu = ctk.CTkOptionMenu(tab_frame, variable=self.selected_monitor_var, values=self.monitor_display_list, width=300, dynamic_resizing=False)
        self.monitor_optionmenu.grid(row=0, column=1, padx=10, pady=(20,5), sticky="ew")
        ctk.CTkLabel(tab_frame, text="Automático tentará o 2º monitor não primário,\n senão o primário.", font=ctk.CTkFont(size=10)).grid(row=1, column=1, padx=10, pady=(0,10), sticky="w")

    def on_save(self):
        selected_mic_display = self.selected_mic_var.get()
        mic_index_to_save = self.mic_indices_map.get(selected_mic_display, "") 
        self.config_manager.set_setting('Audio', 'input_device_index', mic_index_to_save)

        energy_val = self.energy_entry.get()
        if energy_val.isdigit() and int(energy_val) >= 0:
            self.config_manager.set_setting('Audio', 'energy_threshold', energy_val)
        else:
            messagebox.showwarning("Valor Inválido", "Limiar de energia deve ser um número inteiro não negativo.", parent=self)
            self.energy_entry.focus()
            return 

        selected_monitor_display = self.selected_monitor_var.get()
        monitor_index_to_save = self.monitor_map_for_saving.get(selected_monitor_display, "") 
        self.config_manager.set_setting('Display', 'projection_monitor_index', monitor_index_to_save)
        
        messagebox.showinfo("Configurações Salvas", 
                            "As configurações foram salvas.\n\n"
                            "Para que as configurações de áudio tenham efeito,\n"
                            "o Modo IA pode precisar ser desativado e reativado.\n\n"
                            "O monitor de projeção será usado na próxima vez\n"
                            "que a projeção for aberta.",
                            parent=self)

        self.destroy()

    def _center_window_on_master(self):
        self.after(20, self._do_center) 

    def _do_center(self):
        try:
            self.update_idletasks() 
            if not self.master or not self.master.winfo_exists() or not self.winfo_exists(): return
            master_x = self.master.winfo_x(); master_y = self.master.winfo_y()
            master_width = self.master.winfo_width(); master_height = self.master.winfo_height()
            dialog_width = self.winfo_width(); dialog_height = self.winfo_height()
            if dialog_width <= 1 or dialog_height <= 1: self.after(50, self._do_center); return
            x = master_x + (master_width - dialog_width) // 2
            y = master_y + (master_height - dialog_height) // 2
            screen_width = self.winfo_screenwidth(); screen_height = self.winfo_screenheight()
            x = max(0, min(x, screen_width - dialog_width)); y = max(0, min(y, screen_height - dialog_height))
            self.geometry(f"+{x}+{y}")
        except Exception: pass