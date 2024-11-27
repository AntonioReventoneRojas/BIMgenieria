# -*- coding: utf-8 -*-

__title__= "Match elevation" #Name of the button displayed in Revit UI
__doc__= """Version 1.0
Description:
Match elevetion of source conduit or cable tray
to target elements. 
Only works with conduit and cable tray.

How to:
Select a conduit or cable tray, run the tool
then select target elements. 

Author: Ing. Arq. Antonio Rojas
""" #Description of the button displayed in Revit UI

# pyRevit Extra MetaTags (optional)
__author__= "Antonio Rojas"

import clr

clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import *
from Autodesk.Revit.UI.Selection import *

# Importaciones específicas para Conduit y CableTray
from Autodesk.Revit.DB.Electrical import Conduit
from Autodesk.Revit.DB.Electrical import CableTray

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument


def get_middle_elevation(element):
    if isinstance(element, (Conduit, CableTray)):
        start_point = element.Location.Curve.GetEndPoint(0)
        end_point = element.Location.Curve.GetEndPoint(1)
        return (start_point.Z + end_point.Z) / 2
    else:
        return None


def copy_middle_elevation(source_element, target_elements):
    middle_elevation = get_middle_elevation(source_element)
    if middle_elevation is None:
        TaskDialog.Show("Error", "El elemento seleccionado no es un Conduit o Cable Tray.")
        return

    with Transaction(doc, "Copiar Middle Elevation") as t:
        t.Start()
        for element in target_elements:
            if isinstance(element, (Conduit, CableTray)):
                curve = element.Location.Curve
                start_point = curve.GetEndPoint(0)
                end_point = curve.GetEndPoint(1)

                new_start = XYZ(start_point.X, start_point.Y, middle_elevation)
                new_end = XYZ(end_point.X, end_point.Y, middle_elevation)

                new_curve = Line.CreateBound(new_start, new_end)
                element.Location.Curve = new_curve
        t.Commit()


# Seleccionar el elemento fuente
try:
    source_element = doc.GetElement(uidoc.Selection.PickObject(ObjectType.Element,
                                                               "Selecciona el elemento fuente (Conduit o Cable Tray)").ElementId)
except:
    TaskDialog.Show("Error", "No se seleccionó ningún elemento.")
    raise

# Seleccionar los elementos objetivo
try:
    target_references = uidoc.Selection.PickObjects(ObjectType.Element,
                                                    "Selecciona los elementos objetivo (Conduit o Cable Tray)")
    target_elements = [doc.GetElement(ref.ElementId) for ref in target_references]
except:
    TaskDialog.Show("Error", "No se seleccionaron elementos objetivo.")
    raise

# Copiar la elevación media
copy_middle_elevation(source_element, target_elements)

TaskDialog.Show("Completado", "La elevación media se ha copiado a los elementos seleccionados.")