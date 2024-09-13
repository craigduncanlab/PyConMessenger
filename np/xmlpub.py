# XML parsing for gloss/terms first created 29 August 2023. 
#
# The main role of this module now (8.5.2024) is to manage :
# 1. translation of a scripty markdown file into HTML (via the XMLtoHTML function)
# 2. some web page integration (word counts, cross-links etc)
#
# The 'recursion' module handles most of the exploration of the Element Tree (XML)
# 
# The production of HTML is in conjunction with style sheets such as fnlstyle.css
#
# Use UTF 16 in header to ensure special characters are recognised in browsers.
#
# Static Site Generator 16 November 2023 (C) Craig Duncan
# This version 17.12.23; 7-8 May 2024
# https://docs.python.org/3/library/xml.etree.elementtree.html#module-xml.etree.ElementTree
# Useful discussion of ElementTree: https://lxml.de/tutorial.html
import xml.etree.ElementTree as ET
import string
from pathlib import Path # for reading directory
import re
import os.path as OPath
import shutil #shell utilities e.g. file copy
from datetime import date
from np import localinfo,recursion,imagelister as IM,config,xmltaglist,semantics,CSSmappings,streamprocess

# the expcounter is a way of numbering each paragraph
# this assumes you want a formal, essay style
# it is equivalent to auto-numbering the OOXML in a Word document.
# Once it is written into the HTML, a search for paragraph number could find it by looking
# for the characters up to the . at the start of the paragraph.

def resetTotalWordCount():
	global totalwordcount
	totalwordcount=0

def defineTotalWordCount():
	global totalwordcount
	totalwordcount=0

def getTotalWordCount():
	global totalwordcount
	return totalwordcount

def setTotalWordCount(myinput):
	global totalwordcount
	totalwordcount=myinput

def definePosixPath():
	global posixpath
	posixpath=Path(".")

def setCurrentPosixPath(myinput):
	global posixpath
	posixpath=myinput

def getCurrentPosix():
	global posixpath
	return posixpath

def getTodayDateString():
	td=date.today()
	myd=td.strftime("%A %d %B %Y")
	return myd

def getTodayYear():
	td=date.today()
	myd=td.strftime("%Y")
	return myd


def writehtml(input,fn):
	f=open(fn,"w")
	f.write(input)
	f.close()

# assumes utf 16
def opentxt(fn):
	f=open(fn,"r")  # default is utf-8 not 16?
	output=f.read()
	return output

# In some ways, there is no home page, especially if the index.html landing page
# is always set to a copy of the latest article (by date).
# in that case, what you want to do is go to the index page.
# notice how the web was built with the idea your landing page would be an index of some kind.
# This was pre-search engines, and made a lot of sense, especially if you thought of web pages as a kind of book, not as a magazine, a television site or something else.
# Two elements of the footer are needed: (a) Index (b) Feedback link
# The feedback should be a form, so I am not giving out my email.

def addKeySiteLinks():
	linklist=["#Top"]
	output=""
	count=1
	for a in linklist:
		if count>0:
			output=output+" | " #separator
		output=output+'<a href="'+a+'" class="footer">'+a+'</a>'
		count=count+1
	return output

def getPageFooter():
	siteLinks=True
	indexname=config.getIndexName()
	mainauthor=localinfo.getMainAuthor()
	signoff='<p class="footer"><a href="'+indexname+'.html" class="footer">Site Map</a>'
	if (siteLinks==True):
		signoff=signoff+addKeySiteLinks()
	signoff=signoff+"</p>"
	yearnow=getTodayYear()
	signoff=signoff+'<p class="footer">Created by: '+mainauthor+' 2023-'+yearnow+'</p>'
	chosenLicence=localinfo.getSiteLicence()
	signoff=signoff+'<p class="footer">Except where otherwise noted, content on this site is '+chosenLicence+'</p>'
	return signoff

def getVerboseFooter(fname,wc,filesize):
	yearnow=getTodayYear()
	latest=getTodayDateString()
	signoffwc=str(wc)+' words (main paras not quotes or inserts). About '+str(filesize)+' bytes.</p>'
	signoff='<p class="footer">This update: '+latest+'. '+signoffwc
	signoff=signoff+'<p class="footer">To link to a paragraph, use this format in your browser. e.g. '+fname+'#P4</p>'  
	return signoff

def handlepageclass(linkclass,root):
	xmltaglist.initialise()
	xmltaglist.setPageLinkClass(linkclass)
	xmltaglist.registerXMLpagelinks(root,linkclass) # this does this at start of file
	output=xmltaglist.getPageLinksSection(linkclass)
	return output

def handleRecursionStart(linkstext,myinput,pagelinkclass):
	recursion.initialise(linkstext,myinput,pagelinkclass)
	

# root must be an ET object parsed from an XML file
# input is a POSIX path
def getHTMLfromXML(myinput,root,pagelinkclass):
	linkstext=handlepageclass(pagelinkclass,root)
	handleRecursionStart(linkstext,myinput,pagelinkclass)
	definePosixPath()
	setCurrentPosixPath(myinput)
	defineTotalWordCount()
	shortname=myinput.name  # input now has .xml already  +".xml"
	prefix=getNamePrefix(shortname)
	htpathname="htmlpages/"+prefix+".html"
	localhtname=prefix+".html"
	htmloutput=getPageHeader(prefix) #std header and style sheet
	
	# Body
	lc=0
	
	#TO DO: handle actual making of page links
	print("Beginning XML recursion")
	for child in root:
		htmloutput=htmloutput+recursion.main(child,lc)
		lc=lc+1
	print("Finished recursion")
	wordcounter=recursion.getTotalWordCount()
	twc=getTotalWordCount()
	twc=twc+wordcounter
	setTotalWordCount(twc)
	maxparas=streamprocess.getParaCounter() #recursion.getParaCounter()
	fsizetemp=len(htmloutput) # for text files on Mac this is ~ filesize in bytes.
	isNumberingOn=config.isGlobalNumberingOn()
	navlinks="" # no links unless numbering is on
	if isNumberingOn==True:
		navlinks=getParaLinks(localhtname,maxparas) # else no change, but counter keeps running
	testoutput=getPageFooter()
	if config.isFooterVerboseStats()==True:
		verbose=getVerboseFooter(localhtname,wordcounter,fsizetemp)
		testoutput=testoutput+verbose
	testoutput=testoutput+"</body></html>"
	
	
	htmloutput=htmloutput+navlinks+testoutput
	# Footer
	writehtml(htmloutput,htpathname)
	# update css for custom
	# updateCSS()

def updateCSS(newfilename):
	print("UPDATING...")
	fname1=config.getMainStyleSheetName()
	fname1="htmlpages/"+fname1
	mainstylestring=opentxt(fname1)
	revised = CSSmappings.getLatest()

	output=mainstylestring+revised
	#fname="htmlpages/semantics.css"
	writehtml(output,fname1)
	print("Finished writing out CSS update",fname1)


def getPageHeader(shortname):
	htmloutput='<html><head><title>'+shortname+'</title>'
	yearlatest=getTodayYear()
	mainauthor=localinfo.getMainAuthor()
	mainkeywords=localinfo.getMainKeywords()
	mainDescription=localinfo.getMainDescription()
	a='<meta name="copyright" content="© '+mainauthor+' '+yearlatest+'" />'
	b='<meta name="author" lang="en" content="" />'
	c='<meta name="robots" content="Index,Follow" />'
	# preloader scripts are useful
	# <link rel="preload" href="/assets/fonts/open-sans-regular.woff2" as="font" type="font/woff2" crossorigin="">
    #<link rel="preload" href="/assets/fonts/open-sans-bold.woff2" as="font" type="font/woff2" crossorigin="">
    #<link rel="preload" href="/assets/fonts/roboto-slab-variable.woff2" as="font" type="font/woff2" crossorigin="">
	d='<meta name="description" content="'+mainDescription+'" />'
	e='<meta name="keyword" content="'+mainkeywords+'" />'
	f='<meta name="theme-color" content="darkorange">'
	g='<meta http-equiv="content-type" content="text/html; charset=utf-16" />'
	htmloutput=htmloutput+a+b+c+d+e+f+g
	htmloutput=htmloutput+'</head><body id="Top">'
	# style
	stylesheetname=config.getMainStyleSheetName() # fnlstyle.css
	secondsheetname=config.getModifiedStyleSheetName() # semantics.css
	# check second source of tags
	semtagdict=CSSmappings.getPlayMappings()
	updateCSS(stylesheetname)
	htmloutput=htmloutput+'<link rel="stylesheet" href="'+stylesheetname+'">'
	"""
	if len(semtagdict.keys())>0:
		updateCSS(shortname)
		stylesheetname=shortname+"_styles.css"
		htmloutput=htmloutput+'<link rel="stylesheet" href="'+stylesheetname+'">'
	else:
		htmloutput=htmloutput+'<link rel="stylesheet" href="'+stylesheetname+'">'
		#htmloutput=htmloutput+'<link rel="stylesheet" href="'+secondsheetname+'">' # cumulative
		# Nav
	# htmloutput=htmloutput+getPageNav()
	"""
	return htmloutput

def getPageNav():
	output='<nav class="navigation">Test navigation panel</nav>'
	return output

def getParaLinks(pgname,paramax):
	#print(pgname,paramax)
	
	anchors=""
	if (paramax>0):
		p=1
		anchors='<a href="'+pgname+'#P'+str(p)+'">'+str(p)+'</a>  '
	# step value of 5
	for x in range(0,paramax,5):
		if (x>1):
			# pgname is not needed; better for compatibility with WP to not have it
			#anchors=anchors+'<a href="'+pgname+'#P'+str(x)+'">'+str(x)+'</a>  '
			anchors=anchors+'<a href="#P'+str(x)+'">'+str(x)+'</a>  '
	plinks='<br><p class="footer">'+anchors+'</p>'
	#print(plinks)
	#exit()
	return plinks


def getNamePrefix(d):
	prefix=d[0:len(d)-len(".xml")]
	return prefix

# main()