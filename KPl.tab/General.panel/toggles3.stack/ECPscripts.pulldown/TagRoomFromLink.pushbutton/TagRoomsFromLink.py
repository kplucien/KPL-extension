	# these commands get executed in the current scope
# of each new shell (but not for canned commands)
__title__ = "TagRoomsFromLink"
__author__ = 'Kamil Pluciennik'
__context__ = 'Views'

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


links = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_RvtLinks).WhereElementIsNotElementType().ToElements()
from pyrevit import forms
link_name = forms.ask_for_string(
    default='Arch',
    prompt='Link name contain:',
    title='Link name contains'
)

for i in links:
	if i.Name.Contains(link_name):
		link = i
        
link_doc = link.GetLinkDocument()
rooms_id = []
rooms = FilteredElementCollector(link_doc).OfCategory(BuiltInCategory.OST_Rooms).WhereElementIsNotElementType().ToElements()
from Autodesk.Revit.Creation import *
v = doc.ActiveView
tx = Transaction(doc, 'TagRoomFromLink')


tx.Start()
udany = []

for v in selection:
    for j in rooms:
        try:
            p1=UV(j.Location.Point.X, j.Location.Point.Y)
            link_el_id = LinkElementId(link.Id, j.Id)
            udany.append(doc.Create.NewRoomTag(link_el_id, p1, v.Id))
        except:
            continue
tx.Commit()