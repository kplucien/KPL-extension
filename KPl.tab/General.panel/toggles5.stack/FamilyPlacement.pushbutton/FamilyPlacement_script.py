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
from pyrevit import forms
FamSymbols = FilteredElementCollector(doc).OfClass(FamilySymbol).WhereElementIsElementType().ToElements()
families = []
try:
    for i in FamSymbols:
        families.append(i) 


    res = forms.SelectFromList.show(families,
                                    multiselect=False,
                                    name_attr='Name',
                                    button_name='Select Family')


    uidoc.PromptForFamilyInstancePlacement(res)
except:
    pass

#FamSymbols[0].get_Parameter(BuiltInParameter.SYMBOL_NAME_PARAM).AsString()