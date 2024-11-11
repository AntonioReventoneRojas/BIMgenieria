# -*- coding: utf-8 -*-
__title__= "WIP_Get Elements" #Name of the button displayed in Revit UI
__doc__= """Version 1.0
Description:

""" #Description of the button displayed in Revit UI

# pyRevit Extra MetaTags (optional)
__author__= "Antonio Rojas"
__helpurl= ""

#IMPORTS
#---------------------------------------------------------------
import os, sys, datetime                                    #Regular imports
from Autodesk.Revit.DB import *                             #Import DB Classes
from Autodesk.Revit.UI import *                             #Import UI Classes
from Autodesk.Revit.DB.Electrical import  *                 #Import discipline modules

#pyRevit Imports
from pyrevit import forms, revit, script

#.NET Imports
import clr
clr.AddReference('System')
from System.Collections.Generic import List
#List_example = List[ElementId]()

#VARIABLES
#---------------------------------------------------------------
doc     = __revit__.ActiveUIDocument.Document       #type: Document
uidoc   = __revit__.ActiveUIDocument                #type: UIDocument
from Autodesk.Revit.ApplicationServices import *
app     = __revit__.Application                     #type: Application
active_view = doc.ActiveView                        #Get current view
path_scrypt = os.path.dirname(__file__)             #Absolute path to folder where sript is ocated

#GLOBAL VARIABLES

#FUNCTIONS
#---------------------------------------------------------------


#CLASSES
#---------------------------------------------------------------


#MAIN
#---------------------------------------------------------------

# Definir una lista con las categorías deseadas
lista_categorias = [
    OST_LightingDevices
]

# Inicializar una lista para almacenar los elementos encontrados
elementos_encontrados = []

# Recorrer las categorías de la lista
for categoria in lista_categorias:
    # Usar FilteredElementCollector para obtener las instancias de la categoría
    elementos = FilteredElementCollector(doc).OfCategory(categoria).WhereElementIsNotElementType().ToElements()

    # Agregar los elementos a la lista
    elementos_encontrados.extend(elementos)


#CODE ENDS HERE
#---------------------------------------------------------------
 # imprimir cantidad los elementos a la lista
cantidad = len(elementos_encontrados)
print("Se han encontrado: {} elementos".format(cantidad))