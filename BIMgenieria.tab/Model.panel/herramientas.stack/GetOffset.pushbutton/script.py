# -*- coding: utf-8 -*-
__title__= "MEP Offset" #Name of the button displayed in Revit UI
#Description of the button displayed in Revit UI
__doc__= """Description:
Select two horizontal objects, like conduit or cable tray 
and get the offset.

Tested in Revit 2022

Author: Ing. Arq. Antonio Rojas
"""

# pyRevit Extra MetaTags (optional)
__author__= "Antonio Rojas"

#IMPORTS
#---------------------------------------------------------------
import os, sys, datetime                                    #Regular imports

import pyrevit.script
from Autodesk.Revit.DB import *                             #Import DB Classes
from Autodesk.Revit.UI import *                             #Import UI Classes
from Autodesk.Revit.DB.Electrical import  *                 #Import discipline modules

#pyRevit Imports
from pyrevit import forms, revit, script

output = script.get_output()

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
    BuiltInCategory.OST_CableTray,
    BuiltInCategory.OST_DuctCurves,
    BuiltInCategory.OST_PipeCurves
]

#Selección de elementos
with forms.WarningBar(title="Selecciona dos elementos:"):
    selected_elements = revit.pick_elements()

try:
    if len(selected_elements) != 2:
        forms.alert("Debes seleccionar exactamente dos elementos.", exitscript=True)
except:
    for element in selected_elements:
        category = element.Category
        if category.Id.IntegerValue not in [cat.value__ for cat in allowed_categories]:
            forms.alert("Debes seleccionar solo elementos Conduit o Cable Tray", exitscript=True)

# Crear una lista para almacenar los resultados
resultados = []
elevaciones = []

#Intentar obtener los valores
for i in selected_elements:
    middle_elevation = round(get_param_value(i,"Middle Elevation"),7)
    ob_type = i.Category.Name
    ob_id = i.Id.IntegerValue
    resultados.append(
        {"Element": ob_type , "Element Id": ob_id , "Middle Elevation": middle_elevation}
    )
    elevaciones.append(middle_elevation)

offset = elevaciones[0] - elevaciones[-1]


output.print_md("## Result copied to clipboard")
pyrevit.script.clipboard_copy(str(offset))
output.print_md("### Offset between elements is:")
print(offset)
print("meters")
print("""--------------------------------------""")
output.print_md("###Selected elements:")
print("""--------------------------------------""")
for item in resultados:
    print("Element: {}".format(item['Element']))
    print("Middle Elevation: {} meters".format(item['Middle Elevation']))
    print("Element Id: {}".format(item['Element Id']))
    print("--------------------------------------")
