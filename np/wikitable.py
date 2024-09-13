# wiki fast list table algo
# By Craig Duncan 5.4.24.  See README for more information on how script commands are interpreted
# To produce XML tags suitable for transform into HTML using the recursion module.
# separated this from data functions 1.8.24

from np import semantics, htmltagmaker

# 3. Call this to process a command line in a txt file that wants a table
# send the output back to calling function outside this module	
def process(mydict,myargs,activecommand):
	output=handleTableColOrRow(mydict,myargs,activecommand)
	return output

# option is command; myarg is list of data labels
def handleTableColOrRow(mydict,myarg,option):
	counts=[]
	headers=[]
	name=""
	d=[]
	if len(myarg)>0:
		name=myarg[0]
	for a in myarg: # maybe just two cols
		if a in mydict:
			extractData=mydict[a]
			#print("extractData:",extractData)
			counts.append(len(extractData)) # entries in vector/col
			headers.append(a)
			d.append(extractData)
			#print("d = dictionary with new entry now:",d)
		else:
			print("Your tablecol/row argument ",a, " is not in your dictionary:")
			exit()
	mc=max(counts)
	# Final two options. TO DO: Use lists in command.py
	match option:
		case "tablecol" | "tprint" | "tablecoltotals":
			outputStr=runTableColCommand(headers,d,mc)
		case "tablerow":
			outputStr=runTableRowCommand(headers,d,mc)

	return outputStr

def runTableColCommand(headers,d,mc):
	output=""
	tdclass='vert'
	#headers[hcount]
	
	myitem=htmltagmaker.getTableStart()

	classtype='stdrow'
	# header row
	for h in headers:
		myitem=myitem+'<header>'+h+'</header>'
	myitem=myitem+'</headerline>'
	# rest of table
	for counter in range(0,mc,1):
		#myitem=myitem+'<tr class="'+classtype+'">'
		myitem=myitem+'<line>'
		hcount=0
		pclass=""
		if counter % 2 == 0:
			pclass="col1"
		else:
			pclass="pretty"
		for xd in d:
			content=""
			if (counter<len(xd)):
				content=str(xd[counter])
			else:
				content="{CR}"
			myitem=myitem+'<'+pclass+'>'+content+'</'+pclass+'>'
			hcount=hcount+1
		myitem=myitem+"</line>"
	myitem=myitem+"</table>\n"
	output=myitem
	return output

# TO DO:This needs to be updated to match TableCol
def runTableRowCommand(headers,d,mc):
	output=""
	myitem=htmltagmaker.getTableStart()

	classtype='stdrow'
	 #<body><link rel="stylesheet" href="'+stylesheetname+'">'
	#print(d)

	# rowcount
	rowcount=0
	for listrow in d:
		# class not headers[rowcount]
		classtype='stdrow'
		headertype="header"
		myitem=myitem+'<tr class="'+headertype+'"><td>'+headers[rowcount]+'</td>'
		# rest of row
		#print(listrow)
		counter=0
		for xd in range(0,mc,1):
			#print(xd,counter,len(xd))
			if (counter<len(listrow)):
				myitem=myitem+'<td class="'+headers[rowcount]+'">'+listrow[xd]+"</td>"
			else:
				cr="{CR}" # &nbsp;
				myitem=myitem+'<td>'+cr+'</td>'
			counter=counter+1
		myitem=myitem+'</tr>'
		rowcount=rowcount+1
	myitem=myitem+"</table>\n"
	output=myitem
	return output

# input must already be a rectangular data set
def makeTPrintTable(mydata):
	output=""
	#myitem=htmltagmaker.getTableStart()
	myitem='<table class="standard">'
	classtype='stdrow'
	headertype="header"
	rowclasses=["col1","pretty"]
	rowcount=0
	count=0
	pixels=getPixelString(mydata,0)
	for listrow in mydata:
		rowclass=rowclasses[count % 2]
		if count==0:
			rowclass=headertype
		myitem=myitem+'<tr class="'+rowclass+'">'
		rowlen=len(listrow)
		count=count+1
		cellcount=1
		for cell in listrow:
			if count==1 and cellcount==1:
				myitem=myitem+'<td class="'+rowclass+'" width="'+pixels+'">'+cell+'</td>'
				# width="50" etc if name column?
			else:
				myitem=myitem+'<td class="'+rowclass+'">'+cell+'</td>'
			cellcount=cellcount+1
		myitem=myitem+'</tr>'
	myitem=myitem+"</table>\n"
	output=myitem
	return output

def getPixelString(mydata,mycol):
	namemax=0
	for listrow in mydata:
		name=listrow[mycol]
		if(len(name)>namemax):
			namemax=len(name)
	if(namemax>20):
		namemax=20
	pixels=str(namemax*9)
	return pixels

# Cricket specific table
# input must already be a rectangular data set
# This is for XML.  Re-interpreted in recursion.py
def makeCPrintTable(mydata):
	output=""
	#myitem=htmltagmaker.getTableStart()
	myitem='<table class="standard">'
	classtype='stdrow'
	headertype="header"
	rowclasses=["col1","pretty"]
	rowcount=0
	count=0
	pixels=getPixelString(mydata,1)	
	for listrow in mydata:
		rowclass=rowclasses[count % 2]
		if count==0:
			rowclass=headertype
		myitem=myitem+'<tr class="'+rowclass+'">'
		rowlen=len(listrow)
		count=count+1
		widthFlag=False
		cellcount=1
		for cell in listrow:
			# width="50" etc if name column?
			if count==1 and cellcount==2:
				myitem=myitem+'<td class="'+rowclass+'" width="'+pixels+'">'+cell+'</td>'
			# Runs, out etc.  Allow 4 chars for !**!
			elif count==1 and len(cell)>6:
				jtext=cell.lstrip("!*")
				jtext=cell.rstrip("*!")
				testwidth=len(jtext)*8
				if(testwidth)>36:
					testwidth=36
				pixels=str(testwidth)
				myitem=myitem+'<td class="'+rowclass+'" width="'+pixels+'">'+cell+'</td>'
			else:
				myitem=myitem+'<td class="'+rowclass+'">'+cell+'</td>'
			cellcount=cellcount+1
			
		myitem=myitem+'</tr>'
	myitem=myitem+"</table>\n"
	output=myitem
	return output


def makeList(eData):
	output="<table>"
	for a in eData:
		output=output+"<tr>"+a+"</tr>"
	return output

def checkTableCommand(myline):
	output=False
	commandlist=getCOMlist()
	for cc in commandlist:
		mycom=myline[0:len(cc)]	
		if mycom.lower()==cc.lower():
				return True
	return output

