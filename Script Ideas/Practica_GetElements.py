# -*- coding: utf-8 -*-
__title__= "WIP_Get Elements" #Name of the button displayed in Revit UI
__doc__= """Version 1.0
Description:

""" #Description of the button displayed in Revit UI

# pyRevit Extra MetaTags (optional)
__author__= "Antonio Rojas"

import Autodesk
import pyrevit

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
#Selección en pantalla
seleccion = pyrevit.revit.selection.pick_element("Selecciona un elemento")


#CONSULTA DE PARÁMETROS DE INSTANCIA

"""Se obtiene el nombre del parámetro, ver BuiltInParameter Enumeration 
para encontrar la lista completa de parámetros que se pueden consultar"""
# param_name = Autodesk.Revit.DB.BuiltInParameter.ELEM_FAMILY_AND_TYPE_PARAM

#Obtener el parámetro del elemento seleccionado

#El método get_Parameter se utiliza para obtener SOLO parámetros de instancia
# param = seleccion.get_Parameter(BuiltInParameter.INSTANCE_ELEVATION_PARAM)

#El método LookupParameter es para accesar a parámetros de tipo
# param_2 = seleccion.LookupParameter("Elevation from Level").AsValueString()


#Obtiene el nombre del parámetro como se muestra en la Revit UI
# print("Nombre del parámetro:    {}".format(param.Definition.Name))
# print("Valor del parámetro 2:    {}".format(param_2))
# print(int(param_2)+25)

#Obtiene el valor del parámetro como se muestra en la Revit UI
#Es necesario revisar en con un Snoop como se almacena este parámetro, string, iteger, bool, etc
# print("Value:      {}".format(param_2.AsDouble))
# print("Value:      {}".format(param_2.AsValueString))
# print("Value:      {}".format(param_2.AsString))
# print("Value:      {}".format(param_2.Definition.ParameterType))

#CONSULTA DE PARÁMETROS DE TIPO

#Familias de sistema se accesa por el método GetType
type_ID = seleccion.GetTypeId()
selection_type = doc.GetElement(type_ID)
type_comments = selection_type.LookupParameter("Apparent Load")




print(type(type_ID))
print(type(selection_type))
print(type_comments.AsValueString())
#Familias cargables se accesa por el método Symbol