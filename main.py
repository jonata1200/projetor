import customtkinter as ctk
from gui.main_window import MainWindow
from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env (se existir)
load_dotenv()

if __name__ == "__main__":
    # Define a aparência inicial da aplicação
    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("blue")
    
    # Cria e executa a janela principal
    app = MainWindow()
    app.mainloop()