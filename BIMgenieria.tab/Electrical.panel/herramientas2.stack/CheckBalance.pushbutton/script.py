# -*- coding: utf-8 -*-
__title__= "Check\nBalance" #Name of the button displayed in Revit UI
__doc__= """Calcula el porcentaje de desbalanceo
de los tableros del proyecto.

La herramienta tiene dos modos de uso:
1 - Por medio de una selección 
2 - Selecciona todos los tableros del modelo

Para evitar crasheos en proyectos con gran 
cantidad de tableros la opcción 1 está asignada
por defecto para usar la opcción 2 activa la 
herramienta con: "Shift-Click"

Bug Fix: 🐞
La herramienta lanza un error si el elemento 
seleccionado no contiene el parámetro 
Panel Name. 

Autor: Ing. Arq. Antonio Rojas
""" #Description of the button displayed in Revit UI

# pyRevit Extra MetaTags (optional)
__author__= "Antonio Rojas"

#IMPORTS
#---------------------------------------------------------------
import os, sys, datetime                                    #Regular imports
import pdb

import pyrevit.revit.db.query
from Autodesk.Revit.DB import *                             #Import DB Classes
from Autodesk.Revit.UI import *                             #Import UI Classes
from Autodesk.Revit.DB.Electrical import  *                 #Import discipline modules

#pyRevit Imports
from pyrevit import forms, revit, script, output
from pyrevit import EXEC_PARAMS


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

#MAIN
#---------------------------------------------------------------
#CODE START HERE

if EXEC_PARAMS.config_mode:
    # 1️⃣ MÉTODO 1 - TODOS LOS ELECTRICAL EQUIPMENT DEL MODELO
    # Crear el colector para obtener los elementos de la categoría Electrical Equipment
    collector = FilteredElementCollector(doc)

    # Filtrar solo los elementos de la categoría Electrical Equipment
    electrical_equipment_filter = ElementCategoryFilter(BuiltInCategory.OST_ElectricalEquipment)
    electrical_equipment_filter = collector.WherePasses(electrical_equipment_filter).ToElements()

    # Convertir a una lista de FamilyInstance
    elements = [element for element in electrical_equipment_filter if isinstance(element, FamilyInstance)]
else:
    with forms.WarningBar(title="Selecciona uno o varios tableros"):
        # 2️⃣ MÉTODO 2 - TODOS LOS ELECTRICAL EQUIPMENT DEL MODELO
        elements = revit.selection.pick_elements_by_category("Electrical Equipment","Select object")

data_list = []


#BUG FIX 🐞🐞🐞🐞
"""POR AHORA EL SCRIPT FUNCIONA PERO SI EXISTE UN ELECTRICAL EQUIPMENT QUE NO SEA
UN PART TYPE QUE CONTENGA EL PARÁMETRO PANEL NAME, EL SCRIPT SE DETIENE

ESTE ES EL CÓDIGO QUE ME AYUDÓ A ENCONTRAR EL PROBLEMA"""
    # for i, e in enumerate(elements):
    #     try:
    #         element_id = e.Id
    #         print("Procesando el índice {0}, valor: {1}, ElementId {2}".format(i, e, element_id))  # Usando .format()
    #         tab_name = e.get_Parameter(BuiltInParameter.RBS_ELEC_PANEL_NAME).AsString()
    #
    #
    #     except Exception as ex:
    #         print("Error en el índice {0} con valor {1}: {2}".format(i, e, ex))
    #
    #
    # sys.exit()

"""AQUI UNA POSIBLE SOLUCIÓN
AL INICIAR EL SCRIPT CON LA SEGUNDA OPCIÓN SE DEBERÍA HACER UNA COMPROBACIÓN PARA SABER
SI EL ELEMENTO ES UN PART TYPE ACEPTADO

OTRA POSIBLE SOLUCIÓN SERÍA COMPROBAR SI EL PARÁMETRO PANEL NAME O CURRENT PHASE A
EXISTE Y SI NO DETENER EL SCRIPT
"""

    # from Autodesk.Revit.DB import BuiltInParameter, PartType
    #
    #
    # def get_family_part_type(family_instance):
    #     """
    #     Obtiene el PartType de una FamilyInstance.
    #
    #     :param family_instance: FamilyInstance a evaluar.
    #     :return: PartType del FamilyInstance o PartType.Undefined si no se puede determinar.
    #     """
    #     if family_instance and family_instance.Symbol and family_instance.Symbol.Family:
    #         family = family_instance.Symbol.Family
    #         param = family.get_Parameter(BuiltInParameter.FAMILY_CONTENT_PART_TYPE)
    #         if param:
    #             return PartType(param.AsInteger())
    #     return PartType.Undefined


for e in elements:
    # Obtener los parámetros
    tab_name = e.get_Parameter(BuiltInParameter.RBS_ELEC_PANEL_NAME).AsString()
    currentA = e.get_Parameter(BuiltInParameter.RBS_ELEC_PANEL_CURRENT_PHASEA_PARAM).AsDouble()
    currentB = e.get_Parameter(BuiltInParameter.RBS_ELEC_PANEL_CURRENT_PHASEB_PARAM).AsDouble()
    currentC = e.get_Parameter(BuiltInParameter.RBS_ELEC_PANEL_CURRENT_PHASEC_PARAM).AsDouble()
    element_id = e.Id

    #Redondear a 2 decimales
    currentA = round(currentA,2)
    currentB = round(currentB,2)
    currentC = round(currentC,2)

    #obtener máximos y minimos
    max_valor = max(currentA, currentB, currentC)
    min_valor = min(currentA, currentB, currentC)

    # Verificar si el divisor no es cero
    if max_valor != 0 :
        desb = ((max_valor - min_valor)/(max_valor)) * 100
    else:
        desb = "No se puede dividir por cero"

    # Agregar a la lista el desbalanceo de cada tablero
    data_list.append([tab_name, currentA, currentB, currentC, desb, element_id])



# Filtramos las listas que tienen un valor numérico en el índice 4
numeric_lists = [entry for entry in data_list if isinstance(entry[4], (int, float))]

#SALIDAS DE INFORMACIÓN
# Encontramos la lista con el valor más grande en el índice 4
max_value_list = max(numeric_lists, key=lambda x: x[4])


# Ordenamos las listas de mayor a menor según el valor en el índice 4
sorted_lists = sorted(numeric_lists, key=lambda x: x[4], reverse=True)

#CODE ENDS HERE
#---------------------------------------------------------------
output.print_md("# Porcentaje de desbalanceo")
output.print_md("### Fórmula:")
print("""((Corriente Mayor - Corriente Menor) / (Corriente Mayor)) * 100""")
print("-"*75)

output.print_md("### Tablero más crítico")
print("Panel Name: {0}".format(max_value_list[0],max_value_list[4]))
print("% Desbalance : {0}".format(max_value_list[4]))
print("Element Id : {0}".format(max_value_list[5]))
print(output.linkify(max_value_list[5]))


output.print_md("### Desbalanceo por tablero, ordenados de mayor a menor")
for entry in sorted_lists:
    print("Panel Name: {0}".format(entry[0], entry[4]))
    print("% Desbalance : {0}".format(entry[4]))
    print("Element Id : {0}".format(entry[5]))
    print(output.linkify(entry[5]))
    print("-" * 50)