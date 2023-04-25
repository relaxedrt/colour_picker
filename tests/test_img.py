import cv2
import logging as log

#Iniciamos el modo de logging
log.basicConfig(level = 10)

#Creamos la mascara de color
umbral_bajo = (100,100,100)
umbral_alto = (125,255,255)

conf = True
frame = cv2.imread('sample/cuadrado_rojo.jpg')

#Gestionamos el resultado
if conf == True:
    log.debug(msg="Foto tomada correctamente")
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(img, umbral_bajo, umbral_alto)
    res = cv2.bitwise_and(img, img ,mask = mask)
    res_rgb = cv2.cvtColor(res, cv2.COLOR_HSV2BGR)
    contornos, hierachy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
	#Mostramos las imagenes por pantalla
    cv2.drawContours(res_rgb, contornos, -1, (0,255,0), 3)
    if len(contornos) != 0:
        for contorno in contornos:
            epsilon = 0.01*cv2.arcLength(contorno, True)
            vertices = cv2.approxPolyDP(contorno, epsilon, True)
            x,y,w,h = cv2.boundingRect(vertices)
            if len(vertices) == 4:
                cv2.putText(res_rgb, "Cuadrado", (x,y-5),1,1.5,(0,255,0),2)
                cv2.imwrite(f"processed/prueba.png", res_rgb)
                log.debug(msg=f"Cuadrado encontrado en posición: {x},{y}")
            else:
                log.error(msg="No se han detectado 4 vertices.")
    else:
        log.error(msg="No se ha detectado el color azul.")


