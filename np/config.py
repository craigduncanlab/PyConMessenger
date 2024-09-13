# config 12 July 2024.  Anonymous submission purposes
# table width in CSS 'table' set to width:90% for now.  Works for WP output.

from np import semantics

# no suffix
def getIndexName():
	indexname="SiteMap" 
	return indexname

def getIndexFolder():
	indexfolder="AA_Indexes"
	return indexfolder

def getMainStyleSheetName():
	output="fnlstyle_new.css"
	return output

def getModifiedStyleSheetName():
	output="semantics.css"
	return output

# used in recursion.py.  Can be overriden.  See overrides.py
def isGlobalNumberingOn():
	return False
	# return True if you want explicit paragraph numbering in text to be on automatically
	# (HTML links to implicit paragraph numbers are still possible even if you have numbering off)

def isPlayNumberingOn():
	return False

def isSingleSpaced():
	return False
	# return False for 1.8 line spacing or 1.5 etc

def arePageLinksOn():
	return True
	# return True if you want links at top of page for headings in each page

def isFooterVerboseStats():
	return False
	# return True if you want word counts and updated date in your footer

# Default is literature-style indent.
def useFirstLineTabIndent():
	return False
	# return False if you want paragraphs to be aligned left.  

def areTableBordersOn():
	return True
	# return false otherwise

# This returns the max pixel width used by imagelister when resizing 
# this is not image 'size', only the file size, so setting too low causes low res pictures at any size above that.  
# Where CSS is set to a % of max width (as currently) it just needs to be sufficient for that purpose

def getMaxImageWidth():
	return 600

# this specifies the name of the class for the img tags in HTML. Used in imagelister
# requires img.small, img.medium in CSS file etc
# If CSS specifies a % width that will affect display, but not image file size
def getStdImageClassName():
	return "medium"
	# return "small"

# this are sizing options for CSS.  The img tag classes should be set.
def getSizeOptions():
	return ["small","medium","medlge","fullwidth","large"]

# still used in htmltagmaker.py
def isSemanticSubstitionOn():
	return False

# include .
def getAutoTagScriptSuffix():
	output=".ats"
	return output