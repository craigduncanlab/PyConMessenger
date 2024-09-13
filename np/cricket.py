# Created 30.8.24 to add some cricket specific output formatting to tables
# used with 'cprint' command
# relies on the scripts markings for bold (!* *!)

from np import datafunctions

# mydata input is a list of lists
def makeIndexedTableHeader(mydata):
	output=mydata
	if len(mydata)>0:
		firstitem=mydata[0]
		gmax=len(firstitem)
		headrow=[]
		for h in range(0,gmax):
			headrow.append("!*"+str(h)+"*!")
		output=[headrow]+mydata # add two lists of lists produces one list of lists
	return output

def addBatterStats(mydata):
	output=[]
	newcol=[]
	# add a column for row numbers
	firstrow=[" "]+mydata[0]
	row=firstrow
	row.append("!*BF*!")
	row.append("!*4s*!")
	row.append("!*6s*!")
	row.append("!*Runs*!")
	row.append("!*Outs*!")
	row.append("Wd")
	row.append("Nb")
	row.append("B")
	row.append("Lb")
	output.append(row)
	# if this is only used with cprint we can start with begincol=2 (otherwise it would be 1, not 0)
	begincol=2
	beginrow=1 # ignore header row
	for x in range(beginrow,len(mydata)):
		# add rownumber ref
		row=[str(x)]+mydata[x]
		bf=0
		n4=0
		n6=0
		nwd=0
		nbnum=0
		outnum=0
		byenum=0
		legnum=0
		# start second col to ignore refs and names
		for cell in range(begincol,len(row)):
			bc=row[cell].lower()
			if(bc!=" "):
				bf=bf+1
			if(bc=="4"):
				n4=n4+1
			if(bc=="6"):
				n6=n6+1
			if(bc=="x"):
				outnum=outnum+1
			if("w" in bc and "wd" not in bc):
				numb=bc.strip("w")
				try:
					nbint=int(numb)
					if(nbint==0):
						nbint=1
				except:
					nbint=1
				nwd=nwd+nbint
			if("nb" in bc and "r" not in bc):
				numnb=bc.strip("nb")
				try:
					nobint=int(numnb)
					if(nobint==0):
						nobint=1
				except:
					nobint=1
				nbnum=nbnum+nobint
			if("b" in bc and "lb" not in bc and "nb" not in bc):
				numnb=bc.strip("b")
				try:
					nobint=int(numnb)
					if(nobint==0):
						nobint=1
				except:
					nobint=1
				byenum=byenum+nobint
			if("lb" in bc):
				numnb=bc.strip("b")
				try:
					nobint=int(numnb)
					if(nobint==0):
						nobint=1
				except:
					nobint=1
				legnum=legnum+nobint

		numruns=datafunctions.prepareSumForCricketList(begincol,row)
		print(numruns)
		runs=str(int(numruns))
		print(runs)
		row.append(str(bf))
		row.append(str(n4))
		row.append(str(n6))
		row.append(runs)
		row.append(str(outnum))
		row.append(str(nwd))
		row.append(str(nbnum))
		row.append(str(byenum))
		row.append(str(legnum))
		output.append(row)
	return output
