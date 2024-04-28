import re
import json

class Compiler:
    def __init__(self, source_code):
        self.source_code = source_code
        self.tokens = []
        self.errors = []

    def lexical_analysis(self):
        keywords = {
            "CrearBD", "EliminarBD", "CrearColeccion", "EliminarColeccion",
            "InsertarUnico", "ActualizarUnico", "EliminarUnico", "BuscarTodo",
            "BuscarUnico"
        }
        token_patterns = {
            "identifier": r'\w+',
            "string": r'"[^"]*"',
            "number": r'\d+',
            "operator": r'[=+\-*/]',
            "keyword": r'(\b' + '|'.join(keywords) + r'\b)'
        }

        token_regex = '|'.join(token_patterns.values())
        token_iter = re.finditer(token_regex, self.source_code)

        for match in token_iter:
            token_type = next((k for k, v in token_patterns.items() if v == match.re.pattern), None)
            if token_type == 'identifier':
                token_value = match.group()
            else:
                token_value = json.loads(match.group())
            self.tokens.append((token_type, token_value))

    def syntax_analysis(self):
        commands = {
            "CrearBD": self.generate_create_bd_command,
            "EliminarBD": self.generate_drop_bd_command,
            "CrearColeccion": self.generate_create_collection_command,
            "EliminarColeccion": self.generate_drop_collection_command,
            "InsertarUnico": self.generate_insert_command,
            "ActualizarUnico": self.generate_update_command,
            "EliminarUnico": self.generate_delete_command,
            "BuscarTodo": self.generate_find_command,
            "BuscarUnico": self.generate_find_one_command
        }

        current_command = None
        for token_type, token_value in self.tokens:
            if token_type == 'keyword':
                if current_command:
                    self.errors.append(f"Syntax error: unexpected keyword '{token_value}'")
                current_command = commands[token_value]
            elif current_command:
                current_command(token_type, token_value)
                current_command = None
            else:
                self.errors.append(f"Syntax error: unexpected token '{token_value}'")

    def generate_create_bd_command(self, token_type, token_value):
        if token_type == 'identifier':
            return {"command": "db.createDatabase", "args": (token_value,)}

    def generate_drop_bd_command(self, token_type, token_value):
        if token_type == 'identifier':
            return {"command": "db.dropDatabase", "args": (token_value,)}

    def generate_create_collection_command(self, token_type, token_value):
        if token_type == 'identifier':
            return {"command": "db.createCollection", "args": (token_value,)}

    def generate_drop_collection_command(self, token_type, token_value):
        if token_type == 'identifier':
            return {"command": "db.dropCollection", "args": (token_value,)}

    def generate_insert_command(self, token_type, token_value):
        if token_type == 'identifier':
            return {"command": "db.insertOne", "args": ({"_id": token_value},)}

    def generate_update_command(self, token_type, token_value):
        if token_type == 'identifier':
            return {"command": "db.updateOne", "args": (
                {"_id": token_value},
                {"$set": token_value},
                {"upsert": True}
            )}

    def generate_delete_command(self, token_type, token_value):
        if token_type == 'identifier':
            return {"command": "db.deleteOne", "args": ({"_id": token_value},)}

    def generate_find_command(self, token_type, token_value):
        if token_type == 'identifier':
            return {"command": "db.find", "args": ({"_id": token_value},)}

    def generate_find_one_command(self, token_type, token_value):
        if token_type == 'identifier':
            return {"command": "db.findOne", "args": ({"_id": token_value},)}

    def compile(self):
        self.lexical_analysis()
        if self.errors:
            return self.errors
        self.syntax_analysis()
        return [x["command"](*x["args"]) for x in self.tokens if x["command"]]

source_code = """
CrearBD test
CrearColeccion users
InsertarUnico "user1" {"name": "John Doe", "age": 30}
ActualizarUnico "user1" {"age": 31}
EliminarUnico "user1"
BuscarTodo "users"
"""

compiler = Compiler(source_code)
mongodb_commands = compiler.compile()

for command in mongodb_commands:
    print(command)