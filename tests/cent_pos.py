import cv2
import logging as log

#Iniciamos el modo de logging
log.basicConfig(level = 10)

#Creamos la mascara de color
umbral_bajo = (100,100,100)
umbral_alto = (125,255,255)

conf = True
frame = cv2.imread('sample/bluesquare.jpg')

#Gestionamos el resultado
if conf == True:
    #log.debug(msg="Foto tomada correctamente")
    #Pasamos un filtro hsv 
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    #Creamos una mascara con los umbrales predefinidos para el azul
    mask = cv2.inRange(img, umbral_bajo, umbral_alto)
    #Colocamos la mascara sobre el filtro
    res = cv2.bitwise_and(img, img ,mask = mask)
    #Devolvemos el resultado a BGR
    res_rgb = cv2.cvtColor(res, cv2.COLOR_HSV2BGR)
    #Detectamos los contornos que nos ha dejado la mascara
    contornos, hierachy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    #Si encontramos algún contorno seguimos, sino mostramos un error
    if len(contornos) != 0:
        #Para cada contorno encontrado realizamos las operaciones
        for contorno in contornos:
            #Calculamos el perimetro del contorno
            epsilon = 0.01*cv2.arcLength(contorno, True)
            #Calculamos los vertices que tenemos
            vertices = cv2.approxPolyDP(contorno, epsilon, True)
            x,y,w,h = cv2.boundingRect(vertices)
            #Si tiene 4 vértices realizamos la localización del centro
            if len(vertices) == 4:
                #Calculamos el momento del contorno
                M = cv2.moments(contorno)
                #Si el momento es distinto a 0
                if M['m00'] != 0:
                    #Calculamos la x y la y central
                    cx = int(M['m10']/M['m00'])
                    cy = int(M['m01']/M['m00'])
                    #Dibujamos el contorno 
                    cv2.drawContours(res_rgb, [contorno], -1, (0,255,0), 2)
                    #Escribimos la figura que es
                    cv2.putText(res_rgb, f"Cuadrado x:{cx} y:{cy}", (x,y-5),1,1.5,(0,255,0),2)
                    #Creamos un circulo indicando el centro
                    cv2.circle(res_rgb, (cx,cy), 7, (0,0,255), -1)
                    #Guardamos la foto
                    cv2.imwrite(f"processed/prueba.png", res_rgb)
                    #Escribimos por consola la posición del cuadrado
                    log.debug(msg=f"Cuadrado encontrado en posición: {cx},{cy}")
            else:
                #Representamos el error de que no se ha encontrado un cuadrado
                log.error(msg="No se han detectado 4 vertices.")
    else:
        #Representamos el error de que no se ha encontrado el color azul
        log.error(msg="No se ha detectado el color azul.")