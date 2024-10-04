# -*- coding: utf-8 -*-
__title__= "Offset" #Name of the button displayed in Revit UI
__doc__= """Version 1.0
Description:
Select two horizontal objects, like conduit or cable tray 
and get the offset.
""" #Description of the button displayed in Revit UI

# pyRevit Extra MetaTags (optional)
__author__= "Antonio Rojas"

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

#FUNCIONES
#---------------------------------------------------------------
# Obtener valores del parámetro Middle Elevation y Reference Level
def get_param_value(element, param_name):
    param_ft = element.LookupParameter(param_name).AsDouble()
    param_meters = param_ft*0.3048
    if param_meters:
        return param_meters
    return None

def get_reference_level(element):
    param = element.LookupParameter("Reference Level")
    if param:
        return param.AsString()
    return "N/A"

#MAIN
#---------------------------------------------------------------
# Lista de categorías permitidas
allowed_categories = [
    BuiltInCategory.OST_Conduit,
    BuiltInCategory.OST_CableTray
]

#Selección de elementos
selected_elements = revit.pick_elements("Selecciona dos elementos")

try:
    if len(selected_elements) != 2:
        forms.alert("Debes seleccionar exactamente dos elementos.", exitscript=True)
except:
    for element in selected_elements:
        category = element.Category
        if category.Id.IntegerValue not in [cat.value__ for cat in allowed_categories]:
            forms.alert("Debes seleccionar solo elementos Conduit o Cable Tray", exitscript=True)


# Obtener información del primer y segundo elemento
element_1 = selected_elements[0]
element_2 = selected_elements[1]

# Obtener valores del Middle Elevation y Reference Level
middle_elevation_1 = round(get_param_value(element_1, "Middle Elevation"),5)
middle_elevation_2 = round(get_param_value(element_2, "Middle Elevation"),5)

reference_level_1 = get_reference_level(element_1)
reference_level_2 = get_reference_level(element_2)

print(element_1, element_2)
print(middle_elevation_1, middle_elevation_2)
print(abs(abs(middle_elevation_1) - abs(middle_elevation_2)))


# # Calcular el offset (diferencia entre Middle Elevations)
# offset = (middle_elevation_1 - middle_elevation_2)
#
# # Imprimir la información en la terminal
# print("Objeto 1")
# print("Tipo de Objeto: {}".format(element_1.Name))
# print("Reference Level: {}".format(reference_level_1))
# print("Middle Elevation: {:.2f}".format(middle_elevation_1))
#
# print("\nObjeto 2")
# print("Tipo de Objeto: {}".format(element_2.Name))
# print("Reference Level: {}".format(reference_level_2))
# print("Middle Elevation: {:.2f}".format(middle_elevation_2))
#
# print("\n------------")
# print("Offset: {:.2f}".format(offset))

doc.DisplayUnitSystem