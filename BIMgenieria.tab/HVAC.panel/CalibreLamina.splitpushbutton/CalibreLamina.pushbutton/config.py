# -*- coding: utf-8 -*-
__title__= "Calibre de Lamina Configuración" #Name of the button displayed in Revit UI
__doc__= """Asigna el calibre de lamina de a cuerdo 
al lado mayor del ducto, como lo es indicado en la 
norma mexicana de la AMERIC
NAM-001-AA-83

Configuración inicial ⚙️
Shift + Clic 

Autor: Ing. Arq. Antonio Rojas
""" #Description of the button displayed in Revit UI

# pyRevit Extra MetaTags (optional)
__author__= "Antonio Rojas"

#IMPORTS
#---------------------------------------------------------------
import os, sys                                   #Regular imports
import json
import codecs

import pyrevit.revit.db.query
from Autodesk.Revit import DB
from Autodesk.Revit.DB import *                             #Import DB Classes
from Autodesk.Revit.UI import *                             #Import UI Classes
from Autodesk.Revit.DB.Electrical import  *                 #Import discipline modules


#pyRevit Imports
from pyrevit import forms, revit, script, coreutils

#.NET Imports
import clr
clr.AddReference('System')
from System.Collections.Generic import List

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

res = forms.alert("Calibre de Lamina."
                  "\n\n"
                  "Selecciona el parámetro para la selección del calibre \n"
                  "de lamina:\n\n"
                  "El parámetro debe ser tipo texto.",
                  options=["Continuar",
                           "Cancelar"])
if res == "Continuar":
    #COMPRUEBA LA EXISTENSIA DEL .JSON
    datafile = script.get_document_data_file("Calibre_de_lamina", "json")


    if datafile and os.path.exists(datafile) :
        # Si el archivo existe, cargar los datos
        with open(datafile, 'r') as f:
            param_config = json.load(f)
    else:
        # Si no existe, inicializar los datos y crear el archivo
        calibre_lamina = material_lamina = None
        param_config = {
                         "Calibre de lamina": calibre_lamina
                        }

        # Crear el archivo y guardar los datos iniciales
        with open(datafile, 'w') as f:
            json.dump(param_config, f)


    #SELECCIONAMOS EL PRIMER DUCTO DISPONIBLE EN EL MODELO PARA PODER SELECCIONAR
    #LOS PARÁMETROS DE DICHA CATEGORÍA
    collector = (
        FilteredElementCollector(doc)
        .OfCategory(BuiltInCategory.OST_DuctCurves)
        .WhereElementIsNotElementType()
    )

    first_duct = collector.FirstElement()

    #PREGUNTA AL USUARIO POR EL PARÁMETRO CALIBRE DE FASE
    calibre_lamina = forms.select_parameters(
        first_duct,
        title='Calibre de lamina',
        multiple=False,
        include_instance=True,
        include_type=False
    )

    param_config = {
        "Calibre de lamina": unicode(calibre_lamina.name)
    }

    # ESCRIBE LA INFORMACIÓN EN EL ARCHIVO DE CONFIGURACIÓN
    try:
        with codecs.open(datafile, 'w', encoding="utf-8") as f:
            json.dump(param_config, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print("Error: Fail to write .json file")
        sys.exit()

    # IMPRIME UNA CONFIRMACIÓN DEL SCRIPT
    output.print_md("### Configuración guardada")
    for key, value in param_config.iteritems():
        print(u"{}: {}".format(key, value))

elif res == "Cancelar":
            sys.exit()

#CODE ENDS HERE
#---------------------------------------------------------------




