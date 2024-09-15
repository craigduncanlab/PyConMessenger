How it Works (New Processor and MessengerHTML)
--------

A:Craig Duncan

D:12 September 2024

# Licence

See [Licence](LICENCE.md)

# Background and Introduction

The goal is to produce simple text documents in digital media with little 'noise' from both the message (semantic) perspective, as well as the layout perspective.  This means a cleaner, more self-explicable format that it is easier to parse as well.   By focussing on data capture, I hope that it will encourage better upstream tools, not motivated solely by analogue representation equivalence.

The broader research project that underpins the software is a deeper enquiry into the nature of digital documents, as have evolved, as well as those that might become more common in the future.  The main digital formats reviewed include XML formats, HTML documents and word processing documents.  For convenience, and because this academic research doesn't seem to have a better term yet, I call this *Comparative Digital Document Analysis*.  

# Data Philosophy

The basic idea is that we want to try and try and keep any potential semantic categories in our literature or other digital text within the HTML file, even if it is going to be used to prepare analogue output in something like a browser.  We can separate this, in an abstract sense, by making sure that all our layout is based on those semantic categories, as mapped from p tag classes to CSS styles.  

In general, HTML is not a semantic language that is based on particular genres or specific disciplines.  However, its close relationship to XML does raise the natural expectation that the HTML semantic scheme (p tags, img tags, header tags and so on) is where semantic information gets stored.  This is true in so far as analogue representations are concerned.  However, this project is focussed on data as well.  So the organisation of the HTML is also approached differently, by following the principle that the p tags are just there to hold units of data, and the 'class attribute' is the way in which the writer's own semantic data (like characters, dialogue for a play) will be recorded.   Thus, the p tags become a carrier signal for the data, and the attributes carry the message.

In terms of HTML structure and function, the p tags can reproduce the function of most other simple HTML layout tags, except for table, which has a two-dimensional structure.  p tags can also be written within the table cells, which preserves the p tags as a basic unit of data that is still be recognisable in word processors.  

I call this standardised HTML output *MessengerHTML*.

# How my software works

To help design a software pipeline to process text into MessengerHTML, we can work backwards to think about how we can capture the non-HTML semantics, first, before that upstream information can be sequentially processed into HTML.

My original approach was to process the upstream information into a generic XML file, where the tags were based on semantic information of the writer, not HTML.  The XML format is used, but without any universal specification, other than what is convenient to the whole process and writer flexibility.  In practice, there are some conventions about this that help, but this concept is still in development.  

Within the software, the XML to HTML conversion will take XML tags and turn them into p classes.  The module xmlpub.py handles most of the downstream conversion, together with recursion.py and related sub-modules.

Writing XML is not convenient.  This has been the experience of people trying to implement rigid XML structures like LegalXML (and the same can be said of OOXML, used for word processing).   Therefore, we require a process that will make it easier for writers to introduce semantic information into the downstream processes.  There are many ways to do this: our choice of computing model (how we interpret the input text for output) is very important.  If we allow writers to more easily add useful data categories (and not just HTML tags), then we can capture those categories and include them in the HTML.

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

# Theoretical inspirations

My own analysis of digital document formats as summarised in [Comparative Digital Document Analysis](ComparativeDigitalDocAnalysis.md) has implications for how I think about text editing software.  This is mainly related to the idea that we do not have to view text in any file that we can read as a representation of its final state: any text can be used for instructions in a longer pipeline of work, especially if processed in a text streaming model.  

In relation to text streaming models, my workflow has some elements that are similar to the old <i>sed</i> program in unix systems, but has been developed independently in Python, without trying to reproduce that program, or be limited to its assumptions.  Unlike's sed's limited use of a buffer, my program makes data blocks a high-level priority, so that variables and memory use can be actively planned and revised in the course of preparing a document.  Each text document can be interpreted both as a readable text and a record of a sequence of instructions.

If we are using a text streaming model, to allow a human writer/reader to look at text, there is a question about where we might put it in the workflow.  Even a basic text editor provides some analogue representation, because this is how a human reads it, but its place in a computing workflow is discretionary.  Where we choose to place that analogue representation in a computing process, is, however, completely up to us.  Not only can any digital file exist simultaneously as both an analogue representation and one that is capable of computation, but the nature and effect of it can be altered by programs upstream and downstream of it.  By taking this observation and thinking about how it might apply to the whole process of computing, from input to output, we can ensure that the notion of analogue representation does not become a limitation on how we interpret and process digital texts for any purpose, not merely for software engineering.  

This progressive interpretation of a text, in digital form, turns out to work quite well for the regular structure of literature, like plays, which already have a kind of instruction and time-based sequence for human readers.  Even when such a text is only partially completed, the introductory semantic information (like the list of characters), can be useful to both human readers and computer-based interpreters of that information, in that it can be used to help process the information in the remainder of the docoument.   

Having considered this, I think there are other software development analogies that can be made, such as the way in which shader languages are used to enable humans to both visualise and control information passing through a graphic information workflow.  The analogue representation, in text, is an intermediate process for the underlying computing model.  The documents and the shader language can also be used to describe conditions which are then used to help define later conditions for both the software and the subsequent flow of information to rendering output.