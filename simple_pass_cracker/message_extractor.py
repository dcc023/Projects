from PIL import Image

#####################
# FUNCTIONS
#####################

def check_lsb(img_array):
	lsbstring = ""

	for i in img_array:
		if i % 2 == 0:
			lsbstring += "0"
		else:
			lsbstring += "1"

	return lsbstring

######################
# MAIN
######################
im = Image.open("Cchapel/mountain.png")

red_array = list(im.getdata(0))
green_array = list(im.getdata(1))
blue_array = list(im.getdata(2))

rgb=["red", "green", "blue"]

rgb[0] = check_lsb(red_array)
rgb[1] = check_lsb(green_array)
rgb[2] = check_lsb(blue_array)

lsb_image = Image.merge("RGB",(rgb[0],rgb[1],rgb[2]))



print(img_array)
print(lsbstring)
print(im.info)