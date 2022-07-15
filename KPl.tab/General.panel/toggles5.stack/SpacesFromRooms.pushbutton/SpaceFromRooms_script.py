link_name = "ARCH" 


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
from pyrevit import forms

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

check_spaces = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_MEPSpaces).WhereElementIsNotElementType().ToElements()
if len(check_spaces) != 0:
    TaskDialog.Show("Existing space check", "There are existing spaces in the model. Please remove them to avoid duplicates!")


links = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_RvtLinks).WhereElementIsNotElementType().ToElements()

link = forms.SelectFromList.show(links,
                                multiselect=False,
                                name_attr='Name',
                                button_name='Select link with rooms')

link_doc = link.GetLinkDocument()

levels = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Levels).WhereElementIsNotElementType().ToElements()
rooms = FilteredElementCollector(link_doc).OfCategory(BuiltInCategory.OST_Rooms).WhereElementIsNotElementType().ToElements()

bb_room = []
count = []

tx = Transaction(doc, 'default')
tx.Start()


for room in rooms:
    bb_room = room.ClosedShell.GetBoundingBox()
    bb_room_x = (bb_room.Max.X + bb_room.Min.X)/2
    bb_room_y = (bb_room.Max.Y + bb_room.Min.Y)/2
    space_point = UV(bb_room_x, bb_room_y)

#get room level   
    for level in levels:
        if room.Level.Name == level.Name:
            lvl = level
#Create space
    space = doc.Create.NewSpace(lvl, space_point)
    count.append(space)
 #set space name 
    room_name = room.get_Parameter(BuiltInParameter.ROOM_NAME)
    space.get_Parameter(BuiltInParameter.ROOM_NAME).Set(room_name.AsString())

#set space number
    room_number = room.get_Parameter(BuiltInParameter.ROOM_NUMBER)
    space.get_Parameter(BuiltInParameter.ROOM_NUMBER).Set(room_number.AsString())   
    space_new_name=space.get_Parameter(BuiltInParameter.ROOM_NAME)
    space_new_number= space.get_Parameter(BuiltInParameter.ROOM_NUMBER)
    print "{} - {} was created.".format(space_new_name.AsString(), room_name.AsString())

#assign upper limit
    try:

        for level in levels:
            if room.UpperLimit.Name == level.Name:
                upper_limit = level
                space.UpperLimit = upper_limit
    except:
        pass

#assign limit offset
    for level in levels:
        limit_offset = room.LimitOffset
        space.LimitOffset = limit_offset

#assign base offset
    for level in levels:
        base_offset = room.BaseOffset
        space.BaseOffset = base_offset


tx.Commit()
print "{} spaces were created".format(len(count))

##############