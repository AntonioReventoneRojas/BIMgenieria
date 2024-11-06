# -*- coding: utf-8 -*-
__title__ = "Hello pyRevit"
__author__ = "AntonioReventoneRojas"
__doc__ = """Hola Revit este es mi primer add-in MEP para Revit desarrollado con pyRevit"""


#IMPORTS
#---------------------------------------------------------------
import os, sys, datetime                                    #Regular imports
from Autodesk.Revit.DB import *                             #Import DB Classes
from Autodesk.Revit.UI import *                             #Import UI Classes
from Autodesk.Revit.DB.Electrical import  *                 #Import discipline modules

#pyRevit Imports
from pyrevit import forms, revit, script

#.NET Imports
import clr
clr.AddReference('System')
from System.Collections.Generic import List

#MAIN
#---------------------------------------------------------------
#CODE START HERE


