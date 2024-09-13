Comparative Digital Document Analysis
-------------------

A:Craig Duncan

D:12 September 2024

# Licence

See [Licence](LICENCE.md)

# An introduction to Comparative Digital Document Analysis

Comparative Digital Document Analysis is based, in part, on an analytical framework for digital documents that gives priority to the function of digital information (whether it be data, encoding, files etc) that remains within the computing system, in the context of general computing.  It focusses on the process of encoding information in digital form right up to the point it is converted to analogue signals in a standard output device, like a monitor or speaker.  

One initial method of analysis is to view the digital documents as part of a linear sequence of inputs and outputs, bridged by some model of a computer represented by specific software.  Using that analysis, we look for the point at which digital computation ceases, and analogue representations for human beings commence (this is not the end point of thinking, but it may be the end point of computation, in that model).  The layperson may be unaware of this lack of continuity, and will *recognise* or project the on-screen representations of documents in such a way that it is indistinguishable from any unseen, preceding digital form that produced it.  

Sometimes this blurring of the digital/analogue boundary can be broken or rewound.  A browser, for example, can choose to make HTML code, otherwise a <i>preceding</i> step in this model, available as if it were a final analogue output.  This is done by 'view source'.  

The notion of rewinding analogue representations back to preceding digital representations is intimately bound with the need for humans to be offered another analogue representation, in each case, to make sense of that process.  For example, a computer programmer usually wants access to visible text in the form of 'code' because it is considered convenient for manual viewing and updating, and the writing of instructions. In general, we always need to bridge the gap between the mechanical, analogue human, and the digital processor.  

# Subtle reframings in graphical software

What I have just discussed is a linear, sequential model of computing which is convenient because it helps us become aware of how graphical software and windowing models used for digital document editing create a degree of circularity in the computing model.  By presenting an analogue interface to a person for input and output with no additional computing functions.  Typing into a word processor, for example, presents the analogue representation as if it were a mechanical process, for both input and output.  There is no 'rewinding' back to some underlying digital format, only 'rewinding' in the sense of undoing the mechanical process (e.g. an undo button).   

It is possible to use a different model to 'rewind' the model of computing, if you do so deliberately with an awareness of these assumptions.  For example, by looking for the preceding computational form, we might be drawn to look at the file format stored on the disk, and inspect the more explicit digital formats like OOXML.  This is an analogous process to inspecting HTML source code in a browser.  In both cases, what we are doing, in terms of digital document concepts, is more easily explained by a sequential model that pays attention to where digital computing ends, and analogue representation begins.

# E-readers

In the case of digital documents that only have the expectation of prodicng analogue output for human consumption, there is no real expectation of rewinding to the digital/analogue boundary (i.e. they don't offer the ability to view HTML source, for example).  A mobile phone with a broswer application is also likely to be indifferent to offering HTML source inspections.

# Concepts of digital documents

This focus on paying more attention to a model of computing can help us reflect on some terms used for digital documents, by laypersons, that are not based in computing at all.

For example, terms like electronic documents, or e-documents, are not even concerned with digital/analogue distinctions.  They are not informative about computing, let alone a model of computing.  People using these terms are less likely to be considering what forms of digital abstraction are possible, or making them visible in an analogue form.

The preparation of digital media as an analogue output for *consumption* is usually prepared by someone other than the reader.  This framing is strongly influenced by economic models and distinctions: the roles of users/readers are descriptions that often assume that the software producer or manufacturer is the proactive producer of the analogue form of digital media, and has computing enabled, whilst the human readers, whether they be professional information workers or not, are relatively passive recipients, with computing disabled, and analogue representations foregrounded.

# Comparative digital analysis is based on a general computing model for information

Comparative digital analysis is based on paying attention to sequential computing processes, and being aware of the digital/analogue discontinuity in computing.  It is not based on an economic model referring to analogue outputs in commercial software production.

My aim is to be able to to analyse and define digital documents that provide computable data, data that is used for analogue representation on screen, or perhaps both.  The central idea is that we take into account the full extent to which any digital document can form a part of a holistic model of computing, in which we regard analogue representation as only a possible output, and not a necessary output.  I take it as a given that some analogue outputs will look familiar as traditional media, but then ask: despite this, what should we retain or leave out of the digital format that can be interpreted in that way?  We should engage in a broad analysis of the relationships between form and function, structure and purpose.

# A digital document in a computer is analysed differently from its output form

The analysis is not merely based on looking at a sequential input and output process, as a starting point for giving a sense of directionality to the digital/analogue discontinuity: we can prepare an even more detailed analysis of the text within digital documents that are interpreted within a computing model by examining the information flow within the digital part of the analysis.  That is, if we rewind back in our computing model, we can consider multiple ways in which a digital document becomes relevant to the computer, and computing processes, even before it becomes relevant to the human being that is going to perceive the analogue output.  This might include it being repurposed as a kind of program, even one that will operate on itself.

All of what I said at the beginning about how a human being might be invited to visually inspect earlier parts of the computing process still apply: to the extent we can imagine a digital document within the computing process is capable of containing instructions, or programs too, we can then offer an analogue version so that a human can not only see, but interact with that earlier stage of the computing model.   In my view, this is what allows us to think about reframing and interpreting digital text documents as both documents intended for analogue representation, as well as somethign that can be considered a program, even one that operates on itself.

Once we have a broader awareness of what is possible, we can better perceive the limited choices or missed opportunities associated with the form of digital documents that only work backwards from analogue output to determine the form of the intermediate, computable forms.

# What parameters are important in this analysis?

Our analysis of any digital document format can include these questions:

- whether a format like HTML is information-rich or noisy from the perspective of the writer's original semantic data and literary goals.  
- whether any standards for how information and data is packed into HTML will make it easier to retrieve that data in downstream processes.
- whether the information is packed into HTML as a response to the desired analogue output, or independently of it.
- whether the information in the HTML, in terms of data structures prior to its final, published analogue interpretation, is capable of independent interpretation by a computing machine, or whether its importance is only evident in the analogue representation perceived by a human being.

If information other than the writer's own semantic content is incorporated into the document merely through the publication process, then the end result is often a noisy document and inconvenient structures for re-acquiring the information down stream.  However, informed data standards for HTML preparation may make that task easier.  For example, implementing MessengerHTML should make it easier to scrape data from the HTML with something like Beautiful Soup, than HTML prepared in ignorance of downstream uses.  
With Messenger HTML, if you turn off CSS you will still have something that contains the same data in its HTML, and is probably very clean and simple in your browser as well.  Your code should, in its HTML form, be clean and readable without too many nested tags or distractions.

# Writing syntaxes designed for analogue-focussed digital output

Even though writing in a digital computer may seem like 'digital' input, if the main focus of the software output is analogue presentation (to a human reader), and it lacks attention to data, then it is likely that it remains analogue-focussed digital software from input to output.  This analytical description helps us become more aware of the fact that the computable functions in software that interprets or transforms using this as the principal syntax will tend not to offer the writer any intermediate computing functions that do not relate to analogue output.

For example, Markdown syntax (John Gruber) is capable of being analysed as a shorthand version of HTML, in that its primary focus is to help the writer provide instructions for analogue layout, but disguising that function by making the text look like it is a set of detective's notes written in an old mechanical typewriter.  This has little interest in making it easier to record the text for data transmission purposes.  However, it has created or perpetuated the culture of focussing on analogue representations as if they defined what a digital document is.  This now extends to analogue-representation converters like pandoc.  The reason that YAML formats are supplementary data sections within Markdown and pandoc Markdown is largely because the analogue-focussed digital format is supplemented with data only where it is deemed necessary, but not because data is a first-level concern of the computing process.

With GUI formats (WYSIWYG), the insulating effect of analogue representations is even greater.  Instead of there being a linear input to output process focussed on analogue representation, the input is also made to look like the output.  The difference between input and output shrinks, so that it all looks like analogue representation.  The writer is, despite the buttons and mechanisms of the digital software, really being asked to pretend they are still using a digital typewriter without data functions. 

# Informed upstream processing

By adopting a functional definition for digital documents that includes some use of writer's data, we can move toward more deliberate processes that aim to achieve retention of semantic information.  This can help with a new kind of definition for what we mean by digital media and a semantic web.

We have a choice, for example, between digital texts that merely use text decorations for standard output, like Markdown, or ones that build-in the expectation of general functions and data definition blocks within a literary of essay-like text.  This allows the writer to work with a program that does not allow analogue representation to dominate the possibility of data and computable text.  This isn't just a change to how we produce analogue output; it is also a change to the extent to which a writer can use computation and numerical tools, or text processing, within the same software that is allowing them to process text.

I am not merely describing an integrated text editor that has extra features.  My initial project is based on the idea that we can prepare a digital document in any text editor and that what matters is having a program that provides an interpretation of its contents.  To the extent this allows data storage and functions, I call this a programming language, and an interpreter, rather than a 'markup language'.  Of course, it has features in common with both markup languages and programming languages, but these are fundamental to computing: data partitions, grouping of text.  These are true of any data format; what matters is what we enable the computer to do with it.

Another interesting possibility of this analysis is that rule-based processing of documents, as a text stream (rather than using a document object model) can be enabled by allowing the writer to use functions that apply to the balance of the digital document (assuming a top to bottom processing direction).  Any programmatic interpretation of digital text files offers the possibility that line by line marking up can be replaced by an automated pattern-matching and replacement process.  For example, we can deliberate program the text interpreter to act on replacement rules that look for particular text, and if it is found, process it to standard output with a particular category.  This auotomatic semantic labelling is very effective for auto-formatting of plays in literature, for example.

Another observation is that even a basic text editor provides some analogue representation, because this is how a human reads it.  However, in programming or coding, it was always understood that this was merely a means to an end, namely the subsequent processing of the crafted text file as instructions for a computer.  From this we should conclude that any digital file can exist simultaneously as both an analogue representation and one that is capable for computation.  

By taking this observation and thinking about how it might apply to the whole process of computing, from input to output, we can ensure that the notion of analogue representation does not become a limitation on how we interpret and process digital texts for any purpose, not merely for software engineering.  For example, in my project, a text file does not fall neatly into the category of a memo or program, or an essay or program.   It is possible to have functions and data blocks in the same 'file' as a play, as well as having two files where the more functional elements are separated.  The point is, that it is not the fact that we can see the document on the screen that is important: what is important is how much the computer environment is prepared to process the file for different functions, and how much the human writer is prepared to take advantage of that deliberate computing model. 