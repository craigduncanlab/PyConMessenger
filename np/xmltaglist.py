# xmltaglist 26.7.24

from np import config,htmlcleaner,htmltagmaker,semantics
# root is the XML (ET) object

global intropara
global pagelinkclass

def initialise():
	global intropara
	global pagelinkclass
	intropara=0
	pagelinkclass=semantics.getDefaultPageLinkClass() # is this set before this is called?

def setPageLinkClass(myinput):
	global pagelinkclass
	pagelinkclass=myinput

"""
# resetIntroParaCount and pagelink class
def initialise():
	global intropara
	global pagelinkclass
	intropara=0
	pagelinkclass=semantics.getDefaultPageLinkClass() # is this set before this is called?
	#setPageLinkClass(linkclass)
	#registerXMLpagelinks(root,pagelinkclass) # this does this at start of file
	# linkstext for page links in XML (if required)
	output=getPageLinksSection(pagelinkclass)
	return output	
"""
def getPageLinkClass():
	global pagelinkclass
	return pagelinkclass

# if page links are on they appear after the header section
# this means XML processing has to be interrupted before first few meta lines
def main(root,tagname):
	registerXMLpagelinks(root,tagname)
	homepage=config.getIndexName()
	# optional page links section
	myintrolinks = ""
	if (config.arePageLinksOn()==True):	
		myintrolinks=processAllPageLinks(homepage)
	print(myintrolinks)

def registerXMLpagelinks(root,tagname):
	global pagelinkclass
	if (tagname!=pagelinkclass):
		print("This document is not using the default page link class:",pagelinkclass)
		print("It is using:",tagname)
		exit()
	global introlink,introlinkrev
	introlink=dict()
	introlinkrev=dict()
	taglister=[]
	lc=1
	count=1
	for child in root:
		myclass=child.tag
		mytext=child.text
		#htmloutput=htmloutput+recursion.main(child,lc)
		row=[lc,myclass,mytext]
		#print(row)
		if myclass==tagname:
			idlabel="PLN"+str(count)
			row2=[count,idlabel]+row # put another entry at start
			taglister.append(row2)
			introlink[idlabel]=mytext
			introlinkrev[mytext]=idlabel
			count=count+1
		lc=lc+1

def getLinkTextCode(mytext):
	global introlinkrev
	if (mytext in introlinkrev.keys()):
		output=introlinkrev[mytext]
		return output
	else:
		return mytext

# called from recursion
def getPageLinksSection(myclass):
	setPageLinkClass(myclass)
	homepage=config.getIndexName()
	# optional page links section
	output = ""
	if (config.arePageLinksOn()==True):	
		output=processAllPageLinks(homepage)
	return output

# create XML tags
def processAllPageLinks(homepage):
	count=1
	linktext=""
	prefix="Page links:"
	global introlinkrev
	target=len(introlinkrev.keys())
	#print("xtl link loop (",target,")")
	myclass=getPageLinkClass()  # This should be something other than the author's class?
	for a in introlinkrev.keys():
		#print(a,count,"/",target)
		linklabel=htmlcleaner.getClean(a)
		linklabel=linklabel.strip() # remove whitespace
		urllink="#"+getLinkTextCode(a) # introlinkrev[a] 
		# Create directly in HTML
		b= htmltagmaker.getURLlink(urllink,myclass,linklabel)
		if (count>1):	
			linktext=linktext+', '+b
		else:
			linktext=b
			count=count+1
	# 

	# Site Map link
	urllink=homepage
	if ("." and "htm" not in urllink):
		urllink=urllink+".html"
	linklabel=homepage
	innertag=htmltagmaker.getURLlink(urllink,myclass,linklabel)
	SiteMaplink=', '+innertag
	linktext=linktext+SiteMaplink
	wrapperclass=semantics.getPageLinkRelatedClass()
	output=htmltagmaker.convertToHTMLParaTag(wrapperclass,linktext)+"\n"
	return output

def getIntroPara(myvalue):
	global intropara
	intropara=intropara+1
	output="PLN"+str(intropara)
	return output

def handleTagSettings(myargs):
	if (len(myargs)>0):
		pagelinkclass=myargs[0]
		setPageLinkClass(pagelinkclass)
		# saves page link long enough to insert into the XML
		print("page link class saved:",pagelinkclass) 