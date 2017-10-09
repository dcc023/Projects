import zipfile
import string
import sys
from os import path

#################
# FUNCTIONS
#################

def crack_pass(target):
	letters = "".join(string.lowercase)
	for a in letters:
		for b in letters:
			for c in letters:
				for d in letters:
					for e in letters:
						password = (a+b+c+d+e)
						try:
							say(password)
							target.extractall(pwd=password)
							say("The password is: " + password + "\n We did it!")
							return
						except:
							pass

def say(text): #print and flush
	print(text)
	sys.stdout.flush()

#################
# MAIN
#################

say("##########################")
say("#     Password Cracker   #")
say("#    By Dylan Campbell   #")
say("##########################")
say("\n")

say("What file would you like to crack?")
file = raw_input()

while not path.exists(file):
	say('File not found, try again.')
	file = raw_input()	

try:
    targetzip = zipfile.ZipFile(file)
except zipfile.BadZipfile:
    print "[!] There was an error opening your zip file."

crack_pass(targetzip)