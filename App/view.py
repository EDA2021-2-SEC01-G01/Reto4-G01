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
assert cf


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def initSkylines():
   return controller.initSkylines() 


def loadSkylines(skylines):
    print('Serán cargados los archivos por defecto.')
    custom = input('Ingresa 1 para ingresar archivos diferentes, de lo contrario deja vacio:\n> ')
    
    airports = 'airports_full.csv'
    routes = 'routes_full.csv'
    worldcities = 'worldcities.csv'

    if '1' in custom:
        airports = input('Ingresa el nombre del archivo de aeropuertos:\n> ')
        routes = input('Ingresa el nombre del archivo de rutas:\n> ')
        worldcities = input('Ingresa el nombre del archivo de ciudades:\n> ')

    controller.loadData(skylines, airports, routes, worldcities)


def returnInfo(skylines):
    print('El número de aeropuertos cargados el grafo DIRIGIDO es:', lt.size(skylines['digraphAirportsLst']))
    print('El número de aeropuertos cargados el grafo NO DIRIGIDO es:', lt.size(skylines['undirectedAirportsLst']))
    print('El número de ciudades cargadas es:', lt.size(skylines['citiesLst']))
    
    print('\nLa información del primer aeropuerto cargado en el grafo DIRIGIDO es:\n')
    fAirportD = lt.firstElement(skylines['digraphAirportsLst'])
    print('\tNombre:', fAirportD['Name'])
    print('\tCiudad:', fAirportD['City'])
    print('\tPaís:', fAirportD['Country'])
    print('\tIATA:', fAirportD['IATA'])
    print('\tLatitud:', fAirportD['Latitude'])
    print('\tLongitud:', fAirportD['Longitude'])
    
    print('\nLa información del primer aeropuerto cargado en el grafo DIRIGIDO es:\n')
    fAirportU = lt.firstElement(skylines['undirectedAirportsLst'])
    print('\tNombre:', fAirportU['Name'])
    print('\tCiudad:', fAirportU['City'])
    print('\tPaís:', fAirportU['Country'])
    print('\tIATA:', fAirportU['IATA'])
    print('\tLatitud:', fAirportU['Latitude'])
    print('\tLongitud:', fAirportU['Longitude'])

    print('\nLa información de la ultima ciudad cargada es:\n')
    lCity = lt.lastElement(skylines['citiesLst'])
    print('\tCiudad:', lCity['city'])
    print('\tCiudad ASCII:', lCity['city_ascii'])
    print('\tLatitud:', lCity['lat'])
    print('\tLongitud:', lCity['lng'])
    print('\tPaís:', lCity['country'])
    print('\tISO2:', lCity['iso2'])
    print('\tISO3:', lCity['iso3'])
    print('\tNombre Administrador:', lCity['admin_name'])
    print('\tCapital:', lCity['capital'])
    print('\tPoblación:', lCity['population'])
    print('\tID:', lCity['id'])


def shortestRoute(skylines):
    city1 = input('Ingresa el nombre de la ciudad origen (ASCII):\n> ')
    city2 = input('Ingresa el nombre de la ciudad destino (ASCII):\n> ')

    info = controller.shortestRoute(skylines, city1, city2)

    if info is None:
        print('Alguna de las ciudades no existe o no existe una ruta disponible')
        return None

    print('\nEl aeropuerto de origen a una distancia de', str(round(info[0]['distance'], 3)) + 'km', 'de la ciudad de origen es:\n')
    print('\tNombre:', info[0]['airport']['Name'])
    print('\tCiudad:', info[0]['airport']['City'])
    print('\tPaís:', info[0]['airport']['Country'])
    print('\tIATA:', info[0]['airport']['IATA'])
    print('\tLatitud:', info[0]['airport']['Latitude'])
    print('\tLongitud:', info[0]['airport']['Longitude'])

    print('\nEl aeropuerto de destino a una distancia de', str(round(info[1]['distance'], 3)) + 'km', 'de la ciudad de destino es:\n')
    print('\tNombre:', info[1]['airport']['Name'])
    print('\tCiudad:', info[1]['airport']['City'])
    print('\tPaís:', info[1]['airport']['Country'])
    print('\tIATA:', info[1]['airport']['IATA'])
    print('\tLatitud:', info[1]['airport']['Latitude'])
    print('\tLongitud:', info[1]['airport']['Longitude'])

    print('\nLos vuelos necesarios para llegar de', city1, 'a', city2 + ' son:')
    
    totalDistance = info[0]['distance'] + info[1]['distance']

    for route in lt.iterator(info[2]):
        totalDistance += route['weight']
        print('\t', 'De', route['vertexA'], 'a', route['vertexB'] + '.', str(route['weight']) + 'km')

    print('\nLa distancia total es:', str(round(totalDistance, 3)) + 'km.\n')

def printMenu():
    print("Bienvenido")
    print("1- Cargar información en el catálogo")
    print("4- Encontrar la ruta más corta entre ciudades")

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
    elif int(inputs[0]) == 4:
        shortestRoute(skylines)
    else:
        sys.exit(0)
sys.exit(0)
