# navlinks created 18.6.24.  Updated 7 August 2024.

from datetime import date
from np import dateparser,config,semantics
# localinfo

def getNavLinks(myinput):
	if "," in myinput:
		print("Removed commas in navlink.")
		myinput.replace(",","") # clean	
	a=myinput.strip()
	output='<intlink label = "'+a+'">'+a+'</intlink>'
	return output

def getMetaTagList():
	tagdict=dict()
	tagdict["T"]="title"
	tagdict["D"]="date"
	tagdict["A"]="author"
	tagdict["C"]="concept"
	tagdict["R"]="related"
	tagdict["F"]="related"
	tagdict["B"]="related"
	return tagdict

# Trim header rows if there is a definite non-meta row found within first 10
def checkHeaderSection(myrows):
	endMark=semantics.getHeadingTagMarkup()
	lenMark=len(endMark)
	output=[]
	for row in myrows:
		if row[0:lenMark]==endMark:
			return output

		elif len(row)>0 and ":" not in row:
			return output
		else:
			output.append(row)
	return output

# default top section content
def getMetaTagContent(code,headrows):
	tc=code+":"
	cap=len(tc)
	content=""
	linkslist=["R","F","B"]
	# captures only one line matching the tag (first)
	for h in headrows:
		if (":" in h):
			myrowsplit=h.split(":",1)
			#print("splits:",myrowsplit)
			if (myrowsplit[0]==code):
				if (code in linkslist):	
					cc=myrowsplit[0]
					ct=myrowsplit[1]
					#print("split code,content:",cc,ct)
					content=handleheader(cc,ct)
				else:
					content=myrowsplit[1]
	return content

def handleheader(code,content):
	output=""
	#print("handleHeader:",code,content)
	if (code=="R" and len(content)>0):
		output=getRelatedLinks(content)
		if ("Related" in content):
			content=content.replace("Related:","Links:")
	if (code=="F" and len(content)>0):
		#print("Detected F")
		output=getNavLinks(content)
		#output="Forward:"+content
	if (code=="B" and len(content)>0):
		#print("Detected B")
		output=getNavLinks(content)
		#output="Back:"+content
	return output

def getTodayDateString():
	td=date.today()
	myd=td.strftime("%A %d %B %Y")
	return myd

def getDateFromHeaderRow(myinput):
	content=dateparser.parseDate(myinput)
	if len(content)>0:
		setDateFlag(True)
	else:
		setDateFlag(False)
	datefield=dateparser.getDTobject() # stored during parseDate
	storeDateContent(datefield) 
	return content

def setDateFlag(myinput):
	global dateFlag
	dateFlag=myinput

def getDateFlag():
	global dateFlag
	return dateFlag

def storeDateContent(myinput):
	global dateForIndex
	dateForIndex=myinput

def getDateContent():
	global dateForIndex
	return dateForIndex

# Extracts items including date
# When date is present it reformats data and also stores data/article for index
# headrows must be a list not a string
def getXMLHeaderTags(headrows):
	global dateForIndex
	dateForIndex=date.today() # reset for each document
	setDateFlag(False)
	today=getTodayDateString()
	author="DefaultAuthor"
	metalist=getMetaTagList()
	#print(metalist.keys())
	metastring=""
	for h in headrows:
		if len(h)<=2 and len(h)>0:
			print("Error in header row")
			print("Your field is empty in this header code:",h)
			exit()

	headerdict=dict()
	navdict=dict()
	navlist=["F","B"]
	for code in metalist.keys():
		mycontent=getMetaTagContent(code,headrows)
		#print("content:",mycontent)
		if (len(mycontent)>0):
			if code not in navlist:
				headerdict[code]=mycontent
			else:
				navdict[code]=mycontent
	"""
	print(headerdict)
	print(navdict)
	exit()
	"""
	if ("D" in headerdict.keys()):
		datefield=headerdict["D"]
		if (len(datefield)>0):
			datecontent=getDateFromHeaderRow(datefield)
			# still a string.  dateparser stores datetime silently
			headerdict["D"]=datecontent
	#else:
		# This could set any blank date as today.  Remove or simply don't set.
		# headerdict["D"]=None  # getDateFromHeaderRow(today)

	if "A" not in headerdict.keys():
		headerdict["A"]=author

	for code in headerdict.keys():
		content=headerdict[code]
		tag=metalist[code]
		opentag="<"+tag+">"
		closetag="</"+tag+">"
		newtag=opentag+content+closetag+"\n"
		headerdict[code]=newtag
		metastring=metastring+newtag 

	metastring=metastring+getNavXML(navdict)

	mystring=metastring
	
	return mystring

# forward and back line(s)
def getNavXML(navdict):
	output=""
	forward=""
	back=""
	newtag=""
	if ("F" in navdict.keys()):
		forward=navdict["F"]
	if "B" in navdict.keys():
		back=navdict["B"]
	if len(back)>0:	
		newtag=newtag+"Prev:"+back+" "
	if len(forward)>0:
		newtag=newtag+"Next:"+forward
	if len(newtag)>0:
		output="<navlink>"+newtag+"</navlink>"+"\n"
	return output

def getRelatedLinks(rel1):
	#indexname=getIndexName()
	mylist=rel1.split(",")
	homepage=config.getIndexName() # e.g. SiteMap
	mylist.append(homepage)
	"""
	print(mylist)
	exit()
	"""
	#output='Related:<intlink label="SiteMap">'+indexname+'</intlink>, '
	output='Related:'
	if (len(mylist)>0):
		count=1
		for a in mylist:
			a=a.strip() # remove whitespace
			if (len(a)>0):
				b='<intlink label = "'+a+'">'+a+'</intlink>'
				if count>1:
					output=output+', '+b
				else:
					output=output+b
				count=count+1
	return output