# ext links 17 July 2024.  Updated 24 September 2024.

from np import semantics,dateparser

def replaceLinks(mystring):
	#print("input:")
	#print(mystring)
	linklist=findExtLinks(mystring)
	"""
	if (len(linklist)>0):
		for a in linklist:
			print(a)
	"""	
	mystring=replaceLinksFromList(linklist,mystring)
	return mystring

def replaceLinksFromList(linklist,mystring):	
	
	if (len(linklist)>0):
		for x in linklist:
			y=getExternalLink(x)
			#print("Ext",y)
			mystring=mystring.replace(x,y)
		#print("output:")
		#print(mystring)
		#exit()
	return mystring

def findExtLinks(inputstr):
	sub="http"
	subend=" "
	subends=[" ",";","\n",")","]","'","(","[","{","}"]
	outcome=0
	position=0
	results=[]
	intermediate=""
	maxlen=len(inputstr)
	basestring=inputstr	
	while (outcome!=-1):
		intermediate=""
		substring=basestring[position:]
		firstindex=substring.find(sub)
		cap=0
		outcome=firstindex
		# found opening link mark
		if firstindex!=-1:
			newsub=substring[firstindex:]
			#find2=newsub.find(subend)
			find2=-1
			internalresult=[]
			subtokens=[] # subends actually used
			for e in subends:
				ff=newsub.find(e)
				# find all matches in subend list, then find earliest in document.
				if find2==-1 and ff>0:
					internalresult.append(ff)
					subtokens.append(e)
			if (len(internalresult)>0):
				find2=min(internalresult)
				xlen=0
				for a in range(0,len(internalresult)-1):
					if (find2==internalresult[a]):
						xlen=len(subtokens[a])
				#print(internalresult,find2)
				subend=newsub[find2:find2+xlen] # all are length 1 except 1
			outcome=find2
			# found ending link mark
			if (find2!=-1):
				intermediate=substring[firstindex:firstindex+find2]
				# ensure that random / dividers aren't caught
				if (len(intermediate)>2 and "://" in intermediate):
					results.append(intermediate)
				cap=position+firstindex+find2
				position=cap
				# End of file
				if position>=(maxlen-1):
					outcome=-1		
		else:
			# print("Found start link but no other end link in file")
			outcome=-1
	
	return results
	"""
def getExternalLink(mylink):
	output='<extlink label = "'+mylink+'">'+mylink+'</extlink>'
	print(output)
	exit()
	return output

"""
# Called by npmake handleCodePrefix().  PGFlag may be set by page level gutenberg override.
# Conversion of extlink tags takes place in handleNPlinks in streamprocess.py
def getExternalLink(ext1,PGFlag):
	if PGFlag==True:
		output=getTextOnlyLink(ext1)
	else:
		output=getFullHTMLExtLink(ext1)
	return output

def getTextOnlyLink(ext1):
	sda=semantics.getMainParaTagMarkup()
	#sda=sd["defaultpara"] # wrapper for links
	output="<"+sda+">External Link:"
	mylist=handleDataSplit(ext1)
	if (len(mylist)>1):
		mylabel=mylist[0] # not used here
		mylink=mylist[1]
		mydate=""
		if (len(mylink)<1 or type(mylink)==None):
			abortOnError("fault in external link (extlinks.py)")
		if ("www"==mylink[0:3]):
			mylink="http://"+mylink # needed for browser links.  Not https?
		if len(mylist)==3:
			mydate=" (accessed "+mylist[2]+")"
		b='('+mylink+')'+mydate
		output=output+b
	output=output+"</"+sda+">\n"
	# <>ExtLink:[VIQAI (accessed 30 July 2024)]https://viqsolutions.com.au/solutions/aiassist/</>
	return output

def getFullHTMLExtLink(ext1):
	sd=semantics.getReservedXML()
	sda=sd["related"] # wrapper for links
	output="<"+sda+">ExtLink:"
	mylist=handleDataSplit(ext1)
	if (len(mylist)>1):
		mylabel=mylist[0]
		mylink=mylist[1]
		if (len(mylink)<1 or type(mylink)==None):
			abortOnError("fault in external link (extlinks.py)")
		if ("www"==mylink[0:3]):
			mylink="http://"+mylink # needed for browser links.  Not https?
		if len(mylist)==3:
			mylabel=mylist[0]+" (accessed "+mylist[2]+")"
		b='<extlink label = "'+mylabel+'">'+mylink+'</extlink>'
		output=output+b
	output=output+"</"+sda+">\n"
	return output

def handleDataSplit(mystring):
	output=[]
	print(type(output))
	print(mystring)
	if (mystring.count(",")<=2):
		output=mystring.split(",")
	else:
		nc=mystring.count(",")
		mysplits=[]
		for n in range(0,nc):
			mysplits.append(",")
		#print("mysplits:",mysplits)
		found=handleSplitFunction(mysplits,mystring)
		#print("found:",found)
		output=handleRowSplits(found,mystring)
		output=convertLinkToThree(output)
	if len(output)==0:
		print("Something has gone wrong with data split for:",mystring)
		exit()
	return output

def convertLinkToThree(mylist):
	output=[]
	#print(mylist)
	if (len(mylist)>3):
		print("Fixing a link with additional commas:",mylist)
		start=mylist[0]
		end=mylist[-1]
		newdate=dateparser.checkForValidDate(end)

		print(end,newdate)
		
		middle=""
		for a in range(1,len(mylist)-2):
			#print(a)
			#print(mylist[a])
			middle=middle+mylist[a]+","
		middle=middle+mylist[len(mylist)-2]
		output=[start,middle,end]
		if (newdate==False):
			newend=middle+","+end
			output=[start,newend]
			print(output)
			return output
		#print(output)
		#exit()
		return output
	elif (len(mylist)==3):
		print("mylist",mylist)
		end=mylist[-1]
		newdate=dateparser.parseIntoDateTime(end)
		
		return mylist
	else:
		print(len(mylist))
		print(mylist)
		print("Converting link to three in extlinks. End case halt.")
		exit()
		return mylist

# copied from datafunctions.py
def handleRowSplits(found,d):
	output=[]
	prev=-1
	count=1
	for f in found:
		if f>prev and count<=len(found):
			#print(prev+1,f)
			substring=d[prev+1:f].strip(" ")
			#print(substring)
			count=count+1
			prev=f
			output.append(substring)
	if (len(d)>found[-1]):
		#print(prev,len(d))
		substring=d[prev+1:].strip(" ")
		#print(substring)
		output.append(substring)
	if len(output)==0:
		print("External link.  Something has gone wrong with data(row) split for:",mystring)
		exit()
	return output


# copied from datafunctions.py
def handleSplitFunction(mysplits,d):
	found=[]
	cap=0
	for a in mysplits:
		substring=d[cap:len(d)]
		idx=substring.find(a) # find first values only
		store=cap+idx # (stores one before delimiter)
		if idx!=-1 and (store not in found):
			found.append(store)
		else:
			found.append(-1)
		cap=store+1
	return found

def convertXMLtoHTML(mylabel):
	output='<a href="'+mylabel+'" class="external">'+mylabel+'</a>'
	return output

def test1():
	argument=""" I was hoping to smile my way out  of training but shit science leaves me unconvinced. #ABCclickbait. {CR}https://www.abc.net.au/news/2024-06-08/why-smiling-as-you-run-can-improve-your-time/103873582 <This message was edited> More links. {CR}https://www.abc.net.au/funnies <This message was edited>"""
	results=findExtLinks(argument)
	if (len(results)>0):
		for a in results:
			print(a)
	gg=replaceLinksFromList(results,argument)
	print(gg)

#test1()