class Sintax:
    def __init__(self, lex):
        self.lex = lex
        self.sentences = []

    def analizar(self):
        base = ["id", "igual", "nueva"]
        basefinal = ["string", "parentesis_cerrado", "punto_y_coma"]
        grammar = [
            ["crearbd"] + base + ["crearbd"] + ["parentesis_abierto"] + ["parentesis_cerrado", "punto_y_coma"],
            ["eliminarbd"] + base + ["eliminarbd"] + ["parentesis_abierto"] + ["parentesis_cerrado", "punto_y_coma"],
            ["crearcoleccion"] + base + ["crearcoleccion"] + ["parentesis_abierto"] + basefinal,
            ["eliminarcoleccion"] + base + ["eliminarcoleccion"] + ["parentesis_abierto"] + basefinal,
            ["insertarunico"] + base + ["insertarunico"] + ["parentesis_abierto"] + ["string"] + ["coma"] + basefinal,
            ["actualizarunico"] + base + ["actualizarunico"] + ["parentesis_abierto"]  + ["string"] + ["coma"] + basefinal,
            ["eliminarunico"] + base + ["eliminarunico"] + ["parentesis_abierto"] + ["string"] + ["coma"] + basefinal,
            ["buscartodo"] + base + ["buscartodo"] + ["parentesis_abierto"] + basefinal,
            ["buscarunico"] + base + ["buscarunico"] + ["parentesis_abierto"] + basefinal,
        ]

        sentence = None
        sentenceResult = []
        sentenceSize = 0
        actualSize =1

        self.sentences = []
        self.errors = []

        for token in self.lex.tokens:
            if sentence is None:
                for s in grammar:
                    if token["type"] == s[0]:
                        sentence = s
                        sentenceSize = len(s)
                        sentenceResult.append(token["type"])
                        break
            else:
                if token["type"] == sentence[actualSize]:
                    actualSize += 1
                    sentenceResult.append(token["text"])
                else:
                    self.errors.append(
                        {
                            "type": "sintactico",
                            "y": token['y'],
                            "x": token['x'],
                            "texto": sentence[actualSize],
                            "description": f"Se esperaba {sentence[actualSize]} y se recibio {token['type']}",
                        }
                    )
                    sentence = None
                    actualSize = 1
                    sentenceResult = []

            if actualSize == sentenceSize:
                sentence = None
                actualSize = 1
                self.sentences.append(sentenceResult)
                sentenceResult = []

    def reporte_html(self):
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
            <h2>Reporte de Errores Sintactico</h2>
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

        with open("reporte_errores_sin.html", "w") as file:
            file.write(html)

        return "Reportes generados exitosamente"