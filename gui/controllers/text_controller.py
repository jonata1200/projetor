from tkinter import messagebox

class TextController:
    """
    Controlador para a aba 'Avisos / Texto'.
    Gerencia a projeção de texto livre digitado pelo usuário.
    """
    def __init__(self, master, view_widgets, presentation_controller):
        self.master = master
        self.view = view_widgets
        self.presentation_controller = presentation_controller
        self._setup_callbacks()

    def _setup_callbacks(self):
        """Conecta os widgets da UI aos métodos deste controlador."""
        self.view["btn_project"].configure(command=self.project_text)
        self.view["btn_clear"].configure(command=self.clear_textbox)

    def project_text(self):
        """
        Pega o conteúdo da caixa de texto e o envia para a projeção.
        """
        text_content = self.view["textbox"].get("1.0", "end-1c").strip()
        
        if not text_content:
            messagebox.showwarning("Texto Vazio", "Por favor, digite um texto para projetar.", parent=self.master)
            return

        slides = [text_content]
        
        self.presentation_controller.load_content("text", slides)

    def clear_textbox(self):
        """Limpa o conteúdo da caixa de texto."""
        self.view["textbox"].delete("1.0", "end")