# Author module 2.6.24
# Can function as an avatar list as well

def resetAuthors
	global authorlist
	authorlist=dict()
	global currentauthor
	currentauthor=""

def getAuthors():
	global authorlist
	return authorlist

def setAuthors(myinput):
	global authorlist
	authorlist=myinput

def setCurrentAuthor(myinput):
	global currentauthor
	currentauthor=myinput

def getCurrentAuthor():
	global currentauthor
	return currentauthor

class authorobject:

	def __init__(self):
		self.name=""
		self.avatar=""

	def setName(self,myinput):
		self.name=myinput

	def getName(self):
		return self.name