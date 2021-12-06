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
 """

import config as cf
import model
import csv


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de libros

def initSkylines():
  return model.initSkylines()

# Funciones para la carga de datos

def loadData(skylines, airportsFile, routesFile, citiesFile):
  airports = cf.data_dir + airportsFile
  routes = cf.data_dir + routesFile
  cities = cf.data_dir + citiesFile

  airportsInput = csv.DictReader(open(airports, encoding='utf-8'), delimiter=',')
  routesInput = csv.DictReader(open(routes, encoding='utf-8'), delimiter=',')
  citiesInput = csv.DictReader(open(cities, encoding='utf-8'), delimiter=',')

  for airport in airportsInput:
    model.addAirport(skylines, airport)

  for route in routesInput:
    model.addRoute(skylines, route)

  for city in citiesInput:
    model.addCity(skylines, city)

# Funciones de consulta sobre el catálogo

#Req. 1

def connectionPoints(skylines):
  return model.connectionPoints(skylines)

#Req. 2

"""
AQUI REQUERIMIENTO 2
"""

#Req. 3

def shortestRoute(skylines, city1, city2):
  return model.shortestRouteBetweenCities(skylines, city1, city2)

#Req. 4

"""
AQUI REQUERIMIENTO 4
"""

#Req. 5

def quantifyEffect(skylines, airportIATA):
  return model.quantifyEffect(skylines, airportIATA)

#Req. 6

def shortestWebRoute(skylines, city1, city2):
  return model.compareWebService(skylines, city1, city2)

#Req. 6

def viewGraphically(skylines):
  model.viewGraphically(skylines)