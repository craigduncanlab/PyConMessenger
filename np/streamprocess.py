# streamprocess.py 10.9.24 separated from recursion.py

from np import wordcount,localinfo,imagelister as IM,config,semantics,htmltagmaker,xmltaglist,overrides

def setLinkText(myinput):
	global linktext
	linktext=myinput

def getLinkText():
	global linktext
	return linktext

def setCurrentPosix(myinput):
	global posixpath
	posixpath=myinput

def getCurrentPosix():
	global posixpath
	return posixpath

def setupCounters():
	global figurecounter
	global paracounter
	global linktext
	linktext=""
	paracounter=0
	figurecounter=0

def resetParaCounter():
	global paracounter
	paracounter=0

def advanceParaCounter():
	global paracounter
	paracounter=paracounter+1

def getParaCounter():
	global paracounter
	return paracounter

def setParaCounter(myinput):
	global paracounter
	paracounter=myinput

def resetFigureCounter():
	global figurecounter
	figurecounter=0

# unused
def resetCounters():
	resetParaCounter()
	resetFigureCounter()

def advanceFigureCounter():
	global figurecounter
	figurecounter=figurecounter+1

def getFigureCounter():
	global figurecounter
	return figurecounter

def setFigureCounter(myinput):
	global pfigurecounter
	figurecounter=myinput

# tables the only instance where we expect significant XML inner structure
def handleTableTag(child):
	#tableclass=child.tag # assumes the tag is not 'table'.  Set in wikitable.
	line=""
	tableclass=child.get("class")
	rows=""

	for x in child:
		rowclass=x.tag
		row=rowrecursion(x) # this function is is recursion.py
		rows=rows+row
	
	line=line+htmltagmaker.getTableXML(tableclass,rows)
	return line

def handleFigureTag(myclass,utfText):
	advanceFigureCounter()
	figcounter=getFigureCounter()
	stringfig=str(figcounter)
	content="Figure "+stringfig+": "+utfText
	idattr=F+stringfig
	line=htmltagmaker.convertToHTMLParaTagWithId(idattr,myclass,content)
	return line

def handlePageLinkTag(myclass,utfText):
	idattr=xmltaglist.getIntroPara(utfText)
	content=utfText
	line=htmltagmaker.convertToHTMLParaTagWithId(idattr,myclass,content)
	return line

def handleIntroTag(utfText):
	line=""
	# already taken care of if pagelinktag
	if introtag!=pagelinktag:
		content=utfText
		line=htmltagmaker.convertToHTMLParaTag(myclass,content)	
	return line

def handleCodeTags(child,myclass,utfText):
	content=utfText
	if (myclass=="Quote"):
		content=handleNPlinks(child) # trialling this for quote
	#line=handleDecorations(line)
	line=htmltagmaker.convertToHTMLParaTag(myclass,content)	
	return line

def handleImageTags(child):
	filepath=getCurrentPosix() # this is a recursion.py function
	topicpath=str(filepath.parent)
	print(child)
	try:
		imypath=IM.handleImagePath(child,topicpath) # copy image to output if necessary
	except:
		print("there's a problem with this image:",topicpath)
		exit()
	line=IM.handleImageLinks(child,imypath)
	return line

# what if this condition is not satisfied?
def handleAuthorTags(myclass,utfText):
	line=""
	if (utfText[0:2]!="By"):
		utfText="By "+utfText
		authorText=utfText
		mainauthor=localinfo.getMainAuthor()
		content=authorText.replace("DefaultAuthor",mainauthor)
		line=htmltagmaker.convertToHTMLParaTag(myclass,content)
	return line

def handleRelatedLinkTags(child,myclass):
	line=""
	content=handleNPlinks(child)	
	line=htmltagmaker.convertToHTMLParaTag(myclass,content)
	return line

# prepare reverse order hardcoded numbers
def handleRevList(lineinput):
	listitems=lineinput.split(",")
	startitem=len(listitems)
	output=""
	for l in listitems:
		output=output+str(startitem)+". "+l+'<br>'
		startitem=startitem-1
	return output


def handleRevNumbers(myclass,utfText):
	content=handleRevList(utfText)
	line=htmltagmaker.convertToHTMLParaTag(myclass,content)
	return line

# uses the global paracounter reference
def getNextParaNum(child):
	advanceParaCounter()
	expcounter=getParaCounter()
	npattr=child.get("start") 
	if npattr!=None:
		newstart=int(npattr) # convert str to int
		if newstart>0:
			setParaCounter(newstart)
			expcounter=getParaCounter()
	return expcounter

# child must be an ET object, not a string
def handleMainPara(child,myclass):
	paranum=getNextParaNum(child)
	# allow for single spacing
	# spacing="dbl" # default
	"""
	optionSpacing=child.get("spacing")
	if (optionSpacing!=None):
		if optionSpacing=="sgl":
			myclass="np_ss"
	"""		
	# converts child object to string in process
	content=handleNPlinks(child) # these are not being handled for 'list' tags yet
	output=handleParaNumAndIndent(paranum,content,myclass)
	return output

def handleParaNumAndIndent(paranum,content,myclass):
	output=""
	isNumberingOn=config.isGlobalNumberingOn()
	if (isNumberingOn==False and overrides.isNumberingOn()==True):
		isNumberingOn=True
		isPlayNumberingOn=False
	isIndentOn=config.useFirstLineTabIndent()
	isPlayNumberingOn=config.isPlayNumberingOn()
	if isPlayNumberingOn==False:
		if isNumberingOn==True:
			idattr='P'+str(paranum)
			content=str(paranum)+". "+content # else no change, but counter keeps running
			output=htmltagmaker.convertToHTMLParaTagWithId(idattr,myclass,content)
		elif isIndentOn==True:
			content='&emsp;'+content  # no numbers in view of browser but they are in HTML tags
			idattr='P'+str(paranum)
			output=htmltagmaker.convertToHTMLParaTagWithId(idattr,myclass,content)
		else:
			idattr='P'+str(paranum)
			output=htmltagmaker.convertToHTMLParaTagWithId(idattr,myclass,content)
	else:
		idattr='P'+str(paranum)
		ptab='&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'
		multiplier=int(len(content) / 3)
		spacer=""
		cap=26-multiplier
		for a in range(0,cap):
			spacer=spacer+ptab
		if paranum%5==0:
			content=content+' '+spacer+' ('+str(paranum)+") "
		 # else no change, but counter keeps running
		output=htmltagmaker.convertToHTMLParaTagWithId(idattr,myclass,content)
	return output

# now handles internal links 28.8.24
def handleBulletListItem(child,myclass):
	#content=getTextFromTag(child)
	content=handleNPlinks(child)
	optionSpacing=child.get("spacing")
	classtype="list"
	if (optionSpacing!=None):
		if optionSpacing=="sgl": # not dbl
			classtype="list_ss"
	line=htmltagmaker.convertToHTMLParaTag(classtype,content)
	#line='<p class="'+classtype+'">'+utfText+"</p>"
	return line

# This checks for <extlink> and <intlink> inside the node and converts to HTML anchors.  
# No further recursion is performed.
def handleNPlinks(child):
	expcounter=getParaCounter()
	output=child.text # first part of the text, up to anchor tag etc
	if output is None:
		output=""
	#print(output)
	mylinktext=""
	newlink=""
	intlinktag=semantics.getIntLinkXMLtag()
	extlinktag=semantics.getExtLinkXMLtag()

	for y in child:
		linkattr=""
		content=""
		if y.text!=None:
			content=y.text
		if y.tag!=extlinktag and y.tag!=intlinktag:
			output=output+content
		if y.tag==extlinktag:
			linklabel=content
			urllink=content
			myclass=extlinktag

			# check label text for text to appear in web page
			linkattr=y.get("label")
			if linkattr!=None:
				newlink=linkattr
				if(len(newlink)>0):
					linklabel=newlink
			output=output+htmltagmaker.getURLlink(urllink,myclass,linklabel)
			# add the tail of the tag after we find the tag
			if y.tail!=None:
				output=output+y.tail

		if y.tag==intlinktag:
			#pagename text inside an <intlink label ="x">pagename</intlink>
			pagelinkref=y.text 
			if (pagelinkref==None):
				print("no valid link ref. NP:",expcounter)
				print(child.text)
				exit()
			
			# checkformat suits HTML
			urllink=getValidRef(pagelinkref)
			linklabel=y.get("label")

			# default if no label supplied
			if linklabel==None:
				linklabel=urllink
			
			# Check for internal (sasme) page links.
			PageLink=False
			if urllink[0:1]=="#":
				PageLink==True
				#linklabel="^"+linklabel.strip("#")
				linklabel=linklabel.strip("#")
				#print(urllink,linklabel)
				#exit()

			myclass=intlinktag
			output=output+htmltagmaker.getURLlink(urllink,myclass,linklabel)
			
			# add the tail of the tag after we find the tag
			if y.tail!=None:
				output=output+y.tail

	return output

def getTextFromTag(child):
	if (type(child)==str):
		return child
	utfText=child.text # if this is empty it throws an error in next line
	if utfText==None:
		utfText=""
	return utfText

def handleSiteIndexListItem(child,myclass):
	utfText=getTextFromTag(child)
	# specify class as list?
	link=utfText+'.html'
	output=htmltagmaker.getURLlink(link,myclass,utfText)
	if myclass=="listlink":
		output=output+'&nbsp'
	return output


# only used once
def getValidRef(link):
	relhtml=link

	rel1=link.strip() # remove whitespace
	samePage=False
	if ("#" in rel1):
		pararef=rel1.split("#")
		if (len(pararef)>1):
			relhtml=pararef[0]
			para=pararef[1]
			# same page links
			if len(relhtml)==0 and len(para)>0:
				samePage=True
				relhtml=rel1 # i.e. no change.  keeps #.  no need to # + para
		elif (len(pararef)==1):
			relhtml=pararef[0]
			para=""
		#for a in pararef:
		#	if "Close" in a:
		if samePage==False:	
			if ("html" not in relhtml and "htm" not in relhtml):
				if len(pararef)>1:
					relhtml=relhtml+".html"+"#"+para
		"""
			else:
				relhtml=relhtml+"#"+para
		else:
			relhtml="#"+para # put # back for internal links
		"""
	else:
		if ("html" not in link and "htm" not in link):
			relhtml=relhtml+".html"

	return relhtml


# A row here is inside a tag called <glossitem>
def rowrecursion(child):
	output=""
	cells=""
	myclass=child.tag
	output=output+'<tr class="'+myclass+'">'
	# line=line+'<table class="'+myclass+'">'+cells+'</table>'
	cells=""
	for r in child:	
		content=cellrecursion(r)
		cells=cells+content
	output=output+cells
	output=output+"</tr>"
	return output

# whatever the class of the innermost tags is will be retained in the final table
# the outer XML tags are <glossary> and <glossitem>
def cellrecursion(child):
	output=""
	utfText=""
	myclass=""
	myclass=child.tag
	mywidth=child.get("width")
	if(mywidth==None):
		mywidth=""
	content=child.text # if this is empty it throws an error in next line
	#print(myclass)
	#print(utfText)
	# remove chars not suited to browsers or the dot holding xml open
	# ling is a table/table row
	if (content==None or content=="."):
		content="&nbsp;"
	# handle any links inside table cells
	linktaglist=semantics.getLinkXMLtags()
	for x in child:
		xclass=x.tag
		if (xclass in linktaglist):
			#print("Found intlink in table")
			content=handleNPlinks(child)
			#print(utfText)
			# this captures internals in table
	paraHTML=htmltagmaker.convertToHTMLParaTag(myclass,content) 
	if (len(mywidth))==0:
		line='<td>'+paraHTML+'</td>'
	else:
		line='<td width="'+mywidth+'">'+paraHTML+'</td>'
		#print(line)
		#exit()
	output=output+line
	# if attributes, we could use child.attrib to get them
	# print(child.tag, child.attrib, child.text)
	#for y in child:
	#	output=output+recursion(y)
	return output

def main(child,myclass,utfText):
	
	line=""
	
	# classes of tags that will be interpreted as same XML tags
	sd=semantics.getReservedXML()
	tagtype=semantics.getTagClass(myclass)
	match tagtype:
		case "tabletag":
			line=handleTableTag(child) # involves further recursion
		case "siteindextag":
			line=handleSiteIndexListItem(child,myclass)
		case "figuretag":
			line=handleFigureTag(myclass,utfText)
		case "pagelinktag":
			line=handlePageLinkTag(myclass,utfText)
		case "introtag": 
			line=handleIntroTag(utfText)
		case "codetags":
			line=handleCodeTags(child,myclass,utfText)
		case "imagetags":
			line=handleImageTags(child)
		case "authortags":
			line=handleAuthorTags(myclass,utfText)
		case "relatedlinktag":
			line=handleRelatedLinkTags(child,myclass)
		case "pagelinkinserttag": # this is in recursion.py
			line=getLinkText() # already preformatted when recursion is first called
		case "revnumbers":
			line=handleRevNumbers(myclass,utfText)
		case "defaultoption":
			line=handleMainPara(child,myclass)	# recursion.py
		case "bulletlist":
			line=handleBulletListItem(child,myclass) # recursion.py
		case "generic":
			utfText=handleNPlinks(child) #recursion
			line=htmltagmaker.convertToHTMLParaTag(myclass,utfText)

	return line
