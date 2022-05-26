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
if len(selection):
    s0 = selection[0]


total_length = 0
len = 0
for i in selection:
	try:
		len = i.get_Parameter(BuiltInParameter.CURVE_ELEM_LENGTH).AsDouble()*304.8
		total_length += len
	except:
		continue
# print str(round(total_length/1000, 3))+" meters"
tl = str(round(total_length/1000, 3))
TaskDialog.Show("Total length of selected elements is: ", "{} m".format(tl))