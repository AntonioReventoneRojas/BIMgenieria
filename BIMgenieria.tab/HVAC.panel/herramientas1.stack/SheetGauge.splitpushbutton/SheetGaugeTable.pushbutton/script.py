# -*- coding: utf-8 -*-
__title__= "Tabla de Calibres" #Name of the button displayed in Revit UI
__doc__= """Tabla para la construcción de ductos 
rectangulares de baja presión.

Fuente: Guías Técnicas de Construcción 
Instalaciones de Aire Acondicionado 
IMSS
México

""" #Description of the button displayed in Revit UI

# pyRevit Extra MetaTags (optional)
__author__= "Antonio Rojas"

#IMPORTS
#---------------------------------------------------------------
import os, sys, datetime                                    #Regular imports

import pyrevit.revit.db.query
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
output = script.get_output()

#FUNCTIONS
#---------------------------------------------------------------


#CLASSES
#---------------------------------------------------------------


#MAIN
#---------------------------------------------------------------
#CODE START HERE

data = [
    ["Hasta 30cm (12 in)", "No. 26", "No. 24"],
    ["Hasta 76cm (30 in)", "No. 24", "No. 22"],
    ["Hasta 137cm (54 in)", "No. 22", "No. 20"],
    ["Hasta 214cm (84 in)", "No. 20", "No. 16"],
    ["Hasta 215cm (84 in)", "No. 18", "-"]
]

output.print_table(table_data=data,
                       title="Tabla para la construcción de ductos rectangulares de baja presión",
                       columns=["Lado mayor del ducto", "Calibre de lámina galvanizada",
                                "Calibre de lamina de aluminio"],
                       formats=["", "",
                                ""]
                      )
print("""Fuente: Guías Técnicas de Construcción 
Instalaciones de Aire Acondicionado 
IMSS
México""")

#CODE ENDS HERE
#---------------------------------------------------------------