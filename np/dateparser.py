# DateParser (c) 7 May 2024 Craig Duncan
# Converts loosely formatted strings with dates into datetime object. 
# Returns a re-formatted string if required

# To do: convert short dates to long dates

from datetime import date

def getTodayDateString():
	td=date.today()
	myd=td.strftime("%A %d %B %Y")
	return myd

def getPunctuation():
	punctuation=["(",")","[","]","-","/",";",",",".",":"]
	return punctuation

def getMinimalPunctuation():
	punctuation=["(",")","[","]","-","/"]
	return punctuation

def getStripChars():
	output="()[]-/;,.:"
	return output

# Formats datetime object into format required by client functions
# This inclues day of the week in as well
def getDateAsLongString(mydate):
	myd=mydate.strftime("%A, %d %B %Y")
	return myd

def getTodayYearString():
	td=date.today()
	myd=td.strftime("%Y")
	return myd

def getYearAsInt():
	yearstr=getTodayYearString()
	output=int(yearstr)
	return output

def getMonths():
	months=["January","February","March","April","May","June","July","August","September","October","November","December"]
	return months

def getLCMonthDict():
	global lcmonthdict
	return lcmonthdict

def getStartMonths():
	months=["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
	return months

def getShortMonths():
	months=["April","June","September","November"]
	return months

def getDTobject():
	global dtObject
	return dtObject

def setDTobject(myinput):
	global dtObject
	dtObject=myinput

def setupMonthDictionary():
	global mymonthdict
	global lcmonthdict
	global dtObject
	dtObject=None
	mymonthdict=dict()
	lcmonthdict=dict()
	months=getMonths()
	startmonths=getStartMonths()
	for a in startmonths:
		for b in months:
			if a in b:
				mymonthdict[a]=b
	# lc months
	for m in months:
		a=m.lower()
		lcmonthdict[a]=m


def getMonthDictionary():
	global mymonthdict
	return mymonthdict

# main function to extract date information from string
# if more than one date is present, will usually return the last date in the clause.
# attempts to fill the 'date' integer before the year, as a basic rational test
def getSingleDate(mydate):
	removals=getPunctuation()
	stripchars=getStripChars()
	months=getMonths()
	startmonths=getStartMonths()
	lcmdict=getLCMonthDict()
	monthdict=getMonthDictionary()
	output=mydate
	for p in removals:
		output=output.replace(p," ")
	
	finaloutput=""
	words=output.split(" ")
	daytemp=""
	dayother=""
	monthtemp=""
	yeartemp=""
	validYear=False
	oneValidDate=False
	message="my date input:"+mydate
	log(message)
	# if there's insufficient, don't process further
	if (len(words)<3):
		return output
	else:
		newwords=[]
		for w in words:
			w=w.strip(stripchars)
			if (w !=None and len(w)>0):
				newwords.append(w)
		words=newwords
		
		for w in newwords:
			try:
				if int(w)>0 and int(w)<=31 and validYear==False:
					daytemp=w
				elif int(w)>0 and int(w)<=31 and validYear==True:
					dayother=w # hold this just in case
				elif int(w)>1900 and validYear==False:
					yeartemp=w
					if (len(daytemp)>0 and len (monthtemp)>0):
						validYear=True
			except ValueError:
				finaloutput=finaloutput
			newmonth=""
			# handle a few variations in entry of months (lowercase, first 3)
			if (w in months):  
				newmonth=w
			elif (w[0:3] in monthdict):
				newmonth=monthdict[w[0:3]]
			elif (w in lcmdict):
				newmonth=lcmdict[w]
			if len(newmonth)>0 and len(monthtemp)==0 and validYear==False:
				monthtemp=newmonth
				# If we've already found a valid month, note it and move on
			# start date fill again if we encounter another month entry
			if (len(newmonth)>0) and validYear==True and len(dayother)>0:
				daytemp=dayother
				monthtemp=newmonth
				yeartemp="" # start date again
				validYear=False
				oneValidDate=True
	
	if (oneValidDate==False and validYear==False):
		print("I didn't find a valid date")
		print("Review:",mydate)
		exit()

	if (oneValidDate==True and validYear==False):
		print("I found a possible date but it seems you have another invalid date after it")
		print("Review:",mydate)
		exit()

	finaloutput=daytemp+" "+monthtemp+" "+yeartemp
	# test if it is still too big
	tester=finaloutput.split(" ")
	if(len(tester)==3):
		return finaloutput
	else:
		return mydate

# for external functions to call 
# returns a formatted date string back for publication
def parseDate(mydata):
	result=parseIntoDateTime(mydata)
	setDTobject(result)
	# for now, just give back the string not the datetime object
	newdatestring=""
	if (result!=None):
		newdatestring=getDateAsLongString(result)
	return newdatestring 

def checkForValidDate(mydate):
	setupMonthDictionary()
	mydate=mydate.strip(" ")
	fulldate=False
	numdate=False
	dotdate=False
	dateformat=None
	if ("/" in mydate) and mydate.count("/")==2:
		numdate=True
	# TO DO: check proximity of . too
	if ("." in mydate and ("2" in mydate or "4" in mydate)):
		temp=mydate.split(".")
		intcount=0
		if len(temp)==3:
			for a in temp:
				try:
					f=int(a)
					intcount=intcount+1
				except ValueError:
					intcount=intcount+0
			if(intcount==3):
				# to do : further checks
				message="dotdate found:"+mydate
				log(message)
				dotdate=True

	months=getMonths()
	#print(dotdate,numdate,fulldate)
	for x in months:
		if x[0:3] in mydate or x[0:3].lower() in mydate:
			message="found a date:"+mydate
			log(message)
			fulldate=True
	
	if (dotdate==False and numdate==False and fulldate==False):
		return False

	return fulldate

# main internal function
# inputs a string that should have a date of some recognisable format in it (e.g. DD MONTH YYYY) 
# returns a datetime object

def parseIntoDateTime(mydate):
	fulldate=checkForValidDate(mydate)
	months=getMonths()
	#print(dotdate,numdate,fulldate)
	
	if fulldate==True:
		result=checkForMultipleDates(mydate)
		
		# preprocess into 3 words, superficially in a date format (no semantic testing)
		mydate=getSingleDate(mydate)
		splits=mydate.split(" ")
		if len(splits)<3 or len(splits)>3:
			message="Problem with your long date:"+mydate
			for a in splits:
				print(a)
			abort(message)
		log(mydate)
		log("processing long date")
		dateformat=processLongDate(mydate)
	
	else:
		message="I can't find any date in your date field, or you have a typo:"+mydate
		abort(message)

	# TO DO: handle dot dates
	return dateformat

def checkForMultipleDates(myinput):
	months=getMonths()
	monthcount=0
	for m in months:
		if (m in myinput):
			monthcount=monthcount+1
	if monthcount>1:
		return True
	else:
		return False

def getCleanInt(myinput):
	dateint=0
	sp = getStripChars()
	myinput=myinput.strip(sp)
	
	if dateint==0:
		try:
			dateint=int(myinput)
		except ValueError:
			message="Cleaning Integer.  Problem with your date here:"+myinput
			abort(message)
	return dateint

# Carry out further processing on whether date is sensible, then convert to datetime
def processLongDate(mydate):
	g=mydate.split(" ")
	months=getMonths()
	shortMonths=getShortMonths()
	TodayYear = getYearAsInt()
	yearint=0
	mdt=g[0].strip(" ")
	dateint=0
	if (len(mdt)==0):
		abort("Date is of zero length")
	else:
		dateint=getCleanInt(mdt)
	if (len(g)>2):
		yt=g[2].strip(" ")
		yearint=getCleanInt(yt)
	else:
		message="Your date is too short:"+mydate
		abort(message)
	monstr=g[1]

	if dateint<1 or dateint>31:
		abort("Your day in your date is invalid")
	elif monstr not in months:
		message="I can't find a valid month in your date:"+mydate
		abort(message)
	elif (TodayYear-yearint>3):
		message="Your year seems too old (>3 years):"+mydate
		abort(message)
	elif int(g[2])>TodayYear:
		message="Your date is in the future:"+mydate
		abort(message)
	elif dateint>29 and monstr=="February":
		abort("Your day in February is invalid")
	elif dateint>30 and monstr in shortMonths:
		abort("Your day in your month is invalid")	
	else:
		
		monthint=getMonthAsInt(monstr)
		message="Month Int:"+str(monthint)
		log(message)
		# convert to datetime
		newdate=date(yearint,monthint,dateint)
		if (newdate>date.today()):
			abort("Your day is in the future.  Please revise.")
		log(newdate)
		log("Your date is valid")
		return newdate

# replace this with a one time setup and dictionary
def getMonthAsInt(myinput):
	months=getMonths()
	count=1
	for m in months:
		if m in myinput:
			return count
		else:
			count=count+1
	return -1

def testdate():
	date1="4 November"
	parseDate(date1)
	datestr="3 May 2024"
	parseDate(datestr)
	date2="35 November 2023"
	parseDate(date2)
	date4="15 Tuesday 2024"
	parseDate(date4)
	date5 = "13 December 2032"
	parseDate(date5)
	date6 = "13 December 2012"
	parseDate(date6)
	date7= "31 November 2024"
	parseDate(date7)
	date8= "30 February 2024"
	parseDate(date8)
	date9= "2-15 February 2024"
	parseDate(date9)
	date10="29 January 2024; 14 March 2024"
	parseDate(date10)
	date11="  22 December 2023"
	parseDate(date11)
	date12="  22 December 2023-22 March 2024(Motifs Started). and 7 April 2024"
	parseDate(date12)
	date13="  22 December 2023-22 March 2024(Motifs Started). and 7 April 2024 update"
	parseDate(date13)

def log(myinput):
	output=False
	if output==True:
		print(myinput)

def abort(myinput):
	print(myinput)
	exit() # can turn this off for logging

#testdate()