# Autotag module 23.7.2024
# The basic idea is that you can set up a data variable first, then tell the 
# HTML preprocessor to turn any line that starts with one of those variables into the class of tag that is preset.  This will create XML and process into HTML
# This actually turns out to be a very useful way to avoid manual marking up but achieve same effect,
# especially if there are patterns in the text

from np import htmltagmaker

global outertagstate
global tagclass

def initialise():
	global outertagstate
	global tagclass
	outertagstate=False
	outerclass=""

def setOuterTagging(myinput):
	global outertagstate
	outertagstate=myinput

def getOuterTagging():
	global outertagstate
	return outertagstate

def setOutertagClass(myinput):
	global tagclass
	tagclass=myinput

def getOutertagClass():
	global tagclass
	return tagclass

def setCaseOption(myclass,myinput):
	global caseoption
	truelist=["yes","on","true"]
	if myinput.lower() in truelist:
		caseoption[myclass]=True
	else:
		caseoption[myclass]=False

def getCaseOptionForClass(myclass):
	global caseoption
	if (myclass in caseoption.keys()):
		return caseoption[myclass]
	return False

def makeXMLForLine(myinput):
	tagclass=getOutertagClass()
	content=""
	print(myinput)
	exit()
	# remove outer
	if (myinput[0]=="("):
		content=myinput.lstrip("()")
		content=content.rstrip(")")
	if (myinput[0]=="["):
		content=myinput.lstrip("[")
		content=content.rstrip("]")
	output=htmltagmaker.getSimpleXMLtag(tagclass,content)
	return output

def removeOuter(myinput):
	content=myinput
	# remove outer
	if (myinput[0]=="("):
		content=myinput.lstrip("()")
		content=content.rstrip(")")
	if (myinput[0]=="["):
		content=myinput.lstrip("[")
		content=content.rstrip("]")
	output=content
	return output

# checks to see if entire line is quoted at both ends
def checkIsOuter(child):
	dbl='"'
	if (child[0:1]=="(" and child[-1:]==")"):
		return True
	if (child[0:1]=='[' and child[-1:]==']'):
		return True
	return False

# process a double quote line into an XML tag
def processOuter(child):
	newstring=child.strip(dbl)
	newstring=newstring.lstrip('(')
	newstring=newstring.rstrip(')')
	newstring=newstring.lstrip('[')
	newstring=newstring.rstrip(']')
	output=makeXMLForLine(newstring)
	return output

def handleTagSettings(myargs):
	setOuterTagging(True)
	if (len(myargs)>0):
		optionclass=myargs[0]
		setOutertagClass(optionclass)