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
    analyzer['dateIndex'] = om.newMap(omaptype='RBT',
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
    Se toma la fecha del accidente y se busca si ya existe en el arbol
    dicha fecha.  Si es asi, se adiciona a su lista de accidentnes
    y se actualiza el indice de tipos de accidentnes.

    Si no se encuentra creado un nodo para esa fecha en el arbol
    se crea y se actualiza el indice de tipos de accidentnes
    """
    occurreddate = accident['Start_Time']
    accidentdate = datetime.datetime.strptime(occurreddate, '%Y-%m-%d %H:%M:%S')
    entry = om.get(map, accidentdate.date())
    if entry is None:
        datentry = newDataEntry2(accident)
        om.put(map, accidentdate.date(), datentry)
    else:
        datentry = me.getValue(entry)
    addDateIndex(datentry, accident)

    return map

def addDateIndex(dateentry,accident):
    lst = dateentry['lstaccidents']
    lst2 = dateentry['states']
    lt.addLast(lst,accident)
    lt.addLast(lst2,accident['State'])
    severityIndex=dateentry['severityIndex']
    severityEntry = m.get(severityIndex, accident['Severity'])
    if (severityEntry is None):
        entry = newSeverityEntry(accident['Severity'],accident)       
        lt.addLast(entry['lstseverity'],accident)   
        lt.addLast(entry['state'],accident['State'])     
        m.put(severityIndex,accident['Severity'],entry)
        
    else:
        entry=me.getValue(severityEntry)
        lt.addLast(entry['lstseverity'],accident)
        lt.addLast(entry['state'],accident['State'])

    return dateentry



def newDataEntry2(accident):

    entry={'severityIndex':None,'lstaccidents':None, 'states':None}
    entry['severityIndex']=m.newMap(numelements=5,
                                 maptype='PROBING',
                                 comparefunction=compareSeverity)
    entry['lstaccidents']=lt.newList('SINGLE_LINKED',compareDates)
    entry['states'] = lt.newList('ARRAY_LIST',compareStates)

    return entry

def newSeverityEntry(severitygrp, severity):

    severityentry = {'severity':None, 'lstseverity':None, 'state':None }
    severityentry['severity']=severitygrp
    severityentry['lstseverity']=lt.newList('SINGLE_LINKED',compareSeverity)
    severityentry['state']=lt.newList('ARRAY_LIST',compareStates)
    return severityentry

# ==============================
# Funciones de consulta
# ==============================

# ============================
# Requerimiento 1 / GRUPAL
# ============================

def getAccidentsByDate(analyzer,date):
    '''
    Reporta la cantidad de accidentes por severidad para la fecha ingresada
    '''
    accidentDate=om.get(analyzer['dateIndex'],date)
    if accidentDate:
        if accidentDate['key'] is not None:
            lst = lt.newList('ARRAY_LIST')
            severityMap = me.getValue(accidentDate)['severityIndex']
            severityNum1 = m.get(severityMap,'1')
            severityNum2=m.get(severityMap,'2')
            severityNum3=m.get(severityMap,'3')
            severityNum4=m.get(severityMap,'4')
            if (severityNum1 is not None):
                lt.addLast(lst,(m.size(me.getValue(severityNum1)['lstseverity'])))
            else:
                lt.addLast(lst,0)
            if (severityNum2 is not None):
                lt.addLast(lst,(m.size(me.getValue(severityNum2)['lstseverity'])))
            else:
                lt.addLast(lst,0)
            if (severityNum3 is not None):
                lt.addLast(lst,(m.size(me.getValue(severityNum3)['lstseverity'])))
            else:
                lt.addLast(lst,0)
            if (severityNum4 is not None):
                lt.addLast(lst,(m.size(me.getValue(severityNum4)['lstseverity'])))
            else:
                lt.addLast(lst,0)
            return (lt.getElement(lst,1),lt.getElement(lst,2),lt.getElement(lst,3),lt.getElement(lst,4))
    else:
        return 0

# ===============================
# Requerimento 2 / Juan Esteban R
# ===============================

def getAccidentsBefore(analyzer, date):
    #contador = 0
    #
    date_min = minKey( analyzer)
    date_max = date
    dates = om.values(analyzer['dateIndex'],date_min,date_max)

    totalT = 0
    maximo = 0
    fecha_max = ""

    for i in range(1,lt.size(dates)+1):
        fecha = lt.getElement(dates,i)

        severity = getAccidentsByDate(analyzer,fecha)
        total    = severity[0] + severity[1] + severity[2] + severity[3]
        totalT   += total
        
        if total > maximo:
            maximo = total
            fecha_max = fecha


    return(totalT,maximo,fecha_max)



############## REQUERIMIENTO 4 - Germán Rojas ##############################

def getStateWithMoreAccidents(analyzer,initialDate, finalDate):
    '''
    - Reporta en estado con más accidentes en el rango ingresado.
    - Reporta la fecha con más accidentes en el rango ingresado.
    '''
    maxAccidents = 0
    resultDate = ''
    lst = om.values(analyzer['dateIndex'],initialDate,finalDate) #Listado de fechas dentro del rango
    totalData = {} #Aquí se guardan los estados con su número de accidentes
    winnerState=''
    stateQuantity = 0
    for i in range(1,lt.size(lst)+1): #Se recorre cada año para obtener la información necesaria 
        date = lt.getElement(lst,i)
        severities = getAccidentsByDate(analyzer,date)
        total = severities[0]+severities[1]+severities[2]+severities[3]
        if total > maxAccidents:
            maxAccidents = total
            resultDate = str(date)
        data={}
        accidentDate=om.get(analyzer['dateIndex'],date) #Se obtiene el número de accidentes en cada año para cada estado
        if accidentDate:
            if accidentDate['key'] is not None:
                severityMap = me.getValue(accidentDate)['severityIndex']
                severityNum1 = m.get(severityMap,'1')
                severityNum2=m.get(severityMap,'2')
                severityNum3=m.get(severityMap,'3')
                severityNum4=m.get(severityMap,'4')
                if (severityNum1 is not None):
                    a =(me.getValue(severityNum1)['state'])
                    for j in range(1,lt.size(a)):
                        info = lt.getElement(a,j)
                        if info in data.keys():
                            data[info]+=1
                        else:
                            data[info]=1
                else:
                    pass
                if (severityNum2 is not None):
                    b=(me.getValue(severityNum2)['state'])
                    for j in range(1,lt.size(b)):
                        info = lt.getElement(b,j)
                        if info in data.keys():
                            data[info]+=1
                        else:
                            data[info]=1
                else:
                    pass
                if (severityNum3 is not None):
                    c=(me.getValue(severityNum3)['state'])
                    for j in range(1,lt.size(c)):
                        info = lt.getElement(c,j)
                        if info in data.keys():
                            data[info]+=1
                        else:
                            data[info]=1
                else:
                    pass
                if (severityNum4 is not None):
                    d=(me.getValue(severityNum4)['state'])
                    for j in range(1,lt.size(d)):
                        info = lt.getElement(d,j)
                        if info in data.keys():
                            data[info] +=1
                        else:
                            data[info]=1
                else:
                    pass

        for key,value in data.items(): #Se suman los valores de cada año para cada estado
            if key in totalData.keys():
                totalData[key]+=value
            else:
                totalData[key]=value
    
    for key,value in totalData.items(): #Se realizan comparaciones para obtener el estado con más accidentes
        if value > stateQuantity:
            stateQuantity = value
            winnerState=key
    return resultDate,winnerState
#################################################################


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
    severity=me.getKey(severity2)
    if(severity1==severity):
        return 0
    elif (severity1>severity):
        return 1
    else:
        return -1