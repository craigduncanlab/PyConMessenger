# semanticconfig 22.7.2024

import np.semantics

def getSubstitutes():
	se=semantics.getSemanticDict()
	example=se["e"]
	authorref=se["a"]
	listy=se["l"]
	acode=se["c"]
	quote=se["q"]
	#print("New vars:",example,author,listy,code,quote)
	sd=dict()
	sd[example]="dialogue"
	sd[authorref]="character"
	sd[listy]="dramatis"
	sd[acode]="StageDir"
	sd[quote]="littlequote"
	return sd