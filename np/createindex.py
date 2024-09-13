# createindex.py Extracted from xmlpub on 8 May 2024

from datetime import date
import xml.etree.ElementTree as ET

from np import localinfo, recursion,imagelister as IM2,config,htmltagmaker,semantics

def setCurrentPosix(myinput):
	global posixpath
	posixpath=myinput

def getCurrentPosix():
	global posixpath
	return posixpath

def setImageList(mylist):
	global imagelist
	imagelist=mylist

def getImageList():
	global imagelist
	return imagelist

def getMainIndexFooter():
	signoff=''
	mainauthor=localinfo.getMainAuthor()
	yearnow=getTodayYear()
	signoff=signoff+'<p class="footer">(c) '+mainauthor+' '+yearnow+'</p>'
	output=signoff+"</body></html>"
	return output

def getTodayYear():
	td=date.today()
	myd=td.strftime("%Y")
	return myd

def getPrefix(d):
	prefix=d[0:len(d)-len(".xml")]
	return prefix


# create index from list of files
# To do; make horizontal wrap instead of vertical
def main(filelist):
	IM2.makeImageList()
	imagelist=IM2.getImageList()
	setImageList(imagelist)
	content=createContent(filelist)
	XML_ET=makeETfromString(content)
	myhtml=makeHTMLfromET(XML_ET)
	# Write out
	indexname=config.getIndexName()
	htname="htmlpages/"+indexname+".html"
	writefile(myhtml,htname)

# This adopts an XML-based approach.  An alternative is to use scripty markdown and then process all the way through.
def createContent(filelist):
	
	td=date.today()
	todaydate=td.strftime("%A %d %B %Y")
	mainAuthor=localinfo.getMainAuthor()
	startwrap=semantics.getWrapperStartXMLTag()
	content=startwrap+'<title>Site Map</title>\n<author>'+mainAuthor+'</author>\n<date>'+todaydate+'</date>\n'
	
	filestr=content
	folderlist=[]
	defaultlist=[]
	#print(filelist)
	newfilelist=[]
	for x in filelist:
		"""
		a=x.name
		b=x.parent
		"""
		newfilelist.append(str(x))
		mysplit=str(x).split("/")
		#print("...",mysplit)
		if(len(mysplit)>1):
			folder=mysplit[1]  # mysplit[0] is 'Source'
			folderlist.append(folder)
	
	folderset=set(folderlist)
	folderlist=list(folderset)
	# Sorting sorts capitalised entries first
	folderlist=sorted(folderlist)
	newfilelist=sorted(newfilelist)
	gridlist=[]

	# default section.  Now in 'Source' folder or ignored
	for x in newfilelist:
		mysplit=x.split("/")
		if len(mysplit)==2: # assumes all 
			defaultlist.append(mysplit[1])
			newfilelist.remove(x) # avoid duplicates
	#print(newfilelist)
	filecount=len(newfilelist)
	print("Files about to process into index:",filecount)

	if (len(defaultlist)>0):
		dt="Default"
		sublist=[]
		for d in defaultlist:
			print(d)
			prefix=getPrefix(d)
			sublist.append(prefix)
		pair=[dt,sublist] # similar to a dictionary with dt as key.
		gridlist.append(pair)
	
	#print("folderlist:",folderlist)
	#print("New filelist:",newfilelist)
	
	# main grid section
	for y in folderlist:
		folderitems=[]
		pair=[]	
		for fileitem in newfilelist:
			# imagine 'Japan' is a folder and 'Japanese' too'. Can be clashes y,fileitem
			if (y in fileitem):
				mysplit=fileitem.split("/")
				#print(y,mysplit)
				if len(mysplit)>2:
					checkfolder=mysplit[1]
					xx=mysplit[2] # This is filename if inside Source/Subfolder
					# avoid nameclashes
					if (y==checkfolder):
						prefix=getPrefix(xx)
						folderitems.append(prefix)

		if len(folderitems)>0:
			pair=[y,folderitems]
			#print("new pair:",pair)
			gridlist.append(pair)
	
	# sublists = [newfilelist[x:x+rowlength] for x in xrange(0, len(newfilelist), rowlength)]

	# break HTML line every 10 entries
	rowlength=7
	
	for y in gridlist:
		heading=y[0]
		names=y[1]
		tag=semantics.getHeadingTagXML()
		row=htmltagmaker.getSimpleXMLtag(tag,heading)
		#row = '<'+tag+'>'+heading+'</intro>'
		filestr=filestr+row
		ncount=1
		for name in names:
			content=name
			label=name
			tagclass=semantics.getSiteIndexXMLTag()
			row=htmltagmaker.getXMLtag(tagclass,label,content)
			#row=htmltagmaker.getIntLinkXML(label,name)
			#row = '<listlink>'+name+'</listlink>'
			filestr=filestr+row
			if ncount % rowlength ==0:
				filestr=filestr+"<divider>{CR}</divider>" # generic XML class tag
			ncount=ncount+1

	filestr=filestr+semantics.getWrapperEndXMLTag() # '</topic>\n'
	return filestr

def makeETfromString(myinput):
	#print(filestr)
	root = ET.fromstring(myinput)
	return root

# Input is an ElementTree object (from XML)
def makeHTMLfromET(myinput):
	imagelist=getImageList()
	htmloutput=getIndexHeader('SiteMap')
	lcref=0
	for child in myinput:
		htmloutput=htmloutput+recursion.main(child,lcref)
		lcref=lcref+1
	htmloutput=htmloutput+getMainIndexFooter()
	# Footer
	return htmloutput

# Similar to getPageHeader in xmlpub
def getIndexHeader(shortname):
	htmloutput='<html><head><title>'+shortname+'</title>'
	yearlatest=getTodayYear()
	mainauthor=localinfo.getMainAuthor()
	mainkeywords=localinfo.getMainKeywords()
	mainDescription=localinfo.getMainDescription()
	a='<meta name="copyright" content="© '+mainauthor+' '+yearlatest+'" />'
	b='<meta name="author" lang="en" content="" />'
	c='<meta name="robots" content="Index,Follow" />'
	d='<meta name="description" content="'+mainDescription+'" />'
	e='<meta name="keyword" content="'+mainkeywords+'" />'
	f='<meta name="theme-color" content="darkorange">'
	g='<meta http-equiv="content-type" content="text/html; charset=utf-16" />'
	htmloutput=htmloutput+a+b+c+d+e+f+g
	htmloutput=htmloutput+"</head><body>"
	# style
	fname=fname1=config.getMainStyleSheetName()
	htmloutput=htmloutput+'<link rel="stylesheet" href="'+fname+'">'
	return htmloutput

def writefile(input,fn):
	f=open(fn,"w")
	f.write(input)
	f.close()
