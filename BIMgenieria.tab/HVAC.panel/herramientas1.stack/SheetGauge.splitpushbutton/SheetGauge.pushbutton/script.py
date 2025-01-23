# -*- coding: utf-8 -*-
__title__= "Calibre de Lamina" #Name of the button displayed in Revit UI
__doc__= """Asigna el calibre de lamina de a cuerdo 
al lado mayor del ducto, como lo es indicado en la 
A.S.H.R.A.E. "Shift-Click"
""" #Description of the button displayed in Revit UI

# pyRevit Extra MetaTags (optional)
__author__= "Antonio Rojas"

#IMPORTS
#---------------------------------------------------------------
import os, sys, datetime                                    #Regular imports

import pyrevit.revit.db.query
from Autodesk.Revit.DB import *                             #Import DB Classes
from Autodesk.Revit.UI import *
from Autodesk.Revit.DB.Mechanical import  *                 #Import discipline modules

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
output = script.get_output()

#GLOBAL VARIABLES

#FUNCTIONS
#---------------------------------------------------------------


#CLASSES
#---------------------------------------------------------------


#MAIN
#---------------------------------------------------------------
#CODE START HERE

output.print_md('# Calibre de Lamina')

#RECOLECTAR TODOS LOS DUCTOS DEL MODELO
collector = (
    FilteredElementCollector(doc)
    .OfCategory(BuiltInCategory.OST_DuctCurves)
    .WhereElementIsNotElementType()
    .ToElements()
)


#REVISAR SI EL ELEMENTO ES CUADRADO, OVALADO O CIRCULAR
ducts_cuadrado = []
ducts_redondo = []

for d in collector:
    duct_size = d.get_Parameter(BuiltInParameter.RBS_CALCULATED_SIZE).AsString()
    if "x" in duct_size:
        ducts_cuadrado.append(d)
    elif "ø" in duct_size:
        ducts_redondo.append(d)



#LISTAS PARA ALMACENAR LOS ELEMENTOS CLASIFICADOS
    list_cal26 = []
    list_cal24 = []
    list_cal22 = []
    list_cal20 = []
    list_cal18 = []

#ITERAR EN LOS DUCTOS CUADRADOS PARA OBTENER EL LADO MAYOR


for d in ducts_cuadrado:
    duct_height_ft = d.get_Parameter(BuiltInParameter.RBS_CURVE_HEIGHT_PARAM).AsDouble()
    duct_width_ft = d.get_Parameter(BuiltInParameter.RBS_CURVE_WIDTH_PARAM).AsDouble()

    # CONVERTIR DE PIES A PULGADAS
    duct_height_in = duct_height_ft * 12
    duct_width_in = duct_width_ft * 12

    #OBTENER EL LADO MAYOR
    lado_mayor = max(duct_height_in , duct_width_in)

    #LÓGICA PARA CLASIFICAR LOS DUCTOS SEGÚN SU LADO MAYOR
    if lado_mayor <= 12:
        list_cal26.append(d)

    elif lado_mayor > 12.1 and lado_mayor <= 30:
        list_cal24.append(d)

    elif lado_mayor > 30.1 and lado_mayor <= 54:
        list_cal22.append(d)

    elif lado_mayor > 54.1 and lado_mayor <= 84:
        list_cal20.append(d)

    elif lado_mayor > 84:
        list_cal18.append(d)

    else:
        print("Error al obtener el lado mayor")



#ESCRIBIR EN EL PARÁMETRO SELECCIONADO LOS VALORES
t = Transaction(doc, __title__)
t.Start()

for d in list_cal26:
    d.get_Parameter(BuiltInParameter.ALL_MODEL_INSTANCE_COMMENTS).Set("Calibre 26")

for d in list_cal24:
    d.get_Parameter(BuiltInParameter.ALL_MODEL_INSTANCE_COMMENTS).Set("Calibre 24")

for d in list_cal22:
    d.get_Parameter(BuiltInParameter.ALL_MODEL_INSTANCE_COMMENTS).Set("Calibre 22")

for d in list_cal20:
    d.get_Parameter(BuiltInParameter.ALL_MODEL_INSTANCE_COMMENTS).Set("Calibre 20")

for d in list_cal18:
    d.get_Parameter(BuiltInParameter.ALL_MODEL_INSTANCE_COMMENTS).Set("Calibre 18")

t.Commit()

#IMPRESIÓN DE RESULTADOS
output.print_md("##Resultados")
output.print_md("Se han encontrado: **{}** ductos cuadrados **calibre 26**".format(str((len(list_cal26)))))
output.print_md("Se han encontrado: **{}** ductos cuadrados **calibre 24**".format(str((len(list_cal24)))))
output.print_md("Se han encontrado: **{}** ductos cuadrados **calibre 22**".format(str((len(list_cal22)))))
output.print_md("Se han encontrado: **{}** ductos cuadrados **calibre 20**".format(str((len(list_cal20)))))
output.print_md("Se han encontrado: **{}** ductos cuadrados **calibre 18**".format(str((len(list_cal18)))))

#CODE ENDS HERE
#---------------------------------------------------------------