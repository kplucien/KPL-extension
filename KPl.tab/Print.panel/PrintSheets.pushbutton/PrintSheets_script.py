"""Print selected sheets. Titleblock should match witl list in preferences of printer settings"""

__title__ = "Print sheets"
__author__ = 'Kamil Pluciennik'
__context__ = 'Sheets'

printer_name = "PDF-XChange Lite"
default_path = "D:\\_project plots\\"

	# these commands get executed in the current scope
# of each new shell (but not for canned commands)

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

current_time = datetime.datetime.now()
subfolder = current_time.strftime("%y%m%d") + "_" + current_time.strftime("%H%M")
file_path = default_path+"\\"+doc.Title+"\\"+subfolder+"\\"
if os.path.exists(file_path):
    pass
else:
    os.mkdir(file_path)

# doc.PrintManager.SelectNewPrintDriver(printer_name)
pm = doc.PrintManager
settings = pm.PrintSetup.CurrentPrintSetting
ps_delete = []
delete_ids = []
paper_center = PaperPlacementType.Center

pp_is=pm.PrintSetup.InSession.PrintParameters
# pp_cps=pm.PrintSetup.CurrentPrintSetting.PrintParameters

pm.SelectNewPrintDriver(printer_name)

result = []
not_printed = []
paper_sizes = [] #variable, where all paper sizes from printer are collected
paper = 'default value'
for i in pm.PaperSizes:
	paper_sizes.append(i)

for k in paper_sizes:
        if k.Name.ToString() == "4A0":
            paper_max = k

dict= {
	"148x210":"A5", "210x297":"A4", "297x420":"A3", "420x594":"A2", "594x841":"A1", "841x1189":"A0", "841x1399":"A0+1", "841x1609":"A0+2", "841x1819":"A0+3", 
    "841x2029":"A0+4", "841x2239":"A0+5", "841x2449":"A0+6","1189x1682":"2A0", "1682x2378":"4A0", "594x1051":"A1+1", "594x1261":"A1+2", "594x1471":"A1+3", 
    "594x1681":"A1+4", "594x1891":"A1+5", "594x2101":"A1+6", "420x804":"A2+1", "420x1014":"A2+2", "420x1224":"A2+3", "420x1434":"A2+4", "420x1644":"A2+5", 
    "420x1854":"A2+6"
    }
	

a = 0

tx = Transaction(doc)
tx.Start("Printing PDF")
for i in selection:

    py1 = i.Outline.Max.V*304.8
    py2 = i.Outline.Min.V*304.8
    px1 = i.Outline.Max.U*304.8
    px2 = i.Outline.Min.U*304.8
    sh_x = int(px1-px2+0.5)
    sh_y = int(py1-py2+0.5)
    tb_dim = str(sh_y)+"x"+str(sh_x)
    try:
        paper_format = dict[tb_dim]
    except:
        TaskDialog.Show('RevitPythonShell', "Paper size not found in printer settings")
        break
        # __window__.Close()

    for j in paper_sizes:
        if paper_format == j.Name.ToString():
            paper = j


    try:
        pm.PrintSetup.Delete()
    except:
        pass


    sh_number = i.LookupParameter("Sheet Number").AsString()
    sh_name = i.LookupParameter("Sheet Name").AsString()


    settings.PrintParameters.PaperPlacement = PaperPlacementType.Center
    settings.PrintParameters.ZoomType = ZoomType.Zoom
    settings.PrintParameters.Zoom=100
    settings.PrintParameters.ViewLinksinBlue = False
    settings.PrintParameters.HideReforWorkPlanes = True
    settings.PrintParameters.HideUnreferencedViewTags = True
    settings.PrintParameters.MaskCoincidentLines = False
    settings.PrintParameters.HideScopeBoxes = True
    settings.PrintParameters.HideCropBoundaries = True
    settings.PrintParameters.ReplaceHalftoneWithThinLines = False
    settings.PrintParameters.HiddenLineViews = HiddenLineViewsType.VectorProcessing
    settings.PrintParameters.PageOrientation = PageOrientationType.Landscape
    settings.PrintParameters.PaperSize = paper
    settings.PrintParameters.ColorDepth = ColorDepthType.Color
    pm.PrintRange = PrintRange.Current
    pm.CombinedFile = True
    pm.PrintToFile = True
    pm.PrintToFileName = file_path+sh_number+" - "+sh_name+".pdf" #naming convention
    #pm.PrintToFileName = file_path+sh_number+".pdf" #naming convention
    if os.path.isfile(pm.PrintToFileName):
        os.remove(pm.PrintToFileName)

    pm.PrintSetup.CurrentPrintSetting = settings
    save_name = str(paper_format+"_"+str(random.randint(0,1000000)))

    
    ps_delete.append(save_name) #collect print setups, which needs to be deleted
    

    pm.PrintSetup.SaveAs(save_name) #generate name for temporary print setup
    pm.Apply()

    
    if (doc.PrintManager.PrintSetup.CurrentPrintSetting.PrintParameters.PaperSize.Name.ToString() == paper.Name.ToString()) and (pm.PrinterName.ToString() == printer_name):
        result.append(pm.SubmitPrint(i).ToString())
    
    else: #this exception won't work!!: :(
        settings.PrintParameters.PaperSize = paper_max

        pm.PrintSetup.SaveAs("4A0 "+str(random.randint(0,1000000)))
        pm.Apply
        pm.SubmitPrint(i)
        not_printed.append(sh_number)


    print sh_number
    print ("In session: "+pm.PrintSetup.InSession.PrintParameters.PaperSize.Name)
    print ("Current print settings: " + pm.PrintSetup.CurrentPrintSetting.PrintParameters.PaperSize.Name)
    print ("Document: " +doc.PrintManager.PrintSetup.CurrentPrintSetting.PrintParameters.PaperSize.Name)
    print "----"


tx.RollBack()
# tx.Commit()



if result.count("True") == len(selection):
    print ("Task Done! {} sheets printed succesfully".format(len(selection)))
else:
    print "Error in printing following sheets: "
    for i in not_printed:
	print i

path = os.path.realpath(file_path)
os.startfile(path)