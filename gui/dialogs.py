import customtkinter as ctk
from tkinter import messagebox
from tkinter.colorchooser import askcolor
import logging
from typing import Optional, Dict
from core.exceptions import ConfigSaveError, ValidationError
from core.validators import validate_string, validate_color
from gui.utils.dialog_utils import center_dialog

logger = logging.getLogger(__name__)

# =============================================================================
# Diálogo para Adicionar/Editar Músicas (Sem alterações aqui)
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
        self.after(50, lambda: center_dialog(self, self.master))

    def on_save(self):
        try:
            # Validar campos antes de processar (Fail Fast)
            title = validate_string(self.title_entry.get(), "Título", min_length=1)
            artist = validate_string(self.artist_entry.get(), "Artista", min_length=1)
            lyrics_full = validate_string(self.lyrics_textbox.get("1.0", "end-1c"), "Letra Completa", min_length=1)
            
            self.result = { "title": title, "artist": artist, "lyrics_full": lyrics_full }
            self.destroy()
        except ValidationError as e:
            logger.warning(f"Erro de validação ao salvar música: {e}")
            messagebox.showerror("Erro de Validação", str(e), parent=self)

    def on_cancel(self):
        self.result = None
        self.destroy()

    def get_data(self):
        """Espera a janela fechar e retorna os dados inseridos pelo usuário."""
        self.master.wait_window(self)
        return self.result


# =============================================================================
# Diálogo de Configurações (Sem alterações aqui)
# =============================================================================

class SettingsDialog(ctk.CTkToplevel):
    def __init__(self, master, config_manager):
        super().__init__(master)
        self.config_manager = config_manager
        
        self.transient(master)
        self.grab_set()
        self.title("Configurações de Projeção")
        self.geometry("600x550") # Janela um pouco maior
        self.resizable(False, False)

        # Abas para cada tipo de conteúdo
        self.tab_view = ctk.CTkTabview(self, width=580)
        self.tab_view.pack(pady=10, padx=10, fill="both", expand=True)
        
        tab_music = self.tab_view.add("Músicas")
        tab_bible = self.tab_view.add("Bíblia")
        tab_text = self.tab_view.add("Avisos / Texto")
        
        # Dicionários para guardar as variáveis de cada aba
        self.style_vars = {}

        # Cria a UI para cada aba
        self._create_style_tab(tab_music, 'Projection_Music')
        self._create_style_tab(tab_bible, 'Projection_Bible')
        self._create_style_tab(tab_text, 'Projection_Text')
        
        # Botões Salvar/Cancelar
        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.pack(side="bottom", fill="x", pady=(5,15), padx=10)
        button_frame.grid_columnconfigure((0, 3), weight=1)
        ctk.CTkButton(button_frame, text="Salvar", command=self.on_save, width=140).grid(row=0, column=1, padx=5)
        ctk.CTkButton(button_frame, text="Cancelar", command=self.destroy, fg_color="gray50", hover_color="gray60", width=100).grid(row=0, column=2, padx=5)

        self.protocol("WM_DELETE_WINDOW", self.destroy)
        self.after(50, lambda: center_dialog(self, self.master))
        self.focus_force()

    def _create_style_tab(self, tab, section_name):
        """Método auxiliar para criar a UI de estilo dentro de uma aba."""
        tab.grid_columnconfigure(1, weight=1)
        
        vars_dict = {}
        
        # Tamanho da Fonte
        ctk.CTkLabel(tab, text="Tamanho da Fonte:").grid(row=0, column=0, padx=10, pady=(20,5), sticky="w")
        vars_dict['font_size'] = ctk.StringVar(value=self.config_manager.get_setting(section_name, 'font_size'))
        ctk.CTkEntry(tab, textvariable=vars_dict['font_size']).grid(row=0, column=1, padx=10, pady=(20,5), sticky="ew")

        # Cor da Fonte
        ctk.CTkLabel(tab, text="Cor da Fonte:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        frame_fc = ctk.CTkFrame(tab, fg_color="transparent"); frame_fc.grid(row=1, column=1, padx=10, pady=5, sticky="ew"); frame_fc.grid_columnconfigure(0, weight=1)
        vars_dict['font_color'] = ctk.StringVar(value=self.config_manager.get_setting(section_name, 'font_color'))
        ctk.CTkEntry(frame_fc, textvariable=vars_dict['font_color']).grid(row=0, column=0, sticky="ew")
        ctk.CTkButton(frame_fc, text="Escolher...", width=80, command=lambda v=vars_dict['font_color']: self._pick_color(v)).grid(row=0, column=1, padx=(10,0))
        
        # Cor de Fundo
        ctk.CTkLabel(tab, text="Cor de Fundo:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        frame_bg = ctk.CTkFrame(tab, fg_color="transparent"); frame_bg.grid(row=2, column=1, padx=10, pady=5, sticky="ew"); frame_bg.grid_columnconfigure(0, weight=1)
        vars_dict['bg_color'] = ctk.StringVar(value=self.config_manager.get_setting(section_name, 'bg_color'))
        ctk.CTkEntry(frame_bg, textvariable=vars_dict['bg_color']).grid(row=0, column=0, sticky="ew")
        ctk.CTkButton(frame_bg, text="Escolher...", width=80, command=lambda v=vars_dict['bg_color']: self._pick_color(v)).grid(row=0, column=1, padx=(10,0))

        # Fundo semi-transparente (apenas para músicas)
        if section_name == 'Projection_Music':
            ctk.CTkLabel(tab, text="Fundo semitransparente:").grid(row=3, column=0, padx=10, pady=(15,5), sticky="w")
            vars_dict['text_bg_enabled'] = ctk.BooleanVar(value=self.config_manager.get_setting(section_name, 'text_bg_enabled', 'true').lower() in ('1','true','yes','on'))
            ctk.CTkSwitch(tab, text="Ativar retângulo atrás do texto", variable=vars_dict['text_bg_enabled']).grid(row=3, column=1, padx=10, pady=(15,5), sticky="w")

            ctk.CTkLabel(tab, text="Opacidade do fundo (0-1):").grid(row=4, column=0, padx=10, pady=5, sticky="w")
            vars_dict['text_bg_opacity'] = ctk.DoubleVar(value=float(self.config_manager.get_setting(section_name, 'text_bg_opacity', '0.75') or 0.75))
            opacity_frame = ctk.CTkFrame(tab, fg_color="transparent")
            opacity_frame.grid(row=4, column=1, padx=10, pady=5, sticky="ew")
            opacity_frame.grid_columnconfigure(0, weight=1)
            opacity_value_var = ctk.StringVar(value=f"{vars_dict['text_bg_opacity'].get():.2f}")
            ctk.CTkSlider(
                opacity_frame,
                variable=vars_dict['text_bg_opacity'],
                from_=0.0,
                to=1.0,
                number_of_steps=20,
                command=lambda val, v=opacity_value_var: v.set(f"{float(val):.2f}")
            ).grid(row=0, column=0, sticky="ew", padx=(0,8))
            ctk.CTkLabel(opacity_frame, width=40, textvariable=opacity_value_var).grid(row=0, column=1, sticky="e")
        
        # Animação removida de todas as configurações
        # A animação agora é configurada apenas na Ordem de Culto para músicas
        info_label = ctk.CTkLabel(tab, text="💡 A animação é configurada individualmente\nna Ordem de Culto ao adicionar cada música.", 
                                 text_color="gray", justify="left")
        info_label.grid(row=5 if section_name == 'Projection_Music' else 3, column=0, columnspan=2, padx=10, pady=10, sticky="w")

        self.style_vars[section_name] = vars_dict

    def on_save(self):
        # A lógica de salvar é movida para uma função separada
        # para que possamos mostrar la mensagem de sucesso depois.
        success = self._save_all_settings()
        
        if success:
            messagebox.showinfo("Configurações Salvas", 
                                "As configurações de estilo foram salvas com sucesso.", 
                                parent=self)
            self.destroy()
        else:
            # A mensagem de erro agora é mostrada ao usuário.
            messagebox.showerror("Erro ao Salvar", 
                                 "Não foi possível salvar as configurações no arquivo 'config.ini'.\n"
                                 "Verifique as permissões de escrita na pasta do programa.", 
                                 parent=self)

    def _save_all_settings(self):
        """Tenta salvar todas as configurações e retorna True/False."""
        for section_name, vars_dict in self.style_vars.items():
            font_size_val = vars_dict['font_size'].get()
            if not (font_size_val.isdigit() and int(font_size_val) > 0):
                messagebox.showwarning("Valor Inválido",
                                      f"O tamanho da fonte na aba '{section_name}' deve ser um número positivo.",
                                      parent=self)
                return False # Impede o salvamento se a validação falhar

            # Valida opacidade do fundo (quando existir)
            if 'text_bg_opacity' in vars_dict:
                try:
                    opacity_val = float(vars_dict['text_bg_opacity'].get())
                    if not (0.0 <= opacity_val <= 1.0):
                        raise ValueError()
                except Exception:
                    messagebox.showwarning(
                        "Valor Inválido",
                        "A opacidade do fundo deve ser um número entre 0 e 1.",
                        parent=self
                    )
                    return False

            for key, var in vars_dict.items():
                # Não salva animação (animação é configurada apenas na Ordem de Culto)
                if key in ('animation_type', 'animation_color'):
                    continue
                
                # Se qualquer chamada ao set_setting falhar, a função inteira retorna False.
                try:
                    if not self.config_manager.set_setting(section_name, key, var.get()):
                        return False
                except ConfigSaveError as e:
                    logger.error("Erro ao salvar configuração", exc_info=True)
                    messagebox.showerror("Erro ao Salvar",
                                         f"Não foi possível salvar as configurações no arquivo 'config.ini'.\n"
                                         f"Verifique as permissões de escrita na pasta do programa.\n\n"
                                         f"Detalhes: {str(e)}",
                                         parent=self)
                    return False
        return True # Se todas foram salvas com sucesso, retorna True.

    def _pick_color(self, string_var_to_update):
        # (Este método permanece o mesmo)
        color_info = askcolor(parent=self)
        if color_info and color_info[1]: string_var_to_update.set(color_info[1])

# =============================================================================
# Diálogo de Ajuda de Atalhos (COM AS ALTERAÇÕES)
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
        self.geometry("450x240") # Aumentei um pouco a largura para os emojis
        self.resizable(False, False)

        # --- ALTERAÇÃO 1: EMOJIS ADICIONADOS À LISTA ---
        # Adicionei os emojis e mantive o texto para clareza.
        shortcuts = [
            ("➡️ (Seta Direita)", "Avançar para o Próximo Slide"),
            ("⬅️ (Seta Esquerda)", "Voltar para o Slide Anterior"),
            ("C", "Limpar Conteúdo da Projeção"),
            ("Esc", "Fechar Janela de Projeção")
        ]

        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True, padx=15, pady=15)
        # Ajustei o peso da coluna para dar mais espaço à descrição
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=2)

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
        
        # --- ALTERAÇÃO 2: LÓGICA DE CENTRALIZAÇÃO ADICIONADA ---
        self.protocol("WM_DELETE_WINDOW", self.destroy)
        self.after(50, lambda: center_dialog(self, self.master)) # Chama a centralização após a janela ser desenhada
        self.focus_force()


# =============================================================================
# Diálogo para Selecionar Animação de Música
# =============================================================================

class AnimationSelectionDialog(ctk.CTkToplevel):
    """
    Janela de diálogo para selecionar animação ao adicionar música à playlist.
    """
    def __init__(self, master, default_animation_type: str = "Nenhuma"):
        super().__init__(master)
        self.transient(master)
        self.grab_set()
        self.title("Selecionar Animação")
        
        self.geometry("400x180")
        self.resizable(False, False)
        
        self.result = None
        
        self.grid_columnconfigure(1, weight=1)
        
        # Título
        ctk.CTkLabel(self, text="Configure a animação para esta música:", 
                    font=ctk.CTkFont(size=14, weight="bold")).grid(row=0, column=0, columnspan=2, padx=20, pady=(20, 10))
        
        # Tipo de Animação
        ctk.CTkLabel(self, text="Tipo de Animação:").grid(row=1, column=0, padx=20, pady=10, sticky="w")
        animation_options = [
            "Nenhuma", "Chamas", "Chuva", "Espiral",
            "Estrelas Piscando", "Neve",
            "Partículas Flutuantes", "Partículas Pulsantes", "Pétalas", "Poças de Luz"
        ]
        self.animation_type_var = ctk.StringVar(value=default_animation_type)
        animation_menu = ctk.CTkOptionMenu(self, variable=self.animation_type_var, values=animation_options)
        animation_menu.grid(row=1, column=1, padx=20, pady=10, sticky="ew")
        
        # Botões
        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.grid(row=2, column=0, columnspan=2, pady=20)
        
        ctk.CTkButton(button_frame, text="Confirmar", command=self.on_confirm, width=120).pack(side="left", padx=10)
        ctk.CTkButton(button_frame, text="Cancelar", command=self.on_cancel, width=120, fg_color="gray", hover_color="gray70").pack(side="left", padx=10)
        
        self.protocol("WM_DELETE_WINDOW", self.on_cancel)
        self.after(50, lambda: center_dialog(self, self.master))
        self.focus_force()
        
        # Focar no primeiro campo
        animation_menu.focus_set()
    
    def on_confirm(self):
        """Confirma a seleção e retorna os dados."""
        animation_type = self.animation_type_var.get()
        
        self.result = {
            'animation_type': animation_type
        }
        self.destroy()
    
    def on_cancel(self):
        """Cancela a seleção."""
        self.result = None
        self.destroy()
    
    def get_data(self) -> Optional[Dict[str, str]]:
        """Retorna os dados selecionados ou None se cancelado."""
        self.wait_window()
        return self.result