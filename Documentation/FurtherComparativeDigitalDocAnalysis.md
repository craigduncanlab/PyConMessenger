Some Further Comparative Digital Document Analysis
-------------------

A:Craig Duncan

D:15 September 2024

# Analogies with literature

A writer of digital documents, including literature, is still more concerned with representing the flow of events (like in a program), rather than simply the analogue form of the finished play.  Within that flow of events, there are categories of information important to the writer that are independent of the process of making analogue output in a computer.

A writer may prepare a list of characters as part of the work-in-progress, that forms an introductory section to the play.  This primes the reader for what is coming later.  It alters the state of mind of the reader, just as variable definitions in a computer program alter the memory of a computer.  In that way, there is some process going on for which the analogue representation is merely a means to an end, but not the end in itself.  

In fact, the choice of appearance of a play, even in analogue representations, was influenced by the need to vary the appearance according to rules.  We could suggest this as a general rule: any text that orders or arranges events in writing has some information that can be made relevant to rules that are useful patterns for altering the appearance of these things in a computer (this is the basis of the functions for auto-tagging in the New Processor).  The important thing is to ensure that the content has greater priority or precedence than the rules for analogue representation. 

# The usefulness of a model of computation up to the point of analogue representation

How and when analogue representations (as text) are produced, and what part of the 'computing model' they apply to, is a matter of choice.  It relates to how far upstream we want to invite computer users, including professional information workers, to participate in computing processes.  For word processing software, this is usually not very far back at all.  The point is - this availability of an analogue representation is a social convention, or a software industry convention, or something determined by the software market. 

There is a difference between 

- a computing process that offers different break points (analogue representations) to the user, as part of the same work in progress; and
- offering a completely different software product focussed on a completely different analogue representation.

For example, word processors and spreadsheet programs rely on running different programs, each with a different model of computation, rather than treating writing and computation in the same general work-in-process, where they might be just different analogue representations of a holistic state of memory.

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