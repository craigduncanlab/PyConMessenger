# Overrides 14.8.24
# Designed to allow writer to override settings in current document

global isNumbering
global isGutenberg

# should be reset each document
def initialise():
	global isNumbering
	global isGutenberg
	isNumbering=False
	isGutenberg=False

def setNumberingOn(myinput):
	global isNumbering
	if (myinput==True or myinput==False):
		isNumbering=myInput

def isNumberingOn():
	global isNumbering
	return isNumbering

def handleParagraphCommands(myargs):
	global isNumbering
	validvalues=["numbers","number","essay","default","normal"]
	name=""
	try:
		name=myargs[0]

	except:
		if (name) not in validvalues:  #is this case sensitive or not?
			print("Problem with paragraph arguments")
			print("Your argument is not a valid option :",name)
			exit()
		else:
			print("Your data item ",name," is valid but there is an error")
			exit()
	if ("number" in name):
		name="number"
	if ("default" in name or "normal" in name):
		name="default"

	match name:
		case "default":
			isNumbering=False
		case "essay":
			isNumbering=False # indent = on
		case "number":
			isNumbering=True

# gutenberg setting is used only to constrain outputs (XML interpretation)
def isGutenbergOn():
	global isGutenberg
	return isGutenberg

def setGutenbergOn():
	global isGutenberg
	isGutenberg=True

