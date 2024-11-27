# -*- coding: utf-8 -*-
__title__= "Caida de Tensión" #Name of the button displayed in Revit UI
__doc__= """ Calcula la caida de tensión de todos los circuitos
del proyecto y almacena la información en un parámetro.

alt+clic
Inputs:
Calibre del conductor : Texto

Output:
Caida de tensión : Número
    
    Para editar el .dyn y colocar los parámetros de input y output. 

""" #Description of the button displayed in Revit UI

# pyRevit Extra MetaTags (optional)
__author__= "Antonio Rojas"

#IMPORTS
#---------------------------------------------------------------
import os, sys, datetime                                    #Regular imports
import json
import codecs

import pyrevit.revit.db.query
from Autodesk.Revit import DB
from Autodesk.Revit.DB import *                             #Import DB Classes
from Autodesk.Revit.UI import *                             #Import UI Classes
from Autodesk.Revit.DB.Electrical import  *                 #Import discipline modules


#pyRevit Imports
from pyrevit import forms, revit, script, coreutils

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

#GLOBAL VARIABLES
output = script.get_output()

#FUNCTIONS
#---------------------------------------------------------------


#CLASSES
#---------------------------------------------------------------


#MAIN
#---------------------------------------------------------------
#CODE START HERE
#EXPLICA AL USUARIO EL USO DEL SCRIPT

res = forms.alert("Caida de tensión por el método de sección transversal."
                  "\n\n"
                  "Selecciona los parámetros\n"
                  "necesarios para el cálculo:\n\n"
                  "-Calibre AWG del conductor\n"
                  "     Parámetro tipo texto\n\n"
                  
                  "-Caida de tensión\n"
                  "     Parámetro tipo número",
                  options=["Continuar",
                           "Fórmulas usadas",
                            "Tabla de conductores",
                           "Cancelar"])
if res == "Continuar":
    #COMPRUEBA LA EXISTENSIA DEL .JSON
    datafile = script.get_document_data_file("Caida_Tension_Seccion_Transversal", "json")


    if datafile and os.path.exists(datafile) :
        # Si el archivo existe, cargar los datos
        with open(datafile, 'r') as f:
            param_config = json.load(f)
    else:
        # Si no existe, inicializar los datos y crear el archivo
        calibre_fase = cond_por_fase = caida_tension = None
        param_config = {"Calibre AWG del conductor": calibre_fase,
                        "Caida de tension": caida_tension
                        }

        # Crear el archivo y guardar los datos iniciales
        with open(datafile, 'w') as f:
            json.dump(param_config, f)

    #SELECCIONAMOS EL PRIMER ELECTRICAL CIRCUIT DISPONIBLE EN EL MODELO PARA PODER SELECCIONAR
    #LOS PARÁMETROS DE DICHA CATEGORÍA

    collector = DB.FilteredElementCollector(doc).OfClass(DB.Electrical.ElectricalSystem)
    first_circuit = collector.FirstElement()


    #PREGUNTA AL USUARIO POR EL PARÁMETRO CALIBRE DE FASE
    calibre_fase = forms.select_parameters(
        first_circuit,
        title='Calibre de fase',
        multiple=False,
        include_instance=True,
        include_type=True
    )


    #PREGUNTA AL USUARIO POR EL PARÁMETRO CAIDA DE TENSIÓN
    caida_tension = forms.select_parameters(
        first_circuit,
        title='Caida de Tensión',
        multiple=False,
        include_instance=True,
        include_type=True
    )

    param_config = {
        "Calibre de fase": unicode(calibre_fase.name),
        "Caida de tension": unicode(caida_tension.name)
    }




    #ESCRIBE LA INFORMACIÓN EN EL ARCHIVO DE CONFIGURACIÓN
    try:
        with codecs.open(datafile, 'w', encoding="utf-8") as f:
            json.dump(param_config, f,  ensure_ascii=False, indent=4)
    except Exception as e:
        print("Error: Fail to write .json file")
        sys.exit()

    #IMPRIME UNA CONFIRMACIÓN DEL SCRIPT
    output.print_md("### Configuración guardada")
    for key, value in param_config.iteritems():
        print(u"{}: {}".format(key, value))


elif res =="Fórmulas usadas":
    output.print_md("# Fórmulas utilizadas")

    output.print_md("## Circuito Monofásico")
    print("""2 hilos, Fase - Neutro
    %e = (4 * L * In) / (Efn * S)""")

    output.print_md("## Circuito Monofásico 3 hilos (Bifásico)")
    print("""%e = (2 * L * In) / (Efn * S)""")

    output.print_md("## Circuito Trifásico")
    print("""3 Fases, 4 hilos
    %e = (2 * √3 * L * In) / (Eff * S)""")

    output.print_md("###Donde")
    print("""%e: Caída de tensión en porcentaje.
        L: Longitud del conductor (metros).
        In: Corriente nominal (Amp.).
        S: Sección transversal del cable, área en milímetros cuadrados sacada de las tablas de la NOM
        Efn: Tensión del sistema fase-neutro (Volts).
        Eff: Tensión del sistema entre fases (Volts).""")

    sys.exit()

elif res == "Tabla de conductores":
    data = [
        [14, 2.08, 0.19, 0.24, 10.2, 10.2, 10.2, '-', '-', '-'],
        [12, 3.31, 0.177, 0.223, 6.6, 6.6, 6.6, '-', '-', '-'],
        [10, 5.26, 0.164, 0.207, 3.9, 3.9, 3.9, '-', '-', '-'],
        [8, 8.37, 0.171, 0.213, 2.56, 2.56, 2.56, '-', '-', '-'],
        [6, 13.3, 0.167, 0.21, 1.61, 1.61, 1.61, 2.66, 2.66, 2.66],
        [4, 21.2, 0.157, 0.197, 1.02, 1.02, 1.02, 1.67, 1.67, 1.67],
        [2, 33.6, 0.148, 0.187, 0.62, 0.66, 0.66, 1.05, 1.05, 1.05],
        ['1/0', 53.49, 0.144, 0.18, 0.39, 0.43, 0.39, 0.66, 0.69, 0.66],
        ['2/0', 67.43, 0.141, 0.177, 0.33, 0.33, 0.33, 0.52, 0.52, 0.52],
        ['3/0', 85.01, 0.138, 0.171, 0.253, 0.269, 0.259, 0.43, 0.43, 0.43],
        ['4/0', 107.2, 0.135, 0.167, 0.203, 0.22, 0.207, 0.33, 0.36, 0.33],
        [250, 127, 0.135, 0.171, 0.171, 0.187, 0.177, 0.279, 0.295, 0.282],
        [300, 152, 0.135, 0.167, 0.144, 0.161, 0.148, 0.233, 0.249, 0.236],
        [350, 177, 0.131, 0.164, 0.125, 0.141, 0.128, 0.2, 0.217, 0.207],
        [400, 203, 0.131, 0.161, 0.108, 0.125, 0.115, 0.177, 0.194, 0.18],
        [500, 253, 0.128, 0.157, 0.089, 0.105, 0.095, 0.141, 0.157, 0.148],
        [600, 304, 0.128, 0.157, 0.075, 0.092, 0.082, 0.118, 0.135, 0.125],
        [750, 380, 0.125, 0.157, 0.062, 0.079, 0.069, 0.095, 0.112, 0.102],
        [1000, 507, 0.121, 0.151, 0.049, 0.062, 0.059, 0.075, 0.089, 0.082],
    ]
    output.print_table(table_data=data,
                       title="Tabla de conductores",
                       columns=["AWG/kCM", "mm2",
                                "Aluminio", "Acero",
                                "PVC", "Aluminio", "Acero",
                                "PVC", "Aluminio", "Acero"],
                       formats=["", "{} mm2",
                                "", "",
                                "", "", "",
                                "", "", ""]
                      )

    sys.exit()

elif res == "Cancelar":
            sys.exit()


#CODE ENDS HERE
#---------------------------------------------------------------




