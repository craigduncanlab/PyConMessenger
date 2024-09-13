# testdatablocks


# Assumes this is a 'd+'' block with first line for data list name
def getData1():
	mylist=["(column1)","This","is","a","list of items","to be put","into a table","","to see","if it can make a table","automatically."]
	return mylist

def getData2():
	mylist=["(freddy)","A few more", "items", "that will", "serve", "as", "data"]
	return mylist

def getData3():
	mylist=["(basket)","Apple","Banana","Capsicum","Dates","Enchalada","Fozzbottle","Goober"] 
	return mylist

def getData4():
	mylist=["(Title)","Apple(fruit:tidy)","Car(vehicle)","Chimney(building)","Blood(liquid)","Golf(sport)","Icecream(food)"] 
	return mylist

def getData5():
	mylist=["(Title)","Yoolup>bordinyuk:Hungry (40-042T,pb-40-063T)","Bordinyuk:Hungry (40-134T,pb-40-152T)","Bordinyuk>weerart:Hungry (40-160T,pb-40-181T)","NotHungry:Yet"]
	return mylist

def getData6():
	mylist=["(Title)","Dwerda yaggain nganga:Dingo, female [41-320T,pb-41-328T]"]
	return mylist

def getCommands():
	output="tablecol(column1,freddy,basket)"
	return output

def getCOMlist():
	output=["tablecol","tablerow","tablesplit"]	
	return output
