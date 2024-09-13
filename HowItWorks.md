How it Works (New Processor and MessengerHTML)
A:Craig Duncan
D:12 September 2024

# Licence

See [Licence](LICENCE.MD)

# Background and Introduction

The goal is to produce simple text documents in digital media with little 'noise' from both the message (semantic) perspective, as well as the layout perspective.  This means a cleaner, more self-explicable format that it is easier to parse as well.   By focussing on data capture, I hope that it will encourage better upstream tools, not motivated solely by analogue representation equivalence.

The broader research project that underpins the software is a deeper enquiry into the nature of digital documents, as have evolved, as well as those that might become more common in the future.  The main digital formats reviewed include XML formats, HTML documents and word processing documents.  For convenience, and because this academic research doesn't seem to have a better term yet, I call this *Comparative Digital Document Analysis*.  

# Data Philosophy

The basic idea is that we want to try and preserve any form of digital transfer of data as a signal for data, and attempt to make the standard output HTML.  Or, in other words, if we already have uses for which HTML may be appropriate, we are going to try and keep the semantic data or message from the writer in that HTML.  One way of ensuring that the analogue representation does not compromise the message data, is to make any layout features (which are often based on semantic ideas anyway), dependent upon the underlying semantic categories that relate to the message.  The use of CSS fo styling in browser is some for of separation of the text decorations and semantic content, but it is not always appreciated that we need to take more deliberate actions regarding how HTML actually captures the message semantics in the first place.  

In general, HTML is not a semantic language that is based on particular genres or specific discipliens.  However, its close relationship to XML does recognise the possibility of semantic information being captured.   Intead of replacement of HTML, the goal is to use some of HTML (the parts that allow broswers to pass tags as units of information), and then to utilise those areas with the most degrees of semantic freedom (e.g. attributes of p tags) to capture the writer's semantic intentions.

To keep the concept of a carrier layer as simple as possible the software follows the discipline of using the lowest form of interoperable data structure associated with the HTML format: this involves the use of p tags and table tags to the exclusion of most other tags.  The p tags can reproduce the function of most other simple layout tags, except for table, which has a two-dimensional structure.  The writer's semantic information is then to be included in the HTML by way of p tag categories.  p tags can be written within the table cells, which preserves the p tags as a data unit and sources of styles that will still be recognisable in word processors.  I call this standard output *MessengerHTML*.

# How my software works

To help design a software pipeline to process text into MessengerHTML, we can work backwards to think about how we can capture the non-HTML semantics, first, before that upstream information can be sequentially processed into HTML.

My original approach was to process the upstream information into a generic XML file, where the tags were based on semantic information of the writer, not HTML.  The XML format is used, but without any universal specification, other than what is convenient to the whole process and writer flexibility.  In practice, there are some conventions about this that help, but this concept is still in development.  

Within the software, the XML to HTML conversion will take XML tags and turn them into p classes.  The module xmlpub.py handles most of the downstream conversion, together with recursion.py and related sub-modules.

Writing XML is not convenient.  This has been the experience of people trying to implement rigid XML structures like XML (and the same can be said of OOXML, used for word processing).   Therefore, we require a process that will make it easier for writers to introduce semantic information into the downstream processes.  There are many ways to do this: our choice of computing model (how we interpret the input text for output) is very important.  If we allow writers to more easily add useful data categories (and not just HTML tags), then we can capture those categories and include them in the HTML.

However, the way in which text files is interpreted is also important.  In fact, at this point, we may realise that the difference between a plain text file, a computer program and some other format is largely based on whether we have a programming language to turn that text into instructions to the computer.  In turn, whether we have a programming language depends on whether someone has taken the trouble to write an interpreter that will understand what is in the digital text file and act on it accordingly.  If we prepare a programming language that, unlike Markdown, will allow the writer to store text in memory and use it in different ways, then we have created a programmable editing system that gives the writer the ability to make use of more computing functions than a word processor.  We can introduce more and more data-orientated features into the upstream text file, that the writer can then become familiar with.  npmake.py is the main file that processes the input text stream, but it works with other files like commands.py, blockstates.py to provide the writer with a small set of very useful functions.

The design of a new programming language for this process is a creative act.  The way in which we can store data about our writing, re-use it for auto-formatting or manipulation of text before final standard (HTML) output is unlimited.  I have already found a few examples that allow me to format plain text plays (Shakespearean plays from Project Gutenberg) into a readable HTML format whilst still paying attention to semantic categories like Characters and Dialogue.

# An integrated package

This software project is an integrated digital text editing and publication project that provides several writing tools and novel benefits for plain text editing:

- a way of writing as an upstream activity: text preparation of HTML documents for essayists, writers,bloggers and researchers;
- making web pages as collections: a static website production tool, using text files as an alternative to server or database content management systems;
- the option of computable elements in the upstream (input) text: by using a text-streaming model for computation instead of the 'document object model', writers can program other aspects of the formatting of their texts.
- ability to store data and manipulate it before output. This includes the choice of block-based data buffers for working with text, and the ability to filter the pass-through text in default paragraphs (auto-formatting);
- ability to include page numbers and word counts on each page;
- a standardised, minimilist HTML as standard output.  I call this *MessengerHTML*.  By design, this HTML is highly compatible (natively) with word processing formats like those used in LibreOffice and MS Word.

This lays a foundation for interoperable digital storage and transmission formats for literature and law, as well as other possibilities that include integrating computing functions with normal writing projects.

See [NPGuide](NPGuide.md) and [MessengerHTML](MessengerHTML.md)