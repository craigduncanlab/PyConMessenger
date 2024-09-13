# separate module for word counting
# This version 8.4.24 (c) Craig Duncan

global wordcounter
global testcount

# This will only count the numbered paragraphs in these web pages
def updateWordCount(mytext):
	global wordcounter
	if(len(mytext)==0 or "class=" not in mytext):  # TO DO: just test first 20 chars?
		return
	result=""
	split1=mytext.split(">")
	if(len(split1)>1):
		lhs=split1[0]
		if('ss="np"' in lhs):
			rhs=split1[1]
			#print(rhs)
		else:
			return
	split2=rhs.split("<")
	if(len(split2)>=1):
		result=split2[0]
	else:
		return
	counter=result.split(" ")
	linecounter=len(counter)-1 # subtract 1 for the para number
	wordcounter=wordcounter+linecounter 
	#logCount(mytext,counter,linecounter)
	linecounter=0

def logCount(a,b,c):
	global testcount
	print(a)
	print(b)
	print(c)
	testcount=testcount+1
	if (testcount==120):
		exit()
	
	

def getWordCount():
	global wordcounter
	return wordcounter

def resetWordCount():
	global wordcounter,testcount
	testcount=0
	wordcounter=0

def testMethod():
	"""
	testoutput=htmloutput+getTestFooter(wordcounter)
	writehtml(testoutput,'testsize.html')
	filesize=Path('testsize.html').stat().st_size
	print("filesize:",filesize)
	"""
	#prefix=getNamePrefix(shortname)
	# the hypertext file is local (same level as the current page)
	