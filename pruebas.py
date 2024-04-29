from collections import namedtuple

Token = namedtuple("Token", ["name", "value", "Line", "col"])

#numero de linea
line = 1
#numero de columna
col = 1
errores = []
reservadas = {
    "imprimir":"IMPRIMIR",
    "Claves":"CLAVES",
    "Registros": "REGISTROS",
    "imprimirln": "IMPRIMIRLN",
    "conteo": "CONTEO",
    "promedio": "PROMEDIO",
    "contarsi": "CONTARSI",
    "datos": "DATOS",
    "sumar": "SUMAR",
    "max": "MAX",
    "min": "MIN",
    "exportarReporte": "EXPORTARREPORTE",
    "(": "PARENTESISIZQUIERDO",
    ")": "PARENTESISDERECHO",
    "{": "LLAVEIZQUIERDA",
    "}": "LLAVEDERECHA",
    "[": "CORCHETEIZQUIERDO",
    "]": "CORCHETEDERECHO",
    ",": "COMA",
    ":": "DOSPUNTOS",
    ";": "PUNTOYCOMA",
    "'''": "COMENTARIO_MULTILINEA",
    "#": "COMENTARIO",
    "=": "IGUAL",
}


#formar un string
def tokenize_string(input_str, i):
    token = ""
    for char in input_str:
        if char == '"':
            return [token, i]
        token += char
        i += 1
    print("Error: string no cerrado")


# formar un numero
def tokenize_number(input_str, i):
    token = ""
    isDecimal = False
    for char in input_str:
        if char.isdigit():
            token += char
            i += 1
        elif char == "." and not isDecimal:
            token += char
            i += 1
            isDecimal = True
        else:
            break
    if isDecimal:
        return [float(token), i]
    return [int(token), i]        

def tokenize_input(input_str):
    global line, col
    result_tokens = []
    i = 0
    while i < len(input_str):
        char = input_str[i]
        if char.isspace():
            if char == "\n":
                line += 1
                col = 1
            elif char == "\t":
                col += 4
            else:
                col += 1
            i += 1
        elif char == '#':
            while i < len(input_str) and input_str[i] != "\n":
                i += 1
            line +=1
            col = 1
        elif char == "'" and input_str[i : i + 3] == "'''":
            i += 3
            while i < len(input_str) - 2 and input_str[i : i + 3] != "'''":
                if input_str[i] == '\n':
                    line += 1
                    col = 1
                i += 1
            if i >= len(input_str) - 2:  # Se ha llegado al final sin encontrar el cierre
                print("Error: comentario multilínea no cerrado")
            else:
                i += 3  # Saltar los 3 caracteres finales del comentario multilínea
        elif char == '"':
            string, pos = tokenize_string(input_str[i + 1 :], i)
            col += len(string) + 1
            i = pos + 2 
            token = Token("STRING", string, line, col)
            result_tokens.append(token)    
        elif char.isalpha():
            j = i
            while j < len(input_str) and input_str[j].isalpha():
                j += 1 
            word = input_str[i:j]
            if word in reservadas:
                col += len(word)
                token = Token(reservadas[word], word, line, col)
                result_tokens.append(token)
            i = j
        elif char.isdigit():
            number, pos = tokenize_number(input_str[i:], i)
            col += pos - i
            i = pos
            token = Token("NUMBER", number, line, col)
            result_tokens.append(token)
        elif char in reservadas:
            col += 1
            token = Token(reservadas[char], char, line, col)
            result_tokens.append(token)
            i += 1
        else:
            error = {
                "lexema": char,
                "fila": line,
                "columna": col }
               
            i += 1
            
            errores.append(error)
            col += 1 

    return result_tokens
