---
title: 'MessengerHTML and a workflow for semantic Shakespeare'
tags:
  - Python
  - XML
  - HTML
  - programming
  - domain specific languages
  - literature
authors:
  - name: Craig M.Duncan
    orcid: 0000-0000-0000-0000 TBA
    equal-contrib: true
    affiliation: "1" 
affiliations:
 - name: Independent Researcher, Australia
   index: 1
   
date: 25 September 2024
bibliography: paper.bib
---

# Summary

It is rare to find any programming languages easy to use for those who want to perform some simple writing but also want to include simple programming specifically to work with their own text, its output or to avoid marking up.  The main tools available for editing are word processors and markup languages, but there does not seem to be a programming language for writers and essayists that didn't start as a tool for programmers or for markup.  My proposed solution, still in development, is an integrated “four-in-one” software application that uses a simple domain specific scripting language for writers, offering them more tools than markup, and with the assumption they want to produce an integrated writers' website.  The author’s `NP` package is an extremely small end-to-end Python application that provides a text interpreter to hide HXML, produces a consistent HTML output and an integrated set of HTML files and images.  This software arose out of research dedicated to producing HTML as *MessengerHTML* (a form of HTML with restrained tag use, to enable XML-like functions).  

# Statement of need

HTML is often regarded as a format for reading text, but its capacity for carrying non-HTML semantic information is often overlooked.   My research analysing HTML as a signal/message has identified a way of using HTML to carry semantic information that I call MessengerHTML.  It uses the bandwidth available in HTML to carry an extensible semantic scheme like XML in a single tag’s attribute (i.e the ‘carrier’ part of the signal), thus allowing this to be interoperable with Word Processors that reserve this slot for style.   This effectively reduces the differences between HTML and XML.   It was natural to want to build a workflow to make this a standard, but also to allow intelligent use of semantic information throughout the workflow. 

My goals were to employ a suitable front end to take in relevant information about literature or professional texts, to use with MessengerHTML.  The challenge in choosing methods to hide or avoid XML/HTML for writers who want to record semantics is best described as the need for a domain specific scripting language, rather than a markup language.  Many benefits to computer programming are provided by using domain specific programming languages with an appropriate level of abstraction [@Kosar:2010].  In this case, it needs to provide high level domain specific programming assistance for writers and scholars of literature, in preference to scientists, computer programmers or professional manuscript scholars.  

As far as the author is aware, the state of the art for document formats and editing is either plain text markup, word processing formats like ODT and OOXML, or explicit HTML/XML.  This is often perceived as a choice between front side or representational (WYSIWYG) and back side (XML).  Mechanical assistance with XML tagging is provided by programs like *OxygenXML* [@OxygenXML], and *LIME*[@LIME] as illustrated by [@Palmirani:2019].  The tagging itself using Text Encoding Initiative [@TEI] schema can be at word and punctuation level (*Folger Shakespeare Library*)[@FolgerShakespeare] and is often onerous [@Puren:2024].   On the other hand, the goal of avoiding tagging by using simple and general markup schemes is often with the motivation that they should be readable (@ppgen) or provide markup with a set of tools for working with relaxed text [@Goodger:2024].  In some software, like *pandoc*[@pandoc], the tools are designed for conversion between markup formats. 

The choice between XML and plain text markup languages is, in reality, too rigid, but this is encouraged somewhat by general explanations that avoid programming language or computer science theory.   In my view, both plain text markups and XML/HTML can be classified, in a social semiotic sense [@Wells:2015], as representational forms of programming languages.  rather than more abstract computational instructions using symbolic language.  By way of example, if I say “I will need to buy 8 crates of oranges” then the language is useful in a symbolic sense if you understood what I meant without having to draw each of the 8 crates of oranges.  Similarly, I should not always need to draw a table of data, and the gridlines, in order to instruct a computer to prepare a table of data as output.   Yet many popular markup formats like *reStructuredText*[@reStructuredText], *ppgen*[@ppgen], which supports preparation of books for *Project Gutenberg*[@ProjectGutenberg], or *Markdown*[@Markdown] still include this kind of syntax.   This approach merely swaps out one structured representational system (XML/HTML) for another, with the aim of reducing the mechanical effort without introducing a new conceptual scheme.

# Proposed software solution

The *MessengerHTML* software provides a very light markup paradigm with the novel NP scripting language to provide a writer with access to useful data definitions and programming functions.  Although similar in goals to *reStructuredText*, there is a greater emphasis on the use of shortcut blocks and novel functions over markup, and a tighter control over the HTML output as *MessengerHTML*.  The project repository has several different examples of utilising the unaltered text in the document as a data block, which can then assist with auto-tagging the remainder of the document.  An example of the auto-tagging of plain text files to produce styled Shakespearean plays in MessengerHTML is in the repository folder `Plays` [@Duncan:2024].  I have also included some beneficial features like web site indexing, and paragraph numbering options for default paragraphs, features often only present in word processors.   The design favours creating interlinked articles with internal and external links over purely eBook output.  However, *MessengerHTML* pages should satisfy Project Gutenberg HTML submission requirements for individual pages, by restraining CSS to inline CSS2.1 and representing external links as text, which can be enabled as a simple configuration option.  

# Use of Python

The author of this paper is the author of the code for the NP package, available under an MIT licence.  Full instructions, text authoring instructions and a sample project folder to evaluate, are included in the author’s github repository [MessengerHTML](www.github.com/craigduncanlab/PyConMessenger).

The project pipeline for production of *MessengerHTML* uses `Python3.11`, and a few standard `Python` packages, including `xml.etree`.`ElementTree`, `string`, `pathlib`,`os.path`,`shutil` and `datetime`.  

# References


