# -*- coding: utf-8 -*-
__title__= "Impedancia" #Name of the button displayed in Revit UI
__doc__= """ Calcula la caida de tensión de todos los circuitos
del proyecto y almacena la información en un parámetro.

Configuración inicial ⚙️
Shift + Clic 

Autor: Ing. Arq. Antonio Rojas
""" #Description of the button displayed in Revit UI

# pyRevit Extra MetaTags (optional)
__author__= "Antonio Rojas"

#IMPORTS
#---------------------------------------------------------------
import os, sys, datetime                                    #Regular imports
import json
import math

import pyrevit.revit.db.query
from Autodesk.Revit import DB
from Autodesk.Revit.DB import *                             #Import DB Classes
from Autodesk.Revit.UI import *                             #Import UI Classes
from Autodesk.Revit.DB.Electrical import  *                 #Import discipline modules

#IMPORTACIONES DE LIRERIAS PERSONALIZADAS
# from Snippets._electrical_utilities import *

#pyRevit Imports
from pyrevit import forms, revit, script

#.NET Imports
import clr
clr.AddReference('System')
from System.Collections.Generic import List

#VARIABLES
#---------------------------------------------------------------
doc     = __revit__.ActiveUIDocument.Document       #type: Document
uidoc   = __revit__.ActiveUIDocument                #type: UIDocument
from Autodesk.Revit.ApplicationServices import *
app     = __revit__.Application                     #type: Application
active_view = doc.ActiveView                        #Get current view
path_scrypt = os.path.dirname(__file__)             #Absolute path to folder where sript is ocated
output = script.get_output()

#FUNCTIONS
#---------------------------------------------------------------
def calcular_corriente_nominal(fases, carga_instalada, voltage):
    """Calcula la corriente de nominal."""
    if fases == 1:
        corriente_nominal = carga_instalada / (voltage * 0.9)
    elif fases == 2:
        corriente_nominal = carga_instalada / (2 * voltage * 0.9)
    elif fases == 3:
        corriente_nominal = carga_instalada / (math.sqrt(3) * voltage * 0.9)
    else:
        corriente_nominal = 0

    return corriente_nominal



def seccion_del_conductor(seccion_text):
    # Definir el diccionario
    dict1 = {
        "14": 2.08,
        "12": 3.31,
        "10": 5.26,
        "8": 8.37,
        "6": 13.3,
        "4": 21.2,
        "2": 33.6,
        "1/0": 53.49,
        "2/0": 67.43,
        "3/0": 85.01,
        "4/0": 107.2,
        "250": 127,
        "300": 152,
        "350": 177,
        "400": 203,
        "500": 253,
        "600": 304,
        "750": 380,
        "1000": 507
    }
    # Obtener el valor correspondiente a la clave
    seccion = dict1.get(seccion_text, 1)  # Devuelve "Clave no encontrada" si no existe la clave

    return seccion

def calcular_caida_tension(longitud_circuito,
                           corriente_nominal,
                           voltage_sistema,
                           seccion_conductor,
                           numero_fases):
    # Fórmulas de caída de tensión
    caida_tension_monofasico = (4 * longitud_circuito * corriente_nominal) / (voltage_sistema * seccion_conductor)
    caida_tension_bifasico = (2 * longitud_circuito * corriente_nominal) / (voltage_sistema * seccion_conductor)
    caida_tension_trifasico = (2 * math.sqrt(3) * longitud_circuito * corriente_nominal) / (voltage_sistema * seccion_conductor)

    # Cálculo de la caída de tensión
    if numero_fases == 1:
        caida_tension = caida_tension_monofasico
    elif numero_fases == 2:
        caida_tension = caida_tension_bifasico
    elif numero_fases == 3:
        caida_tension = caida_tension_trifasico
    else:
        caida_tension = 0

    return caida_tension


#CLASSES
#---------------------------------------------------------------


#MAIN
#---------------------------------------------------------------
#CODE START HERE

forms.inform_wip()

#CODE ENDS HERE
#---------------------------------------------------------------