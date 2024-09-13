# Autoformat module 12.8.2024
# Store word lists as data variables
# Store the format to use for these variables
# Check each line and use replace to insert relevant HTML formats for words in each list
#
# In documents, use autoformat(Variable,italics,no) etc to request changes
# This is a non-blocking internal swap: it doesn't prevent other auto-tagging at paragraph level

from np import htmltagmaker

global autotagstate
global matchlistdict
global htmlclass
global caseoption
global formatoptions

def initialise():
	global autotagstate
	global matchlistdict
	global htmlclass
	global caseoption
	global formatoptions
	global matchlist
	matchlist=""
	autotagstate=""
	matchlistdict=dict()
	formatoptions=dict()
	htmlclass=""
	caseoption=dict()

def setAutoTagging(myinput):
	global autotagstate
	autotagstate=myinput

def getAutoTagging():
	global autotagstate
	return autotagstate

def setAutotagMatchList(mymatchlist,varname,myformat):
	global matchlistdict
	global formatoptions
	matchlistdict[varname]=mymatchlist
	formatoptions[varname]=myformat
	setAutotagClass(varname)

# redundant if we store each list with the variable name
def getMatchList():
	global matchlist
	return matchlist

def getMatchListDict():
	global matchlistdict
	return matchlistdict

def getFormatOptionDict():
	global formatoptions
	return formatoptions

def getMatchListOption(myclass):
	global matchlistdict
	if (myclass in matchlistdict.keys()):
		return matchlistdict[myclass]
	else:
		return [] # empty list

def getFormatForWords(myclass):
	global formatoptions
	if (myclass in formatoptions.keys()):
		return formatoptions[myclass]
	else:
		return [] # empty list

# This will be a format like bold, italics now (cf autotag.py)
def setAutotagClass(myinput):
	global htmlclass
	htmlclass=myinput

def getAutotagClass():
	global htmlclass
	return htmlclass

def setCaseOption(myclass,myinput):
	global caseoption
	if (myinput==False):
		myinput="no"
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


def handleTagSettings(myargs,optionlist):
	setAutoTagging(True) # On=True # set autotagging options
	#print("myargs",myargs)
	varname=myargs[0] # this is just the name of the variable...
	formatcode=myargs[1]
	setAutotagMatchList(optionlist,varname,formatcode)
	#print("in Autoformat handle Tag I have optionlist,format,varname:",optionlist,formatcode,varname)
	#autotag.setAutotagClass(replaceclass)
	if (len(myargs)>2):
		caseoption=myargs[2]
		setCaseOption(varname,caseoption)
	else:
		setCaseOption(varname,"no")
	if len(optionlist)>0:
		#print("Successfully installed autoformat options")
		"""
		rc=getFormatForWords(varname)
		print("format for words in this class:",rc)
		ml=getMatchListOption(varname)
		print("autoformat matchlist:",ml)
		"""

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

# CUSTOM FUNCTIONS THAT DIFFER FROM AUTOTAG ARE HERE:

# wordlist is the text to be found (may be a list?)
def checkClassForLine(wordlist,myclass,myline):
	#print("Checking class...myline:",myline)
	caseMatch=getCaseOptionForClass(myclass)
	for w in wordlist:
		#print("word:",w)
		wlen=len(w)
		startref=myline.find(w)
		#print("startref:",startref)
		if startref>=0:
			return True

		if caseMatch==False:
			newtext=myline.lower()
			if newtext.find(w.lower())>=0:
				return True

	return False

# at the moment format codes bold, italics etc handles an exact match and formats that part only, 
# if the word 'all' appears in formats then whole line changes
def handleLine(child):

	newline=child
	vv=getVariablesForLine(child)
	recipe=[]
	#print("handleLine:",newline,vv)
	#print("variables:",vv)
	for varname in vv:
		formatcode=getFormatForWords(varname)
		words=getReplaceWordsForVariables(child,varname)
		"""
		print("var in variables:",varname,vv)
		print("I have these words:",words)
		"""
		if ("all" in formatcode):
			for w in words:
				newline=formatLineIfMatch(newline,w,formatcode)
		else:
			
			for w in words:
				newline=replaceWordInLine(newline,w,formatcode)
				"""
				print("Word replacing:",w)
				print("newline:",newline)
				"""
		"""
		if (len(words)>0):
			print("handled line in autoformat")
			print("before:",child)
			print("after:",newline)
		"""
	return newline


def getVariablesForLine(myinput):
	output=[]
	md=getMatchListDict()
	#print(md)
	fd=getFormatOptionDict()
	for m in md.keys():
		wordlist=md[m]
		#print("wordlist:",wordlist)
		#formatoption=fd[m]
		result=checkClassForLine(wordlist,m,myinput)
		#print("myinput:",myinput)
		#print("result:",result)
		if (result==True):
			output.append(m)
	"""
	if (len(output)>0):
		print("variables for line:",output)
	"""
	return output

def getReplaceWordsForVariables(myinput,myvariable):
	output=[]
	md=getMatchListDict()
	wordlist=md[myvariable]
	for w in wordlist:
		if w in myinput:
			output.append(w)
	#print("Replace words for variables:",output)
	return output

def replaceWordInLine(myline,myword,formatcode):
	output=myline
	update=myword
	if ("italic" in formatcode):
		update=italicise(update)
		
	if ("bold" in formatcode):
		update=embolden(update)
		#output=myline.replace(myword,update)
	if ("under" in formatcode or "ulin" in formatcode):
		update=underline(update)
		#output=myline.replace(myword,update)
	output=myline.replace(myword,update)
	
	#print(output)
	#exit()
	
	return output

# 
def formatLineIfMatch(myline,myword,formatcode):
	update=myline
	if (myword in myline):
		if ("italic" in formatcode):
			update=italicise(update)
		if ("bold" in formatcode):
			update=embolden(update)
			#output=myline.replace(myword,update)
		if ("under" in formatcode or "ulin" in formatcode):
			update=underline(update)
	return update

def italicise(myword):
	output="!!"+myword+"!!"
	return output

def embolden(myword):
	output="!*"+myword+"*!"
	return output

def underline(myword):
	output="!_"+myword+"_!"
	return output