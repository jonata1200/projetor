import customtkinter as ctk
from gui.main_window import MainWindow
from dotenv import load_dotenv
from core.logging_config import setup_logging

load_dotenv()

if __name__ == "__main__":
    # Configura logging antes de iniciar a aplicação
    setup_logging()
    
    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("blue")
    
    app = MainWindow()
    app.mainloop()