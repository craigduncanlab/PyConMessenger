# Autotag module 23.7.2024
# The basic idea is that you can set up a data variable first, then tell the 
# HTML preprocessor to turn any line that starts with one of those variables into the class of tag that is preset.  This will create XML and process into HTML
# This actually turns out to be a very useful way to avoid manual marking up but achieve same effect,
# especially if there are patterns in the text

from np import htmltagmaker

global autotagstate
global matchlistdict
global htmlclass
global secondhtmlclass
global caseoption

def initialise():
	global autotagstate
	global autosplitstate
	global matchlistdict
	global splitmatchlistdict
	global htmlclass
	global caseoption
	global firstsplitclass
	global secondsplitclass
	global matchedfirsttag
	autotagstate=""
	autosplitstate=""
	matchlistdict=dict()
	splitmatchlistdict=dict()
	htmlclass=""
	caseoption=dict()
	firstsplitclass=""
	secondsplitclass=""
	matchedfirsttag=""

def setAutoTagging(myinput):
	global autotagstate
	autotagstate=myinput

def getAutoTagging():
	global autotagstate
	return autotagstate

def setAutoSplitTagging(myinput):
	global autosplitstate
	autosplitstate=myinput

def getAutoSplitTagging():
	global autosplitstate
	return autosplitstate

def setAutotagMatchList(myinput,myclass):
	global matchlist
	matchlist=myinput
	global matchlistdict
	matchlistdict[myclass]=matchlist
	setAutotagClass(myclass)

# use shared dictionary for first match?
def setAutotagSplitMatchList(myinput,myclass):
	global matchlist
	matchlist=myinput
	global matchlistdict
	matchlistdict[myclass]=matchlist
	setAutoSplitClass(myclass)
	"""
	global splitmatchlist
	splitmatchlist=myinput
	global splitmatchlistdict
	splitmatchlistdict[myclass]=splitmatchlist
	setAutoSplitClass(myclass)
	"""

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

def setAutoSplitClass(myinput):
	global firstsplitclass
	firstsplitclass=myinput

def getAutoSplitClass():
	global firstsplitclass
	return firstsplitclass

def setSecondtagClass(myinput):
	global secondsplitclass
	secondsplitclass=myinput

def getSecondtagClass():
	global secondsplitclass
	return secondsplitclass

def setMatchedFirstTag(myinput):
	global matchedfirsttag
	matchedfirsttag=myinput

def getMatchedFirstTag():
	global matchedfirsttag
	return matchedfirsttag

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
			setMatchedFirstTag(startstring)
			return True

		if caseMatch==False and w.lower()==startstring.lower():
			setMatchedFirstTag(startstring)
			return True
	return False

def makeXMLForLine(myinput):
	tagclass=getAutotagClass()
	content=myinput
	output=htmltagmaker.getSimpleXMLtag(tagclass,content)
	return output

def makeXMLforSplitLine(myinput):
	output=""
	tagclass=getAutoSplitClass()
	Secondtagclass=getSecondtagClass()
	matchword=getMatchedFirstTag()
	mysplits=myinput.split(matchword)
	content=""
	balance=""
	if (len(mysplits)<2):
		output=makeXMLForLine(myinput)
		return output
	
	else:
		#print(mysplits)
		content=mysplits[0] # if you use the first few several characters of a line for split, there is still an entry in the array, but it's empty
		balance=mysplits[1]
		if (len(content)==0 and len (balance)==0):
			print(content,len(content))
			print(balance,len(balance))
			print("Autotagsplit\n Trouble with splitting this line into two parts:",myinput)
			print("matchword:",matchword)
			print("first class",tagclass)
			print("second class",Secondtagclass)
			exit() 
		if (len(content)==0 and len (balance)>0):
			content=matchword # keeps the splitting word
			output1=htmltagmaker.getSimpleXMLtag(tagclass,content)
			output2=htmltagmaker.getSimpleXMLtag(Secondtagclass,balance)
			output=output1+output2
			
			return output
		else:
			print("Unknown error in splitting for:",myinput)
			exit()

def handleTagSettings(myargs,optionlist):
	setAutoSplitTagging(True) # On=True # set autotagging options
	replaceclass=myargs[1]

	setAutotagSplitMatchList(optionlist,replaceclass)
	#autotag.setAutotagClass(replaceclass)
	if (len(myargs)>3):
		caseoption=myargs[3]
		setCaseOption(replaceclass,caseoption)
	else:
		setCaseOption(replaceclass,"no")
	if (len(myargs)>2):
		replaceclass2=myargs[2]
		setAutoSplitClass(replaceclass)
		setSecondtagClass(replaceclass2) # no match is needed, due to splitting
	if len(optionlist)>0:
		print("Successfully installed autotag split options")
		"""
		rc=getAutoSplitClass()
		sc=getSecondtagClass()
		print("replace class:",rc)
		print("second class:",sc)
		exit()
		"""