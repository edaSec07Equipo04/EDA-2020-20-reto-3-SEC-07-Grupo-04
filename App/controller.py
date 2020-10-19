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

import config as cf
from App import model
import datetime
import csv

"""
El controlador se encarga de mediar entre la vista y el modelo.
Existen algunas operaciones en las que se necesita invocar
el modelo varias veces o integrar varias de las respuestas
del modelo en una sola respuesta.  Esta responsabilidad
recae sobre el controlador.
"""

# ___________________________________________________
#  Inicializacion del catalogo
# ___________________________________________________


def init():
    """
    Llama la funcion de inicializacion del modelo.
    """
    analyzer = model.newAnalyzer()
    return analyzer

# ___________________________________________________
#  Funciones para la carga de datos y almacenamiento
#  de datos en los modelos
# ___________________________________________________

def loadData(analyzer, accidentsfile):
    """
    Carga los datos de los archivos CSV en el modelo
    """
    accidentsfile = cf.data_dir + accidentsfile
    input_file = csv.DictReader(open(accidentsfile, encoding="utf-8-sig"),
                                delimiter=",")
    for accident in input_file:
        model.addAccident(analyzer, accident)
    return analyzer

# ___________________________________________________
#  Funciones para consultas
# ___________________________________________________

## Requerimiento 1
def getAccidentsByDate(analyzer,date):
    date = datetime.datetime.strptime(date, '%Y-%m-%d')
    return model.getAccidentsByDate(analyzer,date.date())

## Requerimiento 2
def getAccidentsBeforeTo(analyzer,date):
    date= datetime.datetime.strptime(date, '%Y-%m-%d')
    
    return model.getAccidentsBefore(analyzer,date.date())



## Requerimiento 4
def getStateWithMoreAccidents(analyzer,initialDate,finalDate):
    initialDate = datetime.datetime.strptime(initialDate, '%Y-%m-%d')
    finalDate = datetime.datetime.strptime(finalDate, '%Y-%m-%d')
    return model.getStateWithMoreAccidents(analyzer,initialDate.date(),finalDate.date())

def getAccidentsByTimeRange(analyzer,initialTime,finalTime):
    initialTime = datetime.datetime.strptime(initialTime,'%H:%M')
    finalTime = datetime.datetime.strptime(finalTime,'%H:%M')
    return model.getAccidentsByTimeRange(analyzer,initialTime.time(),finalTime.time())

def getZoneWithMoreAccidents(analyzer, refLat, refLong,givenRad,preference):
    return model.getZoneWithMoreAccidents(analyzer,refLat,refLong,givenRad,preference)

############# dateIndex #################
def accidentsSize(analyzer):
    """
    Numero de accidentes leidos
    """
    return model.accidentsSize(analyzer)


def indexHeight(analyzer):
    """
    Altura del indice (arbol)
    """
    return model.indexHeight(analyzer)


def indexSize(analyzer):
    """
    Numero de nodos en el arbol
    """
    return model.indexSize(analyzer)

def minKey(analyzer):
    """
    La menor llave del arbol
    """
    return model.minKey(analyzer)


def maxKey(analyzer):
    """
    La mayor llave del arbol
    """
    return model.maxKey(analyzer)

############ timeIndex ################

def timeIndexHeight(analyzer):
    """
    Altura del indice (arbol)
    """
    return model.timeIndexHeight(analyzer)


def timeIndexSize(analyzer):
    """
    Numero de nodos en el arbol
    """
    return model.timeIndexSize(analyzer)

def minKeyTime(analyzer):
    """
    La menor llave del arbol
    """
    return model.minKeyTime(analyzer)


def maxKeyTime(analyzer):
    """
    La mayor llave del arbol
    """
    return model.maxKeyTime(analyzer)