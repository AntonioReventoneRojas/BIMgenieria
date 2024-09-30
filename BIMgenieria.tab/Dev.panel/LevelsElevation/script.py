# -*- coding: utf-8 -*-
__title__ = "Add levels elevation" #Name of the button displayed in Revit UI
__doc__   = """This tool will add/update your level name to hace it's elevation"""
__author__ = "Antonio Rojas"
__highlight__ = "new"
__context__ = doc-project

#Imports

#Regular + Autodesk
import math as mt
from Autodesk.Revit.DB import *

#pyRevit
from pyrevit import *

#