# -*- coding: utf-8 -*-
#========SCRIPT INFO========

__title__ = "Scope Box"
__doc__   = """
Turn off / on the Scope Boxes in current view

Author: Ing. Arq. Antonio Rojas
"""
__author__ = "Antonio Rojas"


#========IMPORTS========
import pyrevit.revit
from  pyrevit import *
from  Autodesk import *

#Regular + Autodesk
import os , sys , datetime , time
from Autodesk.Revit.DB import * #Import everything from DB

#pyRevit
from pyrevit import *
from pyrevit import forms

#.NET Imports
import clr
clr.AddReference("System")

#custom imports (if needed)

#========VARIABLES========
doc     = __revit__.ActiveUIDocument.Document
uidoc   = __revit__.ActiveUIDocument
path_script = os.path.dirname(__file__)

#========FUNCTIONS========


#========CLASSES========



#========MAIN========

# Obtener la vista activa
active_view = doc.ActiveView

# Obtener la categoría de Scope Boxes
scope_boxes_category = doc.Settings.Categories.get_Item(BuiltInCategory.OST_VolumeOfInterest)

# Verificar si la categoría está visible en la vista activa
is_visible = active_view.GetCategoryHidden(scope_boxes_category.Id)

# Iniciar la transacción
t = Transaction(doc, "Toggle Scope Boxes Visibility")
t.Start()

# Cambiar el estado de visibilidad de la categoría
active_view.SetCategoryHidden(scope_boxes_category.Id, not is_visible)

# Finalizar la transacción
t.Commit()


#========OUTPUTS========
