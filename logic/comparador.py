import tkinter as tk
from tkinter import ttk, filedialog
from difflib import ndiff, SequenceMatcher
from logic.file_handlers import cargar_texto_comparador

def abrir_comparador(app):
    ventana = tk.Toplevel(app.root)
    ventana.title("Comparador de Textos")
    ventana.geometry("1000x700")

    frame = ttk.Frame(ventana)
    frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Entradas de texto
    text1 = tk.Text(frame, height=15, width=50, wrap=tk.WORD)
    text1.insert("1.0", "Texto original aquí...")
    text1.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))

    # Botones
    text2 = tk.Text(frame, height=15, width=50, wrap=tk.WORD)
    text2.insert("1.0", "Texto a comparar...")
    text2.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(5, 0))   

    botones_frame = ttk.Frame(ventana)
    botones_frame.pack(pady=(5, 10))

    ttk.Button(botones_frame, text="📄 Cargar texto original", command=lambda: cargar_texto_comparador(text1)).pack(side=tk.LEFT, padx=5)
    ttk.Button(botones_frame, text="📄 Cargar texto a comparar", command=lambda: cargar_texto_comparador(text2)).pack(side=tk.LEFT, padx=5) 

    # Resultado de diferencias
    result_frame = ttk.LabelFrame(ventana, text="Diferencias")
    result_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    result_box = tk.Text(result_frame, height=12, wrap=tk.WORD, bg="#f9f9f9", fg="black")
    result_box.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    # Etiqueta de similitud
    sim_label = ttk.Label(ventana, text="", font=("Segoe UI", 11, "bold"))
    sim_label.pack(pady=(0, 10))

    # Definir estilos de color
    result_box.tag_config("added", foreground="green")
    result_box.tag_config("removed", foreground="red")
    result_box.tag_config("unchanged", foreground="gray")

    # Función para comparar textos con difflib
    def comparar():
        original = text1.get("1.0", "end").strip()
        modificado = text2.get("1.0", "end").strip()

        # Calcular diferencias
        diff = ndiff(original.split(), modificado.split())
        result_box.delete("1.0", "end")

        for linea in diff:
            if linea.startswith('+ '):
                result_box.insert(tk.END, linea + '\n', "added")
            elif linea.startswith('- '):
                result_box.insert(tk.END, linea + '\n', "removed")
            elif linea.startswith('  '):
                result_box.insert(tk.END, linea + '\n', "unchanged")
            else:
                result_box.insert(tk.END, linea + '\n')  # otros casos (raro)

        # Calcular similitud
        matcher = SequenceMatcher(None, original, modificado)
        similitud = round(matcher.ratio() * 100, 2)
        sim_label.config(text=f"Similitud textual: {similitud}%")

    # Botón de acción
    ttk.Button(ventana, text="Comparar textos", command=comparar).pack(pady=5)
