# -*- coding: utf-8 -*-
__title__= "Get 3D Section Box" #Name of the button displayed in Revit UI
__doc__= """ 

""" #Description of the button displayed in Revit UI

# pyRevit Extra MetaTags (optional)
__author__= "Antonio Rojas"


#IMPORTS
#---------------------------------------------------------------
import os, sys, datetime                                    #Regular imports
import json
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
doc     = __revit__.ActiveUIDocument.Document       #type-Document
uidoc   = __revit__.ActiveUIDocument                #type-UIDocument
from Autodesk.Revit.ApplicationServices import *
app     = __revit__.Application                     #type-Application
active_view = doc.ActiveView                        #Get current view
path_scrypt = os.path.dirname(__file__)             #Absolute path to folder where sript is ocated

#GLOBAL VARIABLES
#VARIABLE QUE PERMITE UTILIZAR IMPRESIONES CUSTOM EN LA TERMINAL
output = script.get_output()


#FUNCTIONS
#---------------------------------------------------------------


#CLASSES
#---------------------------------------------------------------


#MAIN
#---------------------------------------------------------------
#CODE START HERE

# Definir una función para seleccionar una caja y obtener las coordenadas
def pick_box_coordinates():
    try:
        # Usar PickBox para obtener la caja seleccionada
        picked_box = uidoc.Selection.PickBox(PickBoxStyle.Directional, "Selecciona una caja")
        
        if picked_box:
            # Obtener las coordenadas XYZ de los puntos min y max
            min_point = picked_box.Min
            max_point = picked_box.Max
            
            # Mostrar las coordenadas al usuario
            print("Punto mínimo: {0}".format(min_point))
            print("Punto máximo: {0}".format(max_point))
        else:
            print("No se seleccionó ninguna caja.")
    except Exception as e:
        print("Error: {0}".format(e))

# Ejecutar la función
pick_box_coordinates()


#CODE ENDS HERE
#---------------------------------------------------------------