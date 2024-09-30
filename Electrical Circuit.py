import Autodesk.Revit.DB.Electrical

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

electrical_Circuit = doc.ActiveView.GetTableData()
section = Autodesk.Revit.DB.Electrical.PanelScheduleData.GetSectionData(schedule,1)
tableData = section.GetCellCalculatedValue(section)
tableCellName = Autodesk.Revit.DB.TableCellCalculatedValueData.GetName(tableData)
print(tableCellName)

tableName = schedule.GetCellText(SectionType.Header,0,0)
qty = schedule.GetCalculatedValueText(SectionType.Body,4,1)
calcValName = schedule.GetCalculatedValueName(SectionType.Body,4,1)
print(tableName)
print("Calculated Qty is: " + qty)
print("Calculated Value Name is: " + calcValName)