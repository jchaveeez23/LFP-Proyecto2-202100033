
import re

text = """/* CrearBD ejemplo = nueva CrearBD() &*/
EliminarBD eje&mplo = nueva EliminarBD("holaaa"); &"""

lexs = {
    "creardb": "creardb",
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

limiters = {
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

comments = {
    "-": "commentsimple",
    "/": "comment",
    "*": "comment",
}



id = re.compile(r'^[a-zA-ZñÑ]+$'),

spaces = {
    " ": 1,
    "\t": 4,
}

saltos = {
    "\n": 1,
    "\r": 1,
}

errores = []

tokens = []
buffer = ""
state = "init"
x = 1
y = 1


def lexer(text):
    global buffer, state, x, y, tokens
    for char in text:
        if ignore(char):
            continue

        buffer += char
        x += 1

        if state == "string":
            if buffer[-1:] == '"':
                verifySave()
                state = "init"
                continue

        if state == "init":
            if buffer[-1:] == '"':
                state = "string"
                buffer = ""
                continue

            verifySave()

        comment()
        validate()

def verifySave():
    global buffer, state, x, y, errores, tokens

    if state == "init":
        temp = buffer.lower()
        if temp in lexs:
            saveToken(lexs[temp])
            return 
        
        if temp in limiters:
            saveToken(limiters[temp])
            return 
        
        temo = buffer[-1:]
        if temo in limiters:
            buffer = buffer[:-1]
            saveToken("id")
            buffer = temo
            saveToken(limiters[temo])
            return

    if state == "string":
        buffer = buffer[:-1]
        saveToken("string")



def saveToken(tipo):
    global buffer, state, x, y, tokens
    tokens.append({"texto": buffer, "tipo": tipo, "posicion": {"x": x, "y": y}})
    buffer = ""

def ignore(char):
    global state, x, y
    if char in spaces:
        x += spaces[char]
        return True
    if char in saltos:
        x = 1
        y += saltos[char]
        return True
    
    return False


def comment():
    global buffer, state
    prob = [buffer[-2:], buffer[-1:]]
    for i in prob:
        if i == "---" and state == "init":
            state = "commentsimple"

        if i == "/*" and state == "init":
            state = "comment"

        if i == "*/" and state == "comment":
            state = "init"
            buffer = ""
            break

        if i == "\n" and state == "commentsimple":
            state = "init"
            buffer = ""
            break

def validate():
    global buffer, state, x, y, errores
    if buffer in ["-", "--", "---", "/*", "*/", "/", "*"]:
        return
    if state == "init" and buffer != "":
        regex = re.compile(re.compile(r'^[a-zA-ZñÑ]+$'))
        match = regex.match(buffer)

        if not match:
            errores.append({"texto": buffer[-1:], "posicion": {"x": x, "y": y}})
            buffer = buffer[:-1]

lexer(text)

base = ["id", "igual", "nueva"]
basefinal = ["string", "parentesis_cerrado", "punto_y_coma"]
grammar = [
    ["creardb"] + base + ["creardb"] + ["parentesis_abierto"] + basefinal,
    ["eliminarbd"] + base + ["eliminarbd"] + ["parentesis_abierto"] + basefinal,
    ["crearcoleccion"] + base + ["crearcoleccion"] + ["parentesis_abierto"] + basefinal,
    ["eliminarcoleccion"] + base + ["eliminarcoleccion"] + ["parentesis_abierto"] + basefinal,
    ["insertarunico"] + base + ["insertarunico"] + ["parentesis_abierto"] + ["string"] + basefinal,
    ["actualizarunico"] + base + ["actualizarunico"] + ["parentesis_abierto"]  + ["string"] + basefinal,
    ["eliminarunico"] + base + ["eliminarunico"] + ["parentesis_abierto"] + ["string"] + basefinal,
    ["buscartodo"] + base + ["buscartodo"] + ["parentesis_abierto"] + basefinal,
    ["buscarunico"] + base + ["buscarunico"] + ["parentesis_abierto"] + basefinal,

]

print(grammar)