template_name = "cwd-kpl"

__title__ = "Parallel section"
__author__ = "Kamil Pluciennik"
__doc__ = """Create section parallel to selected pipe, duct or cable tray.
Alt + click will open script in file explorer. Please set up your private template name (1st line in script), 
"""


import clr
import Autodesk.Revit.DB as DB
from Autodesk.Revit.DB import *
# from Autodesk.Revit.DB.Architecture import *
# from Autodesk.Revit.DB.Analysis import *


uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document
clr.AddReference("System")
from System.Collections.Generic import List as cList

# from Autodesk.Revit.UI import *

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
if len(selection):
    s0 = selection[0]



out=FilteredElementCollector(doc).OfClass(ViewFamilyType).WhereElementIsElementType().ToElements()
bb = s0.get_BoundingBox(doc.ActiveView)

minZ = bb.Min.Z
maxZ = bb.Max.Z
lc=s0.Location
line = lc.Curve

p = line.GetEndPoint(0)
q = line.GetEndPoint(1)
v = q - p

if v.Z == 0:
	pass
else:
	v = XYZ(v.X, v.Y, 0)


v=XYZ(v.X, v.Y, 0) ##z = 0 for pipes with slope

w = bb.Max.X - bb.Min.X
d = bb.Max.Y - bb.Min.Y
h = bb.Max.Z - bb.Min.Z

try:
    offset = s0.Diameter
except:
    offset = s0.Width

if w < 10:
	w = 10
if d < 10 :
	d = 10

min = XYZ(-w, -6.5, -offset)
max = XYZ(w, 6.5, offset)

midpoint = p + 0.5*v
walldir = -v.Normalize()
up = XYZ.BasisZ
viewdir = walldir.CrossProduct(up)

t = Transform.Identity
t.Origin = midpoint
t.BasisX = walldir
t.BasisY = up
t.BasisZ = viewdir

sectionbox = BoundingBoxXYZ()
sectionbox.Transform = t
sectionbox.Min = min
sectionbox.Max = max

sec = []
for i in out:
	 if i.ViewFamily.ToString() == "Section":
		sec.append(i)
		
#create section
tx = Transaction(doc)
tx.Start("Section create")
newsection = ViewSection.CreateSection(doc, sec[0].Id, sectionbox)
tx.Commit()

#apply template to new section
tx = Transaction(doc, "Set template")
try:
	out=FilteredElementCollector(doc).OfClass(View).WhereElementIsNotElementType().ToElements()
	for i in out:
		if i.Name == template_name:
			template = i

	tx.Start()

	newsection.ViewTemplateId = template.Id

except:
	pass

tx.Commit()

#open newly created view
uidoc.ActiveView = newsection

#remove selection from UI
ids = []
sel = cList[ElementId](ids)
uidoc.Selection.SetElementIds(sel)

#set UIView
for uv in uidoc.GetOpenUIViews():
	if uv.ViewId.Equals( doc.ActiveView.Id ):
		uiview = uv
		break
		

#assign
# bb = s0.get_BoundingBox(newsection)
# min = bb.Min
# max = bb.Max
uiview.ZoomToFit()