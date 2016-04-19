import json, requests
import sys
import os
from texttable import Texttable
from datetime import datetime

def get_modules():
	modules_repo = sys.path[0] + '/.modules.json'
	#Check if local modules copy exists
	if os.path.isfile(modules_repo) == True:
		#Get timestamp the file was last updated
		last_update = datetime.fromtimestamp(os.path.getmtime(modules_repo))
		#Check if updated recently
		if ((datetime.now() - last_update).total_seconds() / 60 / 60 / 24) > 7:
			print "Your copy of the module repository is older than 7 days. You should probably run 'mm.py update'."
		#Return installable modules
		with open(modules_repo, 'r') as data_file:    
			return json.load(data_file)
	#Tell user to run 'update' first
	else:
		print "There is no local copy of the module repository. Please run 'mm.py update' first."
		#Exit process
		exit(0)
		
def update():
	url = 'http://viroentertainment.com/data.json'
	resp = requests.get(url=url)
	data = json.loads(resp.text)
	with open(sys.path[0] + '/.modules.json', 'w') as outfile:
		json.dump(data, outfile)

def list():
	#Get installable modules
	modules = get_modules()
	#Create table
	table = Texttable()
	#Set table header
	table.header(['Name', 'Description (short)'])
	#Add each installable module to table
	for module in modules:
		table.add_row([module, modules[module]["description_short"]])
	#show table
	print table.draw()
	
def info(module):
	#Get installable modules
	modules = get_modules()
	if module in modules:
		print module + " - Version " + str(modules[module]["version"])
		print "Author: " + modules[module]["author"]
		print "-"*30
		print str(modules[module]["description_long"])
		print
		print "If you find any issues: " + modules[module]["issues"]
	else:
		print "Module " + module + " not found."

def install(modules):
	for module in modules:
		print "installing " + module
 
def help():
	print "Usage: mm.py [COMMANDS][OPTIONS]"
	print
	table = Texttable()
	table.add_rows([
	['Command', 'Description'], 
	["update", "Update the local copy of the module repository."],
	["list", "List all installable modules with description."],
	["info modulename", "Displays information about a module."],
	["install", "Install one or multiple modules."]
	])
	print table.draw()
	
# get argument list using sys module
if len(sys.argv) > 1:
	if sys.argv[1] == "help":
		help()
	if sys.argv[1] == "update":
		update()
	if sys.argv[1] == "list":
		list()
	if sys.argv[1] == "info":
		if len(sys.argv) < 3:
			print("No module name given.")
		elif len(sys.argv) > 3:
			print("More than one module given.")
		else:
			info(sys.argv[2])
			
	if sys.argv[1] == "install":
		if len(sys.argv) < 3:
			print("No module name given.")
		else:
			modules = sys.argv[2:]
			install(modules)
else:
	help()
		