import clr
import Autodesk.Revit.DB as DB
from Autodesk.Revit.DB import *

uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document


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
if len(selection):
    s0 = selection[0]


__doc__ = """Toggle leader of the tag.
"""
__title__ = "Toggle leader"

tx = Transaction(doc, 'default')
tx.Start()

for i in selection:
    if i.HasLeader == True:
        i.HasLeader = False
    else:
        i.HasLeader = True

tx.Commit()