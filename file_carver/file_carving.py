import base64
import re

#First decode the file

input_file = open("corrupted.docx", "r") #file to be decoded
output_file = open("decoded.txt", "w") #decoded file output

base64.decode(input_file, output_file) #decode the input file and put result in the outputfile

input_file.close() #close the files to save resources, we're done with them
output_file.close()

#Pepare decoded file to be searched

target_file = open("decoded.txt", "rb") #read the binary version

target_text = target_file.read()
target_file.close()

#Search through decoded file for certain hidden files
#I have decided to use regular expressions to find the patterns

jpg_text = re.findall(r'FFD8.FFD9', target_text) #finds all jpeg files
print(jpg_text)

#GENERATE OUTPUT FILES

jpg_file = open("jpg_file.jpg", "wb")
jpg_file.close()