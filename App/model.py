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
import config
from DISClib.ADT import list as lt
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import mapentry as me
from DISClib.ADT import map as m
import datetime
assert config

"""
En este archivo definimos los TADs que vamos a usar,
es decir contiene los modelos con los datos en memoria


"""

# -----------------------------------------------------
# API del TAD Catalogo de accidentes
# -----------------------------------------------------
def newAnalyzer():
    """ Inicializa el analizador

    Crea una lista vacia para guardar todos los accidentnes
    Se crean indices (Maps) por los siguientes criterios:
    -Fechas

    Retorna el analizador inicializado.
    """
    analyzer = {'accidents': None,
                'dateIndex': None
                }

    analyzer['accidents'] = lt.newList('SINGLE_LINKED', compareIds)
    analyzer['dateIndex'] = om.newMap(omaptype='BST',
                                      comparefunction=compareDates)
    return analyzer

# Funciones para agregar informacion al catalogo

def addAccident(analyzer, accident):
    """
    """
    lt.addLast(analyzer['accidents'], accident)
    updateDateIndex(analyzer['dateIndex'], accident)
    
    return analyzer

def updateDateIndex(map, accident):
    """
    Se toma la fecha del accidentn y se busca si ya existe en el arbol
    dicha fecha.  Si es asi, se adiciona a su lista de accidentnes
    y se actualiza el indice de tipos de accidentnes.

    Si no se encuentra creado un nodo para esa fecha en el arbol
    se crea y se actualiza el indice de tipos de accidentnes
    """
    occurreddate = accident['Start_Time']
    accidentdate = datetime.datetime.strptime(occurreddate, '%Y-%m-%d %H:%M:%S')
    entry = om.get(map, accidentdate.date())
    if entry is None:
        datentry = newDataEntry(accident)
        om.put(map, accidentdate.date(), datentry)
    else:
        datentry = me.getValue(entry)
    addDateIndex(datentry, accident)

    return map

def addDateIndex(dateentry, accident):
    lst = dateentry['lstaccidents']
    lt.addLast(lst,accident)
    stateIndex=dateentry['stateIndex']
    stateEntry = m.get(stateIndex, accident['State'])
    if (stateEntry is None):
        entry = newStateEntry(accident['State'],accident)       
        lt.addLast(entry['lststates'],accident)        
        m.put(stateIndex,accident['State'],entry)
        
    else:
        entry=me.getValue(stateEntry)
        lt.addLast(entry['lststates'],accident)

    severityIndex=dateentry['severityIndex']
    severityEntry=m.get(severityIndex,accident['Severity'])
    
    if (severityEntry is None):
        entry2 = newSeverityEntry(accident['Severity'],accident)
        lt.addLast(entry2['lstseverity'],accident)
        m.put(severityIndex,accident['Severity'],entry2)

    else:
        entry2=me.getValue(severityEntry)
        lt.addLast(entry2['lstseverity'],accident)
    return dateentry 


def newDataEntry(accident):

    entry={'stateIndex':None,'lstaccidents':None}
    entry['stateIndex']=m.newMap(numelements=53,
                                 maptype='PROBING',
                                 comparefunction=compareStates)
    entry['lstaccidents']=lt.newList('SINGLE_LINKED',compareDates)
    return entry

def newStateEntry(stategrp, state):

    statentry = {'state':None, 'lststates':None}
    statentry['state']=stategrp
    statentry['lststates']=lt.newList('SINGLE_LINKED',compareStates)
    return statentry


def newDataEntry2(accident):

    entry={'severityIndex':None,'lstaccidents':None}
    entry['severityIndex']=m.newMap(numelements=5,
                                 maptype='PROBING',
                                 comparefunction=compareSeverity)
    entry['lstaccidents']=lt.newList('SINGLE_LINKED',compareDates)
    return entry

def newSeverityEntry(severitygrp, severity):

    severityentry = {'severity':None, 'lstseverity':None}
    severityentry['severity']=severitygrp
    severityentry['lstseverity']=lt.newList('SINGLE_LINKED',compareSeverity)
    return severityentry

# ==============================
# Funciones de consulta
# ==============================
def accidentsSize(analyzer):
    """
    Número de accidentes en el catago
    """
    return lt.size(analyzer['accidents'])


def indexHeight(analyzer):
    """Numero de fechas leidas
    """
    return om.height(analyzer['dateIndex'])


def indexSize(analyzer):
    """Numero de fechas leidas
    """
    return om.size(analyzer['dateIndex'])

def minKey(analyzer):
    """Numero de accidentes leido
    """
    return om.minKey(analyzer['dateIndex'])


def maxKey(analyzer):
    """Numero de accidentes leido
    """
    return om.maxKey(analyzer['dateIndex'])

# ==============================
# Funciones de Comparacion
# ==============================

def compareIds(id1, id2):
    """
    Compara dos accidentes
    """
    if (id1 == id2):
        return 0
    elif id1 > id2:
        return 1
    else:
        return -1

def compareDates(date1, date2):
    """
    Compara dos ids de accidente, id es un identificador
    y entry una pareja llave-valor
    """
    if (date1 == date2):
        return 0
    elif (date1 > date2):
        return 1
    else:
        return -1

def compareStates(state1,state2):
    state=me.getKey(state2)
    if(state1==state):
        return 0
    elif (state1>state):
        return 1
    else:
        return -1

def compareSeverity(severity1,severity2):
    if(severity1==severity2):
        return 0
    elif (severity1>severity2):
        return 1
    else:
        return -1