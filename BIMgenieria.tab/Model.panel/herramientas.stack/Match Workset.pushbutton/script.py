# -*- coding: utf-8 -*-
__title__= "Match Workset" #Name of the button displayed in Revit UI
__doc__= """Version 1.0
Description:

""" #Description of the button displayed in Revit UI

# pyRevit Extra MetaTags (optional)
__author__= "Antonio Rojas"

#IMPORTS
#---------------------------------------------------------------
import os, sys, datetime                                    #Regular imports

import pyrevit.revit
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
def get_workset(element):
    if hasattr(element, 'WorksetId'):
        workset_id = element.WorksetId
        if workset_id and workset_id.IntegerValue != -1:
            return doc.GetWorksetTable().GetWorkset(workset_id)
    return None


def can_change_workset(element):
    # Verificar si el elemento puede cambiar de workset
    if not hasattr(element, 'WorksetId'):
        return False
    if element.Pinned:
        return False
    # Agregar más condiciones si es necesario
    return True


# Paso 1: Seleccionar elementos a cambiar
try:
    selection_ids = uidoc.Selection.GetElementIds()
    elements_to_change = [doc.GetElement(id) for id in selection_ids]
    if not elements_to_change:
        TaskDialog.Show("Error",
                        "Por favor, seleccione los elementos que desea cambiar de workset antes de ejecutar el script.")
        raise SystemExit()
except:
    print("Something went wrong")

    # Paso 2: Seleccionar el elemento de referencia
    reference = pyrevit.revit.pick_element("Seleccione el elemento con el workset de destino")
    target_workset = reference.get_Parameter(BuiltInParameter.ELEM_PARTITION_PARAM).AsElementId()

    if not target_workset:
        TaskDialog.Show("Error", "El elemento seleccionado no tiene un workset válido.")
        raise SystemExit()

    # Cambiar el workset de los elementos seleccionados
    changed_count = 0
    skipped_count = 0
    with Transaction(doc, "Match Workset") as t:
        t.Start()
        for element in elements_to_change:
            if can_change_workset(element):
                current_workset = get_workset(element)
                if current_workset != target_workset:
                    element.WorksetId = target_workset
                    changed_count += 1
            else:
                skipped_count += 1
        t.Commit()

    result_message = "Se ha cambiado el workset de {} elemento(s) al workset '{}'.\n".format(changed_count,
                                                                                             target_workset.Name)
    if skipped_count > 0:
        result_message += "{} elemento(s) no se pudieron cambiar.".format(skipped_count)
    TaskDialog.Show("Resultado", result_message)

except Exception as e:
    import traceback

    error_message = "Ha ocurrido un error:\n\n{}".format(traceback.format_exc())
    TaskDialog.Show("Error", error_message)

#CODE ENDS HERE
#---------------------------------------------------------------
