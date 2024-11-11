# # -*- coding: utf-8 -*-
#
# __title__ = "Family Parameters 2023"
# __author__ = "AntonioReventoneRojas"
# __doc__ = """Load"""
#
# import Autodesk.Revit.DB
# # -*- coding: utf-8 -*-
# import clr
#
# clr.AddReference('RevitAPI')
# clr.AddReference('RevitAPIUI')
# from Autodesk.Revit.DB import *
# from Autodesk.Revit.UI import *
#
# doc = __revit__.ActiveUIDocument.Document
#
# parameterName = "Voltage"
# parameterGroup = GroupTypeId.Electrical
# specType = Autodesk.Revit.DB.SpecTypeId.ElectricalPotential
#
# fam_manager = doc.FamilyManager
#
# new_param = fam_manager.AddParameter(parameterName , parameterGroup ,specType , False)

# -*- coding: utf-8 -*-

__title__ = "Family Parameters 2023"
__author__ = "AntonioReventoneRojas"
__doc__ = """Load"""

import clr

clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import *

doc = __revit__.ActiveUIDocument.Document

parameterName = "Voltage"
parameterGroup = GroupTypeId.Electrical  # Grupo de parámetros eléctricos
specType = SpecTypeId.Reference.LoadClassification

fam_manager = doc.FamilyManager

# Iniciar una transacción para modificar el documento
t = Transaction(doc, "Add Family Parameter")
t.Start()

try:
    # Crear el parámetro
    new_param = fam_manager.AddParameter(parameterName, parameterGroup, specType, False)
    t.Commit()  # Confirmar la transacción
except Exception as e:
    t.RollBack()  # Revertir si algo falla
    print("Error:", e)

