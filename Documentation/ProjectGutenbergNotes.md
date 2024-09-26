---
Author:Craig Duncan

Date: 26 September 2024
---`

# Summary of Gutenberg e-Book submission and validation process

# Intro

The main pages are intended for people submitting a book that has previously been published, and has a known title, but you can use the submission process to check an HTML page that is created for any other kind of book as well, to see if it would meet Project Gutenberg requirements.

In general, Project Gutenberg assumes that any book will be packaged in a single HTML file, not a number of connected pages.  External links are disqualified.

# Reference pages

(https://www.gutenberg.org/help/file_formats.html#htmlhtm-format)
(https://upload.pglaf.org)
(https://ebookmaker.pglaf.org/index.php)

(https://www.pgdp.net/wiki/DP_Official_Documentation:PP_and_PPV/Post-processing_HTML5)
(https://www.gutenberg.org/help/file_formats.html)
(https://www.gutenberg.org/help/public_domain_ebook_submission.html):


Validators:
CSS:

(https://jigsaw.w3.org/css-validator/validator)

HTML5:

(https://validator.w3.org/nu/#file)

Pre HTML5:

(https://validator.w3.org)

Tight tests, higher bar:

(https://www.pgdp.net/ppwb/pphtml.php)

# Submission process

The HTML for the web and eBook versions is is submitted via the upload portal at (https://upload.pglaf.org), and meets the requirements there for formatting and for proofreading accuracy.

This is basically a quality control process.

In general, these are the assumptions Project Gutenberg works with for submissions of HTML for books, and things I learned

 - There is one HTML file submitted
 - It should be HTML5 (ensure there is at least a `<!DOCTYPE html>` tag at the start)
 - You cannot have external links (convert these to text not HTML if you have to)
 - You cannot have an externally linked style sheet (follows from above)
 - All CSS must be included within `<style>` tags within the `<head>`` section.
 - If you specify `<meta charset = utf-8>` it must be within first 1024 blocks so put it before a large block of CSS if you have it.  
 - It uses only recommended W3C CSS.  Currently this is CSS2.1.  So do not include grids in your CSS etc.
 - You need images inside an images folder.  If you want a cover image for the book you must include an image cover.png or similar.
 - To submit the HTML file and the images folder, you need to zip it.  Do not use GUI 'compress' methods on the mac.  Use command line `zip filename file1 file 2`.

Note also that you shouldn't be submitting a separate CSS file to the e-book checker.  THere are separate CSS validity programs that are recommended, but at the end of those checks, you still need to insert the relevant CSS into the embedded CSS in the HTML file (as above).

There may be an assumption that the title to the book is coded with an `<h1>` tag in some checkers

# After your submission checks are run

When this is run from the web is runs this on the server and the output is a web link to a cache of the e-book, kindle, HTML and `output.txt` file.

There will be an images and no images version of the book.

Read the output.txt to diagnose errors in the submission.

