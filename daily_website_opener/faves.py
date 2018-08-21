#! python3
"""
	faves.py - Open up all the pages that you check daily to alleviate
				  the pain of opening them up individually.

	commands:
		faves.py 
			Opens all your saved pages

		faves.py [url]
			Adds the url to your saved pages
		
		fave.py delete [index | url | all]
			Deletes the indicated url from your saved pages

		fave.py ls
			Lists all your saved pages(with the index numbers for easy deletion)
"""
import sys,webbrowser

# Check for savedPages to create one if needed
savedPages = open('savedPages.txt','a')
savedPages.close()

# Set up chrome
chrome_path = "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"
try:
	webbrowser.register('chrome' , None, webbrowser.BackgroundBrowser(chrome_path))
except:
	pass

# Open saved pages
def open_pages():
	pages = open('savedPages.txt').readlines()
	first = True
	for i in pages:
		try:
			webbrowser.get('chrome').open_new_tab(i)
		except:
			webbrowser.open_new_tab(i)


# Add page to saved pages
def save_page():
	open('savedPages.txt','a').write('\n'+sys.argv[1])

# Delete saved pages, using either the index value or raw string
def delete_pages():
	pages = open('savedPages.txt').readlines()
	file = open('savedPages.txt','w')

	for i in pages:
		if i != (sys.argv[2]+'\n') and sys.argv[2] != str(pages.index(i)):
			file.write(i)

# List saved pages
def list_pages():
	pages = open('savedPages.txt').readlines()
	for i in pages:
		print('('+str(pages.index(i))+'): '+i)

# Handle command line arguments
if len(sys.argv) == 1:
	open_pages() 
elif sys.argv[1] == 'ls':
	list_pages()
elif sys.argv[1] == 'delete':
	delete_pages()
else:
	save_page()
