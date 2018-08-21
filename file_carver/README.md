# File Carver
###`file_carving.py`

This program scrapes through a given file and exposes the hidden files amongst it. 
Locates jpeg, gif, pdf, and png files and outputs them.

## Getting Started

There are certain things you may need before getting this program working effectively.

###Prerequisites:

* Python 2.7



###How To:
1. The program is setup to carve any file you give it as an input. For our case we will use
“corrupted.docx”. When prompted, just type “corrupted.docx” (make sure it is in same
directory as file_carving.py)
2. It will then ask if the file is in base64 to know whether it needs to decode it. Type “yes”.
3. It will then search through and output the files into the working directory.(jpeg, gif,
pdf,png)


##Notes
 
* I used HxD to search various filetypes, specifically jpeg, pdf, gif, and png, for their
header and footer tags.
* After grabbing those tags, I just created the regular expressions to find every instance
within the file that starts with the header and end with the footer magic numbers.
* To make the regular expressions work simpler, I used the binascii library to “hexlify” the
file so that the file text became raw hex. Then after searching, I dehexlified it and output
it to the specific filetype.
* Inititally I used the base64 library to decode it from base64 to ascii.

##Author
* Dylan Campbell / [LinkedIn](www.linkedin.com/in/dylancharlescampbell) / [github](http://github.com/dcc023)
