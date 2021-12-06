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

import folium

import DISClib.Algorithms.Graphs.dijsktra as dj
import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.ADT import orderedmap as om
from DISClib.ADT import graph as gp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import mergesort as ms
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
  grafDegrees = mp.newMap(numelements=len(skylines["airportsList"]), maptype="PROBING")
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

def findClusters(skylines):
  pass

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


# ===================================================
#                  REQUERIMIENTO 5
# ===================================================

def quantifyEffect(skylines, airportIATA):
  """
  airportEntry = mp.get(skylines['airports'], airportIATA)

  if airportEntry is None:
    return None

  airport = me.getValue(airportEntry)

  skylinesCopy = {
    'digraph': copy.deepcopy(skylines['digraph']),
    'graph': copy.deepcopy(skylines['graph']),
  }

  adjacentVertexDigraph = gp.adjacents(skylines['digraph'], airport['IATA'])

  gp.removeVertex(skylinesCopy['digraph'], airport['IATA'])
  gp.removeVertex(skylinesCopy['graph'], airport['IATA'])

  adjacentAirports = lt.newList('ARRAY_LIST', cmpfunction=compareByIATA)

  for v in lt.iterator(adjacentVertexDigraph):
    if lt.isPresent(adjacentAirports, me.getValue(mp.get(skylines['airports'], v))) == 0:
      lt.addLast(adjacentAirports, me.getValue(mp.get(skylines['airports'], v)))

  newDigraphEdges = gp.numEdges(skylinesCopy['digraph'])
  newGraphEdges = gp.numEdges(skylinesCopy['graph'])

  skylinesCopy = None

  return [airport, adjacentAirports, newDigraphEdges, newGraphEdges]
  """


# ===================================================
#                  REQUERIMIENTO 6
# ===================================================

def compareWebService(skylines, cityA, cityB):
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
    print(departureAirportWeb['data'], destinationAirportWeb['data'])
    return [None, None]

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
  digraphMap = fl.Map(zoom_start=10)

  shortest = shortestRouteBetweenCities(skylines, input('Ciudad de inicio (ascii): '), input('Ciudad final (ascii): '))

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
      fl.Marker(points[p], tooltip=names[p]).add_to(digraphMap)

    folium.PolyLine(points, tooltip=airportOne['IATA'] + ' ➞ ' + airportTwo['IATA'] + ' ' + str(edge['weight']) + 'km').add_to(digraphMap)

  digraphMap.save(cf.maps_dir + 'digraph_map.html')



# ===================================================
#                FUNCIONES DE AYUDA
# ===================================================


def selectCity(firstCities):
  if firstCities is None:
    return None
  elif lt.size(me.getValue(firstCities)) > 1:
    print('Ingresa un número según la ciudad de origen que deseas: ')
    for cityPos in range(1, lt.size(me.getValue(firstCities)) + 1):
      fiCity = lt.getElement(me.getValue(firstCities), cityPos)
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
    finalFirstCity = lt.getElement(me.getValue(firstCities), int(citySelected))
  else:
    finalFirstCity = lt.getElement(me.getValue(firstCities), 1)

  return finalFirstCity

def haversine(lon1, lat1, lon2, lat2):
  """
    Calculate the great circle distance in kilometers between two points 
    on the earth (specified in decimal degrees)

    IMPLEMENTACION OBTENIDA DE:
    https://stackoverflow.com/questions/4913349/haversine-formula-in-python-bearing-and-distance-between-two-gps-points
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


def compareByIATA(e1, e2):
  if e1['IATA'] > e2['IATA']:
    return 1
  elif e1['IATA'] < e2['IATA']:
    return -1
  return 0

def compareAmount(a, b):
  return a["degree"] < b["degree"]