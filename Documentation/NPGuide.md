The 'NP' (New Processor) Guide
---------

This Guide (c) Craig Duncan 2024.

# Licence

See [Licence](LICENCE.md)

# Basic approach to writing .txt files

The program assumes that general metadata for an article, essay or simply a blog page will appear in the first 10 lines.  You do not need to follow YAML.  Instead use this convention for prefixes (order is not important), including prefixes for high level navigation.

```
T:Title
A:Author
D:24 March 2024. Last update or revised 1 June 2024.
C:Concept, abstract or general description.
R:PageNames
B:BackTo
F:ForwardTo
```

You can include some explanatory text in the date line (as above), so long as there is a long form date that can be detected somewhere.  The right-most date is chosen as the latest date, and it will use this for document indexing (it doesn't check the date sequence only that it is the last).

If there is no date, the document is not included in Date or Article indexes, so use as you feel like.

R: is an optional link to another page in your project, as are B: and F: options (back and forward respectively).  Follow the convention that you need to use the same filename as your source .txt file, but without the .txt suffix (this forms the basis of htmlpages page names).  So if you want to go back to 'MySoftwareProject', enter:

```
B:MySoftwareProject
```

The difference between R and B,F options is that R can include several page names, separated by commas.

A link to SiteMap will be included at the end of automatically generated page links, as well as at the bottom of each page.

# Syntax

The 'intro' paragraph type is indicated by a hash (#) like this:

```
# This is a heading or 'intro' paragraph
```

*Default paragraphs*

Any text that is not in a data block, or uses a command or reserved prefix is treated as the default paragraph style/code (np).  

Default paragraphs are in an essay style by default.  You can change the default potions to make literature style indentation, or paragraph numbering.  

If you wish to specify another semantic category to act as the default paragraph, use this function in your text:

```
defaultpara(playline)
```

substituting 'playline' for your chosen style.  The style must be present in fnlstyle.css or whatever .css you are using.  'playline' is provided with the project as a convenient and tight formatted line.

*Text decorations*

Unlike Markdown, the NP processor will support underlining natively.  Although rule-based processing is encouraged, there are many instances where ad-hoc emphasis might be desired, in which case you can use the following:

```
!_some text_! for underlining
!!some text!! for italices
!*some text*! for bold
!! !*some text*! !! for bold and italics
```

These options are some of the reasons why I now prefer working in NP in preference to Markdown.

*Paragraph numbering*

All paragraphs are numbered in the HTML, even if the paragraph numbers are not shown on screen.

If paragraph numbering is on, default paragraphs will be display hard-coded numbers. (see config.py or use the pagenumbers() command in your file)

This is a portion of MessengerHTML generated for the play 'Macbeth', showing both paragraph numbers and semantic categories within the p tags:

![Macbeth_Messenger](Macbeth_Messenger.png)

*Data blocks*.

Reserve a data block with the d+ and d- tags (see below), and put a variable name in the first row, enclosed in brackets, like this:

```
d+
(dramatis)
PRINCE,
ESCALUS, Prince of Verona.
d-
```

A unique feature of data blocks is that the text will never appear as output without a helper function.  i.e. they are not immediately part of HTML.  They are also not 'code'.  Think of them as raw data, or provisional text.

Raw data in a data block can be text, a list (line separated).  Each line is treated as a new entry.

The philosophy of data blocks is that they are raw data with no expectations.

The default use is that you put all your data in a data block into the system using a single variable.  You then create new variables by splitting the raw data.  

*Delimiter selection for raw data*

Raw data can be comma separated, space separated or even use a completely arbitrary but regular set of symbols for each column.  For example, you might have data separated with a colon (:), then a slash (/) and then a comma.  You can set it up for data splitting to recognise the first instance of these.  This means that any commas before the first colon will be ignored, but those after a slash will be used as a delimiter.

*Using data block variables*

The variable name can be used in available functions.  A few of these are:

- lprint(arg)  = print as a list
- nprint(arg) = print as a sequentially numbered list.
- tprint(arg) = print as a table (it tries to find the most common delimiter)
- codeprint(arg) = print as code style
- eprint(arg) = print as example style.  A tight font with coloured background.
- qprint(arg) = print as quote style
- cprint(arg) = a shortcut to cricket scoring tables (with sums).

For example, include these lines in your .txt file and experiment:

```
d+
(MyList)
Here is something
That I want
To print in different ways
d-

This prints as a list:

lprint(MyList)

This prints as an 'explain' text box:

eprint(MyList)

This prints as numbered list:

nprint (MyList)
```


Some of these shortcut the process of taking in raw data and then splitting it for table purposes.  For example, tprint() is a basic table maker that looks for the delimiter and then just puts numbers for row and columns, and doesn't wait for you to specify a heading.  There are some examples of this in the MathTest.txt file in the source folder.

*Shortcut blocks*

I am experimenting with the utility of shortcut blocks.  So far, they seem very useful but they do not have any memory/buffer use.  For example, you can block in lists with l+ and l- lines like this:

```
l+
This is a list item
Second line
Third line
l-
```

The advantage of this over markdown is that you only have to cap the top and bottom, and not mark up each line.

Similarly, there are shortcut blocks roughly corresponding to the print functions above, namely:

- c+/c- = code block
- e+/e- = example block
- n+/n- = numbered list block.
- i+/i- = image block (see below)

*Tables*

Unlike Markdown, tables are data objects.  This means you can create one using the shortcut functions (above) or by using a data block.  If you use a datablock, you can do this by:
- setup a data block with your raw data 
- process the block into column vectors (rip or split function)
- set your headings
- choose which column vectors you want to print by putting the column heading names into the tablecols(arg1,arg2,...) function

*Images*

My preferred approach at present is to take in image data in a data block, like this:

```
d+
(Image1)
MyImageName.png
A:This ithe author name
C:This is the caption
T:This is the title (alt text).
d-
```

The image will not appear until you enter a line in your text file like this, with :

```
image(Image1)
```

You can see an example of this in the 'NotesOnGutenbergMacbeth.txt' file in the source/Plays folder.

The program will use as much or as little information as you give.  It recognises .png and .jpg or .jpeg files (and .mp4 if you use Safari, but not Firefox).

*Intra page links for navigation*

By default pagelines that act as a table of contents appear at the top of each html page, based on the 'intro' paragraphs (# entries).  However, if you want to change this to some other semantic category, like 'scene' paragraphs, use:

```
pagelinks(scene)
```

*Project HTML Page Links*

One of the real practical benefits of making web sites with NP is that you can simple enclose /SomePageName/ with angled brackets and it will create a link to it (regardless of where the .txt file is in source, because all htmlpages are flat links).

You can extend this to linking to a heading (intro) paragraph in a page with: /SomePageName#IntroHeadingText/

Also, because every paragraph (and heading) has an in-built numbering scheme, you can link to a specific paragraph in any page in the web site like this:

/SomePageName#P12/ where P12 is used for the 12th paragraph.  With paragraph numbering turned on, a reader will already be able to see what paragraph this links to in the browser rendering of the page.  If paragraph numbering is off, it may be necessary to look at HTML source to see it.

*External URL Links*

There are several ways to enter links in the body of the text.

Basic prefix methods for an external link include:

```
E:LinkText,www.linkaddress.com,23 April 2024
```

The date is optional but by including it you get words indicating when last accessed.

There is a parsing method that will ignore any additional commas in URL between the first LinkText and the date.  This means links to sites like Google Maps with location information separated by commas will be interpreted correctly.

*Internal links*



# Example of commands used to process Literature

This is an example of putting data in (the commas in the data are not initially used when ingesting the data, but will be used to split the data for other purposes)

```
d+
(dramatis)
PRINCE,
ESCALUS, Prince of Verona.
MERCUTIO, kinsman to the Prince, and friend to Romeo.
PARIS, a young Nobleman, kinsman to the Prince.
PAGE, to Paris.
MONTAGUE, head of a Veronese family at feud with the Capulets.
LADY MONTAGUE, wife to Montague.
ROMEO, son to Montague.
BENVOLIO, nephew to Montague, and friend to Romeo.
ABRAM, servant to Montague.
BALTHASAR, servant to Romeo.
CAPULET, head of a Veronese family at feud with the Montagues.
LADY CAPULET, wife to Capulet.
JULIET, daughter to Capulet.
d-
```

Now this is how we can split the data and use it for a table.  First, we create our header lables (these will be both table headers and variable names)
```
header(Character,Description)
```

Then we specify the splits.  This is a single comma.  To specify multiple commas you can list them (comma, comma, comma) or just (comma all).
```
splits(comma)
```

Now perform the split.  You can use the keyword 'datasplit' or 'rip'.  This will create two new column variables, based on the header.
```
datasplit(dramatis)
```

Finally, to make the table appear, you now use whatever column names you want, in whatever order you want them to appear:
```
tablecol(Character,Description)
```

# Auto-tagging

Now if we want to experiment with changing the appearance of plain text and creating semantic categories without markdown, we can use the 'autotagline' command.  The basic syntax of this command is:

``` 
autotagline(dataline,style,case)
```
Where:

- dataline = Data list to use (e.g. a list of text string.  These could be the characters names you want to find on a given line in the file). 
- style = a recognised stylename in your CSS file
- case = on/off for case-sensitive matching on the dataline entries.

Specific commands that format the plain text in Gutenberg project for CSS use, without markdown
```
autotagline(EnterTag,stageentry,on)
autotagline(ScenesTag,scene,off)
pagelinks(scene)

autotagline(Character,authorref,on)
defaultpara(playline)
outertag(stagedir)

autotagline(ActTitle,title,on)
```

The outertag looks for square brackets at the extreme left and extreme right of any line.

# Auxillary files and import(file)

You can put functions in between normal text in a text file, but if you want to bring in the text from another file, you can also the 'import' function.

The import function will import a file with an .ats extension (this can be changed in the config.py file).   This file is just a text file which is otherwise identical to the normal .txt files that are processed by the NP interpreter.

The text file loaded by an import command may include data blocks, or functions, or additional text.

The import command allows re-use of any data definitions and autotagging commands that have already been prepared.  It is also a way of bringing in data, functions or other text without interrupting the read-through text of the main document. 
