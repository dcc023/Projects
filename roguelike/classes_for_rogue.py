
#This file contains all the classes used in Blood for Blood roguelike
import firstrl

################
#CONSTANTS: all the constants used in all files for convenience sake
################
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
MAX_ROOM_MONSTERS = 3
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
LEVEL_SCREEN_WIDTH = 40
CHARACTER_SCREEN_WIDTH = 30

#message gui
MSG_X = BAR_WIDTH + 2
MSG_WIDTH = SCREEN_WIDTH - BAR_WIDTH - 2
MSG_HEIGHT = PANEL_HEIGHT - 1

#item constants
LIGHTNING_RANGE = 5
LIGHTNING_DAMAGE = 20
CONFUSE_NUM_TURNS = 10
CONFUSE_RANGE = 8
FIREBALL_RADIUS = 3
FIREBALL_DAMAGE = 12

#custom tile constants
wall_tile = 256
floor_tile = 257
player_tile = 258
scroll_tile = 261
healingpotion_tile = 262
sword_tile = 263
stairsdown_tile = 265
centaur_tile = 267

#xp and levels
LEVEL_UP_BASE = 200
LEVEL_UP_FACTOR = 150

#################################################################
#CLASSES
#################################################################

#MAP-BASED CLASSES
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

#ASSET-BASED CLASSES
class Object: #generic object: player, monster, item. etc

	def __init__(self,x,y,char, name, color, blocks=False, fighter=None, ai=None, item=None, equipment=None):
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

		self.equipment = equipment
		if self.equipment: #let equipment know who owns it
			self.equipment.owner = self
			#there is inherently an item component
			self.item = Item()
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

	def distance(self, x, y):
		#return distance to some coordinates
		return math.sqrt((x-self.x)**2 + (y-self.y)**2)

class Fighter:
	#combat properties (monster, npc, player, etc)
	def __init__(self, hp, defense, power, xp, death_function=None):
		self.xp = xp
		self.death_function = death_function
		self.base_max_hp = hp
		self.hp = hp
		self.base_defense = defense
		self.base_power = power
		
	@property
	def power(self):
		bonus = sum(equipment.power_bonus for equipment in get_all_equipped(self.owner))
		return self.base_power + bonus

	@property
	def defense(self):
		bonus = sum(equipment.defense_bonus for equipment in get_all_equipped(self.owner))
		return self.base_defense + bonus

	@property
	def max_hp(self):
		bonus = sum(equipment.max_hp_bonus for equipment in get_all_equipped(self.owner))
		return self.base_max_hp + bonus

	def take_damage(self, damage):
		#apply damage
		if damage > 0:
			self.hp -= damage

		if self.hp <= 0:
			function = self.death_function
			if function is not None:
				function(self.owner)
				if self.owner != player: #player gains xp if monster is slain
					player.fighter.xp += self.xp

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

class ConfusedMonster:
	#AI for confused monster
	def __init__(self, old_ai, num_turns = CONFUSE_NUM_TURNS):
		self.old_ai = old_ai
		self.num_turns = num_turns

	def  take_turn(self):
		if self.num_turns > 0: #still confused
			#move in a random directions
			self.owner.move(libtcod.random_get_int(0, -1, 1), libtcod.random_get_int(0, -1, 1))
			self.num_turns -= 1
		else:
			self.owner.ai = self.old_ai
			message('The ' + self.owner.name + ' lost its confusion!', libtcod.red)

class Item:
	#item properties(value, stat affected)
	def __init__(self, value=None, stat=None, info=None, use_function=None):
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
			#auto equip item is slot is empty
			equipment = self.owner.equipment
			if equipment and get_equipped_in_slot(equipment.slot) is None:
				equipment.equip()

	def use(self):
		#if object has equipment, use is able to equip or dequip
		if self.owner.equipment:
			self.owner.equipment.toggle_equip()
			return

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

	def drop(self):
		#add to the map and remove from the player's inventory. also place at players tile
		objects.append(self.owner)
		inventory.remove(self.owner)
		self.owner.x = player.x
		self.owner.y = player.y
		message('You dropped a ' + self.owner.name, libtcod.yellow)

class Equipment:
	#a equippable object that will give player bonuses
	def __init__(self, slot, power_bonus=0, defense_bonus=0, max_hp_bonus=0):
		self.power_bonus = power_bonus
		self.defense_bonus = defense_bonus
		self.max_hp_bonus = max_hp_bonus
		self.slot = slot
		self.is_equipped = False



	def toggle_equip(self): #equip and unequip
		if self.is_equipped:
			self.dequip()
		else:
			self.equip()

	def equip(self): #equip object and notify player
		#if the slot is occupied, dequip old item before equipping new
		old_equipment = get_equipped_in_slot(self.slot)
		if old_equipment is not None:
			old_equipment.dequip()

		self.is_equipped = True
		message(str(self.owner.name) + ' is now equipped in slot ' + str(self.slot), libtcod.green )

	def dequip(self):
		if not self.is_equipped:
			return
		self.is_equipped = False
		message(str(self.owner.name) + ' is uneqquiped from slot ' + str(self.slot), libtcod.yellow)
