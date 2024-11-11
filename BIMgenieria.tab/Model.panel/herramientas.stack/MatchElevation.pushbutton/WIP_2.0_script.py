# -*- coding: utf-8 -*-
#Name of the button displayed in Revit UI
__title__= "Match elevation"

#Description of the button displayed in Revit UI
__doc__= """Description:
Match elevation of source element,
to target elements. 
Only works with conduit, cable tray, 
pipes and ducts.

Tested in Revit 2022

Author: Ing. Arq. Antonio Rojas
"""
# pyRevit Extra MetaTags (optional)
__author__= "Antonio Rojas"

import Autodesk.Revit.DB.Mechanical
import clr
import pyrevit.script

clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import *
from Autodesk.Revit.UI.Selection import *

from pyrevit import forms

# Importaciones para Conduit, Cable Tray y Ducts
from Autodesk.Revit.DB.Electrical import *
from Autodesk.Revit.DB.Electrical import *
from Autodesk.Revit.DB.Mechanical import *
from Autodesk.Revit.DB.Plumbing import *

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

# Seleccionar el elemento fuente
try:
    source_element = doc.GetElement(uidoc.Selection.PickObject(ObjectType.Element,
                                                               "Selecciona el elemento fuente").ElementId)

    # Obtener el parámetro Middle Elevation
    middle_elevation_param = source_element.LookupParameter("Middle Elevation")
    if not middle_elevation_param:
        TaskDialog.Show("Error", "El elemento no tiene el parámetro 'Middle Elevation'")
        raise Exception()

    elevation_value = middle_elevation_param.AsDouble()

except:
    TaskDialog.Show("Error", "No se pudo obtener el elemento o su elevación.")
    raise


# Seleccionar los elementos objetivo
try:
    target_references = uidoc.Selection.PickObjects(ObjectType.Element,
                                                    "Selecciona los elementos objetivo")

    # Iniciar la transacción para modificar los elementos
    with Transaction(doc, "Copiar Middle Elevation") as t:
        t.Start()

        processed = 0
        skipped = 0

        for ref in target_references:
            element = doc.GetElement(ref.ElementId)
            param = element.LookupParameter("Middle Elevation")

            if param and param.IsModifiable:
                param.Set(elevation_value)

        t.Commit()

except Exception as e:
    TaskDialog.Show("Error", "Error durante el proceso:")

pyrevit.script.clipboard_copy(str(elevation_value))
print(elevation_value)


