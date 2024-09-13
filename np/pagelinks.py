
from pathlib import Path # for reading directory
from np import htmlcleaner,htmltagmaker,semantics 

global intropara
global intronums
global introlinkdict

def initTagDict():
	global introtags, intronums
	introtags=dict()
	intronums=dict()

def resetIntroTagList():
	global introtags
	introtags=dict()

def setIntroTagDict(myinput):
	global introtags
	introtags=myinput

def getIntroTagDict():
	global introtags
	return introtags

def resetIntroParaCount():
	global intropara
	intropara=0

# This was originally done as part of HTML preprocessing in npmake.  
# It makes more sense to register links once XML classification is done.
# This can take advantage of the end result of classification, rather than having to deal with text-based rules.
def registerMarkupPageLinks(mylines):
	global introlink,introlinkrev
	introlink=dict()
	introlinkrev=dict()
	count=1
	for child in mylines:
		#p="# " # Actually, this was checking the HTML not the XML
		p=semantics.getHeadingTagMarkup() # reset this or XML class with pagelinks() in text
		
		cap=len(p)
		checkstr=child[0:cap]
		if p==checkstr:
			linktext=child[cap:]
			code="PLN"+str(count)
			introlink[code]=linktext
			introlinkrev[linktext]=code
			count=count+1

def getLinkTextCode(mytext):
	global introlinkrev
	if (mytext in introlinkrev.keys()):
		output=introlinkrev[mytext]
		return output
	else:
		return mytext

# create XML tags
def processAllPageLinks(homepage):
	
	count=1
	linktext=""
	prefix="Page links:"
	global introlinkrev
	target=len(introlinkrev.keys())
	print("Link loop (",target,")")
	for a in introlinkrev.keys():
		#print(a,count,"/",target)
		pintro=htmlcleaner.getClean(a)
		pintro=pintro.strip() # remove whitespace
		code="#"+introlinkrev[a] # internal links need this for ID
		b=htmltagmaker.getIntLinkXML(pintro,code)
		# b='<intlink label = "'+pintro+'">'+code+'</intlink>'
		if (count>1):	
			linktext=linktext+', '+b
		else:
			linktext=b
			count=count+1
	# Site Map link
	content=homepage
	if ("." and "htm" not in content):
		content=content+".html"
	label=homepage
	tag=semantics.getIntLinkXMLtag()
	innertag=htmltagmaker.getXMLtag(tag,label,content)
	SiteMaplink=', '+innertag
	# , <intlink label = "SiteMap">SiteMap.html</intlink>
	linktext=linktext+SiteMaplink
	#output=opentag+prefix+linktext+closetag+"\n"
	reltag=semantics.getPageLinkRelatedClass()
	# <related>, <intlink label = "SiteMap">SiteMap.html</intlink></related>
	XMLcontent=htmltagmaker.getSimpleXMLtag(reltag,linktext)
	"""
	print(XMLcontent)
	exit()
	"""
	output=XMLcontent+"\n"
	return output

def getExtLinkXML(mytext):
	output='<extlink label = "'+mytext+'">'+mytext+'</extlink>'
	return output

def getLinkXML(mytext):
	global introlinkrev
	prefix="#"
	# For same page links the para number in same document is relevant
	if (prefix in mytext and mytext[0]==prefix):
		if (prefix in mytext):
			checkstr=mytext.strip(prefix)
			if (checkstr in introlinkrev.keys()):
				code=prefix+introlinkrev[checkstr]
				# change checkstr to mytext if you want the # in the label
				output=htmltagmaker.getIntLinkXML(checkstr,code)
				return output
	
	# If not same page then relevant PLN is in other doc.  Split filename#intro 
	elif (prefix in mytext and mytext[0]!=prefix):
		linkparts=mytext.split(prefix)
		if (len(linkparts)>0 and len(linkparts[0])>0 and len(linkparts[1])>0):
			#filestr=linkparts[0]+".html"+"#"+linkparts[1]
			code = singleLookup(linkparts[0],linkparts[1])
			if len(code)>0:
				linkbase=linkparts[0]+prefix+code
				output=htmltagmaker.getIntLinkXML(mytext,linkbase)
				return output
			else:	
				linkbase=linkparts[0]+prefix+linkparts[1] # suitable for the XML processing
				output=htmltagmaker.getIntLinkXML(mytext,linkbase)
				return output

	else:
			sitelink=mytext # +".html" no html suffix is needed for intlink XML processing
			output=htmltagmaker.getIntLinkXML(mytext,sitelink)
			return output


def getIntronumDict():
	global intronums
	return intronums

def getIntroPara(myvalue):
	global intropara
	intropara=intropara+1
	output="PLN"+str(intropara)
	return output

# Find the paragraph seq number of a specified file filename#intro
# in another document (filename ~ name.txt)
# Searches within other txt files so looks for markup not XML class codes
def singleLookup(filename,intro):
	empty=""
	mylines=openSingleSource(filename)

	if len(mylines)>0:
		count=1
		for child in mylines:
			p=semantics.getHeadingTagMarkup()
			cap=len(p)
			checkstr=child[0:cap]
			if p==checkstr:
				linktext=child[cap:]
				if (linktext==intro):
					output="PLN"+str(count)
					"""
					print("Found a match for file",filename)
					print("Intro ",intro," is ",output)
					exit()
					"""
					return output
				else:
					count=count+1
	return empty

def openSingleSource(myfile):
	p = Path('.')
	mypath=None
	filepattern='Source/**/'+myfile+'.txt'
	for child in p.glob(filepattern):
		if (len(child.name)>0):
			mypath=child
			root=opentext(mypath) # this is an array of lines
			return root

	empty=[]
	return empty

# getarray from file
def opentext(fn):
	f=open(fn,"r")
	mystring=f.read()
	f.close()
	output=[]
	output=mystring.split("\n")
	if (len(output)==0):
		output=[]
	return output