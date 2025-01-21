import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from tabulate import tabulate
#pip install tabulate

def parse_sql_output(input_data):
    lines = input_data.strip().split("\n")
    if lines[-1].strip().lower().endswith("row)") or lines[-1].strip().lower().endswith("rows)"):
        lines = lines[:-1]
    headers = [col.strip() for col in lines[1].split(" | ")]
    separator = lines[2]
    if not all(c == '-' or c == '+' for c in separator):
        raise ValueError("El formato de separador no es válido.")
    data_rows = []
    for row in lines[3:]:
        if row.strip():
            data_rows.append([col.strip() for col in row.split(" | ")])
    return headers, data_rows

def format_table():
    input_data = input_text.get("1.0", tk.END).strip()
    if not input_data:
        messagebox.showwarning("Advertencia", "El campo de entrada está vacío.")
        return
    try:
        headers, rows = parse_sql_output(input_data)
        table = tabulate(rows, headers=headers, tablefmt="grid", numalign="center", stralign="center")
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, table)
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo procesar la entrada: {e}")

root = tk.Tk()
root.title("Formateador de SQL a Tabla")
root.geometry("1200x800")

bg_color = "#000000"
fg_color = "#00FF00"
button_bg = "#003300"
button_fg = "#00FF00"

root.configure(bg=bg_color)

style = ttk.Style()
style.theme_use("default")
style.configure("TButton", background=button_bg, foreground=button_fg, borderwidth=1)
style.map("TButton", background=[("active", "#005500")])

tk.Label(root, text="Entrada de SQL:", font=("Arial", 14), bg=bg_color, fg=fg_color).pack(pady=5)
input_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=10, font=("Courier", 12), bg=bg_color, fg=fg_color, insertbackground=fg_color)
input_text.pack(fill=tk.BOTH, padx=10, pady=5, expand=True)

format_button = ttk.Button(root, text="Formatear a Tabla", command=format_table)
format_button.pack(pady=10)

tk.Label(root, text="Salida Formateada:", font=("Arial", 14), bg=bg_color, fg=fg_color).pack(pady=5)

output_frame = tk.Frame(root, bg=bg_color)
output_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

output_scroll_x = ttk.Scrollbar(output_frame, orient=tk.HORIZONTAL)
output_scroll_y = ttk.Scrollbar(output_frame, orient=tk.VERTICAL)

output_text = tk.Text(
    output_frame, wrap=tk.NONE, font=("Courier", 14),
    bg=bg_color, fg=fg_color, insertbackground=fg_color,
    xscrollcommand=output_scroll_x.set,
    yscrollcommand=output_scroll_y.set
)

output_scroll_x.config(command=output_text.xview)
output_scroll_y.config(command=output_text.yview)

output_text.grid(row=0, column=0, sticky="nsew")
output_scroll_x.grid(row=1, column=0, sticky="ew")
output_scroll_y.grid(row=0, column=1, sticky="ns")

output_frame.rowconfigure(0, weight=1)
output_frame.columnconfigure(0, weight=1)

root.mainloop()
