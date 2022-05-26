	# these commands get executed in the current scope
# of each new shell (but not for canned commands)
__title__ = "AlignViewportOnSheets"
__author__ = 'Kamil Pluciennik'
__context__ = 'Sheets'

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


from pyrevit import forms

selected_sheet = forms.select_sheets(multiple=False)
z = selected_sheet.GetAllViewports()
vp_origin_ids = []

for j in z:
    vp_origin_ids.append(j)
    vp_origin = doc.GetElement(vp_origin_ids[0])
destination = vp_origin.GetBoxCenter()

vp_ids = []
for x in selection:
	y = x.GetAllViewports()
	for i in y:
		vp_ids.append(i)
vp = []
		
tx = Transaction(doc)
tx.Start("Align viewports")

for i in vp_ids:
    element = doc.GetElement(i)
    element.SetBoxCenter(destination)

tx.Commit()
