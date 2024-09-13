An introduction to this project
----------------

A:Craig Duncan (c) 2024

D:11 September 2024

# Licence

This explanatory document is licensed under a [Creative Commons NC by ND 4.0 licence](https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode.en).  


# Intro

The 'NP' (or New Processor) grew out of the MessengerHTML project, as a way of implementing a more complete model of computing that would connect semantic content of MessengerHTML with an upstream text editor process that wasn't solely based on analogue outputs, and document object models, as Markdown and pandoc are.

Through the evolution of the project, a basic text-streaming model has been employed, successfully, to create a static website generator workflow, that produces essay/article/blog type pages, a general static website index, and the ability to open any of the HTML pages in common wordprocessors.  Configuration options and functions are still in a process of testing and development, but include paragraph numbering options and auto-tagging of plain text content.

This document contains the basic install and setup information.  As it is a large project with an academic research project behind it, there are several supplementary documents to this one:

-  [Licence](Documentation/LICENCE.md)
- [How It Works](Documentation/HowItWorks.md)
- [NP Writing Guide](Documentation/NPGuide.md)
- [ComparativeDigitalDocAnalysis](Documentation/ComparativeDigitalDocAnalysis.md) - a theoretical examination of digital documents
- [MessengerHTML](Documentation/MessengerHTML.md)
- [ShakespeareAndMessengerHTML](Documentation/ShakespeareAndMessengerHTML.md)

# Pre-requisites

You will need:

- access to the command line on your computer (e.g. a terminal application, or unix system default), rather than a graphic-basic interface; 
- the Python language installed (Python3), so that you can run python programs from the command line; and   
- any basic text editor (not a Word Processor) to edit and save .txt files into the <i>source</i> folder in your project.

If you can download this project to your computer you will have all the folders you need to being work, already setup, as well as some examples of both .txt source and .html output for your to peruse.  This is clarified below.

You should also have a browser, obviously, if you want to open and view HTML files easily on your computer.

# To setup NP (to produce MessengerHTML web sites)

Download or copy the np folder, html folder and source folders into the same director as run.py

The project has a few example documents including literature and cricket scoring (still in development).

To prepare a Project structure for your work:
- run.py should be in your top project folder, the one that holds the np folder.
- htmlpages, and source folders should also be in the top project folder, so that you have np, htmlpages and source folders in the same location.
- fnlstyle.css (or whatever substitute you have specified in config.py) should be in htmlpages
- there should be an images folder inside htmlpages. (htmlpages/images)
- there should be an Indexes folder inside source (source/Indexes)

When writing new .txt files:
- Save/put your text files (.txt) inside the 'source' folder.
- Name all your .txt files in source uniquely. 
- You can create one level of subfolders inside 'source'.  The names of these folders will also structure your Site Map entries.  Feel free to move your files around and reference by running the 'all' command (see below).
- Put any images that you refer to in your .txt file in the same folder as your .txt file.  The program will copy these into the images folder inside html.

The output:
- output html is a flat structure, in the htmlpages folder.
- all page linking is done to the htmlpages as output (it doesn't care that you have them in different source subfolders, provided they are only one level deep).
- images are resized to a standard size (memory size, not image size) and copied into the images folder.  When the project is built, no further reliance on the source folders is needed.  You can copy the entire htmlpages folder to you desired project location and view from there.

# Processing your .txt files into .html and a website

Start by opening a terminal in the run.py folder, and type:

	python3 run.py

This will bring up a prompt.  

To interpret/process your .txt files into html you have several options at the program input line:
 - type the name of your file (without .txt extension).  Any file matching that name in source folder will be found and processed into HTML.
 - if you just hit enter it will assume you want to reprocess the last file you processed.
 - type 'folder:' followed by the name of one of your subfolders in the source folder.  This will process all the .txt files in that subfolder. e.g.

 ```
 folder:Plays
 ```

 - type 'all' to process the entire project (all source folder and subfolders).  Only if you select 'all' in this way will the SiteMap, ArticlesIndex and DateIndex be rebuilt.  The last two indexes are able to be accessed via sitemap.

General configuration options are available in the config.py file.  Other semantic labelling options are in semantics.py but this is currently being worked on.

There is a helper python file to upload your htmlpages by FTP to a site.

Enter 'exit' to go back to terminal when finished.

# Text file error correction philosophy

If you type in the wrong filename, the NP interpreter will not abort completely.

The run.py program will abort when a serious syntax error in one of your .txt files is encountered, and it will provide information (e.g. if you have forgotten to close off a data block etc).  This has some data checking as well.  There are also messages about problems with your data blocks, or references to variables.

The philosophy of this is the same as coding/compiling in general: fix the error, then carry on.  Otherwise your project will get too big.  

Once you have fixed your text file error, you then need to start it back up with run.py

Part of the reason for this process is that it refreshes the file system and your run.py process will be using the most up to date file information.

If you have a problematic file, don't just keep running 'all', think about running the interpreter over just the subfolder it is in, or just type the file name (without .txt) to process that file until you are happy with it.

# Server uploads of your website

You can use any FTP or other method to upload your files to a server.  The np folder is where the Python files for this package reside.  There is an FTP program that is included there (ftpaccess.py) that would enable you to upload your programs to a server.  It requires a login.py program to run, which I have not uploaded at this stage, but I may be able to do so with dummy information if there is a demand for it.

