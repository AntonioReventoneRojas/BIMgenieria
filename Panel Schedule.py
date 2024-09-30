import Autodesk.Revit.DB.Electrical

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

# Obtener la selección actual
selection = [doc.GetElement(id) for id in uidoc.Selection.GetElementIds()]

# Verificar si hay elementos seleccionados
if len(selection) > 0:
    # Obtener los parámetros del primer elemento seleccionado
    element = selection[0]

    # Obtener el parámetro "True Load" si existe
    true_load_param = element.LookupParameter("Load Name")

    # Verificar si el parámetro "True Load" existe en el elemento
    if true_load_param:
        # Obtener el valor del parámetro "True Load"
        true_load_value = true_load_param.AsValueString()
        true_load_number = int("".join(filter(str.isdigit, true_load_value)))
        print("Valor de True Load:", true_load_number)
    else:
        print("El elemento seleccionado no tiene un parámetro llamado 'True Load'.")
else:
    print("No hay elementos seleccionados.")

