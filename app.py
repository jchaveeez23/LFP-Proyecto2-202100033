import lex
import sin
import translate

text = """
CrearBD DBEjemplo = nueva CrearBD();
EliminarBD DBEjemplo = nueva EliminarBD();
CrearBD Futbol = nueva CrearBD();
CrearColeccion nuevaColeccion = nueva CrearColeccion("Calificacion");
EliminarColeccion eliminarColeccion = nueva EliminarColeccion("Calificacion");
CrearColeccion nuevaColeccion = nueva CrearColeccion("Futbolistas");
--- Messi el único GOAT
InsertarUnico insertarFutbolista = nueva InsertarUnico("Futbolistas","adsfasdf");
ActualizarUnico actualizarFutbolista = nueva ActualizarUnico("Futbolistas", "adsfasdf");
BuscarTodo todosFutbolistas = nueva BuscarTodo("Futbolistas");
BuscarUnico unFutbolista = nueva BuscarUnico("Futbolistas");
EliminarUnico eliminarFutbolista = nueva EliminarUnico("Futbolistas", "Leonel Messi");
BuscarTodo todosFutbolistas = nueva BuscarTodo("Futbolistas");
BuscarUnico unFutbolista = nueva BuscarUnico("Futbolistas");
/* 
	No debería de haber nada en la colección
*/
EliminarUnico eliminarFutbolista = nueva EliminarUnico("Futbolistas", "Leonel Messi");
BuscarTodo todosFutbolistas = nueva BuscarTodo("Futbolistas");
BuscarUnico unFutbolista = nueva BuscarUnico("Futbolistas");
--- Si llegaste hasta acá felicidades, trabajaste duro :')
 &"""

lexer = lex.Lexer()
lexer.tokenizar(text)
sintax = sin.Sintax(lexer)
sintax.analizar()

translator = translate.Translate()
text = translator.translate(sintax.sentences)

lexer.reporte_html()
sintax.reporte_html()

print(text)