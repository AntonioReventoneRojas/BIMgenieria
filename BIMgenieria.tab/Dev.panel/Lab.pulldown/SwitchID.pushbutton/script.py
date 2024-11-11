# -*- coding: utf-8 -*-
__title__= "WIP_Switch ID" #Name of the button displayed in Revit UI
__doc__= """Version 1.0
Description:
Rename switch ID's of selected Lighting Fixtures 
a...z , aa...zz , aaa...zzz and so on
""" #Description of the button displayed in Revit UI

# pyRevit Extra MetaTags (optional)
__author__= "Antonio Rojas"

# Importar librerías necesarias
from pyrevit import forms
from pyrevit import revit, DB


# Definir la categoría deseada
def get_elements_by_category(category_name):
    # Obtener el documento activo
    doc = revit.doc
    # Obtener la categoría a partir del nombre
    category = DB.Category.GetCategory(doc, category_name)

    # Comprobar si la categoría es válida
    if category is None:
        forms.alert("La categoría no se encontró.")
        return []

    # Crear un filtro para obtener los elementos de la categoría
    filter = DB.ElementCategoryFilter(category.Id)

    # Obtener todos los elementos de la categoría
    elements = DB.FilteredElementCollector(doc).WherePasses(filter).ToElements()

    return elements


# Llamar a la función y obtener elementos de una categoría específica
category_name = OST_LightingDevices  # Cambia esto por la categoría deseada
elements = get_elements_by_category(category_name)

# Imprimir los IDs de los elementos encontrados
for element in elements:
    print("Element ID:", element.Id)