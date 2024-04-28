import tkinter as tk
from tkinter import filedialog
from tkinter import ttk  # Asegúrate de importar ttk

import re

class Application(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("MongoDB Compiler")

        self.text_area = tk.Text(self)
        self.text_area.pack(fill=tk.BOTH, expand=True)

        self.menu_bar = tk.Menu(self)
        self.config(menu=self.menu_bar)

        # Crear pestañas para reportes
        self.tab_control = ttk.Notebook(self)
        self.tab_control.pack(fill=tk.BOTH, expand=True)

        self.error_tab = tk.Frame(self.tab_control)
        self.token_tab = tk.Frame(self.tab_control)

        self.tab_control.add(self.error_tab, text='Error Report')
        self.tab_control.add(self.token_tab, text='Token Report')

        # Menú Archivo
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="New", command=self.new_file)
        self.file_menu.add_command(label="Open", command=self.open_file)
        self.file_menu.add_command(label="Save", command=self.save_file)
        self.file_menu.add_command(label="Save As...", command=self.save_file_as)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.destroy)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)

        # Menú Análisis
        self.analysis_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.analysis_menu.add_command(label="Generate MongoDB Sentences", command=self.generate_sentences)
        self.analysis_menu.add_command(label="Generate Error Report", command=self.generate_error_report)
        self.analysis_menu.add_command(label="Generate Token Report", command=self.generate_token_report)
        self.menu_bar.add_cascade(label="Analysis", menu=self.analysis_menu)

        # Variables para almacenar errores y tokens
        self.errors = []
        self.tokens = []

    def new_file(self):
        self.text_area.delete(1.0, tk.END)

    def open_file(self):
        try:
            file_path = filedialog.askopenfilename()
            with open(file_path, 'r') as file:
                self.text_area.insert(1.0, file.read())
        except FileNotFoundError:
            # Handle file not found error
            pass

    def save_file(self):
        try:
            file_path = filedialog.asksaveasfilename()
            with open(file_path, 'w') as file:
                file.write(self.text_area.get(1.0, tk.END))
        except Exception as e:
            # Handle other exceptions
            pass

    def save_file_as(self):
        try:
            file_path = filedialog.asksaveasfilename()
            with open(file_path, 'w') as file:
                file.write(self.text_area.get(1.0, tk.END))
        except Exception as e:
            # Handle exceptions
            pass

    def generate_sentences(self):
        grammar = {
            'create_db': r'CrearBD\s+(\w+)',
            'drop_db': r'EliminarBD\s+(\w+)',
            'create_collection': r'CrearColeccion\s+(\w+)',
            'drop_collection': r'EliminarColeccion\s+(\w+)',
            'insert_document': r'InsertarUnico\s+(\w+)\s+\{(\s*[^{}]+\s*)\}',
            'update_document': r'ActualizarUnico\s+(\w+)\s+\{(\s*[^{}]+\s*)\}\s+\{\'set\':\s+\{(\s*[^{}]+\s*)\}\}',
            'delete_document': r'EliminarUnico\s+(\w+)\s+\{(\s*[^{}]+\s*)\}',
            'find_documents': r'BuscarTodo\s+(\w+)',
            'find_document': r'BuscarUnico\s+(\w+)'
        }

        input_text = self.text_area.get(1.0, tk.END)
        sentences = []

        for line in input_text.split('\n'):
            line = line.strip()

            if not line:
                continue

            for rule_name, pattern in grammar.items():
                match = re.search(pattern, line)
                if match:
                    groups = match.groups()

                    if rule_name == 'create_db':
                        sentences.append(f'use({groups[0]})')
                    elif rule_name == 'drop_db':
                        sentences.append(f'db.dropDatabase()')
                    elif rule_name == 'create_collection':
                        sentences.append(f'db.createCollection(\'{groups[0]}\')')
                    elif rule_name == 'drop_collection':
                        sentences.append(f'db.{groups[0]}.drop()')
                    elif rule_name == 'insert_document':
                        sentences.append(f'db.{groups[0]}.insertOne({groups[1]})')
                    elif rule_name == 'update_document':
                        sentences.append(f'db.{groups[0]}.updateOne({groups[1]}, {{\'set\': {groups[2]}}})')
                    elif rule_name == 'delete_document':
                        sentences.append(f'db.{groups[0]}.deleteOne({groups[1]})')
                    elif rule_name == 'find_documents':
                        sentences.append(f'db.{groups[0]}.find()')
                    elif rule_name == 'find_document':
                        sentences.append(f'db.{groups[0]}.findOne()')
                    break
            else:
                sentences.append(line)

        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(tk.END, '\n'.join(sentences))

    def generate_error_report(self):
        self.error_report_to_html(self.errors, "error_report.html")

    def generate_token_report(self):
        self.token_report_to_html(self.tokens, "token_report.html")

    def error_report_to_html(self, errors, output_file):
        with open(output_file, 'w') as f:
            f.write('<html><head><title>Error Report</title></head><body>')
            f.write('<h1>Error Report</h1>')
            f.write('<ul>')
            for error in errors:
                f.write(f'<li>{error}</li>')
            f.write('</ul>')
            f.write('</body></html>')

    def token_report_to_html(self, tokens, output_file):
        with open(output_file, 'w') as f:
            f.write('<html><head><title>Token Report</title></head><body>')
            f.write('<h1>Token Report</h1>')
            f.write('<ul>')
            for token in tokens:
                f.write(f'<li>{token}</li>')
            f.write('</ul>')
            f.write('</body></html>')

if __name__ == "__main__":
    app = Application()
    app.mainloop()
