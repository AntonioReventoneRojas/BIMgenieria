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
from Autodesk.Revit import DB
from Autodesk.Revit.DB import *                             #Import DB Classes
from Autodesk.Revit.UI import *                             #Import UI Classes
from Autodesk.Revit.DB.Electrical import  *                 #Import discipline modules



#pyRevit Imports
from pyrevit import forms, revit, script

#.NET Imports
import clr


clr.AddReference('System')
clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')
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

# Transacción para crear parámetros
t = Transaction(doc, "Create Electrical Parameters")
t.Start()

try:

    #Revisar la versión de Revit
    version = int(doc.Application.VersionNumber)

    if version <= 2022:
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

#POR AHORA NO ENCUENTRO MANERA DE CREAR EL PARÁMETRO LOAD CLASSIFICATION, NI EL PARÁMETRO LOAD CLASSIFICATION MOTOR
#LA REVIT API NO ESPECIFICA UN SPECTTYPEID PARA ESE TIPO DE PARÁMETROS
    elif version >= 2022:
        # Definir los parámetros a crear
        parameters_to_create = [
            # {
            #     "name": "Number of Poles",
            #     "type": SpecTypeId.Integer,
            #     "group": GroupTypeId.Electrical
            # },
            # {
            #     "name": "Load Classification",
            #     "type": ForgeType.GetTypeId("autodesk.spec.aec:number-2.0.0"),
            #     "group": GroupTypeId.Electrical
            # },
            {
                "name": "Voltage",
                "type": SpecTypeId.ElectricalPotential,
                "group": GroupTypeId.Electrical
            },
            {
                "name": "Apparent Load",
                "type": SpecTypeId.ApparentPower,
                "group": GroupTypeId.Electrical
            },
            {
                "name": "Power Factor",
                "type": SpecTypeId.Number,
                "group": GroupTypeId.Electrical
            },
            # {
            #     "name": "Load Sub-Classification Motor",
            #     "type": SpecTypeId.Boolean,
            #     "group": GroupTypeId.Electrical
            # }
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
                    False  # False para parámetros de tipo
                )
                print("Parámetro creado: " + param["name"])

            else:
                print("El parámetro ya existe: " + param["name"])

        except Exception as param_error:
            print("Error al crear el parámetro {0}: {1}".format(param["name"],str(param_error)))


    t.Commit()
    print("Parámetros creados exitosamente")

except Exception as e:
    t.RollBack()
    print(("Error al crear los parámetros: " + str(e)))



# Transacción para establecer valores
t = Transaction(doc, "Set Parameter Values")
t.Start()

try:
    family_manager = doc.FamilyManager

    # Obtener todas las clasificaciones de carga (Load Classifications) disponibles
    load_classifications = FilteredElementCollector(doc) \
        .OfClass(DB.Electrical.ElectricalLoadClassification) \
        .ToElements()

    # Validar si hay clasificaciones disponibles
    if load_classifications:
        # Tomar la primera clasificación de carga y obtener su Element ID
        first_load_classification = load_classifications[0]
        load_class_element_id = first_load_classification.Id

    #CONVERTIR VOLTAGE A INTERNAL UNITS
    value_voltage = 127
    units = UnitTypeId.Volts
    value_voltage_internal = UnitUtils.ConvertToInternalUnits(value_voltage, units)

    # CONVERTIR POTENCIA APARENTE A INTERNAL UNITS
    value_app_load = 180
    units = UnitTypeId.Watts
    value_app_load_internal = UnitUtils.ConvertToInternalUnits(value_app_load, units)


    # Definir los valores a establecer
    parameter_values = {
        "Number of Poles": 3,
        "Load Classification": load_class_element_id,
        "Voltage": value_voltage_internal,
        "Apparent Load": value_app_load,
        "Power Factor": 0.9,
        "Load Sub-Classification Motor": False
    }

    # Establecer los valores
    for param_name, value in parameter_values.iteritems():
        try:
            param = family_manager.get_Parameter(param_name)
            if param:
                family_manager.Set(param, value)
                # print ("Valor establecido para {0}: {1}".format(param_name, value))
            else:
                print ("No se encontró el parámetro: {0}".format(param_name))
        except Exception as set_error:
            print ("Error al establecer valor para {0}: {1}".format(param_name,str(set_error)))

    t.Commit()
    print ("Valores establecidos exitosamente")

except Exception as e:
    t.RollBack()
    print ("Error al establecer los valores: " + str(e))

#CODE ENDS HERE
#---------------------------------------------------------------