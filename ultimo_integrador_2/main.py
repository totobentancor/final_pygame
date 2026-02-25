import pygame
from la_magia import *
pygame.init()


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("¡ROBALE AL PIRATA!")

if __name__ == "__main__":
    # Mostrar imagen de inicio
    mostrar_imagen_inicio(screen)
    
    # Loop principal del menú
    running = True
    while running:
        opcion = menu_principal(screen)
        
        if opcion == "jugar":
            jugar_preguntados_pirata(screen)
        elif opcion == "clasificacion":
            mostrar_clasificacion_pygame(screen)
        elif opcion == "salir":
            running = False
    pygame.quit()
