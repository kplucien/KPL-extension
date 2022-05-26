# family_name = "GE_Frame_A0-A3_CWD"

__title__ = "Select titleblocks from sheets"
__author__ = 'Kamil Pluciennik'
__context__ = 'Sheets'

import clr
import Autodesk.Revit.DB as DB
from Autodesk.Revit.DB import *
from Autodesk.Revit.DB.Architecture import *
from Autodesk.Revit.DB.Analysis import *
from pyrevit import forms

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

tb_all=collector=FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_TitleBlocks).WhereElementIsNotElementType().ToElements()
tb = []
view_sheets_ids = []

family_name = forms.ask_for_string(
    default='GE_Frame_A0-A3_CWD',
    prompt='Titleblock Family Name',
    title='Select titleblocks from sheets'
)

for i in range(len(selection)):
	view_sheets_ids.append(selection[i].Id)
	for j in range(len(tb_all)):
		if tb_all[j].OwnerViewId.ToString() == view_sheets_ids[i].ToString() and tb_all[j].Symbol.FamilyName == family_name:
			tb.append(tb_all[j].Id)
ids = cList[ElementId](tb)
uidoc.Selection.SetElementIds(ids)