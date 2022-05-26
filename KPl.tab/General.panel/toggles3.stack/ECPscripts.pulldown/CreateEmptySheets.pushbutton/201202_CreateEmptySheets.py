"""Create empty sheets"""

__title__ = "Create sheets with indicated title block"
__author__ = 'Kamil Pluciennik'
__context__ = 'Title Blocks'

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


count = 3 #amount of sheets to be created
SheetNumber = "new number" #naming convenction
SheetName = "new name"
start_number = 0

import Autodesk.Revit.DB as DB
from Autodesk.Revit.DB import *
from Autodesk.Revit.DB.Architecture import *
from Autodesk.Revit.DB.Analysis import *

uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document

from Autodesk.Revit.UI import TaskDialog
from Autodesk.Revit.UI import UIApplication

tx = Transaction(doc,)
tx.Start("SheetsCreation")
new_sheet = []
for i in range(count):
    new_sheet.append(ViewSheet.Create(doc, s0.GetTypeId()))
    new_sheet[i].Name = SheetName
    new_sheet[i].SheetNumber = SheetNumber+" "+str(i+start_number)
tx.Commit()