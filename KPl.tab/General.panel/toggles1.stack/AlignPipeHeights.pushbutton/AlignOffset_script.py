from math import pi

import clr
import Autodesk.Revit.DB as DB
from Autodesk.Revit.DB import *
from Autodesk.Revit.DB.Architecture import *
from Autodesk.Revit.DB.Analysis import *

from Autodesk.Revit.DB import Line, InsulationLiningBase
from Autodesk.Revit.UI.Selection import ObjectType, ISelectionFilter
from Autodesk.Revit import Exceptions

from pyrevit import script
from pyrevit import forms
import rpw


__doc__ = """Align pipes offset.
Select first object to be moved.
Select second object which is on desired offset"""
__title__ = "Align pipe heights"

logger = script.get_logger()
uidoc = rpw.revit.uidoc
doc = rpw.revit.doc


def elevation():
    try:
        with forms.WarningBar(title="Pick pipe to be moved"):
            reference = uidoc.Selection.PickObject(ObjectType.Element)
    except:
        pass
    target_element = doc.GetElement(reference)

    try:
        with forms.WarningBar(title="Pick pipe to be aligned to"):
             reference = uidoc.Selection.PickObject(ObjectType.Element)
    except:
        pass
    moved_element = doc.GetElement(reference)
    
    
    tx = Transaction(doc)
    tx.Start("Align offset")

    target_element.LevelOffset = moved_element.LevelOffset
    
    tx.Commit()

while elevation():
    pass