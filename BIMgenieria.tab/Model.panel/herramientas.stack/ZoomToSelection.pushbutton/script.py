# -*- coding: utf-8 -*-

__title__= "Zoom to Selection" #Name of the button displayed in Revit UI
__doc__= """Version 1.0
Description:
Zoom view to selected objects. 
Only works with model views like, floor plans, 
sections, elevations.
It works with model elements and text notes. 

To do:
- Handle views on sheets, schedules and other
2D elements.

""" #Description of the button displayed in Revit UI

# pyRevit Extra MetaTags (optional)
__author__= "Antonio Rojas"

import clr

clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import *

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

# Obtener los elementos seleccionados
selection = [doc.GetElement(elId) for elId in uidoc.Selection.GetElementIds()]

if not selection:
    TaskDialog.Show("Error", "No hay elementos seleccionados. Por favor, selecciona al menos un elemento.")
else:
    # Crear una lista para almacenar los puntos de los elementos seleccionados
    points = []

    # Obtener los puntos de los elementos seleccionados
    for element in selection:
        if isinstance(element, TextNote):
            # Para TextNote, usamos su punto de ubicación
            location = element.Coord
            points.extend([location, location])  # Añadimos dos veces para crear un "bounding box" mínimo
        else:
            # Para otros elementos, intentamos obtener su bounding box
            bbox = element.get_BoundingBox(None)
            if bbox:
                points.extend([bbox.Min, bbox.Max])

    if points:
        # Crear un bounding box que englobe todos los puntos
        min_point = XYZ(min(p.X for p in points), min(p.Y for p in points), min(p.Z for p in points))
        max_point = XYZ(max(p.X for p in points), max(p.Y for p in points), max(p.Z for p in points))

        # Añadir un pequeño margen al bounding box
        margin = 3  # Unidades en pies, ajusta según sea necesario
        min_point = XYZ(min_point.X - margin, min_point.Y - margin, min_point.Z - margin)
        max_point = XYZ(max_point.X + margin, max_point.Y + margin, max_point.Z + margin)

        # Hacer zoom al bounding box
        uidoc.GetOpenUIViews()[0].ZoomAndCenterRectangle(min_point, max_point)

    else:
        TaskDialog.Show("Error", "No se pudo obtener información de ubicación de los elementos seleccionados.")