import re
import threading
import time
import random
from tkinter import messagebox, ttk
import tkinter as tk


def update_stats(app):
    text = app.text_widget.get("1.0", "end")
    words = len(re.findall(r'\b\w+\b', text))
    chars = len(text.replace("\n", ""))
    lines = text.count("\n") + (0 if text.endswith("\n") else 1)
    sentences = len(re.findall(r'[.!?]+', text))

    app.word_label.config(text=f"Palabras: {words}")
    app.char_label.config(text=f"Caracteres: {chars}")
    app.line_label.config(text=f"Líneas: {lines}")
    app.sentence_label.config(text=f"Oraciones: {sentences}")

def fake_detect(app):
    if app.is_analyzing:
        return
    text = app.text_widget.get("1.0", "end").strip()
    if not text:
        messagebox.showinfo("Texto vacío", "Debes ingresar texto.")
        return

    app.is_analyzing = True
    app.status.config(text="⏳ Analizando texto...")
    app.root.update()

    def process():
        time.sleep(1.5)
        app.root.after(0, lambda: show_fake_results(app))

    threading.Thread(target=process, daemon=True).start()

def show_fake_results(app):
    # Resultados simulados
    ia_score = random.randint(20, 95)
    human_score = 100 - ia_score
    confidence = random.randint(60, 99)
    ai_types = ["GPT-4", "Claude", "Llama", "Gemini", "Falcon"]
    detected_ai = random.choice(ai_types)
    patterns = [
        "Repetición de estructuras sintácticas",
        "Uso excesivo de conectores",
        "Vocabulario demasiado formal",
        "Falta de variedad en la longitud de frases",
        "Ausencia de marcas de oralidad"
    ]
    detected_patterns = random.sample(patterns, k=min(3, len(patterns)))
    sources = [
        ("Wikipedia", 72),
        ("Artículos académicos", 58),
        ("Libros de texto", 45),
        ("Noticias", 37),
        ("Foros en línea", 22)
    ]

    # Mostrar resultados
    app.status.config(text="✅ Análisis completado.")
    app.is_analyzing = False

    # Crear y actualizar widgets (puedes expandir esto según tu diseño de pestañas)
    if hasattr(app, 'analysis_tab'):
        for widget in app.analysis_tab.winfo_children():
            widget.destroy()

        ttk.Label(app.analysis_tab, text="Resultado del análisis", style='Subtitle.TLabel').pack(pady=15)
        ttk.Label(app.analysis_tab, text=f"IA - Generado: {ia_score}%", style='IA.TLabel').pack(pady=5)
        ttk.Label(app.analysis_tab, text=f"Humano - Escrito: {human_score}%", style='Human.TLabel').pack(pady=5)

        if ia_score > 75:
            msg = "Este texto probablemente fue generado por IA."
        elif ia_score > 50:
            msg = "Este texto muestra características de contenido generado por IA."
        else:
            msg = "Este texto parece principalmente escrito por una persona."

        ttk.Label(app.analysis_tab, text=msg, style='Info.TLabel', wraplength=260).pack(pady=15)

    if hasattr(app, 'details_tab'):
        for widget in app.details_tab.winfo_children():
            widget.destroy()

        ttk.Label(app.details_tab, text="Detalles del análisis", style='Subtitle.TLabel').pack(pady=15)
        ttk.Label(app.details_tab, text=f"Tipo de IA: {detected_ai} ({confidence}% confianza)", style='Info.TLabel').pack(anchor='w', padx=10, pady=5)
        ttk.Label(app.details_tab, text="Patrones:", style='Info.TLabel').pack(anchor='w', padx=10)
        for p in detected_patterns:
            ttk.Label(app.details_tab, text=f"• {p}", style='Info.TLabel').pack(anchor='w', padx=20)

    if hasattr(app, 'sources_tab'):
        for widget in app.sources_tab.winfo_children():
            widget.destroy()

        ttk.Label(app.sources_tab, text="Fuentes potenciales", style='Subtitle.TLabel').pack(pady=15)
        for src, prob in sources:
            frame = ttk.Frame(app.sources_tab)
            frame.pack(fill=tk.X, padx=10, pady=2)
            ttk.Label(frame, text=src, style='Stats.TLabel').pack(side=tk.LEFT)
            ttk.Label(frame, text=f"{prob}%", style='Stats.TLabel').pack(side=tk.RIGHT)
            ttk.Progressbar(frame, value=prob, maximum=100, length=150).pack(side=tk.RIGHT, padx=5)