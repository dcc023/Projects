import base64
import binascii
import re
import os
from os import path
import time
import sys

####################
#FUNCTIONS
####################

def decode_base64(file): #decode file from base64 to ASCII
	input_file = open(file, 'rb') #file to be decoded
	output_file = open("decoded.bin", 'wb') #decoded file output

	base64.decode(input_file, output_file) #decode the input file and put result in the outputfile

	input_file.close() #close the files to save resources, we're done with them
	output_file.close()

def search_file(file): #search given file
	#Pepare decoded file to be searched
	target_file = open(file, 'rb').read()
	hex = open("hex.txt", 'wb').write(binascii.hexlify(target_file))

	#Search through decoded file for certain hidden files
	#I have decided to use regular expressions to find the patterns

	#finds all jpeg files
	jpg_text = re.findall(r'ffd8.*ffd9', binascii.hexlify(target_file)) #change to hex and search file for jpeg magic numbers
	jpg_file = open("jpg_file.jpg", 'wb')
	jpg_file.write(binascii.unhexlify(jpg_text[0]))
	jpg_file.close()

	#find all pdf files
	pdf_text = re.findall(r'25504446.*25454f46', binascii.hexlify(target_file))
	pdf_file = open("pdf_file.pdf", 'wb')
	pdf_file.write(binascii.unhexlify(pdf_text[0]))
	pdf_file.close()

	#find all gif files
	gif_text = re.findall(r'47494638.*3b', binascii.hexlify(target_file))
	gif_file = open("gif_file.gif", 'wb')
	gif_file.write(binascii.unhexlify(gif_text[0] + "0"))
	gif_file.close()

	#find all png files
	png_text = re.findall(r'89504e47', binascii.hexlify(target_file))
	png_file = open("gif_file.gif", 'wb')
	png_file.write(binascii.unhexlify(png_text[0]))
	png_file.close()

def say(text): #print and wait
	print(text)
	sys.stdout.flush()

####################
# MAIN
####################

say('----------------------------------');
say('           File Carver:');
say('         by Dylan Campbell');
say('----------------------------------');
sys.stdout.flush()

say('What file would you like to carve?')
file = raw_input()

while not path.exists(file):
	say('File not found, try again.')
	file = raw_input()	

say('Is the file in base64?(yes/no)')
encrypted = raw_input()

if encrypted.lower() == 'yes':
	decode_base64(file)
	search_file("decoded.bin")
else:
	search_file(file)
##notes
# PDF: eof = 25 25 45 4F 46 0D 0A




