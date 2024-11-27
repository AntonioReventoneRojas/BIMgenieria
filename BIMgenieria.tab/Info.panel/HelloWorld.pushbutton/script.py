# -*- coding: utf-8 -*-
__title__ = "Hello pyRevit"
__author__ = "AntonioReventoneRojas"

#IMPORTS
#---------------------------------------------------------------
import os, sys, datetime                                    #Regular imports
from Autodesk.Revit.DB import *                             #Import DB Classes
from Autodesk.Revit.UI import *                             #Import UI Classes
from Autodesk.Revit.DB.Electrical import  *                 #Import discipline modules

#pyRevit Imports
from pyrevit import forms, revit, script
output = script.get_output()


#.NET Imports
import clr
clr.AddReference('System')
from System.Collections.Generic import List

#MAIN
#---------------------------------------------------------------
#CODE START HERE

output.print_md("#BIMgeniería - MEP engeenering tools")
print( """This is my own pyRevit toolset to make easier my BIM modelling, design and calculation of MEP projects.

This project started on 2024 and still in development.

New ideas are wellcome. :hammer_and_pick:

Author: Ing. Arq. Antonio Rojas
""")
output.print_html('<a href="https://www.linkedin.com/in/joseantonioolguinrojas/">LinkedIn :bust_in_silhouette:</a>')
output.print_html('<a href=https://github.com/AntonioReventoneRojas/BIMgenieria">Repositorio de GitHub :card_index_dividers:</a>')
output.print_html('<a href=https://github.com/AntonioReventoneRojas/BIMgenieria/issues">¿Encontraste un Bug? :lady_beetle:</a>')





