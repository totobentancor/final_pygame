import pygame
from funciones_archivos import *
from funciones_configuracion import *
from backend import *


def mostrar_clasificacion_pygame(screen):
    """Muestra la clasificación usando `convertir_json_a_matriz` y recorriendo la matriz.
    
    RECORRIDO DE MATRIZ: fila → columna
    """
    running = True
    font_local = pygame.font.Font(None, FONT_SIZE_PEQUENO)
    path_json = PATH_ESTADISTICAS

    matriz = convertir_json_a_matriz(path_json)

    num_filas_datos = max(0, len(matriz) - 1)
    registros_por_pagina = 10
    pagina = 0
    total_paginas = max(1, (num_filas_datos + registros_por_pagina - 1) // registros_por_pagina)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT and pagina < total_paginas - 1:
                        pagina += 1
                    elif event.key == pygame.K_LEFT and pagina > 0:
                        pagina -= 1
                    elif event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                        running = False
                else:
                    running = False

        if FONDO_CLASIFICACION:
            screen.blit(FONDO_CLASIFICACION, (0,0))
        else:
            screen.fill(WHITE)
        titulo = font_local.render("Clasificación (Estadísticas)", True, COLOR_TITULO)
        screen.blit(titulo, (SCREEN_WIDTH // 2 - titulo.get_width() // 2, 50))

        y0 = 120
        padding_x = 20
        col_count = len(matriz[0]) if matriz else 1
        col_width = (SCREEN_WIDTH - padding_x * 2) // col_count

        if matriz and len(matriz) > 1:
            encabezados = matriz[0]
            # Dibujar encabezados: recorro columna por columna
            for col_idx, encabezado in enumerate(encabezados):
                x = padding_x + col_idx * col_width
                header_surf = font_local.render(str(encabezado), True, COLOR_TITULO)
                screen.blit(header_surf, (x, y0))

            # Recorrido de DATOS: fila → columna
            # Calcular cuáles filas mostrar en esta página
            inicio = pagina * registros_por_pagina
            fin = inicio + registros_por_pagina
            filas_a_mostrar = matriz[1 + inicio : 1 + fin]  # Salto +1 porque fila 0 es encabezado
            
            # Para CADA FILA...
            for fila_idx, fila in enumerate(filas_a_mostrar):
                y = y0 + 40 + fila_idx * 30  # Calculo posición Y de la fila
                
                # recorro CADA COLUMNA en esa fila
                for col_idx, celda in enumerate(fila):
                    x = padding_x + col_idx * col_width  # Calculo posición X de la columna
                    celda_surf = font_local.render(str(celda), True, WHITE)
                    screen.blit(celda_surf, (x, y))  # Dibujo la celda en pantalla
        else:
            msg = font_local.render("No hay datos de clasificación.", True, (255, 100, 100))
            screen.blit(msg, (80, y0))

        info = font_local.render(
            f"Página {pagina + 1}/{total_paginas} - (Flecha izq/der) para navegar, ESC/Enter/clic salir",
            True, (200, 200, 200)
        )
        screen.blit(info, (80, SCREEN_HEIGHT - 60))
        pygame.display.flip()



def mostrar_imagen_inicio(screen):
    """Muestra pantalla de inicio. Se cierra al hacer clic o pulsar una tecla."""
    font_local = pygame.font.Font(None, FONT_SIZE_GRANDE)
    mostrando = True
    while mostrando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                mostrando = False
        if FONDO_INICIO:
            screen.blit(FONDO_INICIO, (0,0))
        else:
            screen.fill((0,0,0))
        texto = font_local.render("Responde Preguntas y ¡ROBALE AL PIRATA!", True, WHITE)
        rect = texto.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 300))
        screen.blit(texto, rect)
        pygame.display.flip()


def menu_principal(screen):
    """Menú principal del juego con tres opciones."""
    button_width = BUTTON_WIDTH_NORMAL
    button_height = BUTTON_HEIGHT_NORMAL
    button_x = (SCREEN_WIDTH - button_width) // 2
    button_spacing = BUTTON_SPACING_NORMAL
    font = pygame.font.Font(None, FONT_SIZE_NORMAL)
    play_button = Button("Roba monedas piratas por preguntas", button_x, 
                        SCREEN_HEIGHT // 2 - button_spacing, button_width, 
                        button_height, GRAY, LIGHT_GRAY, action="jugar", font_size=22)
    leaderboard_button = Button("Ver quien robo mas monedas (Clasificaciones)", button_x, 
                               SCREEN_HEIGHT // 2, button_width, button_height, 
                               GRAY, LIGHT_GRAY, action="clasificacion", font_size=20)
    quit_button = Button("Huir del Pirata (Salir)", button_x, 
                        SCREEN_HEIGHT // 2 + button_spacing, button_width, 
                        button_height, GRAY, LIGHT_GRAY, action="salir", font_size=22)
    
    seleccion = None
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            res1 = play_button.detectar_click(event)
            res2 = leaderboard_button.detectar_click(event)
            res3 = quit_button.detectar_click(event)
            
            if res1 == "jugar":
                seleccion = "jugar"
                running = False
            elif res2 == "clasificacion":
                seleccion = "clasificacion"
                running = False
            elif res3 == "salir":
                seleccion = "salir"
                running = False
                
        if FONDO_MENU:
            screen.blit(FONDO_MENU, (0, 0))
        else:
            screen.fill(BLACK)
        
        titulo_texto = font.render("¡ROBALE AL PIRATA! (Menu Principal)", True, WHITE)
        titulo_rect = titulo_texto.get_rect(center=(SCREEN_WIDTH // 2, 150))
        screen.blit(titulo_texto, titulo_rect)
        
        play_button.dibujar(screen)
        leaderboard_button.dibujar(screen)
        quit_button.dibujar(screen)
        
        pygame.display.flip()
    
    return seleccion

def jugar_preguntados_pirata(screen):
    """Flujo principal del juego: crear usuario, cargar preguntas, jugar, mostrar resultados."""
    # Cargar configuración e imágenes
    usuarios_existentes = cargar_nombre_usuarios(PATH_ESTADISTICAS)
    
    # Mostrar imagen de inicio
    mostrar_imagen_inicio(screen)
    
    # Crear nuevo usuario
    usuario = crear_usuario_final_pygame(usuarios_existentes, screen)
    
    # Cargar preguntas
    todas_preguntas = cargar_preguntas_csv(PATH_PREGUNTAS)
    if not todas_preguntas:
        print("No hay preguntas disponibles.")
        return
    
    # Seleccionar categoría
    categoria, preguntas = seleccionar_categoria(todas_preguntas)
    if not preguntas:
        print(f"No hay preguntas para la categoría {categoria}")
        return
    
    # Inicializar estadísticas del usuario
    vidas = 3
    puntaje = 0 
    aciertos = 0
    errores = 0
    monedas = 0
    tiempos_respuesta = []
    
    # Jugar las preguntas
    for pregunta in preguntas:
        if vidas <= 0:
            break
        
        # Mostrar pregunta y obtener respuesta
        respuesta_usuario = mostrar_pregunta_pygame(screen, pregunta)
        if respuesta_usuario is None:
            continue

    # Verificar respuesta: ya que la respuesta devuelve un índice (0-3)
        respuesta_correcta = pregunta.get('respuesta_correcta')
        es_correcta = pregunta['opciones'][respuesta_usuario] == pregunta['respuesta_correcta']
        if es_correcta:
            aciertos += 1
            puntaje += pregunta.get("puntaje", 0)
            monedas += 1
        else:
            errores += 1
            vidas -= 1
        
        # Mostrar feedback
        mostrar_feedback(screen, es_correcta, puntaje, vidas, aciertos, errores, monedas,respuesta_correcta)
        
        # Mostrar tienda si no es la última pregunta
        if vidas > 0 and pregunta != preguntas[-1]:
            monedas, vidas = tienda_de_vidas_pygame(screen, monedas, vidas, costo_vida=3,
                                                    aciertos=aciertos, errores=errores, puntaje=puntaje, respuesta_correcta=pregunta.get('respuesta_correcta'))
    
    # Guardar estadísticas
    guardar_estadisticas_json(
        usuario,
        puntaje,
        monedas,
        vidas,
        aciertos,
        errores,
        tiempos_respuesta,
        PATH_ESTADISTICAS
    )
    
    # Mostrar clasificación final
    mostrar_clasificacion_pygame(screen)
