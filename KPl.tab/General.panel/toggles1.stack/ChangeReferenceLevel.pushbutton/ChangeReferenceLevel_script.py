	# these commands get executed in the current scope
# of each new shell (but not for canned commands)
import clr
import Autodesk.Revit.DB as DB
from Autodesk.Revit.DB import *
from Autodesk.Revit.DB.Architecture import *
from Autodesk.Revit.DB.Analysis import *

uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document
clr.AddReference("System")
from System.Collections.Generic import List as cList

from Autodesk.Revit.UI import TaskDialog
from Autodesk.Revit.UI import UIApplication
from Autodesk.Revit.UI.Selection import *


def alert(msg):
    TaskDialog.Show('RevitPythonShell', msg)


def quit():
    __window__.Close()
exit = quit


def get_selected_elements(doc):
    """API change in Revit 2016 makes old method throw an error"""
    try:
        # Revit 2016
        return [doc.GetElement(id)
                for id in __revit__.ActiveUIDocument.Selection.GetElementIds()]
    except:
        # old method
        return list(__revit__.ActiveUIDocument.Selection.Elements)
selection = get_selected_elements(doc)
# convenience variable for first element in selection


lvls = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Levels).WhereElementIsNotElementType().ToElements()
lvl_name = []
rvt_lvl = []
lvls_dict  ={}
for i in lvls:
	lvl_name.append(i.Name)
	rvt_lvl.append(i)
for j in range(len(lvl_name)):
    lvls_dict[lvl_name[j]] = rvt_lvl[j]

from rpw.ui.forms import SelectFromList
selected_level = SelectFromList("Select Level", lvls_dict)

tx = Transaction(doc, 'ChangeReferenceLevel')
tx.Start()

for i in selection:
    try:
        i.ReferenceLevel = selected_level
    except:
        try:
            object_param_level = i.get_Parameter(BuiltInParameter.FAMILY_LEVEL_PARAM)
            object_level = doc.GetElement(object_param_level.AsElementId())
            
            object_param_offset = i.get_Parameter(BuiltInParameter.INSTANCE_FREE_HOST_OFFSET_PARAM)
            object_newoffset = object_param_offset.AsDouble() + object_level.Elevation - selected_level.Elevation
            object_param_level.Set(selected_level.Id)
            object_param_offset.Set(object_newoffset)
        except:
            pass

tx.Commit()
