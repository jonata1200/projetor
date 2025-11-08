import customtkinter as ctk
from gui.main_window import MainWindow
from dotenv import load_dotenv

load_dotenv()

if __name__ == "__main__":
    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("blue")
    
    app = MainWindow()
    app.mainloop()