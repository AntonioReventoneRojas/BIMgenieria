# -*- coding: utf-8 -*-
__title__= "Clean AutoCAD trash files" #Name of the button displayed in Revit UI
__doc__= """Version 1.0
Description:
Clean dwl2, dwl and bak files in 
selected folder.

Author: Ing. Arq. Antonio Rojas

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

#FUNCTIONS
#---------------------------------------------------------------


#CLASSES
#---------------------------------------------------------------


#MAIN
#---------------------------------------------------------------
#CODE START HERE

# Solicita la ruta de carpeta al usuario
folder_path = forms.pick_folder()

# Verifica si la ruta es válida
if folder_path:
    # Pregunta al usuario si quiere buscar en subcarpetas
    include_subfolders = forms.alert("¿Quieres buscar en subcarpetas también?", yes=True, no=True)

    # Define las extensiones de archivo a buscar
    extensions_to_delete = [".dwl2", ".dwl", ".bak"]

    # Encuentra archivos con las extensiones especificadas
    files_to_delete = []
    if include_subfolders:
        # Busca en la carpeta y en sus subcarpetas
        for root, _, files in os.walk(folder_path):
            files_to_delete.extend(
                os.path.join(root, f) for f in files if any(f.endswith(ext) for ext in extensions_to_delete)
            )
    else:
        # Busca solo en la carpeta seleccionada, sin incluir subcarpetas
        files_to_delete = [
            os.path.join(folder_path, f) for f in os.listdir(folder_path)
            if os.path.isfile(os.path.join(folder_path, f)) and any(f.endswith(ext) for ext in extensions_to_delete)
        ]

    # Muestra el número de archivos encontrados
    file_count = len(files_to_delete)
    if file_count > 0:
        # Pide confirmación al usuario
        confirmation = forms.alert("Se encontraron {0} archivos para eliminar. ¿Quieres continuar?".format(file_count),
                                    ok=False,
                                    yes=True,
                                    no=True)

        # Si el usuario confirma, borra los archivos
        if confirmation:
            for file_path in files_to_delete:
                os.remove(file_path)
            forms.alert("Archivos eliminados exitosamente.")
        else:
            forms.alert("Operación cancelada por el usuario.")
    else:
        forms.alert("No se encontraron archivos con las extensiones especificadas en la carpeta.")
else:
    forms.alert("No se seleccionó ninguna carpeta.")

#CODE ENDS HERE
#---------------------------------------------------------------