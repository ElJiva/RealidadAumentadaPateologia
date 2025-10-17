import cv2
import pygame
import numpy as np

def main():
    """
    Captura video de la cámara con OpenCV y lo muestra en una ventana de PyGame.
    """
    # Inicializar PyGame
    pygame.init()

    # Configuración de la ventana de PyGame
    screen_width = 640
    screen_height = 480
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("PyGame Video Capture")

    # Inicializar la captura de video de OpenCV
    # El argumento 0 selecciona la cámara web predeterminada.
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: No se puede abrir la cámara.")
        return

    running = True
    while running:
        # Manejo de eventos de PyGame
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Capturar un fotograma de la cámara
        ret, frame = cap.read()
        if not ret:
            print("Error: No se pudo leer el fotograma de la cámara.")
            break

        # Convertir el fotograma de BGR (OpenCV) a RGB (PyGame)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Rotar y voltear el fotograma para la orientación correcta
        # np.rot90 rota la matriz del fotograma
        frame_rotated = np.rot90(frame_rgb)
        # pygame.surfarray.make_surface crea una superficie de PyGame desde la matriz
        pygame_frame = pygame.surfarray.make_surface(frame_rotated)
        # pygame.transform.flip voltea la superficie para un efecto de espejo
        pygame_frame = pygame.transform.flip(pygame_frame, True, False)


        # Dibujar el fotograma en la pantalla de PyGame
        screen.blit(pygame_frame, (0, 0))

        # Actualizar la pantalla
        pygame.display.flip()

    # Liberar la cámara y salir de PyGame
    cap.release()
    pygame.quit()

if __name__ == '__main__':
    main()