# separate code for local/private information
# Craig Duncan (c) 12.7.2024 and beyond

from np import config

def getMainAuthor():
	output='Digital Languages'
	return output

def getMainAvatarImage():
	imagename=""
	return imagename

def getMainAuthor():
	output='Craig Duncan'
	return output
	
def getMainDescription():
	output="This HTML is in the MessengerHTML format.  It contains work created, researched and published by Craig Duncan.  Credits to third party sources appear where appropriate."
	return output

def getMainKeywords():
	output="Digital Humanities, digital thesaurus, interoperability, semantic content, languages, semiotics, linguistics, literate computing, computable text"
	return output

def getSiteLicence():
	output="(C) Copyright"
	licencedict=getLicence("CC_NDNC")
	if (licencedict!=""):
		output=licencedict
	return output

def getLicence(myinput):
	ld=dict()
	ld["MIT"]="licensed under a MIT Licence:"
	linkCCND='https://creativecommons.org/licenses/by-nc-nd/4.0/'
	PGFlag=config.getGutenberg()
	if PGFlag==True:
		ld["CC_NDNC"]='licensed under a Creative Commons Licence CC BY-NC-ND 4.0 ('+linkCCND+')'
	else:
		ld["CC_NDNC"]='licensed under a Creative Commons Licence: <a href="'+linkCCND+'" class="footer">CC BY-NC-ND 4.0</a>'
	output=""
	if (myinput in ld.keys()):
		output=ld[myinput]
	return output