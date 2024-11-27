# -*- coding: utf-8 -*-
#IMPORTS
#---------------------------------------------------------------
from Autodesk.Revit import DB

#pyRevit Imports
from pyrevit import forms, revit, script

#.NET Imports
import clr
clr.AddReference('System')

#VARIABLES
#---------------------------------------------------------------
doc     = __revit__.ActiveUIDocument.Document       #type: Document
uidoc   = __revit__.ActiveUIDocument                #type: UIDocument

#FUNCTIONS
#---------------------------------------------------------------

#CÁLCULO DE CORRIENTE NOMINAL
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


#OBTENER LA SECCIÓN TRANSVERSAL DEL CONDUCTOR
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
    seccion = dict1.get(seccion_text, "Clave no encontrada")  # Devuelve "Clave no encontrada" si no existe la clave

    return seccion