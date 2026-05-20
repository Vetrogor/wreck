from compiler import *
#Your module folder to export compiled files:
export_dir = "c:/Games/Mount&Blade Warband/Modules/Native/"


###################################
#   W.R.E.C.K. Compiler Options   #
###################################



# Change this line to select where compiler will generate ID_* files. Use None instead of the string to completely suppress generation of ID_* files.
# ONLY DO THIS WHEN YOU HAVE COMPLETELY REMOVED ID_* FILE DEPENDENCIES IN MODULE SYSTEM!

write_id_files = "ID_%s.py"     # default vanilla-compatible option
#write_id_files = "ID/ID_%s.py" # will put ID_* files in ID/ subfolder of module system's folder
#write_id_files = None          # will suppress generation of ID_*.py files



# Set to True to display compiler performance information at the end of compilation. Set to False to suppress.

show_performance_data = False   # default: false



##########################
#   W.R.E.C.K. Plugins   #
##########################



import plugin_ms_extension
#import plugin_item_factions_limit_remover
import plugin_presentations

#Plugins from `systems` subfolder are loaded automatically
from systems import *