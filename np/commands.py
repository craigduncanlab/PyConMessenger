# Commands parser 2.6.24.  Updated 31.7.24

from np import semantics,wikitable
"""
import np.semantics
import np.wikitable
"""

def initialise():
	global activecommand,activeargs
	activecommand=""
	activeargs=[]

def setActiveCommand(myinput):
	global activecommand
	activecommand=myinput

def getActiveCommand():
	global activecommand
	return activecommand

def setActiveArgs(myinput):
	global activeargs
	activeargs = myinput

def getActiveArgs():
	global activeargs
	return activeargs

# removes both round and square brackets so they will process the same i.e. header[] or header()
def getClean(mydata):
	output=mydata.strip("[")
	output=output.strip("]")
	output=output.strip("(")
	output=output.strip(")")
	output=output.strip(" ") # just this, not - etc
	return output

def getTagComlist():
	output=["image","autotagline","autotagsplit","defaultpara","outertag","pagelinks","autoformat"]	
	return output

# called by npmake.py
def checkCommand(option,myline):
	#print("option:",option," myline:",myline)
	output=False
	commandlist=getMaxCommandsList()
	option=option.lower()
	if (option not in commandlist):
		print("Your option",option," is not in commands.py command list")
		exit()
		# return False
	cmd=getClean(myline).lower()
	g=len(option)
	if (option[0:g].lower() in myline[0:g].lower()):
		"""
		print("found this command:",option)
		dc=checkCommandBrackets(option,myline)
		print(dc)
		if (option=="autotagline"):
			exit()
		"""
		dc=checkCommandBrackets(option,myline)
		if (dc==True):
			return True # only true if left bracket follows
	return output

def checkCommandBrackets(option,myline):
	output=False
	ml=len(option)
	brackets=myline[ml:ml+1]
	#print(option,brackets)
	if (brackets=="(") or brackets=="[":
		return True
	return output

def getArgs(command,mystring):
	#aa=getClean(myArg)
	dd=mystring[len(command)+1:len(mystring)]
	dd=getClean(dd)
	output=""
	argslist=dd.split(",")
	output=[]
	for v in argslist:
		output.append(getClean(v))

	return output


# This assumes the function only supplies named 'data' variable names as args, 
# and that they have been defined in the text file ahead of the function call
# Throws error if this is not correct.

# Test lowercase of input only
def processArgsForCommand(mycom):
	output=[]
	commandlist=getMaxCommandsList() #getTagComlist()
	option=""
	for cc in commandlist:
		prefix=mycom[0:len(cc)]	
		if prefix.lower()==cc.lower():
			option=cc
	d=[]
	counts=[]
	headers=[]
	
	if (option in commandlist):
		output=getArgs(option,mycom)
					
	return output

# used in 
def getMaxCommandsList():
	output1=getAutoTagCommands()	
	output2=getTableCommands()
	output3=getImageCommands()
	output4=getCodeCommands()
	output5=getDataCommands()
	output6=getParagraphOptionCommands()
	output7=getMathCommands()
	output8=getCricketCommands()
	output9=getPrintCommands()
	output10=getEBookCommands()
	output=output1+output2+output3+output4+output5+output6+output7+output8+output9+output10
	return output

# to do: wordcounts info, or stats option
def getAutoTagCommands():
	output=["autotagline","autotagsplit","autoformat","defaultpara","outertag","pagelinks"]	
	return output

def getEBookCommands():
	output=["gutenberg"]
	return output

def getParagraphOptionCommands():
	output=["paragraph"]
	return output

def getCricketCommands():
	output=["cricketsum"]
	return output

def getMathCommands():
	output=["sum","sumacross","rowtotals"]
	return output

def getCodeCommands():
	output=["import"]
	return output

# cf 
def getDataCommands():
	output=["datasplit","header","splits","rip","ripdown","ripacross","dlim","ripname","ripnames","colnames","rownames"]	
	return output

def getPrintCommands():
	output=["print","eprint","lprint","nprint","qprint","tprintrows","cprintrows","codeprint"]
	return output

# cf wikitable.getCOMSlist()
def getTableCommands():
	output=["tablecol","tablerow","tablesplit","tprint","tablecoltotals"]	
	return output

def getImageCommands():
	output=["image"]
	return output

def checkAllCommands(child):
	outputFlag=False
	#tableCommandFlag=wikitable.checkTableCommand(child)
	scl=getMaxCommandsList()
	for cm in scl:
		result=checkCommand(cm,child)
		if (result==True):
			outputFlag=True
			setActiveCommand(cm)
	quoteCheck=checkIsQuote(child)
	if quoteCheck==True and outputFlag==False:
		outputFlag=True	
		setActiveCommand("quote")	
	return outputFlag

def checkForPrefixCommands(child):
	output=False
	setActiveCommand("")
	prefixlist=semantics.getPrefixList()
	for p in prefixlist:
		cap=len(p)
		checkstr=child[0:cap]
		if p==checkstr:
			output=True
			setActiveCommand(p)
	return output

def isTableOrImage():
	active=getActiveCommand()
	tablelist=getTableCommands()
	imagelist=getImageCommands()
	checks=tablelist+imagelist
	for mystring in checks:
		if (active==mystring):
			return True
	return False

# checks to see if entire line is quoted at both ends
def checkIsQuote(child):
	start=child[0:1]
	end=child[-1:]
	longstart=child[0:6]
	longend=child[-6:]
	"""
	print("Longstart,longend:",longstart,longend)
	print("Start,end:",start,end)
	
	if ("Book Shinkansen" in child):
		print(child)
		exit()
	"""
	dbl='"'
	if(longstart=="&quot;" and longend=="&quot;"):
		return True
	if (start==dbl and end==dbl):
		return True
	if (start=='“' and end=='”'):
		return True
	return False
