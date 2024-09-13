# defaultpara 23.7.2024

from np import htmltagmaker

global defaultparastate
global defaultclass

def initialise():
	global defaultclass
	global isSet
	isSet=False
	defaultclass=""

def setDefaultClass(myinput):
	global defaultclass
	global isSet
	defaultclass=myinput
	isSet=True

def getDefaultClass():
	global defaultclass
	return defaultclass

def getIsDefaultSet():
	global isSet
	return isSet

def handleTagSettings(myargs):
	if (len(myargs)>0):
		optionclass=myargs[0]
		setDefaultClass(optionclass)
		"""
		print("Successfully set a new default para class")
		print(defaultpara.getIsDefaultSet())
		exit()
		"""
