__title__ = "Workset controle"
__author__ = "Kamil Pluciennik"
__doc__ = """This script will create 3d views for all worksets. For each views, other worksets will be turned off.
Only for worksharing projects.

1. Open any 3d view 
2. Run"""

__context__ = ["doc-workshared", "active-3d-view" ]



import clr
from math import pi
from Autodesk.Revit.DB import *


from pyrevit import script
from pyrevit import forms
import rpw


from snip._selection import get_selected_elements

uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document



wrk = FilteredWorksetCollector(doc).OfKind(WorksetKind.UserWorkset)
wrk2 = wrk
vname = []
for i in wrk:
    vname.append(i.Name)
# print vname

# v3d = FilteredElementCollector(doc).OfClass(View3D).WhereElementIsNotElementType().ToElements()
# v3dtype = []
# for i in v3d:
#     if i.ViewType.ToString() == "ThreeD":
#     	v3dtype.append(i)
#     # print i.Name
# for j in v3dtype:
#     print j.Name, j.GetTypeId()

type3d = doc.ActiveView.GetTypeId()
new_views = []
views = []
tx = Transaction(doc, 'Create3DView')
tx.Start()
for i in wrk:
    new_view = View3D.CreateIsometric(doc, type3d)
    new_view.Name = i.Name
    views.append(new_view)

for j in views:
    for k in wrk:
        if j.Name == k.Name:
            j.SetWorksetVisibility(k.Id, WorksetVisibility.Visible)
        else:
            j.SetWorksetVisibility(k.Id, WorksetVisibility.Hidden)      
tx.Commit()
