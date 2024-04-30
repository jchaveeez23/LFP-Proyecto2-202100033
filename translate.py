class Translate:
    def __init__(self):
        self.grammar = {
            "crearbd": "use",
            "eliminarbd": "dropDataBase",
            "crearcoleccion": "createCollection",
            "eliminarcoleccion": "dropCollection",
            "insertarunico": "insertOne",
            "actualizarunico": "updateOne",
            "eliminarunico": "deleteOne",
            "buscartodo": "find",
            "buscarunico": "findOne",
        }
        self.translates = []

    def translate(self, sentences):
        self.sentences = sentences
        result = ""
        for sentence in self.sentences:
            result += self.translate_sentence(sentence) + "\n"
        return result
    
    def translate_sentence(self, sentence):
        if sentence[0] == "crearbd":
            trans = f"use('{sentence[1]}');"
        elif sentence[0] == "eliminarbd":
            trans = f"db.dropDataBase();"
        elif sentence[0] == "crearcoleccion":
            trans = f"db.createCollection('{sentence[1]}');"
        elif sentence[0] == "eliminarcoleccion":
            trans = f"db.{sentence[6]}.drop();"
        elif sentence[0] == "insertarunico":
            trans = f"db.{sentence[6]}.insertOne({sentence[8]});"
        elif sentence[0] == "actualizarunico":
            trans = f"db.{sentence[6]}.updateOne({sentence[8]});"
        elif sentence[0] == "eliminarunico":
            trans = f"db.{sentence[6]}.deleteOne({sentence[8]});"
        elif sentence[0] == "buscartodo":
            trans = f"db.{sentence[6]}.find();"
        elif sentence[0] == "buscarunico":
            trans = f"db.{sentence[6]}.findOne();"
    
        self.translates.append({
            "type": sentence[0],
            "function": self.grammar[sentence[0]],
            "output": trans
        })
        return trans