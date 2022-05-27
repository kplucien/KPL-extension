__title__ = "Review dimension"
__author__ = "Kamil Pluciennik"
__doc__ = """Select dimensions and run this tool. All associated elements will be marked.
"""
__context__ = "Dimensions"

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

##########################################################################
iden = []
for i in selection:
    for s in range(i.References.Size):
        iden.append(i.References[s].ElementId)

##########################################################################


sel = cList[ElementId](iden)
try:

    uidoc.Selection.SetElementIds(sel)
except:
    pass

##########################################################################