import cv2
import numpy as np

cam = cv2.VideoCapture(0)

if not cam.isOpened():
  print("No se pudo abrir la cámara")
  exit()

try:
  while True:
    ret, frame = cam.read()
    if not ret:
      break

    frame = cv2.flip(frame, 2)
    display_frame = frame.copy()

    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame_blur = cv2.GaussianBlur(frame_gray, (5, 5), 0)
    thresh = cv2.adaptiveThreshold(frame_blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                   cv2.THRESH_BINARY_INV, 11, 2)

    kernel = np.ones((5, 5), np.uint8)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
      if cv2.contourArea(contour) < 800:
        continue

      cv2.drawContours(display_frame, [contour], -1, (255, 0, 0), 2)  # Silueta Azul

      (x, y, w, h) = cv2.boundingRect(contour)
      cv2.rectangle(display_frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

      cv2.putText(display_frame, "Hueso detectado", (x, y - 10),
                  cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    cv2.imshow("Silueta (Mascara)", thresh)
    cv2.imshow("Camara - Deteccion de Hueso", display_frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
      break

except KeyboardInterrupt:
  print("\nPrograma interrumpido por el usuario")

finally:
  cam.release()
  cv2.destroyAllWindows()