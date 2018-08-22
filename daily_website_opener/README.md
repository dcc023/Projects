# Daily Websites Opener
### `faves.py`

This program will store all of your favorite websites that you visit daily and will open them all with one simple command line argument.

## Getting Started

There are certain things you may need before getting this program working effectively.

### Prerequisites:

* Python 3
* webbrowser (python package)
```
pip install webbrowser
```

### Commands:
    faves.py 
		Opens all your saved pages in a multi-tab window.

    faves.py [url]
		Adds the url to your saved pages
    
    fave.py ls
		Lists all your saved pages(with the index numbers for easy deletion)
		
    fave.py delete [index | url]
		Deletes the indicated url from your saved pages


## Notes
### Save File 
`savePages.txt`

This program saves the urls in plain text and seperates them by new lines in a text file that is stored in the same directory as the program.

You can easily manipulate the **savedPages.txt** to change your saved pages by just adding a url to a new line or deleting ones you no longer want.

### Default Browser
If you are on Windows, it will try to find Google Chrome in your ProgramFiles(x86).
If not found, it will use whatever your default browser is.

On Edge and Firefox, it seems to open a new window for each website, for me at least. Works best on Chrome.

## Author
* Dylan Campbell / [LinkedIn](https://www.linkedin.com/in/dylancharlescampbell) / [github](http://github.com/dcc023)
