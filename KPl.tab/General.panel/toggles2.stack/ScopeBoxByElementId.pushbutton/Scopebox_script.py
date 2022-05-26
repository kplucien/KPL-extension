__title__ = "Scope box by element id"
__author__ = "Kamil Pluciennik"
__doc__ = """This script will create scope box base on element id (pipe, duct etc.).
Make sure, that any 3d view is active
"""

__context__ = ["active-3d-view" ]

# dependencies
import clr
clr.AddReference('System.Windows.Forms')
clr.AddReference('IronPython.Wpf')
import Autodesk.Revit.DB as DB
from Autodesk.Revit.DB import *
from Autodesk.Revit.DB.Architecture import *
from Autodesk.Revit.DB.Analysis import *

uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document

from Autodesk.Revit.UI import TaskDialog
from Autodesk.Revit.UI import UIApplication
from System.Collections.Generic import List as cList

# find the path of ui.xaml
from pyrevit import UI
from pyrevit import script
xamlfile = script.get_bundle_file('ui.xaml')

# import WPF creator and base Window
import wpf
from System import Windows

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

class MyWindow(Windows.Window):
    def __init__(self):
        wpf.LoadComponent(self, xamlfile)

    # @property
    # def user_name(self):
	# 	amount = self.textBox.Text

    # def say_hello(self, sender, args):
    #     UI.TaskDialog.Show(
    #         "Hello World",
    #         "Hello {}".format(self.user_name or 'World')
    #         )

    def scopebox(self, sender, args):
		if len(selection):
			s0 = selection[0]

		# id = 1453626
		id = int(self.elementid.Text)
		offset = int(self.offset.Text)
		offset_ft = offset/304.8

		element = doc.GetElement(ElementId(id))
		if element is not None and doc.ActiveView.ViewType.ToString() == "ThreeD":
			bb_min_x = element.get_BoundingBox(doc.ActiveView).Min.X-offset_ft
			bb_min_y = element.get_BoundingBox(doc.ActiveView).Min.Y-offset_ft
			bb_min_z = element.get_BoundingBox(doc.ActiveView).Min.Z-offset_ft

			bb_max_x = element.get_BoundingBox(doc.ActiveView).Max.X+offset_ft
			bb_max_y = element.get_BoundingBox(doc.ActiveView).Max.Y+offset_ft
			bb_max_z = element.get_BoundingBox(doc.ActiveView).Max.Z+offset_ft

			new_bb = BoundingBoxXYZ()
			new_bb.Max = XYZ(bb_max_x, bb_max_y, bb_max_z)
			new_bb.Min = XYZ(bb_min_x,bb_min_y, bb_min_z)

			tx = Transaction(doc, 'ScopeBox')
			tx.Start()

			doc.ActiveView.SetSectionBox(new_bb)

			ids = []
			ids.append(element.Id)
			sel = cList[ElementId](ids)

			uidoc.Selection.SetElementIds(sel)
			uidoc.ShowElements(sel)
			
			tx.Commit()

		else:
			TaskDialog.Show("Revit", "Id not found or active view is not 3d view")


# let's show the window (modal)
MyWindow().ShowDialog()
