from tkinter import ttk

def setup_styles():
    style = ttk.Style()
    style.theme_use('clam')

    style.configure('.', font=('Segoe UI', 11), background="#f3f4f6")
    style.configure('Title.TLabel', font=('Segoe UI', 24, 'bold'), foreground="#4f46e5")
    style.configure('Subtitle.TLabel', font=('Segoe UI', 14, 'bold'))
    style.configure('Stats.TLabel', font=('Segoe UI', 11))
    style.configure('Info.TLabel', font=('Segoe UI', 10, 'italic'))
    style.configure('TButton', padding=6)

    style.configure('Primary.TButton', background="#4f46e5", foreground="white")
    style.map('Primary.TButton', background=[('active', '#6366f1')])
    style.configure('Secondary.TButton', background="#64748b", foreground="white")
    style.map('Secondary.TButton', background=[('active', '#94a3b8')])
    style.configure('Danger.TButton', background="#dc2626", foreground="white")
    style.map('Danger.TButton', background=[('active', '#ef4444')])

    style.configure('IA.TLabel', foreground="#d97706")
    style.configure('Human.TLabel', foreground="#16a34a")
    style.configure('TNotebook.Tab', padding=[12, 4])