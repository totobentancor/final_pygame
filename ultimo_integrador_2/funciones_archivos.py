import re
import json
import datetime
import os

def cargar_preguntas_csv(path: str) -> dict:  
    categorias = {}
    try:
        with open(path, "r", encoding="utf-8") as archivo:
            lineas = archivo.readlines()
            for line in lineas[1:]:
                lectura = re.split(",|\n", line)
                if len(lectura) < 9:
                    continue
                dato = {}
                dato["categoria"] = lectura[0]
                dato["dificultad"] = lectura[1]
                dato["puntaje"] = int(lectura[2])
                dato["enunciado"] = lectura[3]
                dato["opcion_1"] = lectura[4]
                dato["opcion_2"] = lectura[5]
                dato["opcion_3"] = lectura[6]
                dato["opcion_4"] = lectura[7]
                dato["opciones"] = [
                    dato.pop("opcion_1"),
                    dato.pop("opcion_2"),
                    dato.pop("opcion_3"),
                    dato.pop("opcion_4")
                ]
                dato["respuesta_correcta"] = lectura[8]

                cat = dato["categoria"]
                if cat not in categorias:
                    categorias[cat] = []
                categorias[cat].append(dato)
    except Exception as e:
        print(f"Error al leer el archivo CSV desde el path {path} con el siguiente error: {e}")
    return categorias

# La configuracion se carga desde un archivo JSON
def cargar_configuracion(path: str) -> dict:
    try:
        with open(path, "r", encoding="utf-8") as archivo:
            config = json.load(archivo)
        return config
    except Exception as e:
        print(f"Error al cargar configuración desde {path}: {e}")
        return {}

# Guarda las estadisticas en un archivo JSON
def guardar_estadisticas_json(nombre_usuario, puntaje, monedas, vidas, aciertos, errores, tiempos_respuesta, path):
    estadistica = {
        "usuario": nombre_usuario,
        "puntaje": puntaje,
        "monedas": monedas,
        "vidas_restantes": vidas,
        "fecha": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "aciertos": aciertos,
        "errores": errores,
        "promedio_tiempo_respuesta": round(sum(tiempos_respuesta)/len(tiempos_respuesta), 2) if tiempos_respuesta else 0,
    }
    datos = []
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as archivo:
                contenido = archivo.read()
                if contenido:
                    datos = json.loads(contenido)
        except Exception as e:
            print(f"Error al leer el archivo de estadísticas desde el path{path} con el siguiente error: {e}")
            datos = []
    datos.append(estadistica)
    try:
        with open(path, "w", encoding="utf-8") as archivo:
            json.dump(datos, archivo, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Error al guardar estadísticas en {path}: {e}")
        return False

    return True


def convertir_json_a_matriz(path_json: str) -> list:
    try:
        with open(path_json, "r", encoding="utf-8") as archivo:
            lista_estadisticas = json.load(archivo)
    except Exception as e:
        print(f"Error al leer el archivo JSON: {e}")
        return []

    encabezados = ["Nombre Usuario", "Puntaje", "Vidas Restantes", "Errores (%)", "Tiempo Promedio (s)"]
    matriz_resultante = [encabezados]

    for estadistica in lista_estadisticas:
        nombre_usuario = estadistica.get("usuario", "Desconocido")
        puntaje = estadistica.get("puntaje", 0)
        vidas_restantes = estadistica.get("vidas_restantes", 0)
        errores = estadistica.get("errores", 0)
        aciertos = estadistica.get("aciertos", 0)
        total = aciertos + errores
        errores_porcentaje = (errores / total * 100) if total > 0 else 0
        tiempo_promedio = estadistica.get("promedio_tiempo_respuesta", 0)

        fila_actual = [
            str(nombre_usuario),
            str(puntaje),
            str(vidas_restantes),
            f"{errores_porcentaje:.2f}%",
            f"{tiempo_promedio:.2f}s"
        ]

        matriz_resultante.append(fila_actual)

    return matriz_resultante

def cargar_nombre_usuarios(path_json: str) -> list:
    nombres = []
    if os.path.exists(path_json):
        try:
            with open(path_json, "r", encoding="utf-8") as archivo:
                contenido = archivo.read()
                if contenido:
                    data = json.loads(contenido)
                    for usuarios in data:
                        if "usuario" in usuarios:
                            nombres.append(usuarios["usuario"])
        except Exception as e:
            print(f"Error al leer usuarios existentes desde {path_json}: {e}")
    return nombres