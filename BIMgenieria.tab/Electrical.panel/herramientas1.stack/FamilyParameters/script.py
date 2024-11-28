# -*- coding: utf-8 -*-
__title__= "Family Parameters" #Name of the button displayed in Revit UI
__doc__= """ Only works on family editor 
    Create electrical parameters in families.
""" #Description of the button displayed in Revit UI

# pyRevit Extra MetaTags (optional)
__author__= "Antonio Rojas"

#IMPORTS
#---------------------------------------------------------------
import os, sys, datetime                                    #Regular imports

import pyrevit.revit.db.query
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

# Verificar si estamos en el editor de familias
if not doc.IsFamilyDocument:
    TaskDialog.Show("Error", "Este script solo funciona en el Editor de Familias")
    raise SystemExit

# Iniciar transacción
t = Transaction(doc, "Create Electrical Parameters")
t.Start()

try:
    # Definir los parámetros a crear
    parameters_to_create = [
        {
            "name": "Number of Poles",
            "type": ParameterType.NumberOfPoles,
            "group": BuiltInParameterGroup.PG_ELECTRICAL
        },
        {
            "name": "Load Classification",
            "type": ParameterType.LoadClassification,
            "group": BuiltInParameterGroup.PG_ELECTRICAL
        },
        {
            "name": "Voltage",
            "type": ParameterType.ElectricalPotential,
            "group": BuiltInParameterGroup.PG_ELECTRICAL
        },
        {
            "name": "Apparent Load",
            "type": ParameterType.ElectricalApparentPower,
            "group": BuiltInParameterGroup.PG_ELECTRICAL
        },
        {
            "name": "Power Factor",
            "type": ParameterType.Number,
            "group": BuiltInParameterGroup.PG_ELECTRICAL
        },
        {
            "name": "Load Sub-Classification Motor",
            "type": ParameterType.YesNo,
            "group": BuiltInParameterGroup.PG_ELECTRICAL
        }
    ]

    # Obtener el manager de parámetros de familia
    family_manager = doc.FamilyManager

    # Crear cada parámetro
    for param in parameters_to_create:
        try:
            # Verificar si el parámetro ya existe
            existing_param = family_manager.get_Parameter(param["name"])

            if existing_param is None:
                # Crear el parámetro si no existe
                family_manager.AddParameter(
                    param["name"],
                    param["group"],
                    param["type"],
                    True  # True para parámetros de Type
                )
                print("Parámetro creado: " + param["name"])
            else:
                print("El parámetro ya existe: " + param["name"])

        except Exception as param_error:
            print("Error al crear el parámetro {}: {}".format(
                param["name"],
                str(param_error)
            ))

    t.Commit()
    TaskDialog.Show("Success", "Parámetros creados exitosamente")

except Exception as e:
    t.RollBack()
    TaskDialog.Show("Error", "Error al crear los parámetros: " + str(e))



#CODE ENDS HERE
#---------------------------------------------------------------