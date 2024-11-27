# -*- coding: utf-8 -*-
__title__= "Config Shortcuts" #Name of the button displayed in Revit UI
__doc__= """


""" #Description of the button displayed in Revit UI

# pyRevit Extra MetaTags (optional)
__author__= "Antonio Rojas"

import json
#IMPORTS
#---------------------------------------------------------------
import os, sys, datetime                                    #Regular imports


#pyRevit Imports
from pyrevit import forms, revit, script, output


#.NET Imports
import clr
clr.AddReference('System')

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
path01 = None

#FUNCTIONS
#---------------------------------------------------------------


#CLASSES
#---------------------------------------------------------------


#MAIN
#---------------------------------------------------------------
#CODE START HERE

#CARGA EL ARCHIVO DE CONFIGURACIÓN
datafile = script.get_document_data_file("FolderShortcuts1", "json")

if datafile and os.path.exists(datafile) :
    # Si el archivo existe, cargar los datos
    with open(datafile, 'r') as f:
        mod_data = json.load(f)

#IMRPIME EN PANTALLA LAS RUTAS ACTUALES ALMACENADAS EN EL ARCHIVO DE CONFIGURACIÓN
output.print_md("## Current folder path's")
for key, value in mod_data.iteritems():
    print(key, value)