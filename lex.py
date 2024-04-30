import re


class Lexer:
    def __init__(self):
        self.lexs = {
            "crearbd": "crearbd",
            "eliminarbd": "eliminarbd",
            "crearcoleccion": "crearcoleccion",
            "eliminarcoleccion": "eliminarcoleccion",
            "insertarunico": "insertarunico",
            "actualizarunico": "actualizarunico",
            "eliminarunico": "eliminarunico",
            "buscartodo": "buscartodo",
            "buscarunico": "buscarunico",
            "nueva": "nueva",
        }

        self.limiters = {
            '"': "string",
            "=": "igual",
            ":": "dos_puntos",
            ",": "coma",
            "{": "llave_abierta",
            "}": "llave_cerrada",
            "[": "corchete_abierto",
            "]": "corchete_cerrado",
            ";": "punto_y_coma",
            "(": "parentesis_abierto",
            ")": "parentesis_cerrado",
        }

        self.comments = {
            "-": "commentsimple",
            "/": "comment",
            "*": "comment",
        }

        self.id = (re.compile(r"^[a-zA-ZñÑ]+$"),)

        self.spaces = {
            " ": 1,
            "\t": 4,
        }

        self.saltos = {
            "\n": 1,
            "\r": 1,
        }

        self.wait = False
        self.temporal = ""

    def initValues(self):
        self.errors = []

        self.tokens = []
        self.buffer = ""
        self.state = "init"
        self.x = 1
        self.y = 1

    def tokenizar(self, text):
        self.initValues()

        for char in text:
            if self.wait:
                self.wait = False
                if char in self.spaces or char in self.saltos or char in self.limiters:
                    self.saveToken(self.temporal)

                    if char in self.limiters:
                        self.buffer = char
                        self.saveToken(self.limiters[char])
                    continue 
                else:
                    self.temporal = ""

            self.buffer += char
            self.comment()

            if self.ignore(char):
                self.buffer = self.buffer[:-1]
                continue

            self.x += 1

            if self.state == "string":
                if self.buffer[-1:] == '"':
                    self.verifySave()
                    self.state = "init"
                    continue

            if self.state == "init":
                if self.buffer[-1:] == '"':
                    self.state = "string"
                    self.buffer = ""
                    continue

                self.verifySave()

            self.validate()

    def verifySave(self):

        if self.state == "init":
            temp = self.buffer.lower()
            if temp in self.lexs:
                self.wait = True
                self.temporal = self.lexs[temp]
                return

            if temp in self.limiters:
                self.saveToken(self.limiters[temp])
                return

            temo = self.buffer[-1:]
            if temo in self.limiters:
                self.buffer = self.buffer[:-1]
                self.saveToken("id")
                self.buffer = temo
                self.saveToken(self.limiters[temo])
                return

        if self.state == "string":
            self.buffer = self.buffer[:-1]
            self.saveToken("string")

    def saveToken(self, tipo):
        self.tokens.append(
            {"text": self.buffer, "type": tipo, "x": self.x, "y": self.y}
        )
        self.buffer = ""

    def ignore(self, char):
        if char in self.spaces:
            self.x += self.spaces[char]
            return True
        if char in self.saltos:
            self.x = 1
            self.y += self.saltos[char]
            return True

        return False

    def comment(self):
        prob = [self.buffer[-2:], self.buffer[-1:], self.buffer]
        for i in prob:
            if i == "---" and self.state == "init":
                self.state = "commentsimple"

            if i == "/*" and self.state == "init":
                self.state = "comment"

            if i == "*/" and self.state == "comment":
                self.state = "init"
                self.buffer = ""
                break

            if i == "\n" and self.state == "commentsimple":
                self.state = "init"
                self.buffer = ""
                break

    def validate(self):
        if self.buffer in ["-", "--", "---", "/*", "*/", "/", "*"]:
            return
        if self.state == "init" and self.buffer != "":
            regex = re.compile(re.compile(r"^[a-zA-ZñÑ]+$"))
            match = regex.match(self.buffer)

            if not match:
                self.errors.append(
                    {
                        "type": "lexico",
                        "y": self.y,
                        "x": self.x,
                        "texto": self.buffer[-1:],
                        "description": "Caracter no valido",
                    }
                )
                self.buffer = self.buffer[:-1]

    def reporte_html(self):
        # add utf-8 encoding
        html = """
        <html lang="es">
        <meta charset="UTF-8">
        <head>
            <style>
                table {
                    font-family: Arial, sans-serif;
                    border-collapse: collapse;
                    width: 100%;
                }
                th, td {
                    border: 1px solid #dddddd;
                    text-align: left;
                    padding: 8px;
                }
                th {
                    background-color: #f2f2f2;
                }
            </style>
        </head>
        <body>
            <h2>Reporte de Tokens Lexico</h2>
            <table>
                <tr>
                    <th>Token</th>
                    <th>Tipo</th>
                    <th>Línea</th>
                    <th>Columna</th>
                </tr>
        """

        for token in self.tokens:
            html += f"""
                <tr>
                    <td>{token['text']}</td>
                    <td>{token['type']}</td>
                    <td>{token['y']}</td>
                    <td>{token['x']}</td>
                </tr>
            """

        html += """
            </table>
        </body>
        </html>
        """

        with open("reporte_tokens.html", "w") as file:
            file.write(html)

        # reporte de errores
        html = """
        <html lang="es">
        <meta charset="UTF-8">
        <head>
            <style>
                table {
                    font-family: Arial, sans-serif;
                    border-collapse: collapse;
                    width: 100%;
                }
                th, td {
                    border: 1px solid #dddddd;
                    text-align: left;
                    padding: 8px;
                }
                th {
                    background-color: #f2f2f2;
                }
            </style>
        </head>
        <body>
            <h2>Reporte de Errores</h2>
            <table>
                <tr>
                    <th>Tipo</th>
                    <th>Línea</th>
                    <th>Columna</th>
                    <th>Texto</th>
                    <th>Descripción</th>
                </tr>
        """

        for error in self.errors:
            html += f"""
                <tr>
                    <td>{error['type']}</td>
                    <td>{error['y']}</td>
                    <td>{error['x']}</td>
                    <td>{error['texto']}</td>
                    <td>{error['description']}</td>
                </tr>
            """

        html += """
            </table>    
        </body>
        </html>
        """

        with open("reporte_errores_lex.html", "w") as file:
            file.write(html)

        return "Reportes generados exitosamente"