# -*- coding: utf-8 -*-
__title__= "Get Elements" #Name of the button displayed in Revit UI
__doc__= """Version 1.0
Description:

""" #Description of the button displayed in Revit UI

# pyRevit Extra MetaTags (optional)
__author__= "Antonio Rojas"
__helpurl= ""

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

#FUNCTIONS
#---------------------------------------------------------------


#CLASSES
#---------------------------------------------------------------


#MAIN
#---------------------------------------------------------------
#CODE START HERE

#Parameter
param_fam_id = ElementId(BuiltInParameter.RBS_ELEC_PANEL_NAME)
value_param      = ParameterValueProvider(param_fam_id)

#Evaluator
evaluator = FilterStringEquals()

#Value

user_input = forms.ask_for_string(      #User input value
    title="",
    default="",
    prompt="Enter a value:"
)

value = user_input                      #Save the value


#Rule
#API Documentation says, there is an obsolete method for RVT 2021 or less
rvt_year = int(app.VersionNumber)
if rvt_year >= 2022:
    rule = FilterStringRule(value_param, evaluator, value)
else:
    rule = FilterStringRule(value_param, evaluator, value, False)

#Filter
filter_param = ElementParameterFilter(rule)

#Apply Filter to FEC
element_ids = FilteredElementCollector(doc)\
    .WhereElementIsNotElementType()\
    .WherePasses(filter_param)\
    .ToElementIds()

#Select elements in Revit
uidoc.Selection.SetElementIds(element_ids)


#CODE ENDS HERE
#---------------------------------------------------------------

print("Script done")