#Layla Game: Obese Ninjas
#By: Layla and Doni

import time
import sys



#FUNCTIONS
#-----------------------------------------------
#death
def death():
	print('GAME OGRE!')
	exit()
#print and wait
def say(text):
	time.sleep(3)
	print('\n' + text)
	sys.stdout.flush()



#GAME
#------------------------------------------------
print('----------------------------------');
print('Obese Ninjas!:');
print('THE GAME');
print('----------------------------------');

#Character creation
charName = input('What shall be your obese ninja name?: ')
print('Greetings, ' + charName + ', it is time to begin your training!')

#Adventure BEGINSSSS

#Coke chugging mission
while(1):
	say('\nWe come to your first quest. Drinking a coke can, ice cold coca cola, in ONE SECOND!!!')
	temp = input('\nAre you ready?(yes or no): ')
	if (temp == 'yes'):
		say('WE MUST BEGIN!! DRINK!!!')
		break
	elif (temp == 'no'):
		say('THEN YOU SHALL DIE!')
		death()
	else:
		print('I can\'t understand you! SPEAK UP BOI!')

say('\nYou pass out from drinking so much ice cold coca cola without breathing..')
say('\nYou wake up in an unknown building.')

#next mission

