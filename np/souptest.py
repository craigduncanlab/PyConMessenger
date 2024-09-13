# A simple way to check MessengerHTML
# Craig Duncan 6.9.24

# use this first from command line: pip install beautifulsoup4

from bs4 import BeautifulSoup

def findAndPrint(myclass):
	# A resultset is a subset of html, in a list form, that conforms to the find requirements.
	mydivs = soup.findAll("p", {"class": myclass}) #class 'bs4.element.ResultSet
	print("This is list of '"+myclass+"' class elements")
	for thispara in mydivs:
		print(thispara.text)

html_string=open("htmlpages/MathTest.html")
soup = BeautifulSoup(html_string, 'html.parser')

# Find a specific element using its tag name and (optional) its attributes
first_paragraph = soup.find('p')

print(first_paragraph.text)

"""
# Only parse part of the document
tag = SoupStrainer('p')
"""

findAndPrint("example")
findAndPrint("np")
