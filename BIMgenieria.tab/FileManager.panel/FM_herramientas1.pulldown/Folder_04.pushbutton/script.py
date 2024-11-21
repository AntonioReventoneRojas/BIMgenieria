# -*- coding: utf-8 -*-
__title__= "Folder 4" #Name of the button displayed in Revit UI
__doc__= """Assign shorcuts to folder project or any windows location.
Set a keyboard shortcut (ks) to this button for easy access.

Shift + Clic: Set the path to the button.
""" #Description of the button displayed in Revit UI

# pyRevit Extra MetaTags (optional)
__author__= "Antonio Rojas"

import json

from pyrevit.coreutils import open_folder_in_explorer

__helpurl= ""

#IMPORTS
#---------------------------------------------------------------
import os
import os
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
#List_example = List[ElementId]()



#VARIABLES
#---------------------------------------------------------------
doc     = __revit__.ActiveUIDocument.Document       #type: Document
uidoc   = __revit__.ActiveUIDocument                #type: UIDocument
from Autodesk.Revit.ApplicationServices import *
app     = __revit__.Application                     #type: Application
active_view = doc.ActiveView                        #Get current view
path_scrypt = os.path.dirname(__file__)             #Absolute path to folder where sript is ocated

#GLOBAL VARIABLES
datafile = script.get_document_data_file("FolderShortcuts1", "json")

#FUNCTIONS
#---------------------------------------------------------------


#CLASSES
#---------------------------------------------------------------


#MAIN
#---------------------------------------------------------------
#CODE START HERE
try:
    with open(datafile, "r") as f:
        mod_data = json.load(f)
except:
    mod_data = None

if mod_data:
    path = mod_data.get("F4")
    path = os.path.realpath(path)
    os.startfile(path)
