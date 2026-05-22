"""main.py — Punto de entrada"""
import tkinter as tk
from screens.registro import PantallaRegistro


def main():
    root = tk.Tk()
    root.title("Control de Acceso RFID")
    root.geometry("820x640")
    root.resizable(True, True)
    root.configure(bg="#1c1f26")

    root.update_idletasks()
    w, h = 820, 640
    x = (root.winfo_screenwidth()  // 2) - (w // 2)
    y = (root.winfo_screenheight() // 2) - (h // 2)
    root.geometry(f"{w}x{h}+{x}+{y}")

    app = PantallaRegistro(root)
    app.pack(fill="both", expand=True)
    root.mainloop()


if __name__ == "__main__":
    main()
