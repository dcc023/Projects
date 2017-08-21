import libtcodpy as libtcod
import math
import textwrap

#size of the window
SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50

#map size
MAP_WIDTH = 80
MAP_HEIGHT = 43

#maximum frames-per-second
LIMIT_FPS = 15

#tile colors
color_dark_wall = libtcod.Color(0,0,100)
color_light_wall = libtcod.Color(130, 110, 50)
color_dark_ground = libtcod.Color(50,50,150)
color_light_ground = libtcod.Color(200, 180, 50)
#black = libtcod.Color(0,0,0)

#player details
playerx = SCREEN_WIDTH/2
playery = SCREEN_HEIGHT/2

#dungeon generation
ROOM_MAX_SIZE = 10
ROOM_MIN_SIZE = 6
MAX_ROOMS = 30
MAX_ROOM_MONSTERS = 1
MAX_ROOM_ITEMS = 3

#field of view
FOV_ALGO = 0 #default
FOV_LIGHT_WALLS = True
TORCH_RADIUS = 10

#sizes and coordinates relevant for GUI
BAR_WIDTH = 25
PANEL_HEIGHT = 7
PANEL_Y = SCREEN_HEIGHT - PANEL_HEIGHT
INVENTORY_WIDTH = 50

#message gui
MSG_X = BAR_WIDTH + 2
MSG_WIDTH = SCREEN_WIDTH - BAR_WIDTH - 2
MSG_HEIGHT = PANEL_HEIGHT - 1

#item constants
LIGHTNING_RANGE = 5
LIGHTNING_DAMAGE = 20

#CLASSES
class Rect: #a rectangle on the map, used to characterize a room
	def __init__(self,x,y,w,h):
		self.x1 = x
		self.y1 = y
		self.x2 = x + w
		self.y2 = y + h

	def center(self):
		center_x = (self.x1 + self.x2)/2
		center_y = (self.y1 + self.y2)/2
		return (center_x, center_y)

	def intersect(self, other):
		#returns true if this rectangle intersects with anothe one
		return (self.x1 <= other.x2 and self.x2 >= other.x1 and
				self.y1 <= other.y2 and self.y2 >= other.y1)

class Tile: #a tile of the map and its properties
	def __init__(self,blocked,block_sight = None):
		self.blocked = blocked

		#by default, if a tile is blocked, it also blocks sight
		if block_sight is None:
			block_sight = blocked
		self.block_sight = block_sight
		#start all tiles unexplored
		self.explored = False

class Object: #generic object: player, monster, item. etc
	global distance

	def __init__(self,x,y,char, name, color, blocks=False, fighter=None, ai=None, item=None):
		self.name = name
		self.blocks = blocks
		self.x = x
		self.y = y
		self.char = char
		self.color = color

		self.fighter = fighter #let fighter know who owns it
		if self.fighter:
			self.fighter.owner = self

		self.ai = ai # let ai know who owns it
		if self.ai:
			self.ai.owner = self

		self.item = item #let item know who owns it
		if self.item:
			self.item.owner = self

	def move(self,dx,dy): #move by given amount
		if not is_blocked(self.x + dx, self.y + dy):
			self.x += dx
			self.y += dy

	def draw(self):
		#only draw if visible to player 
		if libtcod.map_is_in_fov(fov_map, self.x, self.y):
			#set the color and draw char that represent object at position
			libtcod.console_set_default_foreground(con,self.color)
			libtcod.console_put_char(con,self.x,self.y,self.char,libtcod.BKGND_NONE)

	def clear(self): #erase the char that represents this object
		libtcod.console_put_char(con,self.x,self.y,' ',libtcod.BKGND_NONE)

	def move_towards(self, target_x, target_y):
		#vector from this object to the targetm and distance
		dx = target_x - self.x
		dy = target_y - self.y
		distance = math.sqrt(dx ** 2 + dy ** 2)

		#normalkize to length 1(preserve direction), then round it
		#and convert it to int so the movement is restricted to the map grid
		dx = int(round(dx/distance))
		dy = int(round(dy/distance))
		self.move(dx,dy)

	def distance_to(self, other):
		#return the distance to another object
		dx = other.x - self.x
		dy = other.y - self.y
		return math.sqrt(dx ** 2 + dy ** 2)

	def send_to_back(self):
		#make these drawn before anything else, move to front of objects list
		global objects
		objects.remove(self)
		objects.insert(0, self)

class Fighter:
	#combat properties (monster, npc, player, etc)
	def __init__(self, hp, defense, power, death_function=None):
		self.death_function = death_function
		self.max_hp = hp
		self.hp = hp
		self.defense = defense
		self.power = power

	def take_damage(self, damage):
		#apply damage
		if damage > 0:
			self.hp -= damage

		if self.hp <= 0:
			function = self.death_function
			if function is not None:
				function(self.owner)

	def attack(self, target):
		#attack formula
		damage = self.power - target.fighter.defense

		if damage > 0:
			#target takes damage
			message(self.owner.name.capitalize() + ' attacks ' + target.name + ' for ' + str(damage), libtcod.light_red)
			target.fighter.take_damage(damage)
			
		else:
			message(self.owner.name.capitalize() + ' misses ' + target.name, libtcod.white)



	def use_stat_item(self, target):
		#item
		if target.stat == 'health':
			if self.hp < self.max_hp:
				message(self.owner.name.capitalize() + ' uses ' + target.owner.name + ' for ' + str(target.value) + ' health')
				self.hp += target.value
				if self.hp > self.max_hp: #checks to not exceed max hp
					self.hp = self.max_hp
			else:
				message('you already max health fam')
				return 0

		inventory.remove(target.owner)



		


class BasicMonster:
	#AI for basic monster
	def take_turn(self):
		#if monster can see you if you see it
		monster = self.owner
		if libtcod.map_is_in_fov(fov_map, monster.x, monster.y):

			#move towards player if far away
			if monster.distance_to(player) >= 2:
				monster.move_towards(player.x, player.y)

			#close enough, attack! (if player is still alive)
			elif player.fighter.hp > 0:
				monster.fighter.attack(player)

class Item:
	#item properties(value, stat affected)
	def __init__(self, value, stat, info, use_function=None):
		self.value = value
		self.stat = stat
		self.info = info
		self.use_function = use_function

	def pick_up(self):
		#add to inventory
		if len(inventory) >= 26:
			message('inventory is full', libtcod.red)
		else:
			inventory.append(self.owner)
			objects.remove(self.owner)
			message('you picked up a ' + self.owner.name, libtcod.green)

	def use(self):
		#checks if item is useless
		if self.stat is None:
			message('The ' + self.owner.name + 'has no effect')

		#if non stat based item
		elif self.stat == 'special':
			if self.use_function() != 'cancel':
				inventory.remove(self.owner)

		#if nothing else, it is a stat item
		else:
			message('use item')
			player.fighter.use_stat_item(self)
			#inventory.remove(self.owner)




#FUNCTIONS
def create_h_tunnel(x1,x2,y): #horizontal tunnel
	global map
	for x in range(min(x1,x2), max(x1,x2)+1):
		map[x][y].blocked = False
		map[x][y].block_sight = False

def create_v_tunnel(y1,y2,x): #vertical tunnel
	global map
	for y in range(min(y1,y2),max(y1,y2)+1):
		map[x][y].blocked = False
		map[x][y].block_sight = False

def create_room(room):
	global map #go through the tiles inside the rectangle
	for x in range(room.x1+1,room.x2):
		for y in range(room.y1+1,room.y2):
			map[x][y].blocked = False
			map[x][y].block_sight = False

def make_map():
	global map

	#fill map with blocked tiles
	map = [[ Tile(True)
		for y in range(MAP_HEIGHT)]
			for x in range(MAP_WIDTH)]

	rooms = []
	num_rooms = 0

	for r in range(MAX_ROOMS):
		#random width and height
		w = libtcod.random_get_int(0, ROOM_MIN_SIZE, ROOM_MAX_SIZE)
		h = libtcod.random_get_int(0, ROOM_MIN_SIZE, ROOM_MAX_SIZE)
		#random position without going out of the boundaries of the map
		x = libtcod.random_get_int(0,0, MAP_WIDTH - w - 1)
		y = libtcod.random_get_int(0,0, MAP_HEIGHT - h- 1)
		
		new_room = Rect(x,y,w,h)
		
		#run through rooms to see if they intersect with this one
		failed = False
		for other_room in rooms:
			if new_room.intersect(other_room):
				failed = True
				break

		if not failed:
			#no intesections, valid room

			#paint it to map tiles
			create_room(new_room)

			#center coordinates of new room
			(new_x, new_y) = new_room.center()

			#room_no = Object(new_x, new_y, chr(65+num_rooms), 'room number', libtcod.white)
			#objects.insert(0, room_no)

			if num_rooms == 0:
				#first room where player starts
				player.x = new_x
				player.y = new_y

			else:
				#all roomas after first
				#connect to previous room with a tunnel

				#center coordinates of previous room
				(prev_x, prev_y) = rooms[num_rooms - 1].center()

				#draw a coin
				if libtcod.random_get_int(0,0,1) == 1:
					#first move horizontal then vertical
					create_v_tunnel(prev_y, new_y, prev_x)
					create_h_tunnel(prev_x, new_x, new_y)

				else:
					#vertically then horizontally
					create_v_tunnel(prev_y, new_y, prev_x)
					create_h_tunnel(prev_x, new_x, new_y)

			#add some content to rooms, ie monsters
			place_objects(new_room)

			#append new room to list
			rooms.append(new_room)
			num_rooms += 1
	

def render_all():
	global color_light_wall, color_dark_wall
	global color_light_ground, color_dark_ground
	global fov_map, fov_recompute

	if fov_recompute:
		fov_recompute = False
		libtcod.map_compute_fov(fov_map, player.x, player.y, TORCH_RADIUS, FOV_LIGHT_WALLS, FOV_ALGO)

		#go through all tiles, and set their background color
		for y in range(MAP_HEIGHT):
			for x in range(MAP_WIDTH):
				visible = libtcod.map_is_in_fov(fov_map, x, y)
				wall = map[x][y].block_sight
				if not visible: #out of fov
					if map[x][y].explored:
						if wall:
							libtcod.console_set_char_background(con,x,y,color_dark_wall,libtcod.BKGND_SET)
						else:
							libtcod.console_set_char_background(con,x,y,color_dark_ground,libtcod.BKGND_SET)
				else: #in fov
					if wall:
						libtcod.console_set_char_background(con,x,y,libtcod.pink,libtcod.BKGND_SET)
					else:
						libtcod.console_set_char_background(con,x,y,libtcod.fuchsia,libtcod.BKGND_SET)
					map[x][y].explored = True
	#draw all objects in the list
	for object in objects:
		if object != player:
			object.draw()
	player.draw()

	#blit the contents of "con" to the root console
	libtcod.console_blit(con, 0, 0, MAP_WIDTH, MAP_HEIGHT, 0, 0, 0)

	#prepare to render the GUI panel
	libtcod.console_set_default_background(panel, libtcod.black)
	libtcod.console_clear(panel)

	#print the messages one line at a time
	y = 1
	for (line, color) in game_msgs:
		libtcod.console_set_default_foreground(panel, color)
		libtcod.console_print_ex(panel, MSG_X, y, libtcod.BKGND_NONE, libtcod.LEFT, line)
		y += 1

	#show player stats
	render_bar(1, 1, BAR_WIDTH, 'HP', player.fighter.hp, player.fighter.max_hp, libtcod.light_red, libtcod.darker_red)

	#display name of objects under the mouse
	libtcod.console_set_default_foreground(panel, libtcod.light_grey)
	libtcod.console_print_ex(panel, 1, 0, libtcod.BKGND_NONE, libtcod.LEFT, get_names_under_mouse())

	#blit the contents of "panel" to the root console
	libtcod.console_blit(panel,0,0,SCREEN_WIDTH,PANEL_HEIGHT,0,0,PANEL_Y)

	

def handle_keys():
	global fov_recompute
	global key

	#key = libtcod.console_check_for_keypress(True)
	#key = libtcod.console_check_for_keypress() //for real time

	if key.vk == libtcod.KEY_ENTER and key.lalt:
		#Alt + Enter: toggle fullscreen
		libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

	elif key.vk == libtcod.KEY_ESCAPE:
		return 'exit' #exit game

	if game_state == 'playing':
		#movement keys
		if key.vk == libtcod.KEY_UP:
				player_move_or_attack(0,-1)

		elif key.vk == libtcod.KEY_DOWN:
				player_move_or_attack(0,1)
				
		elif key.vk == libtcod.KEY_LEFT:
			player_move_or_attack(-1,0)
			
		elif key.vk == libtcod.KEY_RIGHT:
			player_move_or_attack(1,0)
			
		else:
			#test for other keys
			key_char = chr(key.c)

			if key_char == 'f':
				#pick up item
				for object in objects: #look for item in player tile
					if object.x == player.x and object.y == player.y and object.item:
						object.item.pick_up()
						break

			if key_char == 'i':
				#show inventory
				message('inventest')
				chosen_item = inventory_menu('Press the key next to the item you wish to use \n')
				if chosen_item is not None:
					chosen_item.use()

			return 'didnt-take-turn'



def place_objects(room):
	#random number of monsters
	num_monsters = libtcod.random_get_int(0, 0, MAX_ROOM_MONSTERS)

	#random number of items
	num_items = libtcod.random_get_int(0, 0, MAX_ROOM_ITEMS)

	for i in range(num_monsters):
		#choose random spot for monster
		x = libtcod.random_get_int(0, room.x1+1, room.x2-1)
		y = libtcod.random_get_int(0, room.y1+1, room.y2-1)

		dice = libtcod.random_get_int(0, 0, 100)

		if dice < 75: #75% chance of a centaur
			#create centaur
			fighter_component = Fighter(hp=10, defense=0, power=3, death_function=monster_death)
			ai_component = BasicMonster()

			monster = Object(x, y, 'h', 'centaur', libtcod.dark_sepia, blocks=True, fighter=fighter_component, ai=ai_component)

		elif dice < 80: #5% chance of a CTHULU
			#creat cthulu
			fighter_component = Fighter(hp=1000, defense=10, power=100, death_function=monster_death)
			ai_component = BasicMonster()

			monster = Object(x, y, 'C', 'CTHULU', libtcod.dark_green, blocks=True, fighter=fighter_component, ai=ai_component)
		else:
			#create evil unicorn
			fighter_component = Fighter(hp=25, defense=2, power=5, death_function=monster_death)
			ai_component = BasicMonster()

			monster = Object(x, y, '1', "Evil Unicorn", libtcod.light_azure, blocks=True, fighter=fighter_component, ai=ai_component)

		#only place if tile in not blocked
		if not is_blocked(x, y):
			objects.append(monster)

	#items spawns
	for i in range(num_items):
		#choose random spot for items
		x = libtcod.random_get_int(0, room.x1+1, room.x2-1)
		y = libtcod.random_get_int(0, room.y1+1, room.y2-1)

		dice = libtcod.random_get_int(0, 0, 100)

		if dice < 50:
			#create health potion
			item_component = Item(10, 'health', 'used to recover 10 health')

			item = Object(x, y, 'U', 'Health Potion', libtcod.light_green, item=item_component)
		else:
			#create lightning bolt scroll 50% chance
			item_component = Item(3, 'special', 'used to cast lightning bolts', use_function = cast_lightning)

			item = Object(x, y, 'Z', 'Lightning Bolt Scroll', libtcod.yellow, item = item_component)

		#only place if not blocked
		if not is_blocked(x,y):
			objects.append(item)
			item.send_to_back()

def is_blocked(x, y):
	#test map tile
	if map[x][y].blocked:
		return True

	#check for blocking objects
	for object in objects:
		if object.blocks and object.x == x and object.y == y:
			return True

	return False

def player_move_or_attack(dx, dy):
	global fov_recompute

	#the coordinates of the player is moving to/attacking
	x = player.x + dx
	y = player.y + dy

	#try to find an attackable object there
	target = None
	for object in objects:
		if object.fighter and object.x == x and object.y == y:
			target = object
			break
		
	if target is not None:
		player.fighter.attack(target)

	#attack target if found, otherwise, move along		
	else:
		player.move(dx, dy)
		fov_recompute = True


def player_death(player):
	#game ogre
	global game_state
	message('GAME OGRE', libtcod.red)
	game_state = 'dead'

	#transform player into corpse
	player.char = '%'
	player.color = libtcod.red

def monster_death(monster):
	#tranform into corpse and make it unblock
	message(monster.name.capitalize() + ' is dead!', libtcod.blue)
	monster.char = '%'
	monster.color = libtcod.red
	monster. blocks = False
	monster.fighter = None
	monster.ai = None
	monster.name = 'corpse of ' + monster.name
	monster.send_to_back()

def render_bar(x, y, total_width, name, value, maximum, bar_color, back_color):
	#render a bar (HP, exp, etc), first calc width of bar
	bar_width = int(float(value) / maximum * total_width)

	#render the background first
	libtcod.console_set_default_background(panel, back_color)
	libtcod.console_rect(panel, x, y, total_width, 1, False, libtcod.BKGND_SCREEN)

	#render the top of the bar
	libtcod.console_set_default_background(panel, bar_color)
	if bar_width > 0:
		libtcod.console_rect(panel, x, y, bar_width, 1, False, libtcod.BKGND_SCREEN)

	#text with values
	libtcod.console_set_default_foreground(panel, libtcod.white)
	libtcod.console_print_ex(panel, x + total_width/2, y, libtcod.BKGND_NONE, libtcod.CENTER, name + ': ' + str(value) + '/' + str(maximum))

def message(new_msg, color=libtcod.white):
	#split message if necessary, among multiple lines
	new_msg_lines = textwrap.wrap(new_msg, MSG_WIDTH)

	for line in new_msg_lines:
		#if the buffer is full, remove the first line to make room for new one
		if len(game_msgs) == MSG_HEIGHT:
			del game_msgs[0]

		#add the new line as a tuple, with text and color
		game_msgs.append((line, color))

def get_names_under_mouse():
	global mouse

	#return a string with the name of all objects under the mouse
	(x,y) = (mouse.cx, mouse.cy)

	#create a list with names of all objects at the mouse's coordinates and in FOV
	names = [obj.name for obj in objects
		if obj.x == x and obj.y == y and libtcod.map_is_in_fov(fov_map, obj.x, obj.y)]

	names = ', '.join(names) #join names
	return names.capitalize()

def menu(header, options, width):
	if len(options) > 26: raise ValueError('cannot have a menu with more than 26 options')

	#calculate total height for the header (after auto-wrap) and one line per option
	header_height = libtcod.console_get_height_rect(con, 0, 0, width, SCREEN_HEIGHT, header)
	height = len(options) + header_height

	#create off screen console to rep menu's window
	window = libtcod.console_new(width, height)

	#print the header, with auto-wrap
	libtcod.console_set_default_foreground(window, libtcod.white)
	libtcod.console_print_rect_ex(window, 0, 0, width, height, libtcod.BKGND_NONE, libtcod.LEFT, header)

	#print all the options
	y = header_height
	letter_index = ord('a')
	for option_text in options:
		text = '(' + chr(letter_index) + ') ' + option_text
		libtcod.console_print_ex(window, 0, y, libtcod.BKGND_NONE, libtcod.LEFT, text)
		y += 1
		letter_index += 1

	#blit the contents to root console
	x = SCREEN_WIDTH/2 - width/2
	y = SCREEN_HEIGHT/2 - height/2
	libtcod.console_blit(window, 0, 0, width, height, 0, x, y, 1.0, 0.7)

	#present console and wait for key press
	libtcod.console_flush()
	key = libtcod.console_wait_for_keypress(True)

	#convert ascii to index of inventory items and return it
	index = key.c - ord('a')
	if index >= 0 and index < len(options): 
		return index
	return None

def inventory_menu(header):
	#show menu with each item from inventory as an option
	if len(inventory) == 0:
		options = ['Inventory is empty.']
	else:
		options = [item.name for item in inventory]

	index = menu(header, options, INVENTORY_WIDTH)

	#return chosen item
	if index is None or len(inventory) == 0:
		return None
	return inventory[index].item

def closest_monster(max_range):
	#find closest enemy
	closest_enemy = None
	closest_dist = max_range + 1

	for object in objects:
		if object.fighter and not object == player and libtcod.map_is_in_fov(fov_map, object.x, object.y):
			#calc distance between object and player
			dist = player.distance_to(object)
			if dist < closest_dist: #it's current closest
				closest_enemy = object
				closest_dist = dist

	return closest_enemy

def cast_lightning():
	#find closest enemy, within range, and damage it
	monster = closest_monster(LIGHTNING_RANGE)
	if monster is None: #no enemies in range
		message('No enemy in range', libtcod.red)
		return 'cancel'

	#shock'm
	message('The lightning bolt strikes the ' + monster.name + ' with lightning for ' + str(LIGHTNING_DAMAGE) + ' damage!', libtcod.light_blue)
	monster.fighter.take_damage(LIGHTNING_DAMAGE)
#################################################
#Init and Game Loop
#################################################

#console setup
libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
libtcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, 'python/libtcod tutorial', False)
libtcod.sys_set_fps(LIMIT_FPS)
#new off-screen console
con = libtcod.console_new(MAP_WIDTH, MAP_HEIGHT)

#GUI
panel = libtcod.console_new(SCREEN_WIDTH, PANEL_HEIGHT)

#create object representing the player
fighter_component = Fighter(hp=50, defense=2, power=5, death_function=player_death)
player = Object(0, 0, '@', 'player', libtcod.white, blocks=True, fighter=fighter_component)

#list of objects with those two
objects = [player]

#create game messages and colors, starts empty
game_msgs = []

#player inventory
inventory = []

#generate map
make_map()

#field of view map
fov_map = libtcod.map_new(MAP_WIDTH, MAP_HEIGHT)
for y in range(MAP_HEIGHT):
	for x in range(MAP_WIDTH):
		libtcod.map_set_properties(fov_map, x, y, not map[x][y].block_sight, not map[x][y].blocked)
fov_recompute = True

game_state = 'playing'
player_action = None


#welcome message
message('Blood for Blood', libtcod.red)

mouse = libtcod.Mouse()
key = libtcod.Key()


#Game loop		
while not libtcod.console_is_window_closed():

	libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS|libtcod.EVENT_MOUSE, key, mouse)
	#render the screen
	render_all()

	libtcod.console_flush()

	#erase all anjects at their old locations, before they move
	for object in objects:
		object.clear()

	#handle keys and exit game
	player_action = handle_keys()
	if player_action == 'exit':
		break

	#monsters take their turn
	if game_state == 'playing' and player_action != 'didnt-take-turn':
		for object in objects:
			if object.ai:
				object.ai.take_turn()
