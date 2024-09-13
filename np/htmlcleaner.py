# html cleaner 7 July 2024.  Updated 6 August 2024

# Replace XML and HTML reserved characters 
def getClean(myinput):
	x=myinput.replace("&","&amp;") # always do this as first replacement
	x=x.replace('"','&quot;')
	x=x.replace("'","&apos;")
	x=x.replace('<','&lt;')
	x=x.replace('>','&gt;')
	#x=replaceSpecialChars(x)
	return x

def replaceSpecialChars(myinput):
	x=myinput.replace(")","%29")
	x=x.replace("(","%28")
	return x

# To do: scan for all other HTML invalid characters and change to long string