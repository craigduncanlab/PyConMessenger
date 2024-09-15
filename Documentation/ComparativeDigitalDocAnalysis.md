Comparative Digital Document Analysis
-------------------

A:Craig Duncan

D:13 September 2024

# Licence

See [Licence](LICENCE.md)

# An introduction to Comparative Digital Document Analysis

Comparative Digital Document Analysis is based, in part, on an analytical framework for any digital documents that aims to compare how much they are actively involved in altering the computational state of the computer, and not merely any analogue output.  It focusses on the process of encoding information in digital form right up to the point it is converted to analogue signals in a standard output device, like a monitor or speaker.  

An important aspect of this is to take into account that a digital document is an abstract concept, and so the purpose of creating one, and in what context, should always be referable to a model of computing.  The fact that digital information is used for analogue representations that humans can read is not, by itself, the definition of what a digital document is.  Rather, it explains why some digital documents exist, but it does not limit what digital documents can or should be.

The bias that the layperson or a programmer has toward readable digital documents is natural: these are the ones we interact with.  However, such interaction is itself carefully provided for by software that represents text on screen.  It is merely one branch of a computing process.  A browser, for example, can choose to make HTML code, otherwise a <i>preceding</i> step in the computational model, available as another analogue output.  This is done by 'view source'.  But this does not prevent the same browser continuing to act on that content to provide the analogue representation.

Our ability to interact with the computer is never a fixed state, but one that is always designed by custom software to allow it to happen, even when we are writing and programming.  Rather than think of software designed for analogue representations (of 'documents') as being a special case, we can think of analogue representations of any kind, during the running of a computer program, as being optional (and sometimes co-existing) break points to allow humans to see the state of a work-in-progress.  This work could be the memory state of a runnning program, or it could even be the state of a program yet to be executed, or a written document yet to be put into publishable form.

Rather than think of a single input-output design, we can think of analogue representations as often concerned with computing processes that are in incomplete states. 

At any time that an input-output process is broken, by representing information in an analogue form for humans to read (some standard output), there is a break in the continuity of the computation.  The analogue output is like the leaves on the branch of the tree.  The layperson may be unaware of this lack of continuity.  In fact, it is expected that human readers will *recognise* or project the on-screen representations of documents onto some unseen, preceding digital form that produced it. 

# Analogies with literature

A writer of digital documents, including literature, is still more concerned with representing the flow of events (like in a program), rather than simply the analogue form of the finished play.  Within that flow of events, there are categories of information important to the writer that are independent of the process of making analogue output in a computer.

However, these two models of interaction with a computer are not entirely independent: any text that orders or arranges events in writing has some information that can be made relevant to rules that are useful to a computer than can alter the appearance of the analogue representations.  The important thing is to ensure that the content has greater priority that the rules for analogue representation. 

# The usefulness of a model of computation up to the point of analogue representation

How and when analogue representations (as text) are produced, and what part of the 'computing model' they apply to, is a matter of choice.  It relates to how far upstream we want to invite computer users, including professional information workers, to participate in computing processes.  For word processing, this is usually not very far back at all.  The point is - this availability of an analogue representation is a social convention, or a software industry convention, or something determined by the software market. 

There is a difference between 

- a computing process that offers different break points (analogue representations) to the user, as part of the same work in progress; and
- offering a completely different software product focussed on a completely different analogue representation.

For example, word processors and spreadsheet programs rely on running different programs, each with a different model of computation, rather than treating writing and computation in the same general work-in-process, where they might be just different analogue representations of a holistic document in memory.

If we have one main computing model then we can think of any digital-media analogue representation as interim, break points in a more general process.  We can think of some as, perhaps, 'rewind' points for the same process.  Where we decide to put those breakpoints, ie how far upstream or downstream, is arbitrary.  For example, a computer programmer usually wants access to visible text in the form of 'code' because it is considered convenient for manual viewing and updating low-level instructions for the computer.  You can even write code to produce HTML, so the code that does this might be regarded as 'preceding' the HTML source, which in turn, precedes the analogue representation of that code in a browser, in a form that a human can read.

Using our linear model of digital computing, however, we can also appreciate that programmers work with analogue representations/digital documents that are important for preparing software, but which may ultimately become invisible to end users.  The opportunity to see some documents as digital texts, because an analogue representation is made available, is conditional on that being useful for some human goal.   

Knowing that we can create intermediate points between writing and analogue output, we can consider the extent to which analogue representations involve a sense of continuity, the purity of the semantic information being represented, and how much 'noise' is introduced to the main signal just because it is requested in an analogue form.  For example, how much 'noise' is there in an HTML page, if all we wanted was some information in clear categories?  Would we want to be able to inspect that same information, at an earlier process in the computing process, before such noise was introduced?

# Analysing documents produced by graphical editing software

A graphical software program for text editing might not give the user any sense of computational time.  The analogue interface that represents the image of a final document only models the user interface as an ever-refreshing 'present', rather than a linear sequence.  Concepts like the 'undo' or 'redo' buttons are only concerned with changes to the analogue representation, not the computing model as a whole that produces the final document.   That is, the user is only offered the same analogue representation, but the program might capture what that is at different times.  The program does not offer the user the ability to rewind back to data structures that exist before the analogue representation was attempted at all.

Looking at digital file formats through the lens of 'computing time' or 'writer time', rather than analogue representation alone, is one way we can start to unpack what kinds of pre-graphical information we might want to include in an HTML file that is being imported into a program that will use something like an OOXML format.

It is very useful to think of any analogue representation of text as an <i>optional</i> form of standard output, that is a branch or juncture from the digital computing process already being followed in the computer.  We do not just have to think about one single final output.

Also, if we think about the information that is important to the writer, in writer-time, then we can follow through and ask how much of the data format used for analogue output is actually focussed on this, or some other purpose.

# What parameters are important in this analysis?

Our analysis of any digital document format can include these questions:

- whether a format like HTML is information-rich or noisy from the perspective of the writer's original semantic data and literary goals.  
- whether any standards for how information and data is packed into HTML will make it easier to retrieve that data in downstream processes.
- whether the information is packed into HTML as a response to the desired analogue output, or independently of it.
- whether the information in the HTML, in terms of data structures prior to its final, published analogue interpretation, is capable of independent interpretation by a computing machine, or whether its importance is only evident in the analogue representation perceived by a human being.

If information other than the writer's own semantic content is incorporated into the document merely through the publication process, then the end result is often a noisy document and inconvenient structures for re-acquiring the information down stream.  However, informed data standards for HTML preparation may make that task easier.  For example, implementing MessengerHTML should make it easier to scrape data from the HTML with something like Beautiful Soup, than HTML prepared in ignorance of downstream uses.  
With Messenger HTML, if you turn off CSS you will still have something that contains the same data in its HTML, and is probably very clean and simple in your browser as well.  Your code should, in its HTML form, be clean and readable without too many nested tags or distractions.

# Informed upstream processing and work-in-progress

By adopting a functional definition for digital documents that includes some use of writer's data, we can move toward more deliberate processes that aim to achieve retention of semantic information.  This can help with a new kind of definition for what we mean by digital media and a semantic web.

Programs that derive their syntax mainly from downstream layout formats, like HTML's set of tags, are not going to be sufficient to capture genre or writer-specific information categories.  We have a choice, for example, between digital texts that merely use text decorations to change the appearance of standard output, like Markdown, or ones that aim to capture semantic intentions first.

Thinking about the multiple points at which analogue output can be prepared during a computing process isn't just a usaul way of thinking about analogue output, but also about what is important for work-in-progress.  This isn't just a change to how we produce analogue output; it is also a change to the extent to which a writer can use computation and numerical tools, or text processing, within the same software that is allowing them to process text.

I am not merely describing an integrated text editor that has extra features.  My initial project is based on the idea that we can prepare a digital document in any text editor and that what matters is having a program that provides an interpretation of its contents.  To the extent this allows data storage and functions, I call this a programming language, and an interpreter, rather than a 'markup language'.  Of course, it has features in common with both markup languages and programming languages, but these are fundamental to computing: data partitions, grouping of text.  These are true of any data format; what matters is what we enable the computer to do with it.

# Possibilities for more automated downstream analogue output

Another interesting possibility is that rule-based processing of documents, as a text stream (rather than using a document object model) can help with taking any document as a kind of work-in-progress up to a certain point in the document.  The idea that a document itself has a kind of computational time means it can work more like a program, and allow subsequent output to be affected more deliberately.  

For example, any programmatic interpretation of digital text files offers the possibility that line by line marking up can be replaced by an automated pattern-matching and replacement process.  An earlier part of the document can setup conditions that will then be used for intepreting later parts of the document.   This turns out to work quite well for the regular structure of literature, like plays, which also have a time-based structure. 

# Implications for text editing software

Another observation is that even a basic text editor provides some analogue representation, because this is how a human reads it.  However, in programming or coding, it was always understood that this was merely a means to an end, namely the subsequent processing of the crafted text file as instructions for a computer.  From this we should conclude that any digital file can exist simultaneously as both an analogue representation and one that is capable for computation.  

By taking this observation and thinking about how it might apply to the whole process of computing, from input to output, we can ensure that the notion of analogue representation does not become a limitation on how we interpret and process digital texts for any purpose, not merely for software engineering.  For example, in my project, a text file does not fall neatly into the category of a memo or program, or an essay or program.   It is possible to have functions and data blocks in the same 'file' as a play, as well as having two files where the more functional elements are separated.  The point is, that it is not the fact that we can see the document on the screen that is important: what is important is how much the computer environment is prepared to process the file for different functions, and how much the human writer is prepared to take advantage of that deliberate computing model. 