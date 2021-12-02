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


from math import radians, cos, sin, asin, sqrt, inf
import DISClib.Algorithms.Graphs.dijsktra as dj
import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.ADT import orderedmap as om
from DISClib.ADT import graph as gp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import mergesort as ms
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos

def initSkylines():
  skylines = {
    'citiesLst': lt.newList('ARRAY_LIST'),
    'citiesMap': mp.newMap(numelements=41000, maptype='CHAINING', loadfactor=4.0),
    'airports': mp.newMap(numelements=41000, maptype='CHAINING', loadfactor=4.0),
    'airportsByCoordinates': om.newMap(omaptype='RBT'),
    'digraphAirportsLst': lt.newList('ARRAY_LIST'),
    'digraph': gp.newGraph(datastructure='ADJ_LIST', directed=True),
    'undirectedAirportsLst': lt.newList('ARRAY_LIST'),
    'undirected': gp.newGraph(datastructure='ADJ_LIST', directed=False),
  }

  return skylines

# Funciones para agregar informacion al catalogo

def addAirport(skylines, airport):
  gp.insertVertex(skylines['digraph'], airport['IATA'])
  lt.addLast(skylines['digraphAirportsLst'], airport)
  mp.put(skylines['airports'], airport['IATA'], airport)

  existingLng = om.get(skylines['airportsByCoordinates'], round(float(airport['Longitude']), 2))

  if existingLng is not None:
    existingLat = om.get(me.getValue(existingLng), round(float(airport['Latitude']), 2))
    
    if existingLat is not None:
      airports = me.getValue(existingLat)
      lt.addLast(airports, airport)
    else:
      airports = lt.newList('ARRAY_LIST')
      lt.addLast(airports, airport)
      om.put(me.getValue(existingLng), round(float(airport['Latitude']), 2), airports)
  else:
    latitudes = om.newMap(omaptype='RBT')
    airports = lt.newList('ARRAY_LIST')
    lt.addLast(airports, airport)
    om.put(latitudes, round(float(airport['Latitude']), 2), airports)
    om.put(skylines['airportsByCoordinates'], round(float(airport['Longitude']), 2), latitudes)


def addRoute(skylines, route):
  gp.addEdge(skylines['digraph'], route['Departure'], route['Destination'], weight=float(route['distance_km']))

  if gp.getEdge(skylines['digraph'], route['Destination'], route['Departure']):
    if not gp.containsVertex(skylines['undirected'], route['Departure']):
      gp.insertVertex(skylines['undirected'], route['Departure'])
      lt.addLast(skylines['undirectedAirportsLst'], me.getValue(mp.get(skylines['airports'], route['Departure'])))

    if not gp.containsVertex(skylines['undirected'], route['Destination']):
      gp.insertVertex(skylines['undirected'], route['Destination'])
      lt.addLast(skylines['undirectedAirportsLst'], me.getValue(mp.get(skylines['airports'], route['Destination'])))

    gp.addEdge(skylines['undirected'], route['Departure'], route['Destination'], weight=float(route['distance_km']))


def addCity(skylines, city):
  lt.addLast(skylines['citiesLst'], city)

  existingCity = mp.get(skylines['citiesMap'], city['city_ascii'])

  if existingCity is None:
    cities = lt.newList('ARRAY_LIST')
    lt.addLast(cities, city)
    mp.put(skylines['citiesMap'], city['city_ascii'], cities)
  else:
    cities = me.getValue(existingCity)
    lt.addLast(cities, city)

# Funciones para creacion de datos

# Funciones de consulta

# ===================================================
#                  REQUERIMIENTO 1
# ===================================================

def interconectionPoints(skylines):
  pass

# ===================================================
#                  REQUERIMIENTO 2
# ===================================================

def findClusters(skylines):
  pass

# ===================================================
#                  REQUERIMIENTO 3
# ===================================================

def shortestRouteBetweenCities(skylines, firstCity, secondCity):
  firstCities = mp.get(skylines['citiesMap'], firstCity)

  if firstCities is None:
    return None
  elif lt.size(me.getValue(firstCities)) > 1:
    print('Ingresa un número según la ciudad de origen que deseas: ')
    for cityPos in range(1, lt.size(me.getValue(firstCities)) + 1):
      fiCity = lt.getElement(me.getValue(firstCities), cityPos)
      print('\n===================================================', cityPos, '===================================================\n')
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


  lastCities = mp.get(skylines['citiesMap'], secondCity)

  if lastCities is None:
    return None
  elif lt.size(me.getValue(lastCities)) > 1:
    print('Ingresa un número según la ciudad de destino que deseas: ')
    for latsCityPos in range(1, lt.size(me.getValue(lastCities)) + 1):
      fCity = lt.getElement(me.getValue(lastCities), latsCityPos)
      print('\n===================================================', latsCityPos, '===================================================\n')
      print('\tCiudad:', fCity['city'])
      print('\tCiudad ASCII:', fCity['city_ascii'])
      print('\tLatitud:', fCity['lat'])
      print('\tLongitud:', fCity['lng'])
      print('\tPaís:', fCity['country'])
      print('\tISO2:', fCity['iso2'])
      print('\tISO3:', fCity['iso3'])
      print('\tNombre Administrador:', fCity['admin_name'])
      print('\tCapital:', fCity['capital'])
      print('\tPoblación:', fCity['population'])
      print('\tID:', fCity['id'])
    
    citySelected = input('\n> ')
    finalLastCity = lt.getElement(me.getValue(lastCities), int(citySelected))
  else:
    finalLastCity = lt.getElement(me.getValue(lastCities), 1)

  firstAirport = findAirportNearToCity(skylines, finalFirstCity, 1)
  lastAirport = findAirportNearToCity(skylines, finalLastCity, 1)

  if firstAirport is None or lastAirport is None:
    return None

  search = dj.Dijkstra(skylines['digraph'], firstAirport['airport']['IATA'])

  pathTo = dj.pathTo(search, lastAirport['airport']['IATA'])

  return [firstAirport, lastAirport, pathTo]
    

# Algoritmo de busqueda por coordenadas

def findAirportNearToCity(skylines, city, numberOfSearch):
  """
  Esta función retorna el aeropuerto más cercano a una ciudad dada
  y tambien retorna la distancia terrestre de ambos puntos geográficos.
  """

  info = {
    'airport': None,
    'distance': 0,
  }

  degreesToLat = numberOfSearch * 0.09022 #Grados equivalentes a LATITUD equivalentes a 10km https://forest.moscowfsl.wsu.edu/fswepp/rc/kmlatcon.html
  degreesToLng = numberOfSearch * 0.08983 #Grados equivalentes a LONGITUD equivalentes a 10km https://forest.moscowfsl.wsu.edu/fswepp/rc/kmlatcon.html

  while info['airport'] is None:
    minLat = float(city['lat']) - degreesToLat
    minLng = float(city['lng']) - degreesToLng

    maxLat = float(city['lat']) + degreesToLat
    maxLng = float(city['lng']) + degreesToLng

    betweenLongitudes = om.values(skylines['airportsByCoordinates'], minLng, maxLng)

    if lt.size(betweenLongitudes) == 0:
      info = findAirportNearToCity(skylines, city, numberOfSearch + 1)
    
    else:
      latitudes = lt.newList('ARRAY_LIST')
      
      for latitudeMap in lt.iterator(betweenLongitudes):
        for latitude in lt.iterator(om.values(latitudeMap, minLat, maxLat)):
          for airport in lt.iterator(latitude):
            lt.addLast(latitudes, airport)
      
      if lt.size(latitudes) == 0:
        info = findAirportNearToCity(skylines, city, numberOfSearch + 1)
      elif lt.size(latitudes) > 1:
        info['airport'] = findClosest(latitudes, float(city['lat']), float(city['lng']), skylines['digraph'])
        info['distance'] = haversine(float(info['airport']['Longitude']), float(info['airport']['Latitude']), float(city['lng']), float(city['lat']))
      elif findClosest(latitudes, float(city['lat']), float(city['lng']), skylines['digraph']) is None:
        info = findAirportNearToCity(skylines, city, numberOfSearch + 1)
      else:
        info['airport'] = lt.firstElement(latitudes)
        info['distance'] = haversine(float(info['airport']['Longitude']), float(info['airport']['Latitude']), float(city['lng']), float(city['lat']))
      
  return info


def findClosest(lst, lat, lng, graph):
  closest = None
  minDistance = inf
    
  for airport in lt.iterator(lst):
    distance = haversine(float(airport['Longitude']), float(airport['Latitude']), lng, lat)
    if distance < minDistance and lt.size(gp.adjacents(graph, airport['IATA'])) > 0:
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
  airportEntry = mp.get(skylines['airports'], airportIATA)

  if airportEntry is None:
    return None
  
  airport = me.getValue(airportEntry)

  adjacentVertex = gp.adjacents(skylines['digraph'], airportIATA)

  return [airport, adjacentVertex]
  

# ===================================================
#                  REQUERIMIENTO 6
# ===================================================


# ===================================================
#                  REQUERIMIENTO 7
# ===================================================


#Funciones de ayuda

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
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles. Determines return value units.
    return c * r