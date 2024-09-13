# CSSmappings.py (C) Craig Duncan
# Split off from xmlpub and config 10.9.24
# Used only in xmlpub.py

from np import semantics

# assumes utf 16
def opentxt(fn):
	f=open(fn,"r")  # default is utf-8 not 16?
	output=f.read()
	return output

def getLatest():
	# Update the CSS supplementary file if required
	fname2="np/semantictemp.css"
	template=opentxt(fname2)
	revised=template
	semtagdict=getPlayMappings()
	for x in semtagdict.keys():
		val='p.'+x
		repval='p.'+semtagdict[x]
		revised=revised.replace(val,repval)
	return revised

# each of the std CSS tags in the supplementary file is replaced by these
# anticipates these being the classes used for p tags e.g. autotagline() call

def getPlayMappings():
	se=semantics.getSemanticBlockCodesDict()
	example=se["e"]
	authorref=se["a"]
	listy=se["l"]
	acode=se["c"]
	quote=se["q"]
	intro=se["# "]
	#print("New vars:",example,author,listy,code,quote)
	# default mapping
	sd=dict()
	sd[example]="dialogue"
	sd[authorref]="character"
	sd[listy]="dramatis"
	sd[acode]="StageDir"
	sd[quote]="littlequote"
	sd[intro]="speaker"
	return sd
