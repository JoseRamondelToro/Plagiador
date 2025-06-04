from dotenv import load_dotenv
load_dotenv()
import tkinter as tk
from ui.styles import setup_styles
from ui.interface import build_interface
from logic.file_handlers import setup_menu
from utils.converters import show_about, show_converter

class DetectorIAApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Detector de IA")
        self.root.geometry("1200x750")
        self.root.minsize(900, 600)
        self.root.configure(bg="#f3f4f6")

        self.current_file = None
        self.is_analyzing = False

        # Referencias a funciones externas para poder usarlas en el menú
        self.show_about = show_about
        self.show_converter = show_converter

        setup_styles()
        setup_menu(self)
        build_interface(self)

        self.status.config(text="Listo para comenzar")

if __name__ == "__main__":
    root = tk.Tk()
    app = DetectorIAApp(root)
    root.mainloop()
