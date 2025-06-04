import tkinter as tk
from tkinter import ttk
from logic.file_handlers import paste_text, load_file, save_file, clear_text, lanzar_analisis_con_popup
from logic.analysis import update_stats
from logic.comparador import abrir_comparador

def build_interface(app):
    header = ttk.Frame(app.root)
    header.pack(fill=tk.X, pady=15, padx=30)
    ttk.Label(header, text="Detector de Contenido por IA", style='Title.TLabel').pack(side=tk.LEFT)

    main = ttk.Frame(app.root)
    main.pack(fill=tk.BOTH, expand=True, padx=30, pady=(0, 15))

    left = ttk.Frame(main, width=240)
    left.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
    center = ttk.Frame(main, width=600)
    center.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    right = ttk.Frame(main, width=500)
    right.pack(side=tk.RIGHT, fill=tk.Y, padx=(10, 0))
    right.pack_propagate(False)

    create_left_panel(app, left)
    create_center_panel(app, center)
    create_right_panel(app, right)

    app.status = ttk.Label(app.root, text="", anchor=tk.W, background="#e0e7ff", padding=5)
    app.status.pack(side=tk.BOTTOM, fill=tk.X)

def create_left_panel(app, parent):
    frame = ttk.LabelFrame(parent, text="🛠️ Acciones")
    frame.pack(fill=tk.X, pady=(0, 15))

    actions = [
        ("Pegar texto", lambda: paste_text(app), 'Primary.TButton'),
        ("Abrir documento", lambda: load_file(app), 'Primary.TButton'),
        ("Guardar como", lambda: save_file(app), 'Secondary.TButton'),
        ("Limpiar texto", lambda: clear_text(app), 'Danger.TButton'),
    ]
    for text, cmd, style in actions:
        ttk.Button(frame, text=text, command=cmd, style=style).pack(fill=tk.X, pady=5, padx=5)

    stats = ttk.LabelFrame(parent, text="Estadísticas")
    stats.pack(fill=tk.X, pady=(0, 15))
    app.word_label = ttk.Label(stats)
    app.char_label = ttk.Label(stats)
    app.line_label = ttk.Label(stats)
    app.sentence_label = ttk.Label(stats)
    for label in [app.word_label, app.char_label, app.line_label, app.sentence_label]:
        label.pack(anchor=tk.W, padx=10, pady=2)

    convert_frame = ttk.LabelFrame(parent, text="Convertir")
    convert_frame.pack(fill=tk.X, pady=(0, 15))
    app.conversion_var = tk.StringVar(value="PDF a Word")
    ttk.Combobox(convert_frame, textvariable=app.conversion_var,
                 values=["PDF a Word", "Word a PDF", "TXT a PDF"], state="readonly"
                 ).pack(fill=tk.X, padx=5, pady=5)
    ttk.Button(convert_frame, text="Convertir documento", 
               command=lambda: app.show_converter(), style='Secondary.TButton').pack(fill=tk.X, pady=5, padx=5)
    ttk.Button(frame, text="Comparador de textos", 
               command=lambda: abrir_comparador(app), style='Secondary.TButton').pack(fill=tk.X, pady=5, padx=5)

def create_center_panel(app, parent):
    frame = ttk.Frame(parent)
    frame.pack(fill=tk.BOTH, expand=True)

    app.text_widget = tk.Text(frame, wrap=tk.WORD, font=("Segoe UI", 12), bg="white", fg="black", padx=10, pady=10)
    app.text_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    scrollbar = ttk.Scrollbar(frame, command=app.text_widget.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    app.text_widget.config(yscrollcommand=scrollbar.set)
    app.text_widget.bind("<KeyRelease>", lambda e: update_stats(app))

    
def create_right_panel(app, parent):
    notebook = ttk.Notebook(parent)
    notebook.pack(fill=tk.BOTH, expand=True)

    app.analysis_tab = ttk.Frame(notebook)
    app.sources_tab = ttk.Frame(notebook)
    app.details_tab = ttk.Frame(notebook)
    notebook.add(app.analysis_tab, text="Análisis")
