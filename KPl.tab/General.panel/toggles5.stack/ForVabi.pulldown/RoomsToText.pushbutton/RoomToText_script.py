import random
import os
import datetime
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


##################################################
new_curve = []
room_center = []
room_name = []
room_number = []

def collector(category):
	collect = FilteredElementCollector(doc, doc.ActiveView.Id).OfCategory(category).WhereElementIsNotElementType().ToElements()
	return collect
	
wall_cat=BuiltInCategory.OST_Walls
curtain_wall_mullion_cat = BuiltInCategory.OST_CurtainWallMullions
rooms_cat = BuiltInCategory.OST_Rooms

tx = Transaction(doc, 'default')
tx.Start()


##########################################################################
#Text note type creation start

theight = 1.8 #mm
txt_name = "wall_center_line_script"

try:
	text = FilteredElementCollector(doc).OfClass(TextNoteType).FirstElement()
	nowy = text.Duplicate(txt_name)

	txt_size = nowy.get_Parameter(BuiltInParameter.TEXT_SIZE)
	txt_size.Set(theight/304.8)

	txt_color = nowy.get_Parameter(BuiltInParameter.LINE_COLOR)
	txt_color.Set(255)
	txId = nowy.Id

except:
	txt_existing = FilteredElementCollector(doc).OfClass(TextNoteType).ToElements()
	for y in txt_existing:
		if y.LookupParameter("Type Name").AsString() == txt_name:
			txId = y.Id
""" 
nowy.get_Parameter(BuiltInParameter.TEXT_FONT).AsDouble()
nowy.get_Parameter(BuiltInParameter.LINE_COLOR).AsInteger()
nowy.get_Parameter(BuiltInParameter.TEXT_SIZE).AsDouble() """

#Text note type creation end
#############################################


rooms_collected = collector(rooms_cat)

try:
	for i in range(len(rooms_collected)):
		room_center.append(rooms_collected[i].Location.Point)
		room_name.append(rooms_collected[i].get_Parameter(BuiltInParameter.ROOM_NAME).AsString())
		room_number.append(rooms_collected[i].get_Parameter(BuiltInParameter.ROOM_NUMBER).AsString())
		TextNote.Create(doc, doc.ActiveView.Id, room_center[i], room_number[i]+':'+room_name[i], txId)
except:
	print'Something went wrong with placing text notes!'
tx.Commit()
