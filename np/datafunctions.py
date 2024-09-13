# data functions 31.7.2024
# datablock processing 1.8.24

from np import imagelister

def initialise():
	global mydict # to ensure accessible outside these local functions
	global datalist
	global rowlists
	global rownames
	rowlists=[]
	rownames=[]
	datalist=[]
	setSplitDefaults()

# 1. Call this once per txt document to reset dictionary
def reset():
	global mydict
	mydict=dict()
	setSplitDefaults()

def initialiseDataList():
	global datalist
	datalist=[]
	rowlists=[]
	rownames=[]

def append(myinput):
	global datalist
	datalist.append(myinput)

# Do not override in built python functions by naming this get or set!
def getDataList():
	global datalist
	return datalist

def setDataList(myinput):
	global datalist
	datalist=myinput

def getDataDict():
	global mydict
	return mydict

def getDictionary():
	global mydict
	return

def printDict():
	global mydict
	print(mydict)

def getDictionaryVariable(name):
	if(len(name)==0):
		print("You requested a dictionary variable (in datafunctions.py) but supplied no info.")
		exit()
	global mydict
	if (name in mydict.keys()):
		return mydict[name]
	else:
		print("Requested data variable, but",name,"not in dictionary")
		print("Dictionary status:",mydict)
		exit()

def setDictionaryVariable(mykey,myvalue):
	global mydict
	mydict[mykey]=myvalue # this can be a list of entries

def setSplitDefaults():
	global headermem
	global splitsmem
	headermem=[]
	splitsmem=[]

def setHeaderMem(myinput):
	global headermem
	headermem=myinput

def setSplitsMem(myinput):
	global splitsmem
	splitsmem=myinput

def getHeaderMem():
	global headermem
	if (len(headermem)==0):
		print("Your file hasn't set any headers for data splitting")
		exit()
	return headermem

def getSplitsMem():
	global splitsmem
	if (splitsmem==None or len(splitsmem)==0):
		print("Your file hasn't set any splits delimiters for splitting")
		exit()
	return splitsmem

# input a is a block of text with line separators
# output is a small dictionary with one entry.
# the dictionary key is the first line item (label/variable name) and balance is the value
def convertDataListToDict(a):
	#print("converting data list:",a)
	#exit()
	output=dict()
	firstrow=a[0]
	if "(" in firstrow and ")" in firstrow:
		b=getClean(firstrow)
		if len(a)>=1:
			output[b]=a[1:]
	else:
		print("Problem with data list name:",firstrow)
		exit() # this only exits here if called from another python file, but doesn't terminate the main thread

	return output

# removes both round and square brackets so they will process the same i.e. header[] or header()
def getClean(mydata):
	output=mydata.strip("[")
	output=output.strip("]")
	output=output.strip("(")
	output=output.strip(")")
	output=output.strip(" ") # just this, not - etc
	return output

def convertDataBlock(a):
	global mydict
	dd=dict()	
	tiny=convertDataListToDict(a)
	for x in tiny:
		mydict[x]=tiny[x]
	return mydict

# This assumes a single block with a name in the first row, which then needs to be split
def handleDataSplits(myargs):
	extractData=getDataVariableForSplit(myargs)
	name=myargs[0]
	#print("This is the datablock:",extractData)
	checkDataForCommands(extractData)
	"""
	print("Checked data...")
	print(extractData)
	"""
	
	d=extractData

	#print("HandleDataSplits:",titles,mysplits,name,d,mc)
	runDataSplitCommand(name,d)
	"""
	if (name=="mytest"):
		print("aborting",mysplits)
		exit()
	"""

# This assumes a list of entries as input, not a single entry
def getDataVariableForSplit(myargs):
	try:
		name=myargs[0]
	except:
		print("Your arguments ",myargs," have an error")
		exit()
	try:
		if (name) not in mydict.keys():
			print("Trying to get data variable. I can't find",name,"in the dictionary")
			exit()
	except:
		print("Your data item ",name," gives an error. May not be in the dictionary.")
		exit()
	
	extractData=mydict[name] # data source already in dictionary
	d=extractData
	mc=len(extractData)
	# no output, requires tablecol() to be run afterwards
	if (mc==0):
		mysplits=getSplitsMem() # this checks if there is a split delimtere
		titles=getHeaderMem()
		print("problem with your data acquisition for name:",name)
		print("titles,splits:",titles,mysplits)
		print("data:",d)
		print("dictionary:",mydict)
		exit()
	#print("This is the datablock:",extractData)
	checkDataForCommands(extractData)
	return d

def checkDecoration(mylist,coltotal):
	dolcount=0
	perccount=0
	dolstring="!*$"+str(coltotal)+"*!"
	perstring="!*"+str(coltotal)+"%*!"
	boldstring="!*"+str(coltotal)+"*!"
	for a in mylist:
		if "$" in a:
			dolcount=dolcount+1
		elif "%" in a:
			perccount=perccount+1
	if dolcount>0 and perccount==0:
		return dolstring
	if dolcount==0 and perccount>0:
		return perstring
	elif (dolcount==max(dolcount,perccount) and dolcount>0):
		return dolstrong
	elif (perccount==max(dolcount,perccount) and perccount>0):
		return perstring
	return boldstring

# iterate through columns, calculate sums, add to each column, return as updated dictionary
def getSmallDictWithColTotals(myargs):
	print(myargs)
	output=[]
	mynewdict=dict()
	mylist=[]
	for a in myargs:
		newlist=[] # a new list each time
		mylist=getDictionaryVariable(a)
		checkNumeric=checkNumericList(mylist)
		if (checkNumeric==True):
			coltotal=prepareSumForList(mylist)
			coltotal=checkDecoration(mylist,coltotal)
			
		else:
			coltotal=" "
		mylist.append(coltotal)
		mynewdict[a]=mylist

	if (len(mynewdict.keys())<len(myargs)):
		print("Problem calculating totals for all columns")
		exit()
	else:
		return mynewdict

# TO DO: prepare functions that give totals of rows, columns etc as part of the 
# assumed operating environment : if data is defined, properties are available
# Then the function calls can be property return functions
def handleSumAcross(myargs):
	output=getRowSumVector(myargs)
	print("Row sum vector:",output)

def handleRowTotals(myargs):
	output=[]
	#output=getRowSumVector(myargs)
	#mylist=handleDataRowRips(myargs)
	rowsums=getRowSumVector(myargs)
	global rownames
	if len(rownames)==len(rowsums):
		print("Row names found.")
		#print(rownames,rowsums)
		
	else:
		print("Invalid/Insufficient rownames")
		rownames=[]
		for a in range(0,len(rowsums)):
			rowtext=str(a+1)+"."
			rownames.append(rowtext)

	# update dictionary
	setDictionaryVariable("auto_ref",rownames)
	setDictionaryVariable("auto_total",rowsums)
	for a in range(0,len(rownames)):
		pair=[rownames[a],rowsums[a]] # round brackets is set?
		output.append(pair)
		print(rownames[a],rowsums[a])
	#print(output)
	# output is a set of paired lists, with rowname/ref, total
	# store in dictionary as 'auto_refs' and 'auto_total' so immediately available for tablecol?
	# should a tablecol(auto_ref,auto_total) command invoke this function?
	return output
	
def getRowSumVector(myargs):
	rowsplits=handleDataRowRips(myargs)
	# To do: command to take in row names separately...
	#print("Getting row totals:...")
	count=1
	output=[]
	for x in rowsplits:
		rowtotal=prepareSumForList(x)
		output.append(rowtotal)
		#print(count,":",rowtotal)
		count=count+1
	return output # TO DO: store this in a way it can be obtained for any table named Y
	#print("HandleDataSplits:",titles,mysplits,name,d,mc)
	#name=myargs[0]
	#runDataSplitCommand(name,d)

def handleRowsForTPrint(myargs):
	print("handling rows for tprint...")
	rowsplits=handleDataRowRips(myargs)
	count=1
	output=[]
	rowlengths=[]
	for x in rowsplits:
		rowlengths.append(len(x))
	maxcols=max(rowlengths)
	#print("Maxcols:",maxcols)
	#print(rowsplits)
	for row in rowsplits:
		myrow=[]
		if (len(myrow)<maxcols):
			loop=maxcols-len(row)
			for a in range(0,loop):
				myrow.append(" ")
		row=row+myrow
		if(len(row)<maxcols):
			print("Error filling up row to maximum in handleRowsForTPrint")
			exit()
		output.append(row)

	return output

# rows are split, then resulting lists are appended to a master list
def handleDataRowRips(myargs):
	name=myargs[0]
	#print(name)
	d=getDataVariableForSplit(myargs) # needs a list, returns a list
	#print("Returned library for ",name,"is",d)
	commacount=0
	splitter=diagnoseDelim(d)
	rowsplits=getRowSplits(d,splitter)
	global rowlists
	rowlists=rowsplits
	checkRowNames(rowlists)
	return rowsplits

def checkNumericList(mylist):
	count=0
	for x in mylist:
		e=stripDecorations(x)
		print(e)
		try:
			e=float(e)
			count=count+1 # works for numbers
		except:
			count=count
			# could just return False here.  
	if count==0:
		return False
	# requires all entries non-zero
	if count==len(mylist):
		return True
	else:
		return False

def checkRowNames(myrows):
	global rownames
	names=[]
	for a in myrows:
		firstitem=a[0]
		try:
			exceptiontest=int(firstitem) # this fails for strings
		except:
			# print("exception. found string")
			if isinstance(firstitem,str):
				names.append(firstitem)
			#print("I'm having trouble check row names for:",a)
			#exit()
	if (len(names)==len(myrows)):
		#print("seems to be a names list")
		#print(names)
		#print(len(names))
		unique=set(names)
		if (len(unique)<len(names)):
			print("There is some duplication in the row names (not storing)")
			print(unique)
			rownames=[]
			output=[]
		else:
			output=names
			rownames=output
	else:
		#print("no names?", names)
		rownames=[]
		output=[]
	
	return output


# find most likely delimiter present in all rows of table
def diagnoseDelim(rowslist):
	output=""
	options=["comma","space","bar"]
	splitcounts=dict()
	totalcounts=dict()
	for o in options:
		splitcounts[o]=0
		totalcounts[o]=0
	for a in rowslist:
		commacount=0
		adder=0
		for o in options:
			shortdelim=swapSplitCodes(o)
			if (shortdelim in a):
				#print("found:",o)
				splitcounts[o]=splitcounts[o]+1
		#print(a,splitcounts)
	
	for o in options:
		if (splitcounts[o]==len(rowslist)):
			totalcounts[o]=totalcounts[o]+1
	countmax=max(totalcounts.values())
	for x in totalcounts.keys():
		if int(totalcounts[x])==countmax:
			output=x
	if(len(output)==0):
		print("Could not diagnose splitter for:",rowlist)
		exit()
	return output

# input should be list of row entries, not yet divided further
# each row should have a consistent delimeter?
# first entry should be row names?
def getRowSplits(myinput,delim):
	dl=swapSplitCodes(delim)
	output=[]
	if isinstance(myinput,list):
		for row in myinput:
			rowsplit=row.split(dl)
			if len(rowsplit)>0:
				output.append(rowsplit)
		return output
	else:
		print("row split is not a list")
		print(myinput)
		exit()

def prepareSumForList(mylist):
	intcount=0
	intlist=[]
	for e in mylist:
		e=prepareFloat(e)
		#print("e:",e)
		if(e!=None) and (isinstance(e,int) or isinstance(e,float)):
			e=float(e)
			intcount=intcount+1
			intlist.append(e)
	"""
	if (len(extractData)>len(intlist)):
		print("The numerical entries are less than the size of the data list")
		print("found",len(intlist),"numbers")
	"""
	mynum=sum(intlist)
	mysum=round(mynum,2)
	#print("Sum:",mysum)
	return mysum


# option to start run count at a particular column to right of indexes, names
def prepareSumForCricketList(col,mylist):
	intcount=0
	intlist=[]
	for cell in range(col,len(mylist)):
		e=mylist[cell]
		e=prepareFloat(e)
		if(e!=None) and (isinstance(e,int) or isinstance(e,float)):
			e=float(e)
			intcount=intcount+1
			intlist.append(e)
	mynum=sum(intlist)
	mysum=round(mynum,0) # integers in cricket
	return mysum

# this looks up the input argument as a stored variable
def handleSumCommand(tokens):
	extractData=getDataVariableForSplit(tokens) # only uses the first item in list
	if len(extractData)==1:
		print("You want to sum a single entry? Variable:", name)
		print("Aborting for now")
		exit()
	output=prepareSumForList(extractData)
	return output

def prepareInteger(x):
	e=stripDecorations(x)
	output=int(e)
	return output

# remove units
def stripDecorations(x):
	e=""
	e=x.strip(" ")
	e=e.lstrip("$")
	e=e.rstrip("%")
	return e

def prepareFloat(x):
	e=stripDecorations(x)
	try:
		if (float(e)>0):
			#print(type(e))
			e=float(e)
		if isinstance(e,int) or isinstance(e,float):
			e=float(e)
		else:
			e=0.0
	except:
		e=float(0)
	return e

def checkDataForCommands(mydata):
	titles=[]
	#print("Checking data for legacy commands...")
	metarows=mydata[0:3]
	#print(metarows)
	for line in metarows:
		hdl=len("header[")
		tagprefix=line[0:hdl]
		if ("header[" in line or "splits[" in line):
			print("Commands need to be removed from data in this file")
			print(metarows)
			exit()

# collate data columns for a new table
def collateDataForArgs(xx,mycom):
	dd=mycom[len(xx):len(mycom)]
	#print(dd)
	myarg=processDataArg(dd,mycom)
	
	return myarg

# recover the args 'key' list after checking they are valid variables in this doc
def processDataArg(myArg,myCom):
	global mydict
	aa=getClean(myArg)
	#print(len(aa))
	#print("Arg:",aa)
	argslist=aa.split(",")
	tablecommands=["tablecol","tablerow","tablesplit"]
	for xa in argslist:
		if (myCom in tablecommands):
			if (xa not in mydict):
				print("Data argument:",xa," for "+myCom+" invalid")
				print("my current dictionary entries are:")
				print(mydict)
				exit()
			else:
				d=0
				#print("Data argument:",xa,"in tablerow checks out")
	return argslist

# valid delimiters list.  Input is an array
def getSplitList(myargs):
	output=[]
	for x in myargs:
		if " " in x:
			ylist=x.split(" ")
			for y in ylist:
				myswap=swapSplitCodes(y)
				if (len(myswap)>0):
					output.append(myswap)
		else:
			myswap=swapSplitCodes(x)
			if (len(myswap)>0):
				output.append(myswap)

	# TO DO: introduce case and default values, specific reporting
	if len(output)<len(myargs):
		print("At least one of your split arguments is not recognised")
		print("Expected titles/cols:",myargs)
		print("Working delimiter(s):",output)
		exit()
	return output

def swapSplitCodes(x):
	output=""
	if (x=="space"):
		return " "
	if (x=="equals"):
		return "="
	if (x=="bar"):
		return "|"
	if (x=="lcurly"):
		return "("
	if (x=="rcurly"):
		return ")"
	if (x=="lsquare"):
		return "["
	if (x=="rsquare"):
		return "]"
	if (x=="csv" or x=="comma"):
		return ","
	if (x=="colon"):
		return ":"
	if (x=="dot"):
		return "."
	if (x=="semicolon" or x=="scolon"):
		return ";"
	if (x=="all"):
		return "all"
	if (len(output)==0):
		print("Could not match a split (delimiter) code for:",x)
		exit()
	return output	

def runDataSplitCommand(name,datacol):
	
	mysplits=getSplitsMem() # this checks if there is a split delimtere
	# exclude title from the 'split' arguments
	#print(titles,mysplits,name,datacol,mc)
	if (len(mysplits)==0):
		mysplits=["comma"] # defaults
	splits=getSplitList(mysplits)
	#print("splits:",splits)
	# use the split delimiters to create a split list for each row
	newmaster=createSplitMasterData(datacol,splits)
	# create new transposed column data and store in dictionary for this file
	
	if len(newmaster)==0 or newmaster==None:
		print("problem with your data acquisition from table")
		print("Datacol:",datacol)
		exit()
	newtitles=generateNewData(name,newmaster)
	titles=getHeaderMem()
	if len(newtitles)<len(titles):
		print("Your data splitting did not work")
		print("Expected titles/cols:",titles)
		print("working delimiter(s):",mysplits)
		print("Titles returned:",newtitles)
		exit()
	"""
	print("NewTitles in RunDataSplit:",newtitles)
	global mydict

	print("Updated dictionary:",mydict)
	exit()
	"""

# redundant?
def getNewCommandForSplit(titles):
	mxsplit=len(titles)
	newcommand="tablecol("
	for a in range(0,mxsplit):
		newcommand=newcommand+titles[a]
		if (a<mxsplit-1):
			newcommand=newcommand+","
	newcommand=newcommand+")"
	return newcommand

# The found list is an array of indexes for splitting the string (d)
def handleRowSplits(found,d):
	output=[]
	prev=-1
	count=1
	for f in found:
			if f>prev and count<=len(found):
				# print(prev+1,f)
				substring=d[prev+1:f].strip(" ")
				#print(substring)
				count=count+1
				prev=f
				output.append(substring)
	if (len(found)>0):
		if (len(d)>found[-1]):
			#print(prev,len(d))
			substring=d[prev+1:].strip(" ")
			#print(substring)
			output.append(substring)
	return output

def handleSplitFunction(mysplits,d):
	found=[]
	cap=0
	if ("all" in mysplits):
		#print("Found All")
		#print(mysplits)
		tempsplits=mysplits.copy() # avoid permanent changes to input list
		tempsplits.remove("all") # doesn't return anything
		if len(tempsplits)!=1:
			print("your split function had an 'all' but I can't find a token")
			exit()
		elif len(tempsplits)>1:
			print("you have more than one split function char for 'all':",temp)
			exit()
		else:
			mysplitchar=tempsplits[0]
			for x in range(0,len(d)):
				test=d[x]
				if (d[x]==mysplitchar):
					found.append(x)
			#print("I've found these index for the found string:",found)
			
			return found

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

# split each data row in a left to right sequence for the delimiters
# args: mysplits=delimiters, datacol = list of data
def createSplitMasterData(datacol,mysplits):
	maxsplit=0
	masterdata=[]
	#print(datacol)
	#print(len(datacol))
	bugStop=False
	for d in datacol:
		#print(d)
		#print("mysplits before:",mysplits)
		found=handleSplitFunction(mysplits,d)
		#print("mysplits after found:",mysplits)
		z=handleRowSplits(found,d)
		#print("mysplits after z:",mysplits)
		if len(z)>maxsplit:
			maxsplit=len(z)
		masterdata.append(z)
		
	# fill up any empty cells in a row with blank to keep alignment
	newmaster=[]
	for v in masterdata:
		vv=len(v)
		cc=v
		if (len(v)<maxsplit):
			#print(v)
			tt=maxsplit-vv
			for ad in range(0,tt):
				cc.append(".")
		newmaster.append(cc) # v would be updated as well
	
	return newmaster


def generateNewData(name,mdata):
	
	if(mdata==None or len(mdata)==0):
		titles=getHeaderMem()
		print("Problem with your data in wikitable data")
		print("name,titles:",name,titles)
		exit()
	maxset=len(mdata[0]) # take first row as number of cols
	newdata=[]
	for a in range(0,maxset):
		v=[]
		newdata.append(v)
	# transpose to individual data lists
	md=len(mdata)
	for m in range(0,md):
		for a in range(0,maxset):
			row=mdata[m]
			cell=row[a]
			newdata[a].append(cell)

	# create some default titles for new columns	
	newtitles=getNewTitles(name,maxset)
	#print("newtitles:",newtitles)
	# store in global dictionary
	if (maxset>len(newtitles)):
		print("Titles list length: ",len(newtitles))
		print("First row:",mdata[0])
		titles=getHeaderMem()
		print(titles)
		print("Smaller than width of table,",maxset," in:",name)
		exit()
	for gg in range(0,maxset):
		mykey=newtitles[gg]
		listdata=newdata[gg]
		myitem=dict()
		myitem[mykey]=listdata
		global mydict
		mydict[mykey]=myitem[mykey]

	return newtitles
		

def getNewTitles(name,maxset):
	titles=getHeaderMem()
	newtitles=titles
	colcnt=len(titles)
	if (colcnt==maxset):
		return titles

	hdrnum=maxset-colcnt
	if(len(newtitles)==0):
		newtitles.append(name)
	for a in range(1,hdrnum+2):
		newheader=name+"_"+str(a)
		newtitles.append(newheader)

	return titles

"""
def getCOMlist():
	output=["datasplit","header","splits"]	
	return output
"""

# This assumes the function only supplies named 'data' variable names as args, 
# and that they have been defined in the text file ahead of the function call
# Throws error if this is not correct.

# command lines
def handleHeaderCommand(myargs):
	setHeaderMem(myargs)
	
def handleSplitCommand(myargs):
	setSplitsMem(myargs)
		
# do not loop on 2nd arguments at this stage (they are delimiters, not data)
def handleDataSplitCommand(myargs):
	print("Found data split:",myargs)
	handleDataSplits(myargs)
	global mydict
	print("Finished splits.Current dict:",mydict)
	exit()

def testSplitFunction():
	reset()
	"""
	mydata=getData5()
	db.convertDataBlock(mydata)
	output='tablesplit(Title,lcurly,colon,comma)'
	"""
	mydata=getData6()
	convertDataBlock(mydata)
	output='tablesplit(Title,colon,lsquare,comma)'
	b=process(output)
	print(b)
	

# Test function only
def testFunctions():
	# 
	reset()
	# load some data
	a=getData1()
	a2=getData2()
	a3=getData3()
	# convert into memory
	convertDataBlock(a)
	convertDataBlock(a2)
	convertDataBlock(a3)
	"""
	# output what is in memory
	for y in mydict:
		print(mydict[y])
	"""
	# run some commands
	b=getCommands()
	# get output
	output = process(b)
	# print output
	print(output)