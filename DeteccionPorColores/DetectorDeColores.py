import cv2              #Libreria de OpenCV
import numpy as np              #Libreria de Numpy

cam = cv2.VideoCapture(0)           #Variable e inicio de la captura de la camara
kernel = np.ones((5,5),np.uint8)            #Variable cnn para filtrar la imagen de la camara con un valor de 8 bits

def deteccion():

    rangomax = np.array([80, 255, 255])             #Establecemos un rango maximo de colores a detectar
    rangomin = np.array([36, 80, 18])               #Establecemos un rango minimo de colores a detectar
    frameHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)           #Pasamos de RGB a HSV la imagen de la camara
    mascara = cv2.inRange(frameHSV, rangomin, rangomax)             #Generamos una mascara en blanco y negro que deje en blanco los objetos que encuentre en el rango de colores que le dimos
    opening = cv2.morphologyEx(mascara, cv2.MORPH_OPEN, kernel)             #Eliminamos el ruido
    contorno, _ = cv2.findContours(mascara, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)             #Buscamos los contornos de la mascara
    posibleObjeto = 3000            #Creamos una variable para establecer el area minima del objeto

    for c in contorno:
        area = cv2.contourArea(c)

        if area > posibleObjeto:
            contornoLiso = cv2.convexHull(c)
            cv2.drawContours(frame, [contornoLiso], 0, (0, 255, 0), 3)          #Dibujamos los contornos
            x, y, w, h = cv2.boundingRect(opening)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3)            #Creamos un rectangulo que rodee al objeto
            cv2.putText(frame, "Objeto", (x, y - 20), 2, 0.7, (0, 255, 0), 1, cv2.LINE_AA)          #Creamos un texto sobre el objeto

while (True):
    ret, frame = cam.read()             #Lectura de la camara

    deteccion()             #Llamamos a la funcion

    cv2.imshow('Camara', frame)             #Mostramos las imagenes de la camara

    k = cv2.waitKey(1) & 0xFF           #Guardamos la tecla "ESC" en una variable

    if k==27:
        break           #Finalizamos el bucle al apretar "ESC"