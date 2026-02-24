import pygame
from funciones_archivos import *
from funciones_configuracion import *


BASE_PATH = r"C:\Users\Equipo\OneDrive\Escritorio\Toto(Python)\matrices(arrays)\nuevo_integrador\final_pygame\ultimo_integrador_2"
PATH_CONFIG = BASE_PATH + "\\configuracion.json"
config = cargar_configuracion(PATH_CONFIG)
(PATH_ESTADISTICAS, PATH_PREGUNTAS, PATH_IMAGEN_MENU, PATH_IMAGEN_TIENDA,PATH_IMAGEN_CLASIFICACION, 
 PATH_IMAGEN_INICIO, PATH_IMAGEN_USUARIO, WHITE, BLACK, GRAY, LIGHT_GRAY, 
 COLOR_CORRECTO, COLOR_INCORRECTO, COLOR_TITULO, SCREEN_WIDTH, SCREEN_HEIGHT, 
 FONT_SIZE_NORMAL, FONT_SIZE_GRANDE, FONT_SIZE_PEQUENO, BUTTON_WIDTH_NORMAL, 
 BUTTON_HEIGHT_NORMAL, BUTTON_WIDTH_PREGUNTA, BUTTON_HEIGHT_PREGUNTA, 
 BUTTON_SPACING_NORMAL, BUTTON_SPACING_PREGUNTA) = cargar_todas_constantes(config)

# precargar fondos 
def precarga(path):
    try:
        surf = pygame.image.load(path)
        return pygame.transform.scale(surf, (SCREEN_WIDTH, SCREEN_HEIGHT))
    except Exception as e:
        print(f"No se pudo cargar {path}: {e}")
        return None

FONDO_MENU = precarga(PATH_IMAGEN_MENU)
FONDO_TIENDA = precarga(PATH_IMAGEN_TIENDA)
FONDO_INICIO = precarga(PATH_IMAGEN_INICIO)
FONDO_CLASIFICACION = precarga(PATH_IMAGEN_CLASIFICACION)
FONDO_USUARIO = precarga(PATH_IMAGEN_USUARIO)

class Button:
    """Clase para gestionar botones interactivos en pygame."""
    def __init__(self, text, x, y, width, height, color, hover_color, action=None, font_size=36):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.hover_color = hover_color
        self.action = action
        self.font = pygame.font.Font(None, font_size)

    def dibujar(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.color
        pygame.draw.rect(screen, color, self.rect)
        text_surf = self.font.render(self.text, True, BLACK)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def detectar_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN: # o MOUSEBUTTONUP según preferencia
            if event.button == 1 and self.rect.collidepoint(event.pos):
                if callable(self.action):
                    self.action()
                else:
                    return self.action
        return None



def crear_usuario_final_pygame(usuarios_existentes, screen):
    """Pide al usuario ingresar su nombre y confirmar."""
    usuario = ""
    font_local = pygame.font.Font(None, FONT_SIZE_NORMAL)
    activo = True
    mensaje_error = False
    while activo:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and usuario:
                    if usuario in usuarios_existentes:
                        mensaje_error = True
                        usuario = ""
                    else:
                        confirmado = confirmar_usuario_pygame(usuario, screen)
                        if confirmado:
                            activo = False
                        else:
                            usuario = ""
                elif event.key == pygame.K_BACKSPACE:
                    usuario = usuario[:-1]
                else:
                    if len(usuario) < 15 and event.unicode.isprintable():
                        usuario += event.unicode

        if FONDO_USUARIO:
            screen.blit(FONDO_USUARIO, (0,0))
        else:
            screen.fill(WHITE)
        texto = font_local.render("Ingresa tu nombre y presiona Enter:", True, WHITE)
        nombre = font_local.render(usuario, True, COLOR_TITULO)
        screen.blit(texto, (SCREEN_WIDTH // 2 - texto.get_width() // 2, 200))
        screen.blit(nombre, (SCREEN_WIDTH // 2 - nombre.get_width() // 2, 300))
        if mensaje_error:
            error = font_local.render("El usuario ya existe. Ingresa otro.", True, COLOR_INCORRECTO)
            screen.blit(error, (SCREEN_WIDTH // 2 - error.get_width() // 2, 350))
        pygame.display.flip()
    return usuario


def mostrar_pregunta_pygame(screen, pregunta_categoria):
    """Muestra una pregunta y devuelve el índice de la opción seleccionada (0-3)."""
    running = True
    seleccion = None

    enunciado = pregunta_categoria["enunciado"]
    opciones = pregunta_categoria["opciones"]

    button_width = BUTTON_WIDTH_PREGUNTA
    button_height = BUTTON_HEIGHT_PREGUNTA
    button_x = (SCREEN_WIDTH - button_width) // 2
    button_spacing = BUTTON_SPACING_PREGUNTA
    buttons = []
    for i, opcion in enumerate(opciones):
        btn = Button(
            opcion,
            button_x,
            200 + i * button_spacing,
            button_width,
            button_height,
            GRAY,
            LIGHT_GRAY,
            action=lambda idx=i: idx,
            font_size=30
        )
        buttons.append(btn)

    font_local = pygame.font.Font(None, FONT_SIZE_NORMAL)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for idx, btn in enumerate(buttons):
                    if btn.rect.collidepoint(event.pos):
                        seleccion = idx
                        running = False

        if FONDO_MENU:
            screen.blit(FONDO_MENU, (0,0))
        else:
            screen.fill(WHITE)
            

        enunciado_texto = font_local.render(enunciado, True, BLACK)
        enunciado_rect = enunciado_texto.get_rect(center=(SCREEN_WIDTH // 2, 150))
        screen.blit(enunciado_texto, enunciado_rect)

        for btn in buttons:
            btn.dibujar(screen)

        pygame.display.flip()

    return seleccion


def mostrar_feedback(screen, es_correcta, puntaje, vidas, aciertos, errores, monedas,respuesta_correcta):
    """Muestra feedback (correcto/incorrecto) con estadísticas."""
    running = True
    font_local = pygame.font.Font(None, FONT_SIZE_GRANDE)
    mensaje = "¡Correcto!" if es_correcta else "Incorrecto, respuesta correcta: " + respuesta_correcta
    color = COLOR_CORRECTO if es_correcta else COLOR_INCORRECTO
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                running = False
        if FONDO_MENU:
            screen.blit(FONDO_MENU, (0,0))
        else:
            screen.fill(WHITE)  
        texto = font_local.render(mensaje, True, color)
        rect = texto.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
        screen.blit(texto, rect)
        info_font = pygame.font.Font(None, FONT_SIZE_NORMAL)
        info1 = info_font.render(f"Vidas: {vidas}  Puntaje: {puntaje}", True, BLACK)
        info2 = info_font.render(f"Aciertos: {aciertos}  Errores: {errores}", True, BLACK)
        info3 = info_font.render(f"Monedas: {monedas}", True, BLACK)
        info1_rect = info1.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        info2_rect = info2.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        info3_rect = info3.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))
        screen.blit(info1, info1_rect)
        screen.blit(info2, info2_rect)
        screen.blit(info3, info3_rect)
        pygame.display.flip()


def tienda_de_vidas_pygame(screen, monedas, vidas, costo_vida, aciertos, errores, puntaje, respuesta_correcta):
    """Tienda simple: comprar vidas o seguir sin comprar."""
    running = True
    font_local = pygame.font.Font(None, FONT_SIZE_NORMAL)
    base_y = 305
    spacing = BUTTON_SPACING_NORMAL
    button1 = Button("Comprar vida por 3 monedas", 250, base_y, 300, 50, GRAY, LIGHT_GRAY, action="comprar", font_size=28)
    button2 = Button("Seguir sin comprar", 250, base_y + spacing, 300, 50, GRAY, LIGHT_GRAY, action="seguir", font_size=28)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            res1 = button1.detectar_click(event)
            res2 = button2.detectar_click(event)
            if res1 == "comprar":
                if monedas >= costo_vida:
                    vidas += 1
                    monedas -= costo_vida
                    mostrar_feedback(screen, True, puntaje=puntaje, vidas=vidas, aciertos=aciertos, errores=errores, monedas=monedas, respuesta_correcta=respuesta_correcta) 
                else:
                    mostrar_feedback(screen, False, puntaje=puntaje, vidas=vidas, aciertos=aciertos, errores=errores, monedas=monedas, respuesta_correcta=respuesta_correcta )
                running = False
            elif res2 == "seguir":
                running = False
        if FONDO_TIENDA:
            screen.blit(FONDO_TIENDA, (0,0))
        else:
                screen.fill(WHITE)
        texto = font_local.render(f"Tienda de vidas - Monedas: {monedas} - Vidas: {vidas}", True, BLACK)
        screen.blit(texto, (SCREEN_WIDTH // 2 - texto.get_width() // 2, 200))
        button1.dibujar(screen)
        button2.dibujar(screen)
        pygame.display.flip()
    return monedas, vidas


def confirmar_usuario_pygame(nombre_usuario, screen):
    """Pide confirmación del nombre de usuario (S/N)."""
    font_local = pygame.font.Font(None, FONT_SIZE_NORMAL)
    activo = True
    respuesta = None
    while activo:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    respuesta = True
                    activo = False
                elif event.key == pygame.K_n:
                    respuesta = False
                    activo = False
        if FONDO_USUARIO:
            screen.blit(FONDO_USUARIO, (0,0))
        else:
            screen.fill(WHITE)
        texto = font_local.render(f"¿Seguro que '{nombre_usuario}' será tu usuario? (S/N)", True, BLACK)
        screen.blit(texto, (SCREEN_WIDTH // 2 - texto.get_width() // 2, 250))
        pygame.display.flip()
    return respuesta


