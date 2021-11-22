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
    'airports': mp.newMap(numelements=10000, maptype='CHAINING', loadfactor=2.0),
    'digraph': gp.newGraph(datastructure='ADJ_MATRIX', directed=True),
    'undirected': gp.newGraph(datastructure='ADJ_LIST', directed=False),
  }

  return skylines

# Funciones para agregar informacion al catalogo

def addAirport(skylines, airport):
  createAirport(skylines, airport)
  gp.insertVertex(skylines['digraph'], airport['IATA'])
  gp.insertVertex(skylines['undirected'], airport['IATA'])


def addRoute(skylines, route):

  gp.addEdge(skylines['digraph'], route['Departure'], route['Destination'], weight=route['distance_km'])

  if gp.getEdge(skylines['digrapg'], route['Destination'], route['Departure']):
    gp.addEdge(skylines['undirected'], route['Departure'], route['Destination'], weight=route['distance_km'])

# Funciones para creacion de datos

def createAirport(skylines, airport):
  mp.put(skylines['airports'], airport['IATA'], airport)

# Funciones de consulta

def interconectionPoints(skylines):
  pass

# Funciones utilizadas para comparar elementos dentro de una lista

# Funciones de ordenamiento
