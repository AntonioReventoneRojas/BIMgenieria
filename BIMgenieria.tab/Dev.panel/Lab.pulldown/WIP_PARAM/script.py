# -*- coding: utf-8 -*-

__title__ = "WIP_Family Parameters"
__author__ = "Antonio Rojas"
__doc__ = """Load"""

import clr
clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import *
import sys

doc = __revit__.ActiveUIDocument.Document

# Verificar la versión de Revit
revit_version = int(doc.Application.VersionNumber)

# Función para cambiar la categoría de la familia
# def change_family_category(doc, new_category_id):
#     with Transaction(doc, "Change Family Category") as t:
#         t.Start()
#         doc.OwnerFamily.FamilyCategory = doc.Settings.Categories.get_Item(new_category_id)
#         t.Commit()

# Función para crear un parámetro
def create_parameter(doc, name,group, parameter_type):
    with (Transaction(doc, "Create Parameter") as t):
        t.Start()
        if revit_version >= 2023:
            fp = doc.FamilyManager.AddParameter
            r(name, group, parameter_type, False)
        else:
            fp = doc.FamilyManager.AddParameter(name, group, getattr(ParameterType, parameter_type), False)
        t.Commit()

# # Cambiar la categoría a Generic Model
# change_family_category(doc, BuiltInCategory.OST_GenericModel)

# Crear parámetros
if revit_version >= 2023:
    create_parameter(doc, "Voltage", GroupTypeId.ElectricalCircuiting , SpecTypeId.ElectricalPotential)
    create_parameter(doc, "Number of Poles", GroupTypeId.ElectricalCircuiting, SpecTypeId.Int.NumberOfPoles)
    create_parameter(doc, "Power Factor", GroupTypeId.ElectricalCircuiting, SpecTypeId.Int.Integer)
    create_parameter(doc, "Load Classification", GroupTypeId.ElectricalCircuiting, SpecTypeId.Reference.LoadClassification)
else:
    create_parameter(doc, "Voltage", "ElectricalPotential", BuiltInParameterGroup.PG_ELECTRICAL)
    create_parameter(doc, "Number of Poles", "NumberOfPoles", BuiltInParameterGroup.PG_ELECTRICAL)
    create_parameter(doc, "Power Factor", "Number", BuiltInParameterGroup.PG_ELECTRICAL)
    create_parameter(doc, "Load Classification", "LoadClassification", BuiltInParameterGroup.PG_ELECTRICAL)

# # Cambiar la categoría a Electrical Fixture
# change_family_category(doc, BuiltInCategory.OST_ElectricalFixtures)

TaskDialog.Show("Script completado", "La familia ha sido modificada exitosamente.")
