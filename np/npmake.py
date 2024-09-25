# Program to pre-process text file into XML (as a pre-process for clean HTML)
# In effect, it is a 'scripty' interpreter ('scripty' is my writer-coding interpreted language)
# (C) Craig Duncan 15.12.23.  Latest version 29 May 2024.
# For instructions and marking up format, see README.md

import xml.etree.ElementTree as ET
import string
from pathlib import Path # for reading directory
import re
import sys
import os
import os.path as OPath
import shutil #shell utilities e.g. file copy

from np import wikitable,xmlpub,createindex,imagelister,commands,navlinks as NL,htmlcleaner,pagelinks,config,semantics,extlinks,autotag,defaultpara,htmltagmaker,outertag,xmltaglist,autotagsplit,datafunctions,blockstates,autoformat,overrides,cricket

#import localinfo
#import dateparser # local file for cleaning up dates for consistent format, sorting etc

def setCurrentShortname(myinput):
	global currentShortname
	currentShortname=myinput

def getCurrentShortname():
	global currentShortname
	if (currentShortname==None):
		return ""
	else:
		return currentShortname

def writehtml(input,fn):
	f=open(fn,"w")
	f.write(input)
	f.close()

# This list of meta lines may be empty

def getHeaderRowsWithMeta(headrows):
	metalist=NL.getMetaTagList() # T,D,A,C,R,F,B
	ignorelist=[]
	for a in metalist.keys():
		test=a+":"
		#base=len(test)
		cap=len(test)+1
		#print("Testing:",test)
		if (":" not in test):
			#print("error in :")
			exit()
		for h in headrows:
			pretext=h[0:cap]
			#print("Current row:",h," string:",pretext)
			if (test in pretext):
				# rowstr=h[base:]
				# append the full row
				ignorelist.append(h)
			#else:
			#	print(h,"no action")
		
	return ignorelist


# This function is only called if there is a D: header row (1st few lines) with data in it at the page top.
# Otherwise, the page will not appear in the Article nor the Date index.  It's just ignored.
def storeDateFromHeaderRow(datetimeobj):
	#content=dateparser.parseDate(myinput)
	#datetimeobj=dateparser.getDTobject()
	# update date indexes
	shortname=getCurrentShortname()
	namey=getNamePrefix(shortname)
	#
	myIndex=getTupleList()
	myDL=getDateTupleList() # this ensures global is updated
	startlen=len(myDL)
	startlenIndex=len(myIndex)
	if (namey!=None):
		mytpl=[namey,datetimeobj]
		myIndex.append(mytpl)
	if (datetimeobj!=None):	
		mydtpl=[datetimeobj,namey] # store in reverse order for sort				
		myDL.append(mydtpl)
	if (len(myDL)>startlen):
		setDateTupleList(myDL)
	if (len(myIndex)>startlenIndex):
		setTupleList(myIndex)

def getInternalRelated(rel1):
	
	mylist=rel1.split(",")
	mytag=semantics.getPageLinkRelatedClass()
	content='Related:'
	if (len(mylist)>0):
		count=1
		for a in mylist:
			if (len(a)>0):
				avalid=getValidRef(a)
				if (len(avalid)<1 or type(a)==None):
					abortOnError("fault in internal link")
				b=htmltagmaker.getIntLinkXML(avalid,avalid)
				if count>1:
					content=content+', '+b
				else:
					content=content+b
				count=count+1

	output=htmltagmaker.getSimpleXMLtag(mytag,content)
	return output

def getValidRef(link):
	relhtml=link
	rel1=link.strip() # remove whitespace
	if len(rel1)==0 or rel1==None:
		message="Empty link:"+relhtml
		abortOnError(message)
	return rel1


def checkBoldTags(line):
	loop=line.count("!*")
	loop2=line.count("*!")
	bsnum=int(loop)
	benum=int(loop2)
	if (bsnum>0 or benum>0):
		if (bsnum!=benum):
			return False
		else:
			return True
	return True

# This currently only checks that there is a rational sequence of open and closed tags
# It will detect an open tag at end of file
# It does not yet check if tags enclose other tag types (illegal)

def checkcodetags(symbol,mylines):
	openflag=False
	count=1
	lastcount=1
	lastcountoff=1
	checkmkON=symbol+"+"
	checkmkOFF=symbol+"-"
	cap=len(checkmkON)
	filestr="File:"+getCurrentShortname()
	for a in mylines:
		boldFlag=checkBoldTags(a)
		if boldFlag==False:
			message2="Mismatch in the !* *! detected at line:"+str(count)
			message=[filestr,message2]
			abortOnError(message)

		if checkmkON in a[0:cap] and openflag==True:
			
			message2="Error closing the "+checkmkON+" code tag detected at line:"+str(count)
			message3="Last mark detected:"+str(lastcount)
			message=[filestr,message2,message3]
			abortOnError(message)
		if checkmkON in a[0:cap] and openflag==False:
			openflag=True
			lastcount=count
		if checkmkOFF in a[0:cap] and openflag==False:
			message1=a[0:cap]
			message3="Duplicated "+checkmkOFF+"close tag detected at line:"+str(count)
			message4="Last mark off detected:"+str(lastcountoff)
			message=[message1,filestr,message3,message4]
			abortOnError(message)
		if checkmkOFF in a[0:cap] and openflag==True:
			openflag=False
			lastcountoff=count
		count=count+1
		# last line without closure
		if (count==len(mylines)+1) and openflag==True:
			message2="Failure to close the "+checkmkON+" code tag, last line:"+str(count)
			message3="Last mark detected:"+str(lastcount)
			message=[filestr,message2,message3]
			abortOnError(message)

# checks for HTML-style comments that would be invalid in XML
# use of < or > tag may be remedied by htmlcleaner.py now
def checkcommenttags(mylines):
	
	count=1
	filestr="File:"+getCurrentShortname()
	for a in mylines:
		# Do a hash check here too
		if len(a)<5 and "#" in a and a.strip()=="#":
			message1="Intro tag missing text at line:"+str(count)
			abortOnError(message1)
		# only opening tags seem to be a problem for XML (forward arrows OK)
		if "<-" in a or "<!-" in a:
			#print("Path:",fpath)
			message2="illegal tag and/or comments detected at line:"+str(count)
			print(message2)
			print("Line:",a)
			waiton=input("Fix now or continue? y to proceed")
			if (waiton!="y"):
				message=[filestr,message2]
				abortOnError(message)
		count=count+1

# This is for a prefix line outside a data block
# Updates status but should not return anything unless heading
def handleCodePrefix(child):
	output=""
	prefixlist=semantics.getPrefixList() # Includes the heading # X etc.
	codeMatch="None"
	for p in prefixlist:
		cap=len(p)
		checkstr=child[0:cap]
		if p==checkstr:
			codeMatch=p
	# branching
	if codeMatch=="None":
		return output
	imageoptionlist=semantics.getImagePrefixList()
	#print("imageoptionlist",imageoptionlist)
	#exit()
	headingfigure=semantics.getHeadingFigureTagMarkup() # This is # etc
	cap=len(codeMatch)
	cleanstr=child[cap:].strip()
	#print(cleanstr)
	#introTag=semantics.getHeadingTagMarkup()
	if codeMatch in headingfigure:
		output=output+semantics.getXMLfromLabelContent(codeMatch,cleanstr)
	elif codeMatch=="R:":
		output=output+getInternalRelated(cleanstr)
	elif codeMatch=="L:":
		PGFlag=getGutenberg()
		output=output+extlinks.getExternalLink(cleanstr,PGFlag)
	elif codeMatch in imageoptionlist:
		txtpath=getCurrentFilePath() # this is for .txt file
		#print("Found image prefix")
		#print(codeMatch,cleanstr,txtpath)
		#exit()
		handleImageOptions(codeMatch,cleanstr,txtpath)
		#print("Current image (if any):",imagelister.getCurrentImage())
		
	return output

def getGutenberg():
	output=False
	output=config.getGutenberg()
	if (output==False):
		if overrides.isGutenberg()==True:
			output=True
	return output

# set any one of the current image attributes
def handleImageOptions(code,cleanstr,txtpath):
	imagelister.updateImageStatus(code,cleanstr,txtpath)


# input arg 'child' is text here
# process all blank lines in code or example with CR only
# no storage of the block data occurs.  For non-list blocks, the output is a line with {CR}
def processMidBlock(child,blocktype):
	output=""
	if blocktype=="l":
		tagchecked=processNPLinks(child)
		output=semantics.handleListXMLtag(tagchecked)

	# no processing of internal 'links' here
	else:
		output=semantics.handleMidBlockXMLTags(child,blocktype)
	return output

# process a double quote line into an XML tag
def processQuote(child):
	dbl='"'
	newstring=child.strip(dbl)
	newstring=newstring.lstrip("&quot;")
	newstring=newstring.rstrip("&quot;")
	newstring=newstring.lstrip('“')
	newstring=newstring.rstrip('”')
	output=semantics.handleQuoteXMLTag(newstring)
	return output

def replaceLinkCheck(inputstr):
	output=False
	sub=" /"
	subend="/ "
	cst=inputstr.count(sub)
	cen=inputstr.count(subend)
	if(cst==cen) or cst>0:
		output=True
	return output

def findLinks(inputstr):
	sub=" /"
	subend="/ "
	subends=["/ ","/.","/;","/,","/:","/\n","/)","/]","/'"]
	outcome=0
	position=0
	results=[]
	intermediate=""
	maxlen=len(inputstr)
	while (outcome!=-1):
		substring=inputstr[position:]
		test=substring.find(sub)
		cap=0
		outcome=test
		# found opening link mark
		if test!=-1:
			newsub=substring[test:]
			#find2=newsub.find(subend)
			find2=-1
			internalresult=[]
			subtokens=[]
			for e in subends:
				ff=newsub.find(e)
				# find all matches in subend list, then find earliest in document.
				if find2==-1 and ff>0:
					internalresult.append(ff)
					subtokens.append(e)
			if (len(internalresult)>0):
				find2=min(internalresult)
				#print(internalresult,find2)
				subend=newsub[find2:find2+2] # all are length 2
				
			outcome=find2
			# found ending link mark
			if (find2!=-1):
				intermediate=substring[(test+1):test+find2+1]
				
				# ensure that random / dividers aren't caught
				if (len(intermediate)>2):
					results.append(intermediate)
				cap=position+test+find2+len(subend)				
				position=cap
				# End of file
				if position>=(maxlen-1):
					outcome=-1		
		else:
			# print("Found start link but no other end link in file")
			outcome=-1
		
	return results

# This contains an option for the link label to consist only of the internal page link if it is supplied.
def replaceLinks(lst,mystring):
	output=mystring
	for links in lst:
		linklabel=links.strip("/")
		linktext=pagelinks.getLinkXML(linklabel)
		if (linktext==None):
			print("Problem with link text in process NP Links")
			print("Current link:",links)
			exit()
		output=output.replace(links,linktext)
	return output

def processNPLinks(mystring):
	output=mystring
	result=replaceLinkCheck(output)
	if (result==True):
		bufferstring=" "+mystring+" "
		linklist=findLinks(bufferstring)
		output=replaceLinks(linklist,mystring)
	
	return output

def setLineScan(myinput):
	global inputtextarray
	inputtextarray=myinput

def getLineScan():
	global inputtextarray
	return inputtextarray

def getLineScanRows(count):
	output=[]
	myrows=getLineScan()
	if (count<len(myrows)):
		output=myrows[0:count]
	return output

# this uses the input filename to create an XML file from a .txt file
# input is a POSIX path for the input txt
# output is a string txt file
def getXMLfromFile(input):
	autotag.initialise()
	autoformat.initialise()
	autotagsplit.initialise()
	defaultpara.initialise()
	datafunctions.initialise()
	outertag.initialise()
	xmltaglist.initialise()
	overrides.initialise() # document specific
	setCurrentFilePath(input)
	newname=input.name
	setCurrentShortname(newname)
	# add a new dictionary entry to hold tags in file
	mydict=pagelinks.getIntroTagDict()
	if (newname not in mydict):
		taglist=[]
		mydict[newname]=taglist
		pagelinks.setIntroTagDict(mydict)
	#
	root=opentxt(input) # this is an array of lines
	setLineScan(root)
	# These check and abort if error, with line info about where to fix
	doTagChecks(root)
	output=getXMLFromArray(root)
	# mandatory http link replacement
	return output

# These are checks for the scripty markdown syntax (not XML)
# These will abort if error
def doTagChecks(root):
	taglist=semantics.getAllBlockTagTypes()
	for t in taglist:
		checkcodetags(t,root)
	# do nothing and fix with htmlclean
	#checkcommenttags(root)

# takes a string object separated by \n separated lines
# parses each line and turns it into an XML file (string)
# The main function of this is to turn a sequential,line-based markdown format (scripty) into 
# both data blocks (for pre-processing commands) and also semantically coded blocks for XML/HTML purposes.
def getXMLFromArray(mylines):
	#print("Creating XML structure in memory...prior to HTML")
	# mandatory initialisation of dictionary mydict
	datafunctions.reset()
	if (len(mylines)==0):
		print("Your text loop doesn't have any input data")
		filepath=getCurrentFilePath()
		print("filepath:",filepath)
		exit()

	# Prepare header from data in first few lines
	# up to 10 lines.  Could be less
	headset=NL.checkHeaderSection(mylines[0:10])
	# TO DO: If this data exists, then ignore these lines in main loop for XML
	ignorelist=getHeaderRowsWithMeta(headset)
	#print("Ignore List:",ignorelist)
	# hold this for now: 
	wrapperstart=semantics.getWrapperStartXMLTag()
	headersection=wrapperstart+NL.getXMLHeaderTags(ignorelist) # includes forward,back
	datetest=NL.getDateFlag()
	if datetest==True:
		datecontent=NL.getDateContent()
		storeDateFromHeaderRow(datecontent)
	print("Finished processing header section")
	xmloutput=""
	
	# reset data dictionary for this file
	
	#print("Reset dictionary for new file,",shortname)

	# Body
	
	target=len(mylines)
	pagelinks.registerMarkupPageLinks(mylines)
	print("Processing ",target," lines in file")
	datafunctions.initialise()
	blockstates.initialise()
	count=0
	for child in mylines:
		ignoreThis=False
		if child in ignorelist and count<len(headset):
			ignoreThis=True
		if len(child)>0 and ignoreThis==False:
			xmloutput=xmloutput+handleLine(child,count,"main")
			#print(xmloutput)
		count=count+1

	print("preparing footer")		
	wrapperend=semantics.getWrapperEndXMLTag()
	xmloutput=xmloutput+wrapperend
	if(wrapperend not in xmloutput):
		message="Error creating XML. Didn't complete."
		abortOnError(message)
	#WriteLocal(shortname)
	myfile=getCurrentShortname()
	
	"""
	# This used to process page links as part of initial markup decoding.
	# TO DO: make page link section a single XML tag that will be replaced once XML tags are read in

	print("Processing introductory page links...")
	mydict=pagelinks.getIntroTagDict()

	if myfile in mydict:
		
		#print("Ready to read out tags captured for ",myfile)
		taglist=mydict[myfile]
		homepage=config.getIndexName()
		# optional page links section
		if (config.arePageLinksOn()==True):	
			pagelinkline=pagelinks.processAllPageLinks(homepage)
	"""
	
	# placeholder for page links that will be replaced by links when XML created.
	tagrel=semantics.getPageLinkInsertClass()
	content=semantics.getDefaultPageLinkClass()
	xpc=xmltaglist.getPageLinkClass() # any thing previously saved
	if (xpc!=""):
		content=xpc
	pagelinkline=htmltagmaker.getSimpleXMLtag(tagrel,content)
	xmloutput=headersection+pagelinkline+xmloutput	
	print("Finished XML output")
	return xmloutput	


def handleCommentsMarks(child,typefile):
	ignoreLine=False
	if typefile==config.getAutoTagScriptSuffix and len(child)>2 and child[0:2]=="//":
		ignoreLine=True
	"""
	print(child)
	print("This is a command line/comment and is ignored in an ATS file or regular file")
	exit()
	"""
	# ignore this line in any file
	if len(child)>=2 and child[0:2]=="/*" or child[0:2]=="//":
		ignoreLine=True

	return ignoreLine

def handleLine(child,count,typefile):
	lineoutput=""
	# comments lines/blocks to be ignored
	ignoreLine=handleCommentsMarks(child,typefile)
	if ignoreLine==True:
		return lineoutput

	commands.initialise()
	blockType=""
	#child=child.replace("&","and") # avoids invalid XML	
	child=htmlcleaner.getClean(child) # avoids invalid XML and HTML characters
	endflag=False
	# linear flags not XML yet
	# No nesting of c,e,l flags permitted
	tableCommandFlag=False
	imageCommandFlag=False
	explicitFlag=False
	commandFlag=False
	quoteFlag=False
	prefixFlag=False
	ignoreCommands=False
	if (len(child)>0):
		# preliminary internal line replacements (as if author had written)
		child=handleAutoFormat(child,count) # at most, updates internal line
		# check to see if there is something encoded by author as prefix
		explicitFlag=False
		# check code prefix
		# update blockstates
		blockstates.updateAll(child)
		blockType=blockstates.getBlockType()
		
		if blockType=="" or blockType=="None":
			lineoutput=lineoutput+handleCommandsOrQuotes(child,count)
		else:
			lineoutput=lineoutput+handleMidBlockLines(child,count,blockType)	
			
	return lineoutput

def handleCommandsOrQuotes(child,count):
	output=""
	prefixFlag=commands.checkForPrefixCommands(child)
	quoteFlag=commands.checkIsQuote(child)
	if prefixFlag==True:
		output=handleCodePrefix(child) # Empty unless heading
		return output
	if quoteFlag==True:
		output=processQuote(child)
		return output
	
	output=handleCommandsOrAutoTag(child,count)
	return output

def handleCommandsOrAutoTag(child,count):
	output=""
	commandFlag=commands.checkAllCommands(child)
	if commandFlag==True:
		output=processCommandForLine(child)
		return output
	else:
		#print("Doing autotagging:",child)
		checkBlockTagging(child,count) # This should be earlier?
		output=handleAutoTagging(child,count)
		#print("blocktype None encountered")
		return output

def handleMidBlockLines(child,count,blockType):
	output=""
	output=handleBlockSections(child,blockType)
	#print("blocktype ",blockType,"encountered")
	return output

# only some of these commands will return output 
def processCommandForLine(child):
	output=""
	if (commands.isTableOrImage()==True):
		print("command detected for",child)
		output=output+handleImageOrTableCommand(child)
	else:
		presentcom=commands.getActiveCommand()
		datacommands=commands.getDataCommands()
		paracommands=commands.getParagraphOptionCommands()
		mathcommands=commands.getMathCommands()
		printcommands=commands.getPrintCommands()
		ebookcommands=commands.getEBookCommands()
		if (presentcom=="import"):
			output=output+handleImportCommand(presentcom,child)
		elif presentcom in paracommands:
			handleParagraphCommands(child)
		elif presentcom in datacommands:
			handleDataCommands(child)
		elif presentcom in ebookcommands:
			handleEBookComands(child)
		elif presentcom in mathcommands:
			handleMathCommands(child)
		elif presentcom in printcommands:
			converted=handlePrintCommands(child)
			if (converted!=None):
				output=output+converted #handlePrintCommands(child)	
		else:
			handleTagStateCommands(child)
	return output

# error checking for tags that are spaced far apart (around other blocks)
# this should involve end tags appearing where no local block has been opened
#blockcodes=["l","e","c","d"]
def checkBlockTagging(child,count):
	blockcodes=semantics.getAllBlockTagTypes()
	# find and report on source of this mis-match.
	for bc in blockcodes:
		test=bc+"-"
		cap=len(test)
		if(test in child[0:cap]):
			message=[]
			print(child)
			message1="Illegal nested "+test+" at line:"+str(count)
			#abortOnError(message1)
			message.append(message1)
			prev=bc+"+"
			latest=""
			latestline=0
			upcount=1
			linescan=getLineScanRows(count)
			for linerev in linescan:
				if (prev in linerev[0:cap]):
					latest=linerev
					latestline=upcount
				upcount=upcount+1
			if (latestline>1):
				message2="previous open tag ("+prev+") at line:"+str(latestline)
				message=[]
				message.append(message2)	
			abortOnError(message)
		test2=bc+"+"
		cap2=len(test2)
		if(test2 in child[0:cap2]):
			print("blockcode:",bc)
			print(child)
			message3="Illegal nested "+test2+" at line:"+str(count)+" (or block start not detected)"
			message=[]
			message.append(message3)
			abortOnError(message)

# opens, processes and returns the parsed outcome of the import(file) command
def handleImportCommand(command,mystring):
	output=""
	print("Active:",command)
	myargs=commands.getArgs(command,mystring)
	print("Args:",myargs)
	
	if (len(myargs)==1):
		filename=myargs[0]
		
		if ("." not in filename):
			filename=filename+config.getAutoTagScriptSuffix()
			if ("." not in filename):
				print("You need to include . in config.py file autotagscript suffix")
				exit()
		fullname=constructFullPathForName(filename)
		
		mytextarray=opentxt(fullname)
		minicount=1
		typefile=config.getAutoTagScriptSuffix
		for g in mytextarray:
			output=output+handleLine(g,minicount,typefile)
		
		return output
	else:
		print("Trouble with file information for opening the import file:",filename)
		exit()

def constructFullPathForName(myname):
	filepath=getCurrentFilePath()
	ppath=filepath.parent.absolute()
	output=str(ppath)+"/"+myname
	return output

def handleImageOrTableCommand(child):
	output=""
	myargs=""
	firstarg=""
	activecommand=commands.getActiveCommand()
	if len(activecommand)>0:
		myargs=commands.processArgsForCommand(child)
		if(myargs==None):
			myargs=""
		
			
	#print("Handle image or table command:",activecommand)
	#exit()
	#tableCommandFlag=False
	match activecommand:
		case "tablecol" | "tablerow" | "tprint":
			mydict=datafunctions.getDataDict()
			output=output+wikitable.process(mydict,myargs,activecommand)
			return output

		case "tablecoltotals":
			smldict=datafunctions.getSmallDictWithColTotals(myargs)
			print(smldict)
			output=output+wikitable.process(smldict,myargs,activecommand)
			return output

		case "image":
			#print("image found. myargs:",myargs)
			firstarg=myargs[0]
			if (len(myargs)>0 and len(firstarg)>0):
				txtpath=getCurrentFilePath()
				rows=datafunctions.getDictionaryVariable(firstarg)
				newtext=imagelister.handleRowsForImageData(txtpath,rows)
			else:
				newtext=imagelister.getImageXML()
			output=output+newtext
			return output
	
	return output

#["autotagline","autotagsplit","defaultpara","outertag","pagelinks"]	
def handleTagStateCommands(child):
	activecommand=commands.getActiveCommand()
	if len(activecommand)>0:
		myargs=commands.processArgsForCommand(child)
		firstarg=myargs[0] # variable to be used
	match activecommand:
		case "autotagline":
			optionlist=datafunctions.getDictionaryVariable(firstarg)
			autotag.handleTagSettings(myargs,optionlist)
		case "autotagsplit":
			optionlist=datafunctions.getDictionaryVariable(firstarg)
			autotagsplit.handleTagSettings(myargs,optionlist)
		case "autoformat":
			optionlist=datafunctions.getDictionaryVariable(firstarg)
			autoformat.handleTagSettings(myargs,optionlist)
		case "outertag":
			outertag.handleTagSettings(myargs)
		case "pagelinks":
			xmltaglist.handleTagSettings(myargs)
		case "defaultpara":
			defaultpara.handleTagSettings(myargs)

def handleParagraphCommands(child):
	myargs=""
	activecommand=commands.getActiveCommand()
	if len(activecommand)>0:
		myargs=commands.processArgsForCommand(child)
		#print(myargs)
	match activecommand:
		case "paragraph":
			overrides.handleParagraphCommands(myargs)
			
def handleDataCommands(child):
	#print(child)
	myargs=""
	activecommand=commands.getActiveCommand()
	if len(activecommand)>0:
		myargs=commands.processArgsForCommand(child)
		#print(myargs)
	match activecommand:
		case "header" | "ripname" | "colnames":
			datafunctions.handleHeaderCommand(myargs)
		case "splits" | "dlim":
			datafunctions.handleSplitCommand(myargs)
		case "datasplit" | "rip" | "ripdown":
			datafunctions.handleDataSplits(myargs)
		case "ripacross":
			print(myargs)
			datafunctions.handleDataRowRips(myargs)

def handleMathCommands(child):
	activecommand=commands.getActiveCommand()
	if len(activecommand)>0:
		myargs=commands.processArgsForCommand(child)
	match activecommand:
		case "sum":
			datafunctions.handleSumCommand(myargs)
		case "sumacross":
			datafunctions.handleSumAcross(myargs)
		case "rowtotals":
			datafunctions.handleRowTotals(myargs)

def handleEBookComands(child):
	activecommands=commands.getActiveCommand()
	if len(activecommand)>0:
		myargs=commands.processArgsForCommand(child)
	match activecommand:
		case "gutenberg":
			overrides.setGutenbergOn()

def handlePrintCommands(child):
	output=""
	blockType=None
	activecommand=commands.getActiveCommand()
	if len(activecommand)>0:
		myargs=commands.processArgsForCommand(child)
	blockOutput=False
	match activecommand:
		case "eprint":
			blockType="e"
			blockOutput=True
		case "codeprint":
			blockType="c"
			blockOutput=True
		case "lprint":
			blockType="l"
			blockOutput=True
		case "nprint":
			blockType="n"
			blockOutput=True
		case "qprint":
			blockType="q"
			blockOutput=True

		case "tprintrows":
			blockType="tpr"
			data1=datafunctions.handleRowsForTPrint(myargs)
			alldata=cricket.makeIndexedTableHeader(data1)
			output=output+wikitable.makeTPrintTable(alldata)
		case "cprintrows":
			blockType="cpr"
			data1=datafunctions.handleRowsForTPrint(myargs)
			alldata=cricket.makeIndexedTableHeader(data1)
			#
			cricketsup=cricket.addBatterStats(alldata)
			output=output+wikitable.makeCPrintTable(cricketsup)
	
	if (blockOutput==True):
		if len(activecommand)>0:
			#print("handling print command")
			firstitem=myargs[0]	
			output=output+applyBlockTypeToVariableData(firstitem,blockType)
	return output

def applyBlockTypeToVariableData(firstitem,blockType):
	output=""
	newlines=""
	content=datafunctions.getDictionaryVariable(firstitem)
	listtypes=["l"]
	numtypes=["n"]
	contigtypes=["c","e","q"]
	if blockType in listtypes:
		for a in content:
			newlines=processMidBlock(a,blockType)
			# tag each line
			output=output+semantics.getBlockTagXML(blockType,newlines)
		return output
	elif blockType in numtypes:
		count=1
		for a in content:
			a=str(count)+". "+a
			print(a)
			newlines=processMidBlock(a,blockType)
			# tag each line
			output=output+semantics.getBlockTagXML(blockType,newlines)
			count=count+1
		return output
	elif blockType in contigtypes:
		for a in content:
			newlines=newlines+processMidBlock(a,blockType)
		# tag only the whole new string
		output=output+semantics.getBlockTagXML(blockType,newlines)
		return output

	return output

def handleAutoFormat(child,count):
	output=child
	if autoformat.getAutoTagging()==True:
		output=autoformat.handleLine(child)
	return output	
	
def handleAutoTagging(child,count):
	autooutput=""

	# replace any internal link text with tags. Process locally, not in whole file for now
	autotagged=False
	if autotag.getAutoTagging()==True:
		automatchclass=autotag.getClassForLine(child)

		if len(automatchclass)>0:
			myline=htmltagmaker.makeXMLForLineClass(child,automatchclass)
			autooutput=autooutput+myline
			autotagged=True
		# autooutput=autooutput+

	if autotagsplit.getAutoSplitTagging()==True:
		
		automatchclass=autotagsplit.getClassForLine(child)
		if len(automatchclass)>0:
			myline=autotagsplit.makeXMLforSplitLine(child)
			autooutput=autooutput+myline
			autotagged=True
			#print(myline)
			#exit()

	outertagged=False
	if outertag.getOuterTagging()==True:
		outercheck=outertag.checkIsOuter(child)
		if (outercheck==True):
			myclass=outertag.getOutertagClass()
			content=outertag.removeOuter(child)
			myline=htmltagmaker.makeXMLForLineClass(content,myclass)
			autooutput=autooutput+myline
			outertagged=True 

	if autotagged==False and outertagged==False:
		dpclass=defaultpara.getDefaultClass()
		if (defaultpara.getIsDefaultSet()==True and len(dpclass)>0):
			#myline=htmltagmaker.makeXMLForLineClass(child,dpclass)
			myline=handleMainParaType(child,dpclass)
			autooutput=autooutput+myline
		else:
			tagclass=semantics.getMainParaTagMarkup()
			autooutput=autooutput+handleMainParaType(child,tagclass)
	return autooutput

def handleBlockSections(child,blockType):
	blockoutput=""
	#print("Found a blockstate:",blockType)
	if blockstates.isMidBlock()==True:
		if (blockType=="d"):
				if (len(child)>0):
					newinput=child
					tagchecked=processNPLinks(newinput)
					datafunctions.append(tagchecked)
					#print("Added data to data function",tagchecked)

				else:
					datafunctions.append(".") # prevent empty line in data
		else:
			blockoutput=blockoutput+processMidBlock(child,blockType)	
			# no need to check is block OuterFlag=false?
	else:
		if blockType=="d":
			#print("Block state d, start or end")
			
			if blockstates.getBlockEndFlag()==True:
				datalist=datafunctions.getDataList()
				#print("Finishing data block with this data:",datalist)
				datafunctions.convertDataBlock(datalist) # more general data store
				datafunctions.initialiseDataList() # not all the data!
				blockstates.setBlockType("None")
			# else do nothing (it's not a block type with output)
				
		elif blockType!="d":
			updatedText=blockstates.handleBlocks(child)
			blockoutput=blockoutput+updatedText
	return blockoutput

def handleMainParaType(child,tagclass):
	retagged=processNPLinks(child)
	paraclass="dbl"
	if config.isSingleSpaced()==True:
		paraclass="sgl"
	firsttag=tagclass+' spacing="'+paraclass+'"'
	content=retagged
	newlineXML=semantics.makeMismatchedXMLTag(firsttag,content,tagclass)
	#<'+sdp+' spacing="'+paraclass+'">'+retagged+'</'+sdp+'>\n'
	return newlineXML

# write out xml to same folder as original txt file
# (not needed if no intermediate XML is created)
def writeFolderPath(content,fpath):
	shortname=fpath.name
	htname=getNamePrefix(shortname)+".xml"
	foutput=constructFullPathForName(htname)
	writetxt(content,foutput)
	"""
	print(content)
	exit()
	"""
	
def writeLocal(content,shortname):
	prefix=getNamePrefix(shortname)
	htname=prefix+".xml"
	writetxt(content,htname)

# assumes utf 16?
def opentxt(fn):
	f=open(fn,"r")  # default is utf-8 not 16?
	mystring=f.read()
	if (mystring[0]=="\ufeff"):
		print("Wrong decoder used on this file")
		print("FEFF code in first byte")
		exit()
	f.close()
	output=getArrayFromString(mystring)
	return output

def getArrayFromString(myinput):
	output=[]
	output=myinput.split("\n")
	if (len(output)==0):
		output=[]
	return output

def writetxt(input,fn):
	f=open(fn,"w")
	f.write(input)
	f.close()

def getNamePrefix(input):
	endpt=len(str(input))-4
	prefix=str(input)[0:endpt]
	return prefix

# Process txt files in run folder and subfolders
# Process into simple XML, for subsequent HTML conversion program
# All source folders and .txt files must be in the Source folder

def setupArticleDictionary():
	global myArticleDict
	myArticleDict=dict()


def setArticleDictionary(myinput):
	global myArticleDict
	myArticleDict=myinput

def getArticleDictionary():
	global myArticleDict
	return myArticleDict

def setupFilePaths():
	global currentShortname
	global currentFilePath
	currentFilePath=""
	currentShortname=""

def setCurrentFilePath(myinput):
	global currentFilePath
	currentFilePath=myinput

def getCurrentFilePath():
	global currentFilePath
	return currentFilePath

def setupTupleList():
	global myTupleList
	global myDateTupleList
	pagelinks.initTagDict()
	myTupleList=[]
	myDateTupleList=[]
	
	imagelister.initialise()

def setTupleList(myinput):
	global myTupleList
	myTupleList=myinput

def getTupleList():
	global myTupleList
	return myTupleList

def setDateTupleList(myinput):
	global myDateTupleList
	myDateTupleList=myinput

def getDateTupleList():
	global myDateTupleList
	return myDateTupleList

"""
def main():
	myinput=input("Filename or leave blank for all:")
	if(len(myinput)==0 or myinput=="all"):
		mainall()
	else:
		mainOneFile(myinput)

"""
def userInt():
	global lastinput
	storeLastInput("")
	keycode=0
	"""
	while True:
		userinput=os.read(sys.stdin.fileno(), 3).decode()
		lu=len(userinput)
		if lu==3: # single keypress with ^[[A = 27,1,65 i.e [A
			keycode=ord(userinput[2])
			print(keycode)
			break
	"""
	while True:
		mainlist=[]
		userinput=input("Enter filename :")
		if userinput=="exit":
			break
		elif userinput=="" and lastinput !="":
			userinput=lastinput
		else:
			lastinput=userinput
		#print(userinput)
		"""
		lu=len(userinput)
		if lu==3: # single keypress with ^[[A = 27,1,65 i.e [A
			keycode=ord(userinput[2])
			#print(keycode,userinput[2])
		if keycode==65: # keypress A up cf B (down), C, D
			userinput=getLastInput()
			lastinput=userinput
			print("reusing:",lastinput)
		else:
			lastinput=userinput
		storeLastInput(lastinput)
		"""
		mainlist=mainOneFile(userinput)
		
		if (len(mainlist)==0):
			print("I didn't find any files with that name.  No action taken.")
		if userinput=="all":
			createindex.main(mainlist)
			print("New SiteMap Created")
		


	# create index on exit

def storeLastInput(myinput):
	global lastinput
	lastinput=myinput

def getLastInput():
	global lastinput
	return lastinput


def checkDirectoryExists(idxpath):
	idxtrue=OPath.isdir(idxpath)
	if (idxtrue==False):
		print("You forgot to setup the index directory ",idxpath)
		exit()

# starting point for internal and external (e.g. scripty.py) function call
# use folder: to work on one folder
# use all to work on whole project and update project/site indexes
def mainOneFile(myinput):
	setupArticleDictionary()
	p = Path('.')
	filenames=myinput
	if (myinput=="all"):
		filenames='*'
	p = Path('.')
	allfilepaths=[]
	keystart=len("folder:")
	filepattern='Source/**/'+filenames+'.txt'
	if (myinput[0:keystart]=="folder:"):
		folderset=myinput[keystart:]
		print("folderset:",folderset)
		filepattern='Source/'+folderset+'/*.txt'
	for child in p.glob(filepattern):
		if (len(child.name)>0):
			allfilepaths.append(child)
	setupTupleList()

	"""
	As of 8 May 2024, the lean XML intermediate format produced from scripty markup is still used to produce HTML, but not saved to disk as a record.
	There is time saving in avoiding disc I/O.  Also the intermediate data format is a software structure, 
	useful for reasoning about data for this workflow, but perhaps not generally.

	XML file ops can be reinstated as an additional step if required.

	One consequence is that the 'openXML' function in xmlpub no longer runs.  This used to do some 
	re-arrangement of line endings and insertion of {CR}.  This step is now in npmake.
	"""

	for x in allfilepaths:
		print("working on file...",x)

		xml=getXMLfromFile(x) # a string containing XML
		# page link class is updated after the getXMLfromFilefunction
		pagelinkclass=xmltaglist.getPageLinkClass() # updated after processing
		if (pagelinkclass=="" or pagelinkclass==None):
			pagelinkclass=semantics.getDefaultPageLinkClass()
		"""
		print(xml)
		# TO DO: some xml validity checks
		exit()
		"""

		try:
			print("Creating ET XML object")
			myDataET=ET.fromstring(xml)
			"""
			for name in root.iter('name'):
				print(root.tag, name.text)
			"""
		except ET.ParseError as e:
			#pass
			print ("Exception found in XML file based on:",x)
			pos=e.position
			line=pos[0]
			lineindex=line-1
			col=pos[1]
			cod=e.code
			print("line:",line,"col:",col,"code:",cod)
			if (line>0):
				rows=xml.split("\n")
				print(rows[lineindex])
			"""
			if (line>0):
				rows=xml.split("\n")
				print(rows[lineindex])
				print("---")
				#for a in range(0,line):
				#	print(rows[a])
				print("Right about here:")
				linestart=line
				if (line>0):
					linestart=linestart-1
				for a in range(linestart,line):
					print(rows[a])
			"""
			exit()
		
		print("Now obtaining HTML from XML")
		newname=str(x.name)
		newname=newname.replace("txt","xml")
		f = x.parent / (newname)
		fp=Path(f)
		xmlpub.getHTMLfromXML(fp,myDataET,pagelinkclass) # This will save the file too

	if (len(allfilepaths)==0):
			print("No action taken.")
	else:
		print("Finished processing txt files for:",myinput)
	
	# only update index for all. TO DO: option to make this independently of script parsing.
	if (myinput=="all"):
		# This process indexes straight through to an HTML file without saving any intermediate XML
		# It creates the ET object from string, not XML file
		myarray2=getDateIndexArray() # an array of lines, as in a text file
		if (myarray2!=None):
		# check paths
			idxpath='./Source/Indexes'
			checkDirectoryExists(idxpath)
			xmlString=getXMLFromArray(myarray2) # a string containing XML tags
			#
			print("Preparing indexes")
			datefilexml=getIndexPath("DateIndex",".xml")
			datefiletxt=getIndexPath("DateIndex",".txt")
			artfilexml=getIndexPath("ArticleIndex",".xml")
			artfiletxt=getIndexPath("ArticleIndex",".txt")
			p = Path(datefilexml) # As if there was a file
			dataET = ET.fromstring(xmlString) # now an ET object
			defaultlinkclass=semantics.getDefaultPageLinkClass()
			xmlpub.getHTMLfromXML(p,dataET,defaultlinkclass)
			dateidxpath=Path(datefiletxt)
			allfilepaths.append(dateidxpath)

			myarray=getTupleIndexArray()
			xmlStringT=getXMLFromArray(myarray)
			pagelinkclass=xmltaglist.getPageLinkClass()
			p2 = Path(artfilexml) # As if there was a file
			dataET2 = ET.fromstring(xmlStringT) # now an ET object
			#
			print("Writing out HTML")
			# page link class is updated after the getXMLfromFilefunction
			defaultlinkclass=semantics.getDefaultPageLinkClass()
			xmlpub.getHTMLfromXML(p2,dataET2,defaultlinkclass)
			articleidxpath=Path(artfiletxt)
			allfilepaths.append(articleidxpath)
			print("updated Article Indexes")

		# image links WIP
		print("And here are all the paths for images used in this build")
		myimagelistall=imagelister.getImagesUsed()
		
		for m in myimagelistall:
			print(m)
	
	return allfilepaths

#'./Source/Indexes/DateIndex.xml'
def getIndexPath(myinput,ext):
	folder=config.getIndexFolder()
	output="./Source/"+folder+"/"+myinput+ext
	return output

def getTupleIndexArray():

	myTL=getTupleList()
	newlist=sorted(myTL) # makes a tuple not a dict
	output="T:Articles by Title\n\n"
	output=output+"d+\n(TitleData)\n"
	for a in newlist:
		title=a[0]
		dateobj=a[1]
		if (dateobj==None):
			datestr=""
		else:
			datestr=dateobj.strftime("%d %B %Y")
		# make sure there is a space before the slash for link purposes
		row=" /"+title+"/ ,"+datestr+" \n"
		output=output+row
	output=output+"d-\n"
	output=output+"header[Article,Date]\nsplits[comma]\ndatasplit(TitleData)\ntablecol(Date,Article)\n"
	myarray=getArrayFromString(output)
	return myarray

	# do an early call to make XML from data in memory, not in a .txt file
	
def getDateIndexArray():
	myDL=getDateTupleList()
	if len(myDL)==0:
		print("This list has no data, aborting...")
		return
	newlist2=sorted(myDL, reverse=True) # makes a tuple not a dict
	output2="T:Articles by Date\n\n"
	output2=output2+"d+\n(ListData)\n"
	for a in newlist2:
		dateobj=a[0]
		if (dateobj==None):
			datestr=""
		else:
			datestr=dateobj.strftime("%d %B %Y")
		title=a[1]
		#print(datestr,",",title)
		row=datestr+", /"+title+"/"+" \n"
		output2=output2+row
	output2=output2+"d-\n"
	output2=output2+"header[Date,Article]\nsplits[comma]\ndatasplit(ListData)\ntablecol(Article,Date)\n"
	myarray2=getArrayFromString(output2)
	return myarray2

def mainall():
	
	p = Path('.')
	allfilepaths=[]
	for child in p.glob('Source/**/*.txt'):
		if (len(child.name)>0):
			allfilepaths.append(child)

	# make std link to main index at top in related keywords section
	# make same in xmlpub.py
	# this will only load and operate on each file one at a time
	for x in allfilepaths:
		print("processing:"+x.name)
		datafunctions.reset()
		xml=getXMLfromFile(x)
		print("Finished XML (internal)")
		writeFolderPath(xml,x)
	print("Finished processing txt files.")

# To manage errors and give option to terminate all processes
# This is python handling different function arguments
def abortOnError(description):
	if (type(description)==str):
		print(description)
	if (type(description)==list):
		for d in description:
			print(d) # inserts CR automatically
	exit()

#main()
userInt()
