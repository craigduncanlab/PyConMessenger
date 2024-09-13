# htmltagmaker 22 July 2024

from np import semantics,config

# used in recursion, xmltaglist
def convertToHTMLParaTag(myclass,content):
	myclass=semantics.getSemanticSubstitutions(myclass) # not effect at present
	output='<p class="'+myclass+'">'+content+'</p>'
	return output

# used in recursion
def convertToHTMLParaTagWithId(idattr,myclass,content):
	myclass=semantics.getSemanticSubstitutions(myclass)
	output='<p id="'+idattr+'" class="'+myclass+'">'+content+'</p>'
	return output

# for pagelinks
def getIntLinkXML(label,content):
	#tag="intlink" # link to semantic.py or config.py
	tag=semantics.getIntLinkXMLtag()
	output=getXMLtag(tag,label,content)
	return output

def getSimpleXMLtag(tag,content):
	output='<'+tag+'>'+content+'</'+tag+'>'
	return output

def makeXMLForLineClass(myinput,tagclass):
	content=myinput
	output=getSimpleXMLtag(tagclass,content)
	return output

def getXMLtag(tag,label,content):
	output='<'+tag+' label = "'+label+'">'+content+'</'+tag+'>'
	return output

# used in recursion. HTML output
def getInternalLink(content):
	myclass=semantics.getIntLinkXMLtag() # doesn't need to be same.  Is currently.
	replaces=["https://","http://",".html",".org.au",".org",".com.au",".com",".net.au",".net"]
	newcontent=content
	for a in replaces:
		newcontent=newcontent.replace(a,"")
	output=getURLlink(content,myclass,newcontent)
	return output

# used in recursion
def getURLlink(urllink,myclass,linklabel):
	output='<a href="'+urllink+'" class="'+myclass+'">'+linklabel+'</a>'
	return output

# XML prep.  Uses class rather than label attribute
def getTableXML(tableclass,content):
	tabletag=semantics.getTableTag()
	output='<'+tabletag+' class="'+tableclass+'">'+content+'</'+tabletag+'>'
	return output

# HTML output
def getTableStart():
	tabletag=semantics.getTableTag()
	tblclasstype=semantics.getTableClass()
	stylesheetname=config.getMainStyleSheetName() # fnlstyle.css
	myitem='<'+tabletag+' class="'+tblclasstype+'"><headerline>'
	return myitem

def formatWordInLine(child,automatchword,newformat):
	output=""
	# only handles exact case swap for now