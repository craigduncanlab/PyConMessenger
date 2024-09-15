Comparative Digital Document Analysis
-------------------

A:Craig Duncan

D:13 September 2024

# Licence

See [Licence](LICENCE.md)

# An introduction to Comparative Digital Document Analysis

Comparative Digital Document Analysis is based, in part, on a model that distinguishes between the data that is processed invisibly in computing processes and the representations of information in standard analogue output.  It is a deeper analysis of how visual information in the form of text (which is, at some level, just a visual analogue stimulus for humans), worked on by human beings in digital devices.

The topic concerns analytical framework for any digital documents that focusses on the relationship between the main computing model (whether we analyse it as simple input-output or not) and at what point analogue representions (like text or graphics/images) are requested, and for what purpose.  It aims to compare :

- intermediate final representations of computer memory, and the data structures they are based on; 
- how much of a writer's semantic work-in-progress is available in a computable data structure throughout the process;
- analogue representations of computer memory at any point in the computational process (including final 'word processing' formats in analogue form); and
- how much the writer or human actor can alter the subsequent state of the computer through those analogue representations.

My focus, at present, is on visual textual representations, because there is more room for confusion about the difference between analogue and digital representations than there is with purely image or sound-based representations.  The fact that digital information is used for analogue representations that humans can read, as text, may lead many people to think that a 'digital document' is defined by the analogue representation alone.  In fact, the only distinction that some people make is between documents and electronic documents (e-documents), which at some level is equating the two on the basis that they are both analogue representations, but one is in an electronic medium.

In my view, the fact that a computer delivers an analogue representation of a recognisable document should not mean that this is how it is analysed with respect to its digital nature in an electronic computing device.  Within a computer, the notion of an 'electronic document' is insufficient because it says nothing about the information in the document and how it is processed.  We need some way of distinguishing the variety of ways that any kind of analogue representation of text (which is, in effect, an image for human perception) is also an input or output with respect to digital information.  In fact, an analogue representation focusses almost entirely on an optional 'output', and less on input.  Analogue outputs can be derived from the same underlying digital representations, but may represent different break points, or branches, in that process.  A browser, for example, can choose to make HTML code, otherwise a <i>preceding</i> step in the computational model, available as another analogue output.  This is usually requested by a 'view source' option.  But this does not prevent the same browser continuing to act on that content to provide the clean text in the usual analogue representation.  Rather than think of a single input-output design, we can think of analogue representations as often concerned with computing processes that are in incomplete states. 

# Software development implications

This approach to digital document analysis can help with informed upstream processing and more attention to work-in-progress for both the writer and the software itself.  We can analyse digital documents as multi-stage representations (digital or analogue) of a more continuous computer state.  This is the basis for many data and computing pipelines, but unless we look for a computing process that provides continuity, we are unable to analyse events within the digital domain. 

In relation to text-production, this pipeline is not entirely new, but sometimes the focus is too much on the analogue representations and not on what binds them together.  For example, John Gruber's [Markdown syntax](https://daringfireball.net/projects/markdown/) is a kind of break-point language, in that it allows a person to work with an analogue representation prior to the formulation of HTML.  However, its definition was a reaction to HTML, and a way of asking for some other intermediate analogue representation for human writers (as if they were typing on a typewriter, not in HTML).  It was less focussed on modelling these two analogue points of output as if they were linked by an underlying computational model with a continuous representation of information in memory.  

The point is, that it is not the fact that we can see the document on the screen that is important: what is important is how much the computer environment is prepared to process the file for different functions, and how much the human writer is prepared to take advantage of that deliberate computing model. 

# Implications for text editing software

Even a basic text editor provides some analogue representation, because this is how a human reads it, but its place in a computing workflow is discretionary.  Where we choose to place that analogue representation in a computing process, is, however, completely up to us.  Not only can any digital file exist simultaneously as both an analogue representation and one that is capable of computation, but the nature and effect of it can be altered by programs upstream and downstream of it.  

By taking this observation and thinking about how it might apply to the whole process of computing, from input to output, we can ensure that the notion of analogue representation does not become a limitation on how we interpret and process digital texts for any purpose, not merely for software engineering.  

One consequence of the above framework of analysis is that an intermediate analogue representation of text need not be an interim version of some document's visual appearance that is presented passively.  An intermediate analogue representation in text can be used as an opportunity for interpretation as a sequence of instructions, especially if processed using a text streaming model.    

This progressive interpretation of a text, in digital form, turns out to work quite well for the regular structure of literature, like plays, which already have a kind of instruction and time-based sequence for human readers.  Even when such a text is only partially completed, the introductory semantic information (like the list of characters), can be useful to both human readers and computer-based interpreters of that information, in that it can be used to help process the information in the remainder of the docoument.   

Having considered this, I think there are other software development analogies that can be made, such as the way in which shader languages are used to enable humans to both visualise and control information passing through a graphic information workflow.  The analogue representation, in text, is an intermediate process for the underlying computing model.  The documents and the shader language can also be used to describe conditions which are then used to help define later conditions for both the software and the subsequent flow of information to rendering output.