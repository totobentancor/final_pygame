import random

def seleccionar_categoria(categorias: dict):
    """Selecciona aleatoriamente una categoría y mezcla sus preguntas.

    Devuelve (categoria_seleccionada, lista_preguntas).
    Si `categorias` está vacío, devuelve (None, []).
    """
    if not categorias:
        return None, []

    categoria_seleccionada = random.choice(list(categorias.keys()))
    preguntas = categorias[categoria_seleccionada][:]
    random.shuffle(preguntas)
    return categoria_seleccionada, preguntas


def cargar_todas_constantes(config: dict) -> tuple:
    """Extrae TODAS las constantes del config.json.
    
    Retorna tupla con todas las constantes necesarias para juego_pygame.
    """
    rutas = config.get("rutas", {})
    game_path = rutas.get("game_path") or rutas.get("game_pygame_path", "")
    game_pygame_path = rutas.get("game_pygame_path", "")
    
    # Rutas
    PATH_ESTADISTICAS = game_path + rutas.get("estadisticas", "\\estadisticas.json")
    PATH_PREGUNTAS = game_path + rutas.get("preguntas", "\\preguntas.csv")
    PATH_IMAGEN_MENU = game_pygame_path + rutas.get("imagen_menu", "\\imagen_menu.png")
    PATH_IMAGEN_TIENDA = game_pygame_path + rutas.get("imagen_tienda", "\\tienda.png")
    PATH_IMAGEN_INICIO = game_pygame_path + rutas.get("imagen_inicio", "\\imagen_inicio.png")
    PATH_IMAGEN_CLASIFICACION = game_pygame_path + rutas.get("imagen_clasificacion", "\\imagen_clasificacion.png")
    PATH_IMAGEN_USUARIO = game_pygame_path + rutas.get("imagen_usuario", "\\imagen_usuario.png")
    
    # Colores
    WHITE = tuple(config["colores"]["WHITE"])
    BLACK = tuple(config["colores"]["BLACK"])
    GRAY = tuple(config["colores"]["GRAY"])
    LIGHT_GRAY = tuple(config["colores"]["LIGHT_GRAY"])
    COLOR_CORRECTO = tuple(config["colores"]["COLOR_CORRECTO"])
    COLOR_INCORRECTO = tuple(config["colores"]["COLOR_INCORRECTO"])
    COLOR_TITULO = tuple(config["colores"]["COLOR_TITULO"])
    
    # Pantalla
    SCREEN_WIDTH = config["pantalla"]["ancho"]
    SCREEN_HEIGHT = config["pantalla"]["alto"]
    
    # Fuentes
    FONT_SIZE_NORMAL = config["fuentes"]["normal"]
    FONT_SIZE_GRANDE = config["fuentes"]["grande"]
    FONT_SIZE_PEQUENO = config["fuentes"]["pequeno"]
    
    # Botones
    BUTTON_WIDTH_NORMAL = config["botones"]["ancho_normal"]
    BUTTON_HEIGHT_NORMAL = config["botones"]["alto_normal"]
    BUTTON_WIDTH_PREGUNTA = config["botones"]["ancho_pregunta"]
    BUTTON_HEIGHT_PREGUNTA = config["botones"]["alto_pregunta"]
    BUTTON_SPACING_NORMAL = config["botones"]["spacing_normal"]
    BUTTON_SPACING_PREGUNTA = config["botones"]["spacing_pregunta"]
    
    
    # Estadísticas iniciales del juego
    
    CANTIDAD_PREGUNTAS = config.get("cantidad_preguntas", 5)
    VIDAS_INICIALES = config.get("vidas_iniciales", 3)
    PUNTAJE_INICIAL = config.get("puntaje_inicial", 0)
    MONEDAS_INICIALES = config.get("monedas_iniciales", 0)
    ACIERTOS_INICIAL = config.get("aciertos", 0)
    ERRORES_INICIAL = config.get("errores", 0)
    TIEMPOS_RESPUESTA_INICIAL = config.get("tiempos_respuesta", [])
    COSTO_VIDA = config.get("costo_vida", 3)
    
    return (
        PATH_ESTADISTICAS, PATH_PREGUNTAS,
        PATH_IMAGEN_MENU, PATH_IMAGEN_TIENDA, PATH_IMAGEN_CLASIFICACION, PATH_IMAGEN_INICIO,PATH_IMAGEN_USUARIO,
        WHITE, BLACK, GRAY, LIGHT_GRAY, COLOR_CORRECTO, COLOR_INCORRECTO, COLOR_TITULO,
        SCREEN_WIDTH, SCREEN_HEIGHT,
        FONT_SIZE_NORMAL, FONT_SIZE_GRANDE, FONT_SIZE_PEQUENO,
        BUTTON_WIDTH_NORMAL, BUTTON_HEIGHT_NORMAL, BUTTON_WIDTH_PREGUNTA, BUTTON_HEIGHT_PREGUNTA,
        BUTTON_SPACING_NORMAL, BUTTON_SPACING_PREGUNTA,
        CANTIDAD_PREGUNTAS,
        VIDAS_INICIALES, PUNTAJE_INICIAL, MONEDAS_INICIALES, ACIERTOS_INICIAL, ERRORES_INICIAL, TIEMPOS_RESPUESTA_INICIAL, COSTO_VIDA
    )

