"""
 * Copyright 2020, Departamento de sistemas y Computación,
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
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """
import copy
import os
from math import radians, cos, sin, asin, sqrt, inf

import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.ADT import orderedmap as om
from DISClib.ADT import graph as gp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import mergesort as ms
from DISClib.Algorithms.Graphs import dijsktra as dj
import DISClib.Algorithms.Graphs.prim as prim
import DISClib.Algorithms.Graphs.scc as scc
from DISClib.DataStructures import edge as e
import requests
import folium as fl

assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""


# Construccion de modelos

def initSkylines():
  skylines = {}

  skylines['airports'] = mp.newMap(numelements=9100, maptype='CHAINING', loadfactor=2.0)
  skylines['airportsList'] = lt.newList('ARRAY_LIST')
  skylines['airportsCoordinates'] = om.newMap(omaptype='RBT')

  skylines['digraph'] = gp.newGraph(datastructure='ADJ_LIST', directed=True)
  skylines['graph'] = gp.newGraph(datastructure='ADJ_LIST', directed=False)

  skylines['citiesList'] = lt.newList('ARRAY_LIST')
  skylines['cities'] = mp.newMap(numelements=41100, maptype='CHAINING', loadfactor=3.0)

  return skylines

# om.get(ARBOl, me.getValue(mp.get(TABLA, tullave))['degree'])
# Funciones para agregar informacion al catalogo

def addAirport(skylines, airport):
  gp.insertVertex(skylines['digraph'], airport['IATA'])
  gp.insertVertex(skylines['graph'], airport['IATA'])
  lt.addLast(skylines['airportsList'], airport)
  mp.put(skylines['airports'], airport['IATA'], airport)

  coordinatesMap = skylines['airportsCoordinates']

  longitude = round(float(airport['Longitude']), 2)
  latitude = round(float(airport['Latitude']), 2)
  existingLongitude = om.get(coordinatesMap, longitude)

  if existingLongitude is None:
    latitudesMap = om.newMap(omaptype='RBT')
    airports = lt.newList('ARRAY_LIST')
    lt.addLast(airports, airport)
    om.put(latitudesMap, latitude, airports)
    om.put(coordinatesMap, longitude, latitudesMap)
  else:
    longitudesMap = me.getValue(existingLongitude)
    existingLatitude = om.get(longitudesMap, latitude)

    if existingLatitude is None:
      airports = lt.newList('ARRAY_LIST')
      lt.addLast(airports, airport)
      om.put(longitudesMap, latitude, airports)
    else:
      airports = me.getValue(existingLatitude)
      lt.addLast(airports, airport)


def addRoute(skylines, route):
  gp.addEdge(skylines['digraph'], route['Departure'], route['Destination'], weight=float(route['distance_km']))

  if gp.getEdge(skylines['digraph'], route['Destination'], route['Departure']) is not None:
    gp.addEdge(skylines['graph'], route['Departure'], route['Destination'], weight=float(route['distance_km']))


def addCity(skylines, city):
  lt.addLast(skylines['citiesList'], city)
  existingCity = mp.get(skylines['cities'], city['city_ascii'])

  if existingCity is None:
    cities = lt.newList('ARRAY_LIST')
    lt.addLast(cities, city)
    mp.put(skylines['cities'], city['city_ascii'], cities)
  else:
    cities = me.getValue(existingCity)
    lt.addLast(cities, city)


# Funciones para creacion de datos

# Funciones de consulta

# ===================================================
#                  REQUERIMIENTO 1
# ===================================================

def connectionPoints(skylines):
  graf = gp.vertices(skylines["digraph"])
  grafDegrees = mp.newMap(numelements=len(skylines["airportsList"]), maptype="PROBING", loadfactor=0.5)
  degreesRev = om.newMap()
  
  for airport in lt.iterator(graf):
    degree = gp.outdegree(skylines["digraph"], airport) + gp.indegree(skylines["digraph"],airport)
    if degree != 0:
      mp.put(grafDegrees, airport, degree) 

      if om.contains(degreesRev, degree):
        entry = om.get(degreesRev,degree)
        entry = me.getValue(entry)
        lt.addLast(entry, airport)
      else:
        entry = lt.newList("ARRAY_LIST")
        lt.addLast(entry, airport)
        om.put(degreesRev, degree, entry)   

  return (mp.keySet(grafDegrees), degreesRev)


# ===================================================
#                  REQUERIMIENTO 2
# ===================================================

def findClusters(skylines, IATA1, IATA2):
  cc = scc.KosarajuSCC(skylines["digraph"])
  numberOfcc = scc.connectedComponents(cc)
  
  boolean = scc.stronglyConnected(cc, IATA1, IATA2)

  return numberOfcc, boolean


# ===================================================
#                  REQUERIMIENTO 3
# ===================================================

def shortestRouteBetweenCities(skylines, firstCity, secondCity):
  firstCities = mp.get(skylines['cities'], firstCity)

  finalFirstCity = selectCity(firstCities)

  lastCities = mp.get(skylines['cities'], secondCity)

  finalLastCity = selectCity(lastCities)

  if finalFirstCity is None or finalLastCity is None:
    return None

  firstAirport = findAirportNearToCity(skylines, finalFirstCity, 1, True)
  lastAirport = findAirportNearToCity(skylines, finalLastCity, 1, False)

  if firstAirport is None or lastAirport is None:
    return None

  search = dj.Dijkstra(skylines['digraph'], firstAirport['airport']['IATA'])

  pathTo = dj.pathTo(search, lastAirport['airport']['IATA'])

  return [firstAirport, lastAirport, pathTo]


# Algoritmo de busqueda por coordenadas

def findAirportNearToCity(skylines, city, numberOfSearch, isDeparture):
  """
  Esta función retorna el aeropuerto más cercano a una ciudad dada
  y tambien retorna la distancia terrestre de ambos puntos geográficos.
  """

  info = {
    'airport': None,
    'distance': 0,
  }

  degreesToLat = numberOfSearch * 0.09022  # Grados equivalentes a LATITUD equivalentes a 10km https://forest.moscowfsl.wsu.edu/fswepp/rc/kmlatcon.html
  degreesToLng = numberOfSearch * 0.08983  # Grados equivalentes a LONGITUD equivalentes a 10km https://forest.moscowfsl.wsu.edu/fswepp/rc/kmlatcon.html

  while info['airport'] is None:
    minLat = float(city['lat']) - degreesToLat
    minLng = float(city['lng']) - degreesToLng

    maxLat = float(city['lat']) + degreesToLat
    maxLng = float(city['lng']) + degreesToLng

    betweenLongitudes = om.values(skylines['airportsCoordinates'], minLng, maxLng)

    if lt.size(betweenLongitudes) == 0:
      info = findAirportNearToCity(skylines, city, numberOfSearch + 1, isDeparture)

    else:
      latitudes = lt.newList('ARRAY_LIST')

      for latitudeMap in lt.iterator(betweenLongitudes):
        for latitude in lt.iterator(om.values(latitudeMap, minLat, maxLat)):
          for airport in lt.iterator(latitude):
            lt.addLast(latitudes, airport)

      if lt.size(latitudes) == 0:
        info = findAirportNearToCity(skylines, city, numberOfSearch + 1, isDeparture)
      elif lt.size(latitudes) > 1 and findClosest(latitudes, float(city['lat']), float(city['lng']), skylines['digraph'], isDeparture) is not None:
        info['airport'] = findClosest(latitudes, float(city['lat']), float(city['lng']), skylines['digraph'], isDeparture)
        info['distance'] = haversine(float(info['airport']['Longitude']), float(info['airport']['Latitude']),
                                     float(city['lng']), float(city['lat']))
      elif findClosest(latitudes, float(city['lat']), float(city['lng']), skylines['digraph'], isDeparture) is None:
        info = findAirportNearToCity(skylines, city, numberOfSearch + 1, isDeparture)
      else:
        info['airport'] = lt.firstElement(latitudes)
        info['distance'] = haversine(float(info['airport']['Longitude']), float(info['airport']['Latitude']),
                                     float(city['lng']), float(city['lat']))

  return info


def findClosest(lst, lat, lng, graph, isDeparture):
  closest = None
  minDistance = inf

  for airport in lt.iterator(lst):
    distance = haversine(float(airport['Longitude']), float(airport['Latitude']), lng, lat)

    if isDeparture:
      degree = gp.outdegree(graph, airport['IATA'])
    else:
      degree = gp.indegree(graph, airport['IATA'])

    if distance < minDistance and degree > 0:
      closest = airport
      minDistance = distance

  return closest


# ===================================================
#                  REQUERIMIENTO 4
# ===================================================

def useTravellerMilles(skylines, milles):
  mllToKm = milles*1.6
  pri = prim.PrimMST(skylines["graph"]) 
  PRI = prim.edgesMST(skylines["graph"], pri)

  return PRI, mllToKm

# ===================================================
#                  REQUERIMIENTO 5
# ===================================================

def quantifyEffect(skylines, airportIATA):
  """
  Analize the effect of "delete" or close an airport
  Args:
    skylines: The cattalog
    airportIATA: The IATA code of the airport to search

  Returns: The information of the airport, the affected airports, number of routes in digraph after of delete the airport,
   number of routes in graph after of delete the airport, deleted routes on digrpah and deleted routes in graph.

  """
  airportEntry = mp.get(skylines['airports'], airportIATA)

  if airportEntry is None:
    return None

  airport = me.getValue(airportEntry)

  adjacentVertexDigraph = gp.adjacents(skylines['digraph'], airport['IATA'])

  noVertexInDigraph = removeVertex(skylines['digraph'], airport['IATA'])
  noVertexInGraph = removeVertex(skylines['graph'], airport['IATA'])

  adjacentAirports = lt.newList('ARRAY_LIST', cmpfunction=compareByIATA)

  for v in lt.iterator(adjacentVertexDigraph):
    if lt.isPresent(adjacentAirports, me.getValue(mp.get(skylines['airports'], v))) == 0:
      lt.addLast(adjacentAirports, me.getValue(mp.get(skylines['airports'], v)))

  newDigraphEdges = gp.numEdges(skylines['digraph']) - lt.size(noVertexInDigraph)
  newGraphEdges = gp.numEdges(skylines['graph']) - lt.size(noVertexInGraph)

  return [airport, adjacentAirports, newDigraphEdges, newGraphEdges, noVertexInDigraph, noVertexInGraph]


# ===================================================
#                  REQUERIMIENTO 6
# ===================================================

def compareWebService(skylines, cityA, cityB):
  """
  Connects to AMADEUS API to identify the nearest relevant airports
  Args:
    skylines:
    cityA:
    cityB:

  Returns:

  """
  url = 'https://test.api.amadeus.com/v1'

  ownFunction = shortestRouteBetweenCities(skylines, cityA, cityB)

  city1Entry = mp.get(skylines['cities'], cityA)
  city2Entry = mp.get(skylines['cities'], cityB)

  if city1Entry is None or city2Entry is None:
    return [None, None]

  city1 = selectCity(city1Entry)
  city2 = selectCity(city2Entry)

  if city1 is None or city2 is None:
    return [None, None]

  accessTokenReq = requests.post('https://test.api.amadeus.com/v1/security/oauth2/token',
                                 headers={'Content-Type': 'application/x-www-form-urlencoded'},
                                 data={
                                   'grant_type': 'client_credentials',
                                   'client_id': os.environ['CLIENT_ID'],
                                   'client_secret': os.environ['CLIENT_SECRET'],
                                 })
  accessToken = accessTokenReq.json()['access_token']

  departureAirportWeb = requests.get('https://test.api.amadeus.com/v1/reference-data/locations/airports',
                              headers={'Authorization': 'Bearer ' + accessToken},
                              params={'latitude': city1['lat'], 'longitude': city1['lng'], 'page[limit]': 1}).json()

  destinationAirportWeb = requests.get('https://test.api.amadeus.com/v1/reference-data/locations/airports',
                              headers={'Authorization': 'Bearer ' + accessToken},
                              params={'latitude': city2['lat'], 'longitude': city2['lng'], 'page[limit]': 1}).json()


  if len(departureAirportWeb['data']) == 0 or len(destinationAirportWeb['data']) == 0:
    return [ownFunction, None]

  webDepartureAirport = me.getValue(mp.get(skylines['airports'], departureAirportWeb['data'][0]['iataCode']))
  webDestinationAirport = me.getValue(mp.get(skylines['airports'], destinationAirportWeb['data'][0]['iataCode']))

  distanceFromCityToDepartureAirport = haversine(float(webDepartureAirport['Longitude']), float(webDepartureAirport['Latitude']), float(city1['lng']), float(city1['lat']))
  distanceFromCityToDestinationAirport = haversine(float(webDestinationAirport['Longitude']), float(webDestinationAirport['Latitude']), float(city2['lng']), float(city2['lat']))

  search = dj.Dijkstra(skylines['digraph'], webDepartureAirport['IATA'])

  pathTo = dj.pathTo(search, webDestinationAirport['IATA'])

  return [ownFunction, [
    {'airport': webDepartureAirport, 'distance': distanceFromCityToDepartureAirport},
    {'airport': webDestinationAirport, 'distance': distanceFromCityToDestinationAirport},
    pathTo
  ]]

# ===================================================
#                  REQUERIMIENTO 7
# ===================================================

def viewGraphically(skylines):
  """
  Allows to select the function that will be illustred in a Map.
  Args:
    skylines: The catalog

  Returns: None

  """
  view = True

  while view:
    print("1- puntos de interconección aérea")
    print("2- Ver clústers de tráfico aéreo")
    print("3- Ver la ruta más corta entre ciudades")
    print("4- Ver el viaje del viajero al utilizar sus millas")
    print("5- Ver el efecto de un aeropuerto cerrado")
    print("6- Salir")
    inputs = input('Seleccione una opción para continuar\n> ')
    if int(inputs[0]) == 1:
      viewConnectionPoints(skylines, 'connection_points')
    elif int(inputs[0]) == 2:
      pass
    elif int(inputs[0]) == 3:
      viewShortestRouteGraphically(skylines, 'shortest_route')
    elif int(inputs[0]) == 4:
      pass
    elif int(inputs[0]) == 5:
      viewClosedAirportEffect(skylines, 'closed_effect')
    elif int(inputs[0]) == 6:
      view = False


def viewConnectionPoints(skylines, filename):
  data = connectionPoints(skylines)
  airports = lt.newList(datastructure="ARRAY_LIST")

  for i in lt.iterator(om.valueSet(data[1])):
    for airport in lt.iterator(i):
      lt.addLast(airports, airport)

  connectionsMap = fl.Map(zoom_start=5)

  for a in lt.iterator(airports):
    airport = me.getValue(mp.get(skylines['airports'], a))
    fl.Marker(location=(airport['Latitude'], airport['Longitude']), tooltip=airport['IATA']).add_to(connectionsMap)

  connectionsMap.save(cf.maps_dir + filename + '.html')


def viewShortestRouteGraphically(skylines, filename):
  """
  Create an HTML file showing the shortest path on a map.
  Args:
    skylines: The catalog
    filename: The name that will be used for save the file.

  Returns: None

  """

  shortest = shortestRouteBetweenCities(skylines, input('Ciudad de inicio (ascii): '), input('Ciudad final (ascii): '))

  if shortest is None:
    print('Alguna de las ciudades no existe o no existe una ruta')
    return None

  foliumMap = fl.Map(zoom_start=5)

  planes = shortest[2]

  for edge in lt.iterator(planes):
    points = []
    names = []
    airportOne = me.getValue(mp.get(skylines['airports'], edge['vertexA']))
    pointA = (float(airportOne['Latitude']), float(airportOne['Longitude']))
    points.append(pointA)
    names.append(airportOne['IATA'])

    airportTwo = me.getValue(mp.get(skylines['airports'], edge['vertexB']))
    pointB = (float(airportTwo['Latitude']), float(airportTwo['Longitude']))
    points.append(pointB)
    names.append(airportTwo['IATA'])

    for p in range(len(points)):
      fl.Marker(points[p], tooltip=names[p]).add_to(foliumMap)

    fl.PolyLine(points, tooltip=airportOne['IATA'] + ' ➞ ' + airportTwo['IATA'] + ' ' + str(edge['weight']) + 'km').add_to(foliumMap)

  foliumMap.save(cf.maps_dir + filename + '.html')


def viewClosedAirportEffect(skylines, filename):
  """
  Create an HTML file showing the effect of close an airport on a map.
  Args:
    skylines: The catalog
    filename: The name that will be used for save the file.

  Returns: None

  """

  effect = quantifyEffect(skylines, input('Ingresa el código IATA del aeropuerto:\n> '))

  if effect is None:
    print('El Aeropuerto no existe')
    return None

  digraphMap = fl.Map(zoom_start=10)
  graphMap = fl.Map(zoom_start=10)

  for ed in lt.iterator(effect[4]):
    points = []
    names = []
    airportOne = me.getValue(mp.get(skylines['airports'], ed['vertexA']))
    pointA = (float(airportOne['Latitude']), float(airportOne['Longitude']))
    points.append(pointA)
    names.append(airportOne['IATA'])

    airportTwo = me.getValue(mp.get(skylines['airports'], ed['vertexB']))
    pointB = (float(airportTwo['Latitude']), float(airportTwo['Longitude']))
    points.append(pointB)
    names.append(airportTwo['IATA'])

    for p in range(len(points)):
      fl.Marker(points[p], tooltip=names[p]).add_to(digraphMap)

    fl.PolyLine(points, tooltip=airportOne['IATA'] + ' ➞ ' + airportTwo['IATA'] + ' ' + str(ed['weight']) + 'km').add_to(digraphMap)

  for ed in lt.iterator(effect[5]):
    points = []
    names = []
    airportOne = me.getValue(mp.get(skylines['airports'], ed['vertexA']))
    pointA = (float(airportOne['Latitude']), float(airportOne['Longitude']))
    points.append(pointA)
    names.append(airportOne['IATA'])

    airportTwo = me.getValue(mp.get(skylines['airports'], ed['vertexB']))
    pointB = (float(airportTwo['Latitude']), float(airportTwo['Longitude']))
    points.append(pointB)
    names.append(airportTwo['IATA'])

    for p in range(len(points)):
      fl.Marker(points[p], tooltip=names[p]).add_to(graphMap)

    fl.PolyLine(points, tooltip=airportOne['IATA'] + ' ⇄ ' + airportTwo['IATA'] + ' ' + str(ed['weight']) + 'km').add_to(graphMap)

  graphMap.save(cf.maps_dir + filename + '_graph.html')
  digraphMap.save(cf.maps_dir + filename + '_digraph.html')


# ===================================================
#                FUNCIONES DE AYUDA
# ===================================================

def selectCity(cities):
  """
  Displays a menu that allows to choose a city if there are more than one
  with the same name.
  Args:
    cities: City entry

  Returns: The selected city

  """
  if cities is None:
    return None
  elif lt.size(me.getValue(cities)) > 1:
    print('Ingresa un número según la ciudad de origen que deseas: ')
    for cityPos in range(1, lt.size(me.getValue(cities)) + 1):
      fiCity = lt.getElement(me.getValue(cities), cityPos)
      print('\n===================================================', cityPos,
            '===================================================\n')
      print('\tCiudad:', fiCity['city'])
      print('\tCiudad ASCII:', fiCity['city_ascii'])
      print('\tLatitud:', fiCity['lat'])
      print('\tLongitud:', fiCity['lng'])
      print('\tPaís:', fiCity['country'])
      print('\tISO2:', fiCity['iso2'])
      print('\tISO3:', fiCity['iso3'])
      print('\tNombre Administrador:', fiCity['admin_name'])
      print('\tCapital:', fiCity['capital'])
      print('\tPoblación:', fiCity['population'])
      print('\tID:', fiCity['id'])

    citySelected = input('\n> ')
    finalFirstCity = lt.getElement(me.getValue(cities), int(citySelected))
  else:
    finalFirstCity = lt.getElement(me.getValue(cities), 1)

  return finalFirstCity


def haversine(lon1, lat1, lon2, lat2):
  """
  Calculate the great circle distance in kilometers between two points
  on the earth (specified in decimal degrees)

  IMPLEMENTATION OBTAINED FROM:
  https://stackoverflow.com/questions/4913349/haversine-formula-in-python-bearing-and-distance-between-two-gps-points

  Args:
    lon1: Longitude of the point A
    lat1: Latitude of the point A
    lon2: Longitude of the point B
    lat2: Latitude of the point B

  Returns: The distance in Kilometers

  """
  # convert decimal degrees to radians
  lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

  # haversine formula
  dlon = lon2 - lon1
  dlat = lat2 - lat1
  a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
  c = 2 * asin(sqrt(a))
  r = 6371  # Radius of earth in kilometers. Use 3956 for miles. Determines return value units.
  return c * r


def removeVertex(graph, vertex):
  """
  Get the number of edges that will disappear if vertex is deleted and that edges into a list.
  Necessary function because the removeVertex function is not implemented in the API

  Args:
    graph: The graph that will be analized
    vertex: The vertex that will be searched

  Returns: A list with the edges.
  """
  deletedEdges = lt.newList('ARRAY_LIST', e.compareedges)
  vertices = gp.vertices(graph)

  for v in lt.iterator(vertices):
    edgesFromV = gp.adjacentEdges(graph, v)
    for ed in lt.iterator(edgesFromV):
      if ed['vertexA'] == vertex or ed['vertexB'] == vertex:
        lt.addLast(deletedEdges, ed)

  return deletedEdges


def compareByIATA(e1, e2):
  """
  Compare the IATA of two airports
  Args:
    e1: First airport to compare
    e2: Second airport to compare

  Returns: 0 if the airports are the same, and 1 if not

  """
  if e1['IATA'] > e2['IATA'] or e2['IATA'] > e1['IATA']:
    return 1
  return 0