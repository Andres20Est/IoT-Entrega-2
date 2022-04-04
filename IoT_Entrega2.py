"""
Tema = IoT Entrega #2
@author: Julian Betancout, Laura Rodriguez, Andres Jaramillo
"""
#%% Librerias
#! /usr/bin/python2
from datetime import datetime, date
import sys
import requests
from time import sleep
import RPi.GPIO as GPIO
import board
import Adafruit_DHT
from datetime import datetime, date
from HX711 import *
from datetime import timedelta


#%% Variables Globales

T_Sleep= 80 #Tiempo entre dato y dato (decimas de segundos)
Conteo=0    #Delta entre la medicion del sensor infrarojo y los otros 2
PersonaIR=False # Variable para que no se spamee el sensor infra rojo
PersonasDetectadas=0
#%% Inicializacion Sensor Temperatura
sensor = Adafruit_DHT.DHT11
pinTemp = 4 # Pin sensor temperatura = pin 4
#%% Inicializacion Celda de carga
hx = AdvancedHX711(27, 17, 20000, 1, Rate.HZ_80)
#%% Inicializacion Sensor infrarojo
GPIO.setmode(GPIO.BOARD)
pin = 16

GPIO.setup (16, GPIO.IN)
input = GPIO.input(16)
#%% Ciclo infinito 
while True:
    if (Conteo==T_Sleep):
        Conteo=0
        #%% Obtencion temperatura y humedad
        humedad, temperatura = Adafruit_DHT.read_retry(sensor, pinTemp)
        #Temperatura en Farenheight
        Temperatura_f= temperatura *(9/5)+32
        #Muestra en pantalla la temperatura en °C, °F y la humedad del aire    
        print (
            "temperatura:{:.1f} F° / {:.1f} C°  humedad: {}%".format(
                Temperatura_f, temperatura, humedad
                )
            )
        valor = (hx.weight(timedelta(seconds=1)))
        
        Enviar = requests.get("https://api.thingspeak.com/update?api_key=MBJ69CL4SOIPA45O&field1=0"
    +str(temperatura)+"&field3=0"+str(humedad)+"&field4=0"+str(PersonasDetectadas)+"&field5=0"+str(valor))
        
        #%% Sensor de presion
        
        
    
        print(valor) #eg. 0.03 g
        
    #%% Deteccion Persona usando sensor infrarojo
    # Si el sensor detecta y no hay nadie
    if (not (GPIO.input(pin)) and (PersonaIR==False)):
        print("persona derectada")
        PersonasDetectadas+=1
        PersonaIR=True
        print("Personas detectadas totales = " + str(PersonasDetectadas))
    # Si el sensor detecta y hay algo en el sensor
    elif(PersonaIR==True and (not (GPIO.input(pin)))):
        pass
    #Si el sensor justo deja de detectar a alguien 
    else:
        PersonaIR=False
        
    #Espera 10 segundo para tomar el proximo dato
    sleep(0.1)
    Conteo+=1