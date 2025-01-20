# -*- coding: utf-8 -*-
__title__= "Config Shortcuts" #Name of the button displayed in Revit UI
__doc__= """ 
Use this tool to config the paths of the
shortcut folders.

Shift + Click: Show the actual stored folder location.
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


datafile = script.get_document_data_file("FolderShortcuts1", "json")


if datafile and os.path.exists(datafile) :
    # Si el archivo existe, cargar los datos
    with open(datafile, 'r') as f:
        mod_data = json.load(f)
else:
    # Si no existe, inicializar los datos y crear el archivo
    path1 = path2 = path3 = path4 = None
    mod_data = {"F1": path1, "F2": path2, "F3": path3, "F4": path4}

    # Crear el archivo y guardar los datos iniciales
    with open(datafile, 'w') as f:
        json.dump(mod_data, f, indent=4)

#PREGUNTA AL USUARIO QUE SHORTCUT DESEA CONFIGURAR
try:
    selected_option = forms.CommandSwitchWindow.show(
        ['Folder 1', 'Folder 2', 'Folder 3', 'Folder 4'],
         message='Select Option:',
    )
except:
    exit()

# Lógica para seleccionar carpetas
if selected_option == 'Folder 1':
    mod_data["F1"] = forms.pick_folder()


elif selected_option == 'Folder 2':
    mod_data["F2"] = forms.pick_folder()


elif selected_option == 'Folder 3':
    mod_data["F3"]  = forms.pick_folder()


elif selected_option == 'Folder 4':
    mod_data["F4"] = forms.pick_folder()

#ESCRIBE LA INFORMACIÓN EN EL ARCHIVO DE CONFIGURACIÓN
try:
    f = open(datafile, 'w')
    json.dump(mod_data, f)
    f.close()
except:
    print("Error: Fail to write .json file")

#IMPRIME UNA CONFIRMACIÓN DEL SCRIPT
output.print_md("## Saved folder paths")
for key, value in mod_data.iteritems():
    print(key, value)

#CODE ENDS HERE
#---------------------------------------------------------------