import os, time, threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pdf2docx import Converter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

def convert_pdf_to_word(src, dst):
    try:
        cv = Converter(src)
        cv.convert(dst)
        cv.close()
        return True, ""
    except Exception as e:
        return False, str(e)

def convert_word_to_pdf(src, dst):
    try:
        from docx2pdf import convert
        convert(src, os.path.dirname(dst))
        gen_pdf = os.path.join(os.path.dirname(dst), os.path.splitext(os.path.basename(src))[0] + ".pdf")
        if gen_pdf != dst and os.path.exists(gen_pdf): os.rename(gen_pdf, dst)
        return True, ""
    except:
        return False, "docx2pdf solo funciona en Windows con Microsoft Word instalado."

def convert_txt_to_pdf(src, dst):
    try:
        with open(src, 'r', encoding='utf-8') as f:
            text = f.read()

        from textwrap import wrap
        c, y = canvas.Canvas(dst, pagesize=letter), 750
        c.setFont("Helvetica", 12)
        lines = text.split("\n")

        for line in lines:
            wrapped = wrap(line, width=90)  # ajusta el ancho aquí
            for subline in wrapped:
                if y < 72:
                    c.showPage()
                    c.setFont("Helvetica", 12)
                    y = 750
                c.drawString(72, y, subline)
                y -= 14
            y -= 5  # espacio entre párrafos

        c.save()
        return True, ""
    except Exception as e:
        return False, str(e)

def show_about():
    messagebox.showinfo("Acerca de", "Detector de IA\nVersión 1.0")

def show_converter():
    win = tk.Toplevel()
    win.title("Convertidor")
    win.geometry("460x300"); win.resizable(False, False); win.grab_set()

    tipo = tk.StringVar(value="PDF a Word")
    entrada, salida, estado, progreso = tk.StringVar(), tk.StringVar(), tk.StringVar(value="Listo"), tk.IntVar()

    def seleccionar():
        ext = {"PDF a Word": "*.pdf", "Word a PDF": "*.docx", "TXT a PDF": "*.txt"}[tipo.get()]
        path = filedialog.askopenfilename(filetypes=[("Archivos", ext)])
        if path:
            entrada.set(path)
            nombre = os.path.splitext(os.path.basename(path))[0]
            salida.set(os.path.join(os.path.dirname(path), f"{nombre}.{'docx' if tipo.get()=='PDF a Word' else 'pdf'}"))

    def guardar():
        ext = {"PDF a Word": "*.docx", "Word a PDF": "*.pdf", "TXT a PDF": "*.pdf"}[tipo.get()]
        salida.set(filedialog.asksaveasfilename(defaultextension=ext, filetypes=[("Archivo", ext)]))

    def convertir():
        if not entrada.get() or not salida.get(): return messagebox.showwarning("⚠️", "Seleccione archivos.")
        progreso.set(0); estado.set("Convirtiendo...")

        def run():
            time.sleep(0.2)
            conv = {"PDF a Word": convert_pdf_to_word, "Word a PDF": convert_word_to_pdf, "TXT a PDF": convert_txt_to_pdf}
            ok, msg = conv[tipo.get()](entrada.get(), salida.get())
            progreso.set(100 if ok else 0)
            estado.set("✔️ Completado" if ok else "❌ Error")
            messagebox.showinfo("Resultado", "Conversión exitosa" if ok else f"Error: {msg}")

        threading.Thread(target=run, daemon=True).start()

    ttk.Label(win, text="Tipo de Conversión").pack(pady=(10,0))
    ttk.Combobox(win, textvariable=tipo, values=["PDF a Word", "Word a PDF", "TXT a PDF"], state="readonly").pack(fill='x', padx=20)

    for lbl, var, cmd in [("Archivo de Entrada", entrada, seleccionar), ("Guardar Como", salida, guardar)]:
        ttk.Label(win, text=lbl).pack(pady=(10, 0))
        f = ttk.Frame(win); f.pack(fill='x', padx=20)
        ttk.Entry(f, textvariable=var).pack(side='left', fill='x', expand=True)
        ttk.Button(f, text="📁", command=cmd).pack(side='right')

    ttk.Button(win, text="Convertir", command=convertir).pack(pady=10)
    ttk.Label(win, textvariable=estado).pack()
    ttk.Progressbar(win, variable=progreso, maximum=100).pack(fill='x', padx=20, pady=5)
