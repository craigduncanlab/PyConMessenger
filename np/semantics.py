# introduce custom semantic tags for pipeline. 13.7.24 Craig Duncan
# At the moment, the single letter codes are required by the parser
# The RHS tag labels can vary, but in doing so the CSS may lose its link
# The solution to completely flexible RHS (to do) is to create the CSS file in the html file as per these values.

from np import htmlcleaner,extlinks,config,defaultpara

# This includes all tags except d and l tags.
def handleStartXMLBlock(child,blocktype):
	output=""
	listd=getNoListBlockList()
	sd=getSemanticBlockCodesDict()
	if blocktype in listd:
		cleantext=htmlcleaner.getClean(child[2:])
		sdc="<"+sd[blocktype]+">"
		output=sdc+cleantext #+"\n"	
	return output

# This is a start
def handleListXMLtag(content):
	listxml=getListTagXML()
	paraclass="dbl"
	if config.isSingleSpaced()==True:
		paraclass="sgl"
	
	tag1=listxml+' spacing="'+paraclass+'"'
	endtag=listxml
	output=makeMismatchedXMLTag(tag1,content,endtag)
	
	return output

def makeMismatchedXMLTag(tagone,content,tagtwo):
	output='<'+tagone+'>'+content+'</'+tagtwo+'>\n'
	return output

# Function to process links and add a {CR} for the XML so they appear in tags as such		
# These are not 'data' blocks. Processes all tags except d and l tags.
# These are mid-block only (no end tags)
def handleMidBlockXMLTags(child,blocktype):
	output=""
	listd=getNoListBlockList()
	if blocktype in listd: # like q tags etc
		cleaned=htmlcleaner.getClean(child)
		if ("<--" in cleaned):
			print("Cleaning did not work in mid block")
			exit()
		output=extlinks.replaceLinks(cleaned)+'{CR}' # "\n"
		#output=output+cleaned+"{CR}" #"\n"
	return output

# makes and end XML to conclude the {CR} type blocks
# TO DO: treat these formatting-only blocks as data, then process the entire block?
# This includes all tags except d and l tags.
def handleEndBlockXMLTag(content,blocktype):
	output=""
	listd=getNoListBlockList()
	if (blocktype in listd):
		sd=getSemanticBlockCodesDict()
		sdc="</"+sd[blocktype]+">\n"
		cleaned=htmlcleaner.getClean(content[2:])
		output=output+cleaned+sdc
	return output

def getQuoteXMLTag():
	sd=getSemanticBlockCodesDict()
	output=sd["q"] # find markup key, then return the XML equivalent
	return output

def handleQuoteXMLTag(content):
	xmlclass=getQuoteXMLTag()
	output=getSimpleXMLtag(xmlclass,content)
	return output

def getBlockTagXML(blocktype,content):
	sd=getSemanticBlockCodesDict()
	if (blocktype not in sd.keys()):
		print("Your blocktype",blocktype,"is not in list of valid blocktypes. Aborting.")
		exit()
	tag=sd[blocktype]
	output=getSimpleXMLtag(tag,content)
	return output


def getSimpleXMLtag(tag,content):
	output='<'+tag+'>'+content+'</'+tag+'>'
	return output

# Standard set of p classes invoked by block codes or related functions
# These form basis of XML semantic tags and CSS requirements
# Called, indirectly, by recursion.py
# Called by CSSmappings.py to add additional CSS code with tag names added/replaced.

# All interpreted block codes, but excludes 'd' as that is purely for data
def getSemanticBlockCodesDict():
	sd=dict()
	sd["a"]="authorref"
	sd["c"]="code"
	sd["e"]="example"
	sd["i"]="image"
	sd["l"]="list"
	sd["n"]="numlist" # should be parseable ?
	sd["q"]="Quote"
	sd["s"]="scene"
	sd["# "]="intro" # The hash-tag headings
	return sd

# tags in xml that require CR between the main tags
# to do.  use this function instead of globals
def getCodeTags():
	output=["code","example","Quote"]
	return output

def getRevNums():
	return ["revlist"]

# Used in npmake for tag checking. Includes "d" and "# "
def getAllBlockTagTypes():
	sd=getSemanticBlockCodesDict()
	output=list(sd.keys())
	output.append("d")
	return output

# These are the codes that are a subset of SemanticDict and are written in markup as a+ a- etc
def getMidBlockList():
	output=getNoListBlockList()  
	output.append("l")
	return output

# do not include d or l here: these are semantic tags.  Should match all other block types
def getNoListBlockList():
	sd=getSemanticBlockCodesDict() #was ["c","e","q","n","a","s"]  
	output=list(sd.keys())
	output.remove("l")
	output.remove("# ")
	return output

def getDataTag():
	output=["d"]
	return output

def getReservedXML():
	sd=dict()
	sd["img"]="image"
	sd["np"]="np" # reserved word?
	sd["list"]="list"
	sd["title"]="title"
	sd["date"]="date"
	sd["concept"]="concept"
	sd["author"]="author"
	# These are internal XML items.  TO DO:separate
	sd["pl"]="pagelinks" # default page link class
	sd["wrapper"]="topic" # This is the outermost tag in the XML file.
	sd["related"]="related" # standard wrapper tag for links
	sd["figcaption"]="figcaption"
	sd["table"]="standard" # not negotiable at this stage.  See recursion
	sd["footer"]="footer"
	return sd

def LinkCodesToMarkup():
	old=MarkupToLinkCodes()
	sd=dict()
	for o in old.keys():
		sd[o.value]=o.key
	return sd
	
# Hash tags used for headings, like in H1 in HTML and # in markdown
# Used in npmake to obtain the markup keys.  Equivalent for XML is getXMLHeading
def getHeadingTagMarkup():
	output="# "
	return output

def getFigureTagMarkup():
	output="#f "
	return output

def getMainParaTagMarkup(): # sd["np"] 
	sd=getReservedXML()
	output=sd["np"]
	return output

def getAuthorTagMarkup():
	output="author"
	return output

def getHeadingFigureTagMarkup():
	part1=getHeadingTagMarkup()
	part2=getFigureTagMarkup()
	output=[part1,part2]
	return output

def getListTagXML():
	sd=getReservedXML()
	output=sd["list"]
	return output

# This is the standard HTML tag.  Not negotiable
def getTableTag():
	output="table"
	return output

def getTableClass():
	sd=getReservedXML()
	sk=getTableTag()
	output=sd[sk]
	return output

def getHeadingTagXML():
	sd=getSemanticBlockCodesDict()
	sk=getHeadingTagMarkup()
	output=sd[sk]
	return output

def getDefaultPageLinkClass():
	sd=getSemanticBlockCodesDict()
	sk=getHeadingTagMarkup()
	output=sd[sk]
	return output

# used in recursion when cycling table cells
def getLinkXMLtags():
	part1=getIntLinkXMLtag()
	part2=getExtLinkXMLtag()
	output=[part1,part2]
	return output

def getExtLinkXMLtag():
	output="extlink"
	return output

def getIntLinkXMLtag():
	output="intlink"
	return output

def getSiteIndexXMLTag():
	output="listlink"
	return output

# general tags file.  This is the label for XML and p class for 'image' in imagelister, recursion modules
def getImageXMLTag():
	sd=getReservedXML()
	output=sd["img"] # "image","img"
	return output

# used in imagelister as a p class for image captioning
def getImageXMLCaptionTag():
	output='caption'
	return output

# used in recursion for XML tags that will be matched to a table
def getTableXMLTags():
	output=["tablestandard","table","glossary","ling"]
	return output

# used in both npmake and recursion to track figcaption to XML and then to a p class.
def getFigureCaptionXML():
	# sd["figcaption"]
	output="figcaption"
	return output

# used once in recursion
def getPageLinkRelatedClass():
	sd=getReservedXML()
	output=sd["related"]
	return output

def getPageLinkInsertClass():
	sd=getReservedXML()
	output=sd["pl"]
	return output

# used in npmake for preparing final XML final with wrapper tags
def getWrapperStartXMLTag():
	sd=getReservedXML()
	sdw=sd["wrapper"]
	output="<"+sdw+">\n"
	return output

def getWrapperEndXMLTag():
	sd=getReservedXML()
	sdw=sd["wrapper"]
	output="</"+sdw+">\n" # end of topic/wrapper
	return output

def setupCodeLookupDict():
	code1=getHeadingTagMarkup()
	xmlcode1=getHeadingTagXML()
	code2=getFigureTagMarkup()
	xmlcode2=getFigureCaptionXML()
	mydict=dict()
	mydict[code1]=xmlcode1
	mydict[code2]=xmlcode2 
	return mydict

# used in npmake. Input code is the markup code not the XML label
def getXMLfromLabelContent(code,content):
	codeclass=getXMLCodeFromMarkupCode(code)
	output="<"+codeclass+">"+content+"</"+codeclass+">\n"
	return output

def getXMLCodeFromMarkupCode(code):
	output="defaultXMLtag"
	mydict=setupCodeLookupDict()
	if (code in mydict.keys()):
		output=mydict[code]
	return output

# checks longest first
def getImagePrefixList():
	output=["IC:","IA:","ID:","I:"]
	return output

# checks longest first
def getPrefixList():
	part1=getImagePrefixList()
	part2=["R:","L:"]
	prefixlist=part1+part2
	heading=getHeadingTagMarkup()
	prefixlist.append(heading)
	figure=getFigureTagMarkup()
	prefixlist.append(figure)
	return prefixlist

def getMasterTagDict():
	pagelinktag=getDefaultPageLinkClass() # xmltaglist.getPageLinkClass() 
	authortags=getAuthorTagMarkup()
	tabletag=getTableTag()
	imagetags=getImageXMLTag()
	siteindextag=getSiteIndexXMLTag()
	figuretag=getFigureCaptionXML()
	introtag=getHeadingTagXML() # These are the class of pagelinks too?
	relatedlinktags=getPageLinkRelatedClass()
	numbertag=getMainParaTagMarkup() # sd["np"] # what about 'explanation'?
	pagelinkinserttag=getPageLinkInsertClass()
	tagclass=getMainParaTagMarkup()
	codetags=getCodeTags()
	dpclass=defaultpara.getDefaultClass() # getDefaultClass()
	revnumbers=getRevNums()
	
	b=dict()
	b["tabletag"]=[tabletag]
	b["siteindextag"]=[siteindextag]
	b["figuretag"]=[figuretag]
	b["pagelinktag"]=[pagelinktag]
	b["introtag"]=[introtag]
	b["imagetags"]=[imagetags]
	b["authortags"]=[authortags]
	b["relatedlinktag"]=[relatedlinktags]
	b["pagelinkinserttag"]=[pagelinkinserttag]
	b["revnumbers"]=revnumbers
	b["codetags"]=codetags
	b["defaultoption"]=dpclass+tagclass
	return b

def getTagClass(myclass):
	b=getMasterTagDict()
	for category in b.keys():
		listy=b[category]
		if myclass in listy:
			return category
	# nothing found so far

	if myclass !='a': # ignore HTML anchors
		if myclass==getListTagXML():
			return "bulletlist"
		else:
			return "generic"
	# default
	return "generic"

# SUPERSEDED?
# these are left until the final HTML creation.  Not used for XML
# currently not used (separate function to CSS mappings)
def getSemanticSubstitutions(code):
	# print("code",code)
	if (config.isSemanticSubstitionOn()==False):
		return code
	srw=getReservedXML()
	sd=config.getSubstitutes()
	# make this independent of changes to main semantic dictionary
	#print("sd:",sd)
	if (code in sd.keys()):
		return sd[code]
	else:
		if code in srw.keys():
			return srw[code]
		else:
			print("your markup code:",code," is not detected in custom or reserved dict")
			exit()
