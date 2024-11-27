# -*- coding: utf-8 -*-
__title__= "Set Switch ID" #Name of the button displayed in Revit UI
__doc__= """Version 1.0
Description:
Rename switch ID's of all Lighting Devices of the model
a...z , aa...zz and so on

To do:
Handle three way switches
Ignore switches that all ready has Switch Id

Author: Ing. Arq. Antonio Rojas
""" #Description of the button displayed in Revit UI


#---------------------------------------------------------------
import os, sys, datetime                                    #Regular imports
import pyrevit.revit.db.query
from Autodesk.Revit.DB import *                             #Import DB Classes
from Autodesk.Revit.UI import *                             #Import UI Classes
from Autodesk.Revit.DB.Electrical import  *                 #Import discipline modules
import string

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
def sucesion_abecedario(longitud):
    abecedario = string.ascii_lowercase  # 'abcdefghijklmnopqrstuvwxyz'
    sucesion = []

    for i in range(longitud):
        # Si ya hemos pasado de la z, empezamos con combinaciones de dos letras
        if i < 26:
            sucesion.append(abecedario[i])
        else:
            # Se calcula el índice de combinación, empezando desde 'aa'
            combinacion = abecedario[(i - 26) // 26] + abecedario[(i - 26) % 26]
            sucesion.append(combinacion)

    return sucesion

#MAIN
#---------------------------------------------------------------

#Crear un colector con los apagadores del modelo
all_switch = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_LightingDevices).WhereElementIsNotElementType()

#Crear una lista con todos los swtches
elements = all_switch.ToElements()

#Obetener la longitud de la lista
longitud_list = len(elements)

#Crear lista de claves de apagador
list_SwitchId = sucesion_abecedario(longitud_list)


#Inicia transacción para cambiar parámetro
t = Transaction(doc, __title__)
t.Start()

for e, id in zip(elements, list_SwitchId):
    param_switchid = e.get_Parameter(BuiltInParameter.RBS_ELEC_SWITCH_ID_PARAM)
    param_switchid.Set(str(id))

t.Commit()

output.print_md("## Switch ID's Updated")
output.print_md("### Number of elements edited:")
print(longitud_list)

