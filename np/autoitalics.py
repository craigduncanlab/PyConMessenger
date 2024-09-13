# Autoitalics module 24.7.2024
# The basic idea is that you can set up a data variable first, then tell the 
# HTML preprocessor to turn any line that starts with one of those variables into the class of tag that is preset.  This will create XML and process into HTML
# This actually turns out to be a very useful way to avoid manual marking up but achieve same effect,
# especially if there are patterns in the text

from np import htmltagmaker

global autotagstate
global matchlistdict
global htmlclass
global caseoption

def initialise():
	global autotagstate
	global matchlistdict
	global htmlclass
	global caseoption
	autotagstate=""
	matchlistdict=dict()
	htmlclass=""
	caseoption=dict()

def setAutoTagging(myinput):
	global autotagstate
	autotagstate=myinput

def getAutoTagging():
	global autotagstate
	return autotagstate

def setAutotagMatchList(myinput,myclass):
	global matchlist
	matchlist=myinput
	global matchlistdict
	matchlistdict[myclass]=matchlist
	setAutotagClass(myclass)

def getMatchList():
	global matchlist
	return matchlist

def getMatchListDict():
	global matchlistdict
	return matchlistdict

def getMatchListOption(myclass):
	global matchlistdict
	if (myclass in matchlistdict.keys()):
		return matchlistdict[myclass]
	else:
		return [] # empty list

def setAutotagClass(myinput):
	global htmlclass
	htmlclass=myinput

def getAutotagClass():
	global htmlclass
	return htmlclass

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

# if any of the match words are found at the start of line, returns True
# case sensitive
def getClassForLine(myinput):
	md=getMatchListDict()
	for m in md.keys():
		wordlist=md[m]
		result=checkClassForLine(wordlist,m,myinput)
		if (result==True):
			return m
	return ""

def checkClassForLine(wordlist,myclass,myline):
	
	caseMatch=getCaseOptionForClass(myclass)
	for w in wordlist:
		wlen=len(w)
		startstring=myline[0:wlen]

		if w==startstring:
			return True

		if caseMatch==False and w.lower()==startstring.lower():
			return True
	return False

def makeXMLForLine(myinput):
	tagclass=getAutotagClass()
	content=myinput
	output=htmltagmaker.getSimpleXMLtag(tagclass,content)
	return output

