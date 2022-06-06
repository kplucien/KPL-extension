import os
from distutils.command.sdist import sdist
import rpw
from pyrevit import forms, script
from pyrevit import script

# get the name of the computer user
import getpass as gt
login = gt.getuser() 

#ask about template name and save this variable in config file
config = script.get_config()
config.filelocation = "C:\Users\{}\AppData\Roaming\pyRevit-Master\extensions\KPl.extension\KPl.tab\DevTools.panel\Test.pushbutton".format(login)
config.template_name = forms.ask_for_string(
        default = 'cwd-kp',
        prompt = 'Enter your template name',
        title = 'Template'
    )
script.save_config()