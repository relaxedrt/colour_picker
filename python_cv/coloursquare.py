# Paso 1: Importar la biblioteca OpenCV en Python
import cv2

# Paso 2: Cargar la imagen en la que queremos buscar el objeto cuadrado de color azul
imagen = cv2.imread('sample/bluesquare.jpg')

# Paso 3: Convertir la imagen a escala de grises
imagen_gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)

# Paso 4: Aplicar un filtro Gaussiano para suavizar la imagen y eliminar el ruido
imagen_suavizada = cv2.GaussianBlur(imagen_gris, (5, 5), 0)

# Paso 5: Aplicar la detección de bordes Canny para detectar los bordes en la imagen
bordes = cv2.Canny(imagen_suavizada, 50, 150)

# Paso 6: Encontrar los contornos en la imagen usando la función findContours de OpenCV
contornos, jerarquia = cv2.findContours(bordes, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Paso 7: Iterar a través de cada contorno y verificar si es un cuadrado utilizando la función approxPolyDP de OpenCV
while True:
    for contorno in contornos:
        perimetro = cv2.arcLength(contorno, True)
        aprox = cv2.approxPolyDP(contorno, 0.04 * perimetro, True)
        cv2.drawContours(imagen, contorno, -1, (0,255,0), 3)
        cv2.imshow('res', imagen)
        if len(aprox) == 4:
            # Es un cuadrado
        
            # Paso 8: Comprobar si el cuadrado es de color azul
            x, y, w, h = cv2.boundingRect(aprox)
            roi = imagen[y:y+h, x:x+w]
            color_promedio = cv2.mean(roi)
            if color_promedio[0] < 100 and color_promedio[1] < 100 and color_promedio[2] > 150:
                # Es de color azul
                print("Se ha encontrado un objeto cuadrado de color azul en la imagen.")
    if cv2.waitKey(1) & 0xFF == ord('s'):
        break
