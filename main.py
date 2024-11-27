# from fastapi import FastAPI
# from pydantic import BaseModel
# import random

# app = FastAPI()

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

import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Ruta del archivo Excel donde se guardarán los datos
DATABASE_PATH = "usuarios_db.xlsx"

# Modelo de datos del usuario
class Usuario(BaseModel):
    nombre: str
    edad: int
    enfermedades: List[str]

# Función para cargar datos desde Excel
def cargar_datos():
    try:
        # Leer el archivo Excel
        return pd.read_excel(DATABASE_PATH)
    except FileNotFoundError:
        # Si el archivo no existe, crear un DataFrame vacío
        return pd.DataFrame(columns=["nombre", "edad", "enfermedades"])

# Función para guardar datos en Excel
def guardar_datos(data):
    data.to_excel(DATABASE_PATH, index=False)

# Cargar la base de datos al iniciar la aplicación
usuarios_df = cargar_datos()

# Endpoint para registrar o verificar usuarios
@app.post("/registro/")
def registro_usuario(usuario: Usuario):
    global usuarios_df

    # Verificar si el usuario ya existe en el DataFrame
    if not usuarios_df.empty and usuario.nombre.lower() in usuarios_df['nombre'].str.lower().values:
        # Si el usuario existe, devolver un mensaje
        datos_existentes = usuarios_df[usuarios_df['nombre'].str.lower() == usuario.nombre.lower()]
        return {
            "mensaje": f"El cliente '{usuario.nombre}' ya se encuentra registrado.",
            "datos": datos_existentes.to_dict(orient="records")
        }

    # Si el usuario no existe, agregarlo al DataFrame
    nuevo_usuario = {
        "nombre": usuario.nombre,
        "edad": usuario.edad,
        "enfermedades": ",".join(usuario.enfermedades)  # Convertir la lista en una cadena separada por comas
    }
    # Usar concat() para agregar el nuevo usuario al DataFrame
    usuarios_df = pd.concat([usuarios_df, pd.DataFrame([nuevo_usuario])], ignore_index=True)
    guardar_datos(usuarios_df)  # Guardar los datos en el archivo Excel
    return {
        "mensaje": f"El cliente '{usuario.nombre}' ha sido registrado exitosamente.",
        "datos": nuevo_usuario
    }

# Endpoint para listar todos los usuarios registrados
@app.get("/usuarios/")
def listar_usuarios():
    if usuarios_df.empty:  # Si el DataFrame está vacío
        return {"mensaje": "No hay usuarios registrados."}
    
    # Convertir el DataFrame a una lista de diccionarios
    usuarios = usuarios_df.to_dict(orient="records")
    
    # Convertir la cadena de enfermedades de nuevo en lista
    for usuario in usuarios:
        usuario["enfermedades"] = usuario["enfermedades"].split(",")  # Convertir cadena de enfermedades a lista
    
    return {"usuarios": usuarios}


