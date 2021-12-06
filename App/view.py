"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
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
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

import config as cf
import sys
import controller
from DISClib.ADT import list as lt
from DISClib.ADT import graph as gp
from DISClib.ADT import map as mp
from DISClib.ADT import orderedmap as om 
from DISClib.DataStructures import mapentry as me
from colorama import Fore as c
from colorama import Style as cs
assert cf


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def y(data):
  return c.YELLOW + str(data) + cs.RESET_ALL

def initSkylines():
  return controller.initSkylines()


def loadSkylines(skylines):
  print('Serán cargados los archivos por defecto. (Small)')
  custom = input('Ingresa 1 para ingresar archivos diferentes, 2 para cargar los datos grandes, de lo contrario deja vacio:\n> ')

  airports = 'airports-utf8-small.csv'
  routes = 'routes-utf8-small.csv'
  worldcities = 'worldcities-utf8.csv'

  if '1' in custom:
    airports = input('Ingresa el nombre del archivo de aeropuertos:\n> ')
    routes = input('Ingresa el nombre del archivo de rutas:\n> ')
    worldcities = input('Ingresa el nombre del archivo de ciudades:\n> ')
  elif '2' in custom:
    airports = 'airports-utf8-large.csv'
    routes = 'routes-utf8-large.csv'
    worldcities = 'worldcities-utf8.csv'

  controller.loadData(skylines, airports, routes, worldcities)


def returnInfo(skylines):

  print('El número de aeropuertos cargados el grafo DIRIGIDO es:', y(gp.numVertices(skylines['digraph'])))
  print('El número de arcos cargados el grafo DIRIGIDO es:', y(gp.numEdges(skylines['digraph'])))

  print('\nLa información del primer aeropuerto cargado en el grafo DIRIGIDO es:\n')
  fAirportD = lt.firstElement(skylines['airportsList'])
  print('\tNombre:', y(fAirportD['Name']))
  print('\tCiudad:', y(fAirportD['City']))
  print('\tPaís:', y(fAirportD['Country']))
  print('\tIATA:', y(fAirportD['IATA']))
  print('\tLatitud:', y(fAirportD['Latitude']))
  print('\tLongitud:', y(fAirportD['Longitude']))

  print('\nLa información del ultimo aeropuerto cargado en el grafo DIRIGIDO es:\n')
  lAirportD = lt.lastElement(skylines['airportsList'])
  print('\tNombre:', y(lAirportD['Name']))
  print('\tCiudad:', y(lAirportD['City']))
  print('\tPaís:', y(lAirportD['Country']))
  print('\tIATA:', y(lAirportD['IATA']))
  print('\tLatitud:', y(lAirportD['Latitude']))
  print('\tLongitud:', y(lAirportD['Longitude']))

  print('\nEl número de aeropuertos cargados el grafo NO DIRIGIDO es:', y(gp.numVertices(skylines['graph'])))
  print('El número de arcos cargados el grafo NO DIRIGIDO es:', y(gp.numEdges(skylines['graph'])))

  print('\nLa información del primer aeropuerto cargado en el grafo NO DIRIGIDO es:\n')

  fAirportU = lt.firstElement(skylines['airportsList'])
  print('\tNombre:', y(fAirportU['Name']))
  print('\tCiudad:', y(fAirportU['City']))
  print('\tPaís:', y(fAirportU['Country']))
  print('\tIATA:', y(fAirportU['IATA']))
  print('\tLatitud:', y(fAirportU['Latitude']))
  print('\tLongitud:', y(fAirportU['Longitude']))

  print('\nLa información del ultimo aeropuerto cargado en el grafo NO DIRIGIDO es:\n')

  lAirportU = lt.lastElement(skylines['airportsList'])
  print('\tNombre:', y(lAirportU['Name']))
  print('\tCiudad:', y(lAirportU['City']))
  print('\tPaís:', y(lAirportU['Country']))
  print('\tIATA:', y(lAirportU['IATA']))
  print('\tLatitud:', y(lAirportU['Latitude']))
  print('\tLongitud:', y(lAirportU['Longitude']))

  print('\nEl número de ciudades cargadas es:', y(lt.size(skylines['citiesList'])))

  print('\nLa información de la primera ciudad cargada es:\n')

  fCity = lt.firstElement(skylines['citiesList'])
  print('\tCiudad:', y(fCity['city']))
  print('\tCiudad ASCII:', y(fCity['city_ascii']))
  print('\tLatitud:', y(fCity['lat']))
  print('\tLongitud:', y(fCity['lng']))
  print('\tPaís:', y(fCity['country']))
  print('\tISO2:', y(fCity['iso2']))
  print('\tISO3:', y(fCity['iso3']))
  print('\tNombre Administrador:', y(fCity['admin_name']))
  print('\tCapital:', y(fCity['capital']))
  print('\tPoblación:', y(fCity['population']))
  print('\tID:', y(fCity['id']))

  print('\nLa información de la ultima ciudad cargada es:\n')

  lCity = lt.lastElement(skylines['citiesList'])
  print('\tCiudad:', y(lCity['city']))
  print('\tCiudad ASCII:', y(lCity['city_ascii']))
  print('\tLatitud:', y(lCity['lat']))
  print('\tLongitud:', y(lCity['lng']))
  print('\tPaís:', y(lCity['country']))
  print('\tISO2:', y(lCity['iso2']))
  print('\tISO3:', y(lCity['iso3']))
  print('\tNombre Administrador:', y(lCity['admin_name']))
  print('\tCapital:', y(lCity['capital']))
  print('\tPoblación:', y(lCity['population']))
  print('\tID:', y(lCity['id']))

#====================================================================#
#                          REQUERIMIENTO 1                           #
#====================================================================#

def findAirConnections(skylines):
  data = controller.connectionPoints(skylines)
  first5 = lt.newList(datastructure="ARRAY_LIST")
  totalConected = 0

  for i in lt.iterator(om.valueSet(data[1])):
    totalConected += lt.size(i)

  print("Hay "+ str(totalConected) + " aeropuertos conectados en la red actual:")
  while lt.size(first5) < 5:
    max = om.get(data[1], om.maxKey(data[1]))
    max = me.getValue(max)
    for value in lt.iterator(max):
      if lt.size(first5) < 5:
        lt.addLast(first5, value)
    om.deleteMax(data[1])
    max = None

  print("El TOP 5 aeropuertos conectados es:")
  for airport in lt.iterator(first5):
    info = mp.get(skylines["airports"],airport)
    info = me.getValue(info)
    print("\tNombre del Aeropuerto: " + y(info["Name"]))
    print("\tCiudad: " + y(info["City"]))
    print("\tPais: " + y(info["Country"]))
    print("\tIATA: " + y(info["IATA"]))
    print("\tConecciones totales: " + y(gp.outdegree(skylines["digraph"], airport) + gp.indegree(skylines["digraph"],airport)))
    print("\tConexiones entrantes: " + y(gp.indegree(skylines["digraph"],airport)))
    print("\tConexiones salientes: " + y(gp.outdegree(skylines["digraph"], airport)))
    print("--------------------------------------------------------------------------------------\n")


#====================================================================#
#                          REQUERIMIENTO 2                           #
#====================================================================#

def findAirTrafficClusters(skylines):
  pass

#====================================================================#
#                          REQUERIMIENTO 3                           #
#====================================================================#

def shortestRoute(skylines):
  city1 = input('Ingresa el nombre de la ciudad origen (ASCII):\n> ')
  city2 = input('Ingresa el nombre de la ciudad destino (ASCII):\n> ')

  info = controller.shortestRoute(skylines, city1, city2)

  if info is None:
    print(c.RED + 'Alguna de las ciudades no existe o no existe una ruta disponible' + cs.RESET_ALL)
    return None

  print('\nEl aeropuerto de origen a una distancia de', y(round(info[0]['distance'], 3)) + y('km'), 'de la ciudad de origen es:\n')
  print('\tNombre:', y(info[0]['airport']['Name']))
  print('\tCiudad:', y(info[0]['airport']['City']))
  print('\tPaís:', y(info[0]['airport']['Country']))
  print('\tIATA:', y(info[0]['airport']['IATA']))
  print('\tLatitud:', y(info[0]['airport']['Latitude']))
  print('\tLongitud:', y(info[0]['airport']['Longitude']))

  print('\nEl aeropuerto de destino a una distancia de', y(round(info[1]['distance'], 3)) + y('km'), 'de la ciudad de destino es:\n')
  print('\tNombre:', y(info[1]['airport']['Name']))
  print('\tCiudad:', y(info[1]['airport']['City']))
  print('\tPaís:', y(info[1]['airport']['Country']))
  print('\tIATA:', y(info[1]['airport']['IATA']))
  print('\tLatitud:', y(info[1]['airport']['Latitude']))
  print('\tLongitud:', y(info[1]['airport']['Longitude']))

  print('\nLos vuelos necesarios para llegar de', y(city1), 'a', y(city2) + ' son:')

  totalDistance = info[0]['distance'] + info[1]['distance']

  for route in lt.iterator(info[2]):
    totalDistance += route['weight']
    print('\t', 'De', y(route['vertexA']), 'a', y(route['vertexB']) + '.', y(str(route['weight']) + 'km'))

  print('\nLa distancia total es:', y(round(totalDistance, 3)) + y('km.\n'))

#====================================================================#
#                          REQUERIMIENTO 4                           #
#====================================================================#

def travelerMilles(skylines):
  pass

#====================================================================#
#                          REQUERIMIENTO 5                           #
#====================================================================#

def quantifyEffect(skylines):
  airport = input('Ingresa el código IATA del aeropuerto:\n> ')
  info = controller.quantifyEffect(skylines, airport)

  if info is None:
    print(c.RED + "El aeropuerto no existe" + cs.RESET_ALL)

  print('\nEl aeropuerto seleccionado es:\n')
  print('\tNombre:', y(info[0]['Name']))
  print('\tCiudad:', y(info[0]['City']))
  print('\tPaís:', y(info[0]['Country']))
  print('\tIATA:', y(info[0]['IATA']))
  print('\tLatitud:', y(info[0]['Latitude']))
  print('\tLongitud:', y(info[0]['Longitude']))

  print('\nLos primeros y ultimos 3 aeropuertos afectados son:\n')

  if lt.size(info[1]) >= 6:
    p1 = lt.subList(info[1], 1, 3)
    p2 = lt.subList(info[1], lt.size(info[1]) - 2, 3)

    for e in lt.iterator(p2):
      lt.addLast(p1, e)

    lst = p1
  else:
    lst = info[1]

  for airport in lt.iterator(lst):
    print('\n============================')
    print('\tNombre:', y(airport['Name']))
    print('\tCiudad:', y(airport['City']))
    print('\tPaís:', y(airport['Country']))
    print('\tIATA:', y(airport['IATA']))
    print('\tLatitud:', y(airport['Latitude']))
    print('\tLongitud:', y(airport['Longitude']))

  print('\nLa cantidad de arcos en el grafo DIRIGIDO antes era de', y(gp.numEdges(skylines['digraph'])), 'y ahora es', y(info[2]))
  print('\nLa cantidad de arcos en el grafo NO DIRIGIDO antes era de', y(gp.numEdges(skylines['graph'])), 'y ahora es', y(info[3]))


#====================================================================#
#                          REQUERIMIENTO 6                           #
#====================================================================#

def compareWebService(skylines):
  city1 = input('Ingresa el nombre de la ciudad origen (ASCII):\n> ')
  city2 = input('Ingresa el nombre de la ciudad destino (ASCII):\n> ')

  completeInfo = controller.shortestWebRoute(skylines, city1, city2)

  info = completeInfo[0]
  web = completeInfo[1]

  if info is None:
    print(c.RED + 'Alguna de las ciudades no existe o no existe una ruta disponible' + cs.RESET_ALL)
    return None

  print('\nEl aeropuerto de origen a una distancia de', y(round(info[0]['distance'], 3)) + y('km'), 'de la ciudad de origen es:\n')
  print('\tNombre:', y(info[0]['airport']['Name']))
  print('\tCiudad:', y(info[0]['airport']['City']))
  print('\tPaís:', y(info[0]['airport']['Country']))
  print('\tIATA:', y(info[0]['airport']['IATA']))
  print('\tLatitud:', y(info[0]['airport']['Latitude']))
  print('\tLongitud:', y(info[0]['airport']['Longitude']))

  print('\nEl aeropuerto de destino a una distancia de', y(round(info[1]['distance'], 3)) + y('km'), 'de la ciudad de destino es:\n')
  print('\tNombre:', y(info[1]['airport']['Name']))
  print('\tCiudad:', y(info[1]['airport']['City']))
  print('\tPaís:', y(info[1]['airport']['Country']))
  print('\tIATA:', y(info[1]['airport']['IATA']))
  print('\tLatitud:', y(info[1]['airport']['Latitude']))
  print('\tLongitud:', y(info[1]['airport']['Longitude']))

  print('\nLos vuelos necesarios para llegar de', y(city1), 'a', y(city2) + ' son:')

  totalDistance = info[0]['distance'] + info[1]['distance']

  for route in lt.iterator(info[2]):
    totalDistance += route['weight']
    print('\t', 'De', y(route['vertexA']), 'a', y(route['vertexB']) + '.', y(str(route['weight']) + 'km'))

  print('\nEl aeropuerto de origen a una distancia de', y(round(web[0]['distance'], 3)) + y('km'), 'de la ciudad de origen es:\n')
  print('\tNombre:', y(web[0]['airport']['Name']))
  print('\tCiudad:', y(web[0]['airport']['City']))
  print('\tPaís:', y(web[0]['airport']['Country']))
  print('\tIATA:', y(web[0]['airport']['IATA']))
  print('\tLatitud:', y(web[0]['airport']['Latitude']))
  print('\tLongitud:', y(web[0]['airport']['Longitude']))

  print('\nEl aeropuerto de destino a una distancia de', y(round(web[1]['distance'], 3)) + y('km'), 'de la ciudad de destino es:\n')
  print('\tNombre:', y(web[1]['airport']['Name']))
  print('\tCiudad:', y(web[1]['airport']['City']))
  print('\tPaís:', y(web[1]['airport']['Country']))
  print('\tIATA:', y(web[1]['airport']['IATA']))
  print('\tLatitud:', y(web[1]['airport']['Latitude']))
  print('\tLongitud:', y(web[1]['airport']['Longitude']))

  print('\nLos vuelos necesarios para llegar de', y(city1), 'a', y(city2) + ' son:')

  totalWebDistance = web[0]['distance'] + web[1]['distance']

  for route in lt.iterator(web[2]):
    totalWebDistance += route['weight']
    print('\t', 'De', y(route['vertexA']), 'a', y(route['vertexB']) + '.', y(str(route['weight']) + 'km'))

  print('\nLa distancia total calculada sin uso del servicio web es:', y(round(totalDistance, 3)) + y('km.\n'))
  print('\nLa distancia total calculada con uso del servicio web es:', y(round(totalWebDistance, 3)) + y('km.\n'))


#====================================================================#
#                          REQUERIMIENTO 7                           #
#====================================================================#

def viewGraphically(skylines):
  controller.viewGraphically(skylines)


def printMenu():
  print("Bienvenido")
  print("1- Cargar información en el catálogo")
  print("2- Encontrar puntos de interconexión aérea")
  print("3- Encontrar clústeres de tráfico aéreo")
  print("4- Encontrar la ruta más corta entre ciudades")
  print("5- Utilizar las millas de viajero")
  print("6- Cuantificar el efecto de un aeropuerto cerrado")
  print("7- Comparar con servicio WEB externo")
  print("8- Visualizar gráficamente los requerimientos")

skylines = initSkylines()

"""
Menu principal
"""
while True:
  printMenu()
  inputs = input('Seleccione una opción para continuar\n> ')
  if int(inputs[0]) == 1:
    print("Cargando información de los archivos ....")
    loadSkylines(skylines)
    returnInfo(skylines)
  elif int(inputs[0]) == 2:
    findAirConnections(skylines)
  elif int(inputs[0]) == 3:
    findAirTrafficClusters(skylines)
  elif int(inputs[0]) == 4:
    shortestRoute(skylines)
  elif int(inputs[0]) == 5:
    travelerMilles(skylines)
  elif int(inputs[0]) == 6:
    quantifyEffect(skylines)
  elif int(inputs[0]) == 7:
    compareWebService(skylines)
  elif int(inputs[0]) == 8:
    viewGraphically(skylines)
  else:
    sys.exit(0)
sys.exit(0)
