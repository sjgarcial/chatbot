# from fastapi import FastAPI 
# from pydantic import BaseModel 
# from typing import List 

# app = FastAPI() #Instancia de la aplicación FastAPI, especifica un recurso particular de un servidor

# # Diccionario de categorías con palabras clave y respuestas
# categorias = {
#     "saludo": {
#         "palabras_claves": ["hola", "buenos dias", "buenas tardes", "buenas noches"],
#         "respuestas": {
#             "hola": "Hola, ¿qué tal?",
#             "buenos dias": "Buenos días, un gusto saludarte",
#             "buenas tardes": "Buenas tardes, un gusto saludarte",
#             "buenas noches": "Buenas noches, un placer tenerte en esta noche tan maravillosa"
#         }
#     },
#     "despedida": {
#         "palabras_claves": ["adios", "chao", "hasta luego", "nos vemos", "bye"],
#         "respuestas": {
#             "adios": "Gracias por su visita",
#             "chao": "Un gusto atenderlo",
#             "hasta luego": "Que tenga un buen día",
#             "nos vemos": "Nos vemos pronto",
#             "bye": "Nos vemos pronto"
#         }
#     },
#     "precio": {
#         "palabras_claves": ["precio", "cuánto cuesta", "cuánto vale", "cuánto es", "valor"],
#         "respuestas": {
#             "precio": "El precio depende del modelo del celular. ¿Cuál te interesa?",
#             "cuánto cuesta": "El precio depende del modelo del celular. ¿Cuál te interesa?",
#             "cuánto vale": "El precio depende del modelo del celular. ¿Cuál te interesa?",
#             "cuánto es": "El precio depende del modelo del celular. ¿Cuál te interesa?",
#             "valor": "El valor es de 500.000 pesos "
#         }
#     }
# }

# # Clasificador de categorías con palabra clave
# def clasificar_categoria(frase):
#     frase = frase.lower()  # Convierte en minúsculas
#     for categoria, data in categorias.items():
#         for palabra_clave in data["palabras_claves"]:
#             if palabra_clave in frase:  # Coincidencia exacta o parcial
#                 return categoria, palabra_clave
#     return "desconocido", None

# # Chatbot
# def chatbot(frase_usuario):
#     categoria, palabra_clave = clasificar_categoria(frase_usuario)
#     if categoria == "desconocido":
#         return "Lo siento, no entendí tu pregunta. Por favor, sea más específico."
#     # Devuelve la respuesta correspondiente a la palabra clave
#     return categorias[categoria]["respuestas"].get(palabra_clave, "Lo siento, no tengo una respuesta para eso.")

# # Modelo para entrada de datos
# class FraseEntrada(BaseModel):
#     frase: str

# # Endpoint del chatbot
# @app.post("/chatbot/")
# def obtener_respuesta(entrada: FraseEntrada):
#     respuesta = chatbot(entrada.frase)
#     return {"respuesta": respuesta}


# from fastapi import FastAPI
# from pydantic import BaseModel
# from typing import List, Dict

# app = FastAPI()

# # Base de datos simulada en memoria
# usuarios_db = []  # Lista que actuará como base de datos

# # Modelo para los datos del cliente
# class Usuario(BaseModel):
#     nombre: str
#     edad: int
#     enfermedades: List[str]

# # Endpoint para agregar o verificar usuarios
# @app.post("/registro/")
# def registro_usuario(usuario: Usuario):
#     # Verificar si el usuario ya existe
#     for registrado in usuarios_db:
#         if registrado['nombre'].lower() == usuario.nombre.lower():
#             return {
#                 "mensaje": f"El cliente '{usuario.nombre}' ya se encuentra registrado.",
#                 "datos": registrado
#             }
#     # Si no existe, registrar al usuario
#     nuevo_usuario = {
#         "nombre": usuario.nombre,
#         "edad": usuario.edad,
#         "enfermedades": usuario.enfermedades
#     }
#     usuarios_db.append(nuevo_usuario)
#     return {
#         "mensaje": f"El cliente '{usuario.nombre}' ha sido registrado exitosamente.",
#         "datos": nuevo_usuario
#     }

# # Endpoint para mostrar todos los usuarios registrados
# @app.get("/usuarios/")
# def listar_usuarios():
#     if not usuarios_db:
#         return {"mensaje": "No hay usuarios registrados."}
#     return {"usuarios": usuarios_db}

# # Endpoint interactivo para el chatbot
# @app.post("/chatbot/")
# def chatbot(pregunta: str):
#     if "registrar" in pregunta.lower():
#         # return {"mensaje": "Por favor, proporcione su nombre, edad y enfermedades para registrarse."}
#         return registro_usuario()
#     elif "listar" in pregunta.lower():
#         return listar_usuarios()
#         # return {"mensaje": "Puede ver todos los usuarios registrados en el sistema usando el endpoint '/usuarios/'."}
#     else:
#         return {"mensaje": "¿En qué más puedo ayudarte? Puede registrarse o listar usuarios."}

import pandas as pd #Biblioteca para manejar hojas de cálculo Excel, sirve para cargar, manipular y guardar datos
from fastapi import FastAPI #Herramienta pydantic para validar y estructurar datos, se usa para definir el modelo de datos que manejará la API
from pydantic import BaseModel #define una lista en Python 
from typing import List #Se usa para representar múltiples elementos, como enfermedades

app = FastAPI() #Contiene los endpoints y toda la lógica de la API.

# Ruta del archivo Excel donde se guardarán los datos
DATABASE_PATH = "usuarios_db.xlsx" # Especifica la ruta del archivo Excel donde se almacenarán los datos de los usuarios. Si no existe, se crea uno nuevo más adelante.

# Modelo de datos del usuario
class Usuario(BaseModel): #Modelo que define la estructura de los datos de un usuario
    nombre: str #Nombre del usuario (cadena de texto)
    edad: int #Edad del usuario (entero).
    enfermedades: List[str] #Lista de enfermedades asociadas al usuario (lista de cadenas).

# Función para cargar datos desde Excel
def cargar_datos(): #Intenta cargar el archivo en Excel en un "DataFrame"(crea una tabla de datos en filas y en columnas)
    try: #maneja errores o excepciones que existen durante la ejecución del programa
        # Leer el archivo Excel
        return pd.read_excel(DATABASE_PATH) #Guarda el "DataFrame" en el archivo Excel especificado por "DATABASE_PATH" (ubicación o ruta del archivo que actúa como base de datos)
    except FileNotFoundError: #Si el archivo no está en la ruta especificada, maneja una excepción, que se produce cuando intentas acceder a un archivo que no existe en la ruta especificada
        # Si el archivo no existe, crear un "DataFrame" (tabla de datos)vacío con las columnas esperadas: nombre, edad, y enfermedades.
        return pd.DataFrame(columns=["nombre", "edad", "enfermedades"])

# Función para guardar datos en Excel
def guardar_datos(data): #Guardar en un "DataFrame"(tabla de datos en excel un archivo fisico)
    data.to_excel(DATABASE_PATH, index=False) #Permite exportar el contenido a una ruta donde se guardan los datos y evita columnas no deseadas

# Cargar la base de datos al iniciar la aplicación
usuarios_df = cargar_datos() #almacena los datos devueltos por la función "cargar_datos

# "Endpoint" (permite a la aplicación interactuar con el servidor) para registrar o verificar usuarios
@app.post("/registro/") #define lo que sucede cuando se hace una solicitud POST a la ruta registro "registra nuevos usuarios"
def registro_usuario(usuario: Usuario): #registra nuevos usuarios
    global usuarios_df #indica que la variable usuarios es accesible desde cualquier parte del código

    # Verificar si el usuario ya existe en el "DataFrame" (tabla de datos)
    if not usuarios_df.empty and usuario.nombre.lower() in usuarios_df['nombre'].str.lower().values: #Comprueba si el nombre del usuario (convertido en minúsculas) está en la lista de valores de la columna
        # Si el usuario existe, devolver un mensaje
        datos_existentes = usuarios_df[usuarios_df['nombre'].str.lower() == usuario.nombre.lower()] #Realiza una comparación de igualdad entre cada valor de la columna "nombre" (en minúsculas) y el nombre del usuario (también en minúsculas).
        return { #Indica que la función debe devolver un resultado
            "mensaje": f"El cliente '{usuario.nombre}' ya se encuentra registrado.", #El resultado es una cadena que incluye el valor dinámico de usuario.nombre
            "datos": datos_existentes.to_dict(orient="records") #convierte un tabla de datos en una lista de diccionarios, donde cada fila es un diccionario.
        }

    # Si el usuario no existe, agregarlo al DataFrame
    nuevo_usuario = {
        "nombre": usuario.nombre,
        "edad": usuario.edad,
        "enfermedades": ",".join(usuario.enfermedades)  # convierte una lista de enfermedades almacenada en usuario.enfermedades en una única cadena de texto, donde cada elemento de la lista está separado por una coma.
    }
    # Usar concat() para agregar el nuevo usuario al DataFrame
    usuarios_df = pd.concat([usuarios_df, pd.DataFrame([nuevo_usuario])], ignore_index=True) #agrega un nuevo registro (contenido en el diccionario nuevo_usuario) al DataFrame usuarios_df, asegurando que el índice se actualice automáticamente.
    guardar_datos(usuarios_df)  # Guardar los datos en el archivo Excel
    return {
        "mensaje": f"El cliente '{usuario.nombre}' ha sido registrado exitosamente.",
        "datos": nuevo_usuario
    }

# Endpoint para listar todos los usuarios registrados
@app.get("/usuarios/") #devuelve información relacionada con los usuarios
def listar_usuarios(): # devolver una lista de usuarios típicamente en formato JSON.
    if usuarios_df.empty:  # Si el DataFrame (tabla de datos) está vacío
        return {"mensaje": "No hay usuarios registrados."} #devuelme un mensaje
    
    # Convertir el DataFrame a una lista de diccionarios
    usuarios = usuarios_df.to_dict(orient="records")
    
    # Convertir la cadena de enfermedades de nuevo en lista
    for usuario in usuarios:
        usuario["enfermedades"] = usuario["enfermedades"].split(",")  # Convertir cadena de enfermedades a lista
    
    return {"usuarios": usuarios}


