# imagelist module Extracted from xmlpub.py 8 May 2024 (c) Craig Duncan
# image finding functions also extracted 2-3 June 2024.

from pathlib import Path # for reading directory
import os.path as OPath
import shutil #shell utilities e.g. file copy
# Importing Image class from PIL module .  "Pillow" library is now most up to date/supported
from PIL import Image 
from np import semantics,config

def resetImages():
	global imagelist
	imagelist=[]

def initialise():
	resetImagesUsed()

def resetImagesUsed():
	global imagesused
	imagesused=[]
	global imagedict	
	imagedict=dict()
	global currentimage
	currentimage=""

def getImageList():
	global imagelist
	return imagelist

def setImageList(myinput):
	global imagelist
	imagelist=myinput

def makeImageList():
	resetImages()
	images=[]
	p = Path('.')
	for img in p.glob('htmlpages/images/*.*'):
		images.append(img)
	setImageList(images)


def setImagesUsed(myinput):
	global imagesused
	imagesused=myinput

def getImagesUsed():
	global imagesused
	return imagesused

def setCurrentImage(myinput):
	global currentimage
	currentimage=myinput

def getCurrentImage():
	global currentimage
	if currentimage==None or currentimage=="":
		print("You are attempting to retrieve image or set image properties but cannot - ")
		print("You haven't yet set an image with I: in your source file")
		exit()
	"""
	else:
		print("I appear to have found an image:",currentimage)
		print(type(currentimage))
		exit()
	"""
	return currentimage

def getCurrentImageObject():
	myImageName=getCurrentImage()
	myobject=getImageObject(myImageName)
	return myobject

def getImageDict():
	global imagedict
	return imagedict

def setImageDict(myinput):
	global imagedict
	imagedict=myinput

# Called when source text file contains a line with prefix I:
# This prepares an XML string with <image tag prefix.  Ultimately transformed into HTML by second stage
# syntax:
# I:imagename e.g. imagename.png
# I:imagename (default is imagename.png)
# I:imagename,jpeg e.g.imagename.jpeg
# I:imagename,J e.g.imagename.jpeg
# image location is same as txt source
# txtpath is the path to the txt file that contains the image ref
# img1 should be path as supplied by writer
def setInternalImage(img1,txtpath):
	mylist=[]  # this holds the arguments for the image: name, alt text etc
	if (txtpath==None):
		print("Cannot find/no txtpath for image:",imgprefix)
		exit()
	imgtype="suffix"
	alttext=""
	if ("." in img1 and "," not in img1):
		mylist=img1.split(".")
		imgprefix=mylist[0]
	elif ("." not in img1 and "," in img1):
		mylist=img1.split(",")
		imgprefix=mylist[0]
	elif "." not in img1 and "," not in img1:
		mylist=img1.split(",")
		imgprefix=img1
	elif "." in img1 and "," in img1:
		mylist=img1.split(",")
		imgprefix=mylist[0]
		if len(mylist)>1:
			if("." in mylist[0]):
				myprefix=mylist[0].split(".")
				if(len(myprefix)>0):
					imgprefix=myprefix[0]
				else:
					imgprefix=myprefix[0]
			for y in range(1,len(mylist)):
				alttext=alttext+mylist[y]
				if (y<len(mylist)-1):
					alttext=alttext+"," # add back in
		
	
	imgname=""
	imageypath=""
		
	if (len(mylist)>0):
		if (len(mylist)==1): # i.e. no alt text present
			if ('.' not in imgname):
				imgtype="z"
			
		if (len(mylist))>=2:
			imgtype=mylist[1].lower()
		
		imgname=findImage(imgprefix,imgtype,txtpath)
		# This should not be called if imgname = """
		if (imgname==None):
			print("Cannot find image:",imgprefix)
			exit()
		if (len(imgname)>0):
			imageypath=str(txtpath.parent)+"/"+imgname
			if (len(imageypath)>0):
				# store this image name and path for site backup purposes
				myimlist=getImagesUsed()
				if (imageypath not in myimlist):
					myimlist.append(imageypath)
					setImagesUsed(myimlist)
					myimage=imageobject()
					myimage.setName(imgname)
					myimage.setPrefix(imgprefix)
					myimage.setAlt(alttext)
					myimage.setPath(imageypath)
					addImageToDictionary(imgname,myimage)
					setCurrentImage(imgname)
					return imgname
		else:
			return imgname

#getInternalImage
def getImageXML():	
	output=""
	"""
	currentimage=getCurrentImageObject()
	myimage=getImageObject(name)
	print(myimage,currentimage)
	exit()
	"""
	name=getCurrentImage()
	myimage=getImageObject(name)
	if (myimage !=None):	
		output=composeImageTag(myimage)		
		return output
	return output

def addImageToDictionary(name,object):
	global imagedict
	if (name not in imagedict.keys()):
		imagedict[name]=object
		#print(imagedict)
		#exit()

def getImageObject(name):
	global imagedict
	if (name in imagedict.keys()):
		return imagedict[name]

def updateCaption(myinput):
	checkValue("caption",myinput)
	imgname=getCurrentImage()
	currentimage=getImageObject(imgname)
	currentimage.setCaption(myinput)
	alttext=currentimage.getAlt()
	title=currentimage.getTitle()
	if alttext=="":
		currentimage.setAlt(myinput)
	if title=="":
		currentimage.setTitle(myinput)	
	updateWithImage(imgname,currentimage)

def updateAuthor(myinput):
	checkValue("author",myinput)
	imgname=getCurrentImage()
	currentimage=getImageObject(imgname)
	currentimage.setAuthor(myinput)
	updateWithImage(imgname,currentimage)

def updateSize(myinput):
	checkValue("size",myinput)
	imgname=getCurrentImage()
	currentimage=getImageObject(imgname)
	currentimage.setSize(myinput)
	updateWithImage(imgname,currentimage)

def updateTitle(myinput):
	checkValue("title",myinput)
	imgname=getCurrentImage()
	currentimage=getImageObject(imgname)
	currentimage.setTitle(myinput)
	updateWithImage(imgname,currentimage)

def updateDate(myinput):
	checkValue("date",myinput)
	imgname=getCurrentImage()
	currentimage=getImageObject(imgname)
	currentimage.setDate(myinput)
	updateWithImage(imgname,currentimage)

def checkValue(item,myinput):
	if (myinput==None):
		print("You have not specified this attribute for image:",item)
		exit()

# update this dictionary key name with the passed imageobject
def updateWithImage(imgname,myimageobj):
	#print("Updating with image...",imgname,myimageobj)
	thisdict=getImageDict()
	thisdict[imgname]=myimageobj
	m2=getCurrentImageObject()
	setImageDict(thisdict)

# Prepare an XML style tag based on image information
# myimage is an imageobject
def composeImageTag(myimage):
	attributes=myimage.getAttributes()
	imgclass=myimage.getImgClass()
	imgprefix=myimage.getPrefix()
	"""
	print(size,possiblesizes)
	print(imgclass)
	print("aborting imagelister")
	exit()
	"""
	# final tag composition
	imtag=semantics.getImageXMLTag()
	tag1=imtag+' size="'+imgclass+'"'+attributes
	output=semantics.makeMismatchedXMLTag(tag1,imgprefix,imtag)
	#output='>'+imgprefix+'</'+imtag'>\n'
	return output

#imgtype should be z for no file extension, suffix for file extension
# As at 24.7.24 Safari will display mp4 gifs inside img tags, Firefox won't (not by default)
def findImage(imgprefix,imgtype,txtpath):
	#print("Searching.  Image Input info:",imgprefix,imgtype,txtpath)
	imgname=""
	foundimgtype=False
	dirpath=OPath.dirname(txtpath)
	if imgtype=="jpg" or imgtype=="jpeg" or imgtype=="png" or imgtype=="mp4":
		testname=imgprefix+'.'+imgtype
		foundimgtest=lookForFile(testname,dirpath)
		if foundimgtest==True:
			imgname=testname
			foundimgtype=True
	else:
		ftypes=["jpg","jpeg","png","mp4"]
		for f in ftypes:
			testname=imgprefix+'.'+f
			foundimgtest=lookForFile(testname,dirpath)
			if foundimgtest==True:
				imgname=testname
				foundimgtype=True
			
	#print("Finished Image search.  Returning: ",imgname,"\n")		
	if foundimgtype==False:
		#imgname=imgprefix+deftype # never found
		message="Image not found in source folder:"+imgprefix
		print(message)
		# imgname="NOT FOUND" # or incorporate name?
		# DO NOTHING: imgname=testname
		waiton=input("Fix later and continue? y to proceed")
		if (waiton!="y"):
			message=[txtpath,message]
			abortOnError(message)
		else:
			print("continuing")
		
	return imgname

def lookForFile(testname,dirpath):
	relpath=OPath.join(dirpath,testname)
	#print(str(relpath))
	if OPath.isfile(relpath):   # os.path
		print("Image found in source folder:",testname)
		return True
	return False


def checkDirectoryExists(idxpath):
	idxtrue=OPath.isdir(idxpath)
	if (idxtrue==False):
		print("You forgot to setup the index directory ",idxpath)
		exit()

# check for image, copy and resize if necessary
# loc = filename
def handleImagesFolder(topicpath,fname):
	idxpath='./htmlpages/images'
	checkDirectoryExists(idxpath)
	imagelist=["jpg","jpeg","png"]
	isWebImage=False # check for mp4
	for a in imagelist:
		stub=fname[-5:]
		if a in stub:
			isWebImage=True
	p = Path('.') # pathlib.Path()
	# current working directory (for the xmlpub)
	pwd=str(p.absolute())  # p.cwd() might also work
	#print(thispath, "image not in site folder")
	localpath=pwd+"/"+topicpath+"/"+fname
	#print(localpath)
	destpath=pwd+"/htmlpages/images/"+fname
	# copy it over.
	# TO DO: check image exists first
	if OPath.isfile(localpath):  # os.path
		# currently copies it over first, then resizes
		try:
			shutil.copyfile(localpath,destpath)
		except:
			print("Imagelister.  Problem copying over file:",localpath)
			print("To:",destpath)
			exit()
		#print("Copied an image:",destpath)
		if isWebImage==True:
			imageResizer(destpath)  # this is imported here, not via npmake first
			#print("Resized an image:",destpath)
		
	else:
		print("Error with Image File")
		print("Does not exist at location:",localpath)
		waiton=input("Fix now or continue? Enter to proceed")
		if (waiton==0):
			exit()
	# copy thispath image to that folder


# change the max absolute size of images in html pages for practical opening in Word Processors etc
# mypath is string not POSIX
def imageResizer(mypath): 
	# Opens a image in RGB mode 
	im = Image.open(mypath) 
	resizewidth=config.getMaxImageWidth()
	# Size of the image in pixels (size of original image) 
	# (This is not mandatory) 
	width, height = im.size 
	# This width seems to work okay when opening HTML up in Word etc
	if (width>resizewidth):
		oldwidth=width
		width=resizewidth
		height=int(width/oldwidth*height)
		newsize=(width,height)
		im1 = im.resize(newsize)
		# Resave in new size
		im1.save(mypath)

class imageobject:

	from np import config

	def __init__(self):
		self.name=""
		self.prefix=""
		#suffix
		self.path=""
		self.title=""
		self.alttext=""
		self.caption=""
		self.author=""
		self.size=""
		self.position=""
		self.date=""

	def setName(self,myinput):
		self.name=myinput

	def setPrefix(self,myinput):
		self.prefix=myinput

	def setPath(self,myinput):
		self.path=myinput

	def setTitle(self,myinput):
		self.title=myinput

	def setAlt(self,myinput):
		self.alttext=myinput

	def setCaption(self,myinput):
		self.caption=myinput

	def setAuthor(self,myinput):
		self.author=myinput

	def setSize(self,myinput):
		self.size=myinput

	def setPosition(self,myinput):
		self.position=myinput

	def setDate(self,myinput):
		self.date=myinput

		#

	def getName(self):
		return self.name

	def getPrefix(self):
		return self.prefix

	def getPath(self):
		return self.path

	def getTitle(self):
		return self.title

	def getAlt(self):
		return self.alttext

	def getCaption(self):
		return self.caption

	def getAuthor(self):
		return self.author

	def getSize(self):
		return self.size

	def getPosition(self):
		return self.position

	def getDate(self):
		return self.date

	def getImgClass(self):
		imgclass=""
		# These sizes are used by recursion.py but ultimately here: handleImage..
		possiblesizes=config.getSizeOptions()
		if len(self.size)>0 and self.size in possiblesizes:
			imgclass=self.size
		else:
			imgclass=config.getStdImageClassName()

		return imgclass

	# For XML/HTML tag construction
	def getAttributes(self):
		
		attributes=""	
		
		if (len(self.name)>0):
			attributes=attributes+' src="'+self.name+'"'
		if (len(self.alttext))>0:
			attributes=attributes+' alt="'+self.alttext+'"'
		if (len(self.caption)>0):
			attributes=attributes+' caption="'+self.caption+'"'
		if (len(self.author)>0):
			attributes=attributes+' author="'+self.author+'"'
		if (len(self.title)>0):
			attributes=attributes+' title="'+self.title+'"'
		if (len(self.date)>0):
			attributes=attributes+' date="'+self.date+'"'

		return attributes

def updateImageStatus(code,cleanstr,txtpath):
	if code=="I:":
		setInternalImage(cleanstr,txtpath) # imgname in case useful
		#print("UpdatedImageStatus:",getCurrentImage())
	elif code=="IC:":
		#print("found",codeMatch)
		updateCaption(cleanstr)
	elif code=="IA:":
		updateAuthor(cleanstr)
	elif code=="ID:":
		updateDate(cleanstr)

# ftypes=["jpg","jpeg","png","mp4"]
# handle rows for image data
# These are really data interpretation functions
def handleRowsForImageData(txtpath,content):

	ftypes=["jpg","jpeg","png","mp4"]
	count=1
	output=[]
	rowlengths=[]
	title=""
	myauthor=""
	caption=""
	imagefile=""
	imageprefix=""
	imagesuffix=""
	size=""
	mdate=""
	count=0
	myfileID=0
	imageindex=[]
	for x in content:
		for ft in ftypes:
			if ft in x:
				imageindex.append(count)
		count=count+1
	if len(imageindex)>0:
		myfileID=min(imageindex)
		imagefile=content[myfileID]
		if ("." in imagefile):
			imagesplit=imagefile.split(".")
			if (len(imagesplit)>1):
				imageprefix=imagesplit[0]
				imagesuffix=imagesplit[1]
			else:
				print("Problem finding image name and suffix:",imagefile)
				exit()
	elif len(imagefile)==0 or imagefile==None:
		print("Call by image(). Problem identifying image file in image block here:",content)
		exit()
	#print("Found:",imagefile)
	for x in content:
		x=x.lstrip(" ")
		if ("A:"==x[0:2] and len(myauthor)==0):
			myauthor=x[2:].strip()
		elif ("C:"==x[0:2] and len(caption)==0):
			caption=x[2:].strip()
		elif ("T:"==x[0:2]and len(title)==0):
			title=x[2:].strip()
		elif ("D:"==x[0:2]and len(mdate)==0):
			mdate=x[2:].strip()
		else:
			sizeoptions=config.getSizeOptions()
			for s in sizeoptions:
				if x[0:len(s)].lower()==s and len(size)==0:
					size=s

	myvariables=[imagefile,myauthor,caption,title,mdate,size]
	# update image meta data
	setInternalImage(imagefile,txtpath) # check image exists etc
	updateCaption(caption) # this is a caption below the image.
	updateAuthor(myauthor)
	updateTitle(title) # title is the hover text in Safari browser
	updateDate(mdate)
	updateSize(size)
	# turn it into a comprehensive image string
	output=getImageXML()
	return output


# topicpath is source folder
def handleImagePath(child,topicpath):
	loc=child.get("src") # location (this will be the image name)
	images = getImageList()
	# this is relative to the calling page (already inside htmlpages)
	basefolder="images/"
	thispath=basefolder+loc
	imageExists=False
	for i in images:
		if (thispath==i):
			print(thispath, "image already exists")
			imageExists=True
			# TO DO: check for more recent copy locally

	if imageExists==False:
		handleImagesFolder(topicpath,loc) 
	return thispath

# this creates a reference but the image needs to be copied to images
# Input is an ET node child object i.e. XML stream with specified attributes
def handleImageLinks(child,imgpath):
	
	size=child.get("size") #imgsize
	alttext=child.get("alt")
	title=child.get("title")
	caption=child.get("caption")
	author=child.get("author")
	mydate=child.get("date")
	"""
	print("handling image links")
	print(size,alttext,title,caption,author,mydate)
	print(str(child))
	exit()
	"""
	if (mydate is None):
		mydate=""
	if (author is None):
		author=""
	if (alttext is None):
		#print("Image link has no alt text")
		alttext=""
	if (title is None):
		title=alttext
	if (caption is None):
		caption=""
	if size is None:
		size="medium"
	
	if alttext=="":
		if (len(caption)>0):
			alttext=caption	
	
	# Convert XML to standard HTML output for images (img tag)
	attributes=""
	line1='<img '
	if (len(size)>0):
		myclass=size # inherited from initial class definition
		line1='<img class="'+myclass+'"' 
	attributes=' src="'+imgpath+'"'
	if (len(alttext)>0):
		attributes=attributes+' alt="'+alttext+'"'
	if (len(title)>0):
		attributes=attributes+' title="'+title+'"'
	line1=line1+attributes+'>'

	#text is used for caption
	
	#print(myclass,caption,loc)
	if (len(caption)==0):
		if (len(title)>0):
			caption=title
	#insert an author reference for an image if there is one
	captionStop=False
	if ("." in caption):
		captionStop=True
	if(len(author)>0):
		caption='<b>'+author+'</b>,<em>'+caption+'</em>'
	# insert date if there is one.
	if (len(mydate)>0):
		if (captionStop==False):
			caption=caption+"."
		caption=caption+" "+mydate
	line2=''
	imgclass=semantics.getImageXMLCaptionTag()
	if (len(caption)>0):
		line2='<p class="'+imgclass+'">'+caption+'</p>'
	
	output=line1+line2
	
	return output

# generic feedback
def abortOnError(description):
	if (type(description)==str):
		print(description)
	if (type(description)==list):
		for d in description:
			print(d) # inserts CR automatically
	exit()