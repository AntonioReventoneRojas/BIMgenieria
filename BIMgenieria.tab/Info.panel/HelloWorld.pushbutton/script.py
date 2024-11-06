# -*- coding: utf-8 -*-
__title__ = "Hello pyRevit"
__author__ = "AntonioReventoneRojas"
__doc__ = """This is my own pyRevit toolset to make easier my BIM modelling, design and calculation of MEP projects.

This project started on 2022 and still in development.

New ideas are wellcome. 💡

Author: Ing. Arq. Antonio Rojas
"""


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
print(__doc__)


