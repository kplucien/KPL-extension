import clr
import Autodesk.Revit.DB as DB
from Autodesk.Revit.DB import *
from Autodesk.Revit.DB.Architecture import *
from Autodesk.Revit.DB.Analysis import *


import os

if __shiftclick__ == "true": 
	file_path = os.path.realpath(__file__)
	st = "start  notepad.exe "+file_path
	os.system(st)
else:
    pass
