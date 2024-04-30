import customtkinter
from tkinter import filedialog
customtkinter.set_appearance_mode("System") 
customtkinter.set_default_color_theme("blue") 

import lex
import sin
import translate

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.tokens = []
        self.actualFile = None
        self.actualPath = None
        self.title("Proyecto 2 - Lenguajes")
        self.geometry(f"{1100}x{580}")

        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Traductor", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, text="Abrir archivo", command=self.abrir_archivo)
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, text="Guardar", command=self.guardar_archivo)
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)
        self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame, text="Guardar archivo", command=self.guardar_como)
        self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=10)
        self.sidebar_button_4 = customtkinter.CTkButton(self.sidebar_frame, text="Reportes", command=self.reportes)
        self.sidebar_button_4.grid(row=4, column=0, padx=20, pady=10)

        self.entry = customtkinter.CTkTextbox(self, width=250)
        self.entry.grid(row=2, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")

        self.main_button_1 = customtkinter.CTkButton(master=self, text="Analizar", fg_color="transparent", command=self.analizar, border_width=2, text_color=("gray10", "#DCE4EE"))
        self.main_button_1.grid(row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")

        self.textbox = customtkinter.CTkTextbox(self, width=250)
        self.textbox.grid(row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")

        self.lexer = lex.Lexer()
        self.sintax = sin.Sintax(self.lexer)
        self.translator = translate.Translate()

    def abrir_archivo(self):
      self.textbox.delete("1.0", "end")
      ruta_archivo = filedialog.askopenfilename(title="Seleccione un archivo")
      self.actualPath = ruta_archivo
      self.actualFile = ruta_archivo.split("/")[-1]
      self.title(f"Proyecto 1 - Lenguajes - {self.actualFile}")
      if ruta_archivo:
         with open(ruta_archivo, "r", encoding="utf-8") as archivo:
            contenido = archivo.read()
            self.textbox.insert("1.0", contenido)

    def guardar_archivo(self):
        if self.actualPath:
            with open(self.actualPath, "w", encoding="utf-8") as archivo:
                archivo.write(self.textbox.get("1.0", "end-1c"))
        else:
            self.guardar_como()

    def guardar_como(self):
        ruta_archivo = filedialog.asksaveasfilename(title="Guardar archivo", defaultextension=".txt", filetypes=[("Archivos de texto", "*.txt")])
        self.actualPath = ruta_archivo
        self.actualFile = ruta_archivo.split("/")[-1]
        self.title(f"Proyecto 2 - Lenguajes - {self.actualFile}")
        if ruta_archivo:
            with open(ruta_archivo, "w", encoding="utf-8") as archivo:
                archivo.write(self.textbox.get("1.0", "end-1c"))


    def reportes(self):
        self.lexer.reporte_html()
        self.sintax.reporte_html()

    def analizar(self):
        texto = self.textbox.get("1.0", "end-1c")
        self.lexer.tokenizar(texto)
        self.sintax.analizar()
        translate = self.translator.translate(self.sintax.sentences)

        self.entry.delete("1.0", "end")
        self.entry.insert("1.0", translate)
        self.reportes()

if __name__ == "__main__":
    app = App()
    app.mainloop()