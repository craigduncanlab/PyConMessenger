# Recursion code extracted from xmlpub 8 May 2024 (c) Craig Duncan
# The purpose of this module is to iterate within an XML element tree and interpret the tags, then return a string of formatted HTML
# The input XML format is based on the output of npmake, which transforms scripty markdown into simple XML tags
# The HTML format is based on a design favouring semantic classes, paragraph navigation links, and compatibility with class-based Word processors
# As such it makes not use of div tags


from pathlib import Path # for reading directory
import os.path as OPath
import shutil #shell utilities e.g. file copy
from np import wordcount,imagelister as IM,pagelinks,config,xmltaglist,streamprocess

def initialise(linkstext,myinput,pagelinkclass):
	setupCounters()
	streamprocess.setLinkText(linkstext)
	streamprocess.setCurrentPosix(myinput)
	setPageLinkClass(pagelinkclass)

def getTotalWordCount():
	wordcounter=wordcount.getWordCount()
	return wordcounter

def setupCounters():
	streamprocess.setupCounters()
	wordcount.resetWordCount()
	IM.makeImageList()
	imagelist=IM.getImageList()
	IM.setImageList(imagelist)
	pagelinks.resetIntroParaCount()
	xmltaglist.initialise()

# unusued?
def setPageLinkClass(myinput):
	global pagelinkclass
	pagelinkclass=myinput

def getPageLinkClass():
	global pagelinkclass
	return pagelinkclass

def getTextFromTag(child):
	if (type(child)==str):
		return child
	utfText=child.text # if this is empty it throws an error in next line
	if utfText==None:
		utfText=""
	return utfText

# str (text, 'utf-8')
# input is a 'child' node of the 'root' object
def main(child,lcnum):
	authortags=["author"]
	"""
	expcounter=getParaCounter()
	figcounter=getFigureCounter()
	"""
	linecounter=0
	output=""
	utfText=""
	alttext=""
	myclass=""
	istable=False
	
	# myclass can be any XML tag in document
	myclass=child.tag
	utfText=getTextFromTag(child)
	# overrides: non printable XML like <override> to specify Gutenberg output? if myclass !=override process line...
	# This would, in effect, be asking the XML to hold metadata i.e a 'state' relevant to the XML parser and output.
	line=streamprocess.main(child,myclass,utfText)
	# this was once in utfText, now just handle CR replace for each line
	wordcount.updateWordCount(line)
	line=handleDecorations(line)
	output=output+line
	return output

def handleDecorations(line):
	# handle breaks
	line=line.replace("{CR}","<br>")
	# handle italics
	emcount=line.count("!!")
	emnum=int(emcount/2)
	if (emcount % 2 ==0):
		for x in range(0,emnum):
			line=line.replace("!!","<em>",1)
			line=line.replace("!!","</em>",1)	
	# handle bold
	loops=line.count("!*")
	if (loops>0):
		bsnum=int(loops)
		benum=int(line.count("*!"))
		if (bsnum==benum):
			for x in range(0,loops):
				line=line.replace("!*","<b>",1)
				line=line.replace("*!","</b>",1)
	# handle underline
	loops=line.count("!_")
	if (loops>0):
		bsnum=int(loops)
		benum=int(line.count("_!"))
		if (bsnum==benum):
			for x in range(0,loops):
				line=line.replace("!_","<u>",1)
				line=line.replace("_!","</u>",1)
	return line