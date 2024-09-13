# blockstates 31.7.24

from np import semantics

def initialise():
	global blockStartFlag,blockOuterFlag,blockEndFlag,blockType
	blockStartFlag=False
	blockOuterFlag=False
	blockEndFlag=False
	blockType="None"

def setBlockStartFlag(myinput):
	global blockStartFlag
	blockStartFlag=myinput

def setBlockOuterFlag(myinput):
	global blockOuterFlag
	blockOuterFlag=myinput

def setBlockEndFlag(myinput):
	global blockEndFlag
	blockEndFlag=myinput

def setBlockType(myinput):
	global blockType
	blockType=myinput

def isMidBlock():
	bs=getBlockStartFlag()
	be=getBlockEndFlag()
	if (bs==False and be==False):
		return True
	else:
		return False

def getBlockStartFlag():
	global blockStartFlag
	return blockStartFlag

def getBlockOuterFlag():
	global blockOuterFlag
	return blockOuterFlag

def getBlockEndFlag():
	global blockEndFlag
	return blockEndFlag

def getBlockType():
	global blockType
	return blockType

def updateAll(child):
	checkOuterBlock(child)	
	checkStartBlock(child)
	checkEndBlock(child)

def checkOuterBlock(child):
	codelist=getCodeList()
	update=False
	for v in codelist:
		codeopen=v+"+"
		codeclose=v+"-"
		cap=len(codeopen)
		if (codeopen in child[0:cap]) or (codeclose in child[0:cap]):
			update=True
	setBlockOuterFlag(update)

def checkStartBlock(child):
	codelist=getCodeList()
	update=False
	for v in codelist:
		codeopen=v+"+"
		cap=len(codeopen)
		if (codeopen in child[0:cap]):
			update=True
			setNewBlockType(child)
	setBlockStartFlag(update)

def checkEndBlock(child):
	codelist=getCodeList()
	update=False
	for v in codelist:
		codeclose=v+"-"
		cap=len(codeclose)
		if (codeclose in child[0:cap]):
			update=True
	setBlockEndFlag(update)

# used in npmake to identify any valid '+' block for start of text parsing
def setNewBlockType(mystring):
	codelist=semantics.getAllBlockTagTypes() #["c","e","l","q","d"]
	update="None"
	for v in codelist:
		codeopen=v+"+"
		cap=len(codeopen)+1
		if (codeopen in mystring[0:cap]):
			update=v
			#print("Set new block type to:",v)
	
	setBlockType(update)
	if (update=="None"):
		print("Couldn't set new block type for string:",mystring)
		exit()

# For block processing, even d an l blocks are included
def getCodeList():
	output=semantics.getAllBlockTagTypes() #["c","e","l","q","d","s","a"]
	return output

def processStartBlock(child,blocktype):
	output=semantics.handleStartXMLBlock(child,blocktype)
	return output

# For blocks that are enclosed by single tags, close the XML tag
def processEndBlock(child,blocktype):
	output=semantics.handleEndBlockXMLTag(child,blocktype)
	return output

def handleBlocks(child):
	output=""
	bs=getBlockStartFlag()
	be=getBlockEndFlag()
	if bs==True:
		output=processStartBlock(child,blockType)
	elif be==True:
		output=processEndBlock(child,blockType)
		setBlockType("None")
	return output