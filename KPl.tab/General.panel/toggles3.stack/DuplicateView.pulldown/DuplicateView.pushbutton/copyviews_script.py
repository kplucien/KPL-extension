# dependencies
__context__ = 'Views'
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

    def duplication(self, sender, args):
		name1 = "level 1 system " #new view name template
		amount = self.textBox.Text
		cycle = int(amount) #amount ofcopies

		tx = Transaction(doc)
		tx.Start("DuplicateView")
		i=0
		duplicated = []

		for i in range(cycle):
			duplicated.append(selection[0].Duplicate(ViewDuplicateOption.Duplicate))
			# print "Duplication is done"
		tx.Commit()

		filtered_views = []
		view = FilteredElementCollector(doc).OfClass(View).WhereElementIsNotElementType().ToElements()
		asd = []
		
		if len(duplicated) == cycle:
			TaskDialog.Show("Revit", "{} new views were created".format(cycle))
		else:
			TaskDialog.Show("Revit", "Something went wrong")

		# tx.Start("ViewPlanNameChange")

		# for i in range(len(duplicated)):
		# 	asd.append(doc.GetElement(duplicated[i]))
		# for i in range(len(asd)):
		# 	asd[i].Name = name1+str(i)
		# tx.Commit()


# let's show the window (modal)
MyWindow().ShowDialog()
