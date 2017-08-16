import libtcodpy as libtcod

#size of the window
SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50

#map size
MAP_WIDTH = 80
MAP_HEIGHT = 45

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
MAX_ROOM_MONSTERS = 3

#field of view
FOV_ALGO = 0 #default
FOV_LIGHT_WALLS = True
TORCH_RADIUS = 10


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
	def __init__(self,x,y,char, name, color, blocks=False):
		self.name = name
		self.blocks = blocks
		self.x = x
		self.y = y
		self.char = char
		self.color = color

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
						libtcod.console_set_char_background(con,x,y,color_light_wall,libtcod.BKGND_SET)
					else:
						libtcod.console_set_char_background(con,x,y,color_light_ground,libtcod.BKGND_SET)
					map[x][y].explored = True
	#draw all objects in the list
	for object in objects:
		object.draw()

	#blit the contents of "con" to the root console
	libtcod.console_blit(con,0,0,SCREEN_WIDTH,SCREEN_HEIGHT,0,0,0)

	
def handle_keys():
	global fov_recompute
	key = libtcod.console_check_for_keypress(True)
	#key = libtcod.console_check_for_keypress() //for real time

	if key.vk == libtcod.KEY_ENTER and key.lalt:
		#Alt + Enter: toggle fullscreen
		libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

	elif key.vk == libtcod.KEY_ESCAPE:
		return 'exit' #exit game

	if game_state == 'playing':
		#movement keys
		if libtcod.console_is_key_pressed(libtcod.KEY_UP):
			#diagonal checks!
			if libtcod.console_is_key_pressed(libtcod.KEY_RIGHT):
				player_move_or_attack(1,-1)
				
			elif libtcod.console_is_key_pressed(libtcod.KEY_LEFT):
				player_move_or_attack(-1,-1)
				
			else:
				player_move_or_attack(0,-1)
				

		elif libtcod.console_is_key_pressed(libtcod.KEY_DOWN):
			#diagonal checks!
			if libtcod.console_is_key_pressed(libtcod.KEY_RIGHT):
				player_move_or_attack(1,1)

			elif libtcod.console_is_key_pressed(libtcod.KEY_LEFT):
				player_move_or_attack(-1,1)
				
			else:
				player_move_or_attack(0,1)
				

		elif libtcod.console_is_key_pressed(libtcod.KEY_LEFT):
			player_move_or_attack(-1,0)
			

		elif libtcod.console_is_key_pressed(libtcod.KEY_RIGHT):
			player_move_or_attack(1,0)
			
		else:
			return 'didnt-take-turn'



def place_objects(room):
	#random number of monsters
	num_monsters = libtcod.random_get_int(0, 0, MAX_ROOM_MONSTERS)

	for i in range(num_monsters):
		#choose random spot for monster
		x = libtcod.random_get_int(0, room.x1, room.x2)
		y = libtcod.random_get_int(0, room.y1, room.y2)

		dice = libtcod.random_get_int(0, 0, 100)

		if dice < 75: #75% chance of a centaur
			#create centaur
			monster = Object(x, y, 'h', 'centaur', libtcod.dark_sepia, blocks=True)
		elif dice < 80: #5% chance of a CTHULU
			#creat cthulu
			monster = Object(x, y, 'C', 'CTHULU', libtcod.dark_green, blocks=True)
		else:
			#create Jogoth
			monster = Object(x, y, 'J', "Jogoth", libtcod.light_cyan, blocks=True)

		#only place if tile in not blocked
		if not is_blocked(x, y):
			objects.append(monster)	

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
		if object.x == x and object.y == y:
			target = object
			break

	#attack target if found, otherwise, move along
	if target is not None:
		print 'The ' + target.name + ' gets hit! For 0 damage..'
	else:
		player.move(dx, dy)
		fov_recompute = True


#################################################
#Init and Game Loop
#################################################

#console setup
libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
libtcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, 'python/libtcod tutorial', False)
libtcod.sys_set_fps(LIMIT_FPS)

#new off-screen console
con = libtcod.console_new(SCREEN_WIDTH,SCREEN_HEIGHT)

#create object representing the player
player = Object(0, 0, '@', 'player', libtcod.white, blocks=True)

#list of objects with those two
objects = [player]

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


#Game loop		
while not libtcod.console_is_window_closed():

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
			if object != player:
				print 'The ' + object.name + ' growls!'
