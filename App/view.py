"""
 * Copyright 2020, Departamento de sistemas y Computación
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 """

import sys
import config
from DISClib.ADT import list as lt
from App import controller
assert config

"""
La vista se encarga de la interacción con el usuario.
Presenta el menu de opciones  y  por cada seleccion
hace la solicitud al controlador para ejecutar la
operación seleccionada.
"""

# ___________________________________________________
#  Ruta a los archivos
# ___________________________________________________

#accidentsFile = "US_Accidents_Dec19.csv"
accidentsFile = "us_accidents_small.csv"
#accidentsFile = "us_accidents_dis_2016.csv"
#accidentsFile = "us_accidents_dis_2017.csv"
#accidentsFile = "us_accidents_dis_2018.csv"
#accidentsFile = "us_accidents_dis_2019.csv"

# ___________________________________________________
# Funciones para imprimir información
# ___________________________________________________

def printAccidentsByTimeRange(cont,timeInit,Finaltime):
    lstTimeInit = timeInit.split(":")
    lstTimeFinal = Finaltime.split(":")
    hourInit = int(lstTimeInit[0])
    minuteInit = int(lstTimeInit[1])
    hourFinal = int(lstTimeFinal[0])
    minuteFinal = int(lstTimeFinal[1])

    if hourInit == 23 and minuteInit >= 30:
        lstTimeInit[0] = "00"
        lstTimeInit[1] = "00"
    elif minuteInit >= 30:
        minuteInit = "00"
        hourInit += 1
        hourInit = str(hourInit)
        lstTimeInit[0] = hourInit
        lstTimeInit[1] = minuteInit
    else:
        minuteInit = "00"
        lstTimeInit[1] = minuteInit

    if hourFinal == 23 and minuteFinal >= 30:
        lstTimeFinal[0] = "00"
        lstTimeFinal[1] = "00"
    elif minuteFinal >= 30:
        minuteFinal = "00"
        hourFinal += 1
        hourFinal = str(hourFinal)
        lstTimeFinal[0] = hourFinal
        lstTimeFinal[1] = minuteFinal
    else:
        minuteFinal = "00"
        lstTimeFinal[1] = minuteFinal
    
    timeInit = ":".join(lstTimeInit)
    Finaltime=":".join(lstTimeFinal)

    severities, percentages=controller.getAccidentsByTimeRange(cont,timeInit,Finaltime)
    for key,value in severities.items():
        print("El número de accidentes para la severidad "+key+" es: "+ str(value)+". Esto equivale a un porcentaje de "+str(percentages[key])+"%"+ "sobre el nivel total de accidentes.")

def printZoneWithMoreAccidents(analyzer,latitude,length,rad,preference):
    weekDays,total = controller.getZoneWithMoreAccidents(analyzer,latitude,length,rad,preference.lower())
    print("El total de accidentes en el radio de búsqueda es de: "+str(total))
    print("Los accidentes según el día de la semana son los siguientes: ")
    print("__________________________________")
    for key,value in weekDays.items():
        print(key+": \t"+str(value))
    print("__________________________________")

# ___________________________________________________
#  Menu principal
# ___________________________________________________


def printMenu():
    print("\n")
    print("*******************************************")
    print("Bienvenido")
    print("1- Inicializar Analizador")
    print("2- Cargar información de accidentes")
    print("3- Conocer los accidentes en una fecha")
    print("4- Conocer los accidentes anteriores a una fecha")
    print("5- Conocer los accidentes en un rango de fechas")
    print("6- Conocer el estado con más accidentes")
    print("7- Conocer los accidentes por rango de horas")
    print("8- Conocer la zona geográfica más accidentada")
    print("0- Salir")
    print("*******************************************")


"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n>')

    if int(inputs[0]) == 1:
        print("\nInicializando....")
        # cont es el controlador que se usará de acá en adelante
        cont = controller.init()

    elif int(inputs[0]) == 2:
        print("\nCargando información de accidentes aéreos ....")
        controller.loadData(cont, accidentsFile)
        print('ÁRBOL DE FECHAS')
        print('Accidentes cargados: ' + str(controller.accidentsSize(cont)))
        print('Altura del arbol: ' + str(controller.indexHeight(cont)))
        print('Elementos en el arbol: ' + str(controller.indexSize(cont)))
        print('Menor Llave: ' + str(controller.minKey(cont)))
        print('Mayor Llave: ' + str(controller.maxKey(cont)))
        print('\n')
        print('ÁRBOL DE HORAS')
        print('Altura del arbol: ' + str(controller.timeIndexHeight(cont)))
        print('Elementos en el arbol: ' + str(controller.timeIndexSize(cont)))
        print('Menor Llave: ' + str(controller.minKeyTime(cont)))
        print('Mayor Llave: ' + str(controller.maxKeyTime(cont)))

    elif int(inputs[0]) == 3:
        print("\nBuscando accidentes en una fecha específica: ")
        date = input("Ingrese la fecha a buscar (YYYY-MM-DD): ") 
        numAccidents = controller.getAccidentsByDate(cont,date)
        if numAccidents == 0:
            print("La fecha ingresada no tiene accidentes relacionados.")
        else:
            print('\nNúmero total de accidentes con severidad 1 en esa fecha: ' + str(numAccidents[0]))
            print('\nNúmero total de accidentes con severidad 2 en esa fecha: ' +str(numAccidents[1]))
            print('\nNúmero total de accidentes con severidad 3 en esa fecha: ' +str(numAccidents[2]))
            print('\nNúmero total de accidentes con severidad 4 en esa fecha: ' +str(numAccidents[3]))

    elif int(inputs[0]) == 4:
        print("\nBuscando accidentes anteriores a una fecha: ")

        date = input("Ingrese la fecha a buscar (YYYY-MM-DD): ")
        total,fecha = controller.getAccidentsBeforeTo(cont,date)
        print("El total de accidentes antes de la fecha ingresada son : " )
        print(total)
        print("La fecha con más accidentes registrados, anterior a la fecha ingresada es:")
        print(fecha)

    elif int(inputs[0]) == 5:
        print("\nBuscando accidentes en un rango de fechas: ")
        #dateInit = input("Ingrese la fecha inicial (YYYY-MM-DD): ")
        #finalDate = input("Ingrese la fecha final (YYY-MM-DD): ")

    elif int(inputs[0]) == 6:
        print("\nBuscando el estado con más accidentes: ")
        dateInit = input("Ingrese la fecha inicial (YYYY-MM-DD): ")
        finalDate = input("Ingrese la fecha final (YYY-MM-DD): ")
        result = controller.getStateWithMoreAccidents(cont,dateInit,finalDate)
        print("La fecha con más accidentes reportados en el rango de fechas es: "+result[0])
        print("El estado con más accidentes reportados en el rango de fechas es: " + result[1])

    elif int(inputs[0]) == 7:
        print("\nBuscando accidentes por rango de horas: ")
        timeInit = input("Ingrese la hora inicial (00:00-23:59): ") 
        Finaltime = input("Ingrese la hora final (00:00-23:59): ")
        printAccidentsByTimeRange(cont,timeInit,Finaltime)
          
    elif int(inputs[0]) == 8:
        print("\nBuscando la zona geográfica más accidentada: ")
        preference = input("Digite 'Mi' si desea realizar la búsqueda en Millas. 'Km' si desea realizarla en Kilómetros: ")
        latitude = input("Ingrese la latitud: ")
        length = input("Ingrese la longitud: ")
        rad = input("Ingrese el radio a buscar: ")
        printZoneWithMoreAccidents(cont,float(latitude),float(length),float(rad),preference)

    else:
        sys.exit(0)
sys.exit(0)
