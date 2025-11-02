import customtkinter as ctk
import os
from gui.main_window import MainWindow
from dotenv import load_dotenv

load_dotenv()

if __name__ == "__main__":
    if os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
        print("INFO: Credenciais do Google Cloud carregadas com sucesso via .env.")
        if not os.path.exists(os.getenv("GOOGLE_APPLICATION_CREDENTIALS")):
            print(f"AVISO: A variável GOOGLE_APPLICATION_CREDENTIALS está definida, mas o arquivo JSON não foi encontrado em: {os.getenv('GOOGLE_APPLICATION_CREDENTIALS')}")
            print("AVISO: A autenticação da IA provavelmente falhará. Verifique o caminho no arquivo .env.")
    else:
        print("AVISO: Variável GOOGLE_APPLICATION_CREDENTIALS não encontrada. A IA não funcionará.")

    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("blue")
    app = MainWindow()
    app.mainloop()