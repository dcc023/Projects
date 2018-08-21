# Blood for Blood
### `game.py`

This is a simple roguelike that has you traversing infinite randomized dungeons with monsters to kill,
 gear to snag, items to consume, and levels/attributes to gain.

## Getting Started

There are certain things you may need before getting this program working effectively.

### Prerequisites:

* Python 2.7
* [libtcod 1.6](https://bitbucket.org/libtcod/libtcod/downloads/): Download the latest release of libtcod 1.6 and extract it somewhere. Be warned that both Python and libtcod must either be both 32 bit, or both 64 bit.




### How To:
1. From the command line, cd into the directory containing `game.py`
2. Then run `python2 game.py` or whatever your python command is.

## Game Handbook

### Controls:
* `W``A``S``D`: to move character around map
* `F`: to pick up item when standing on top of it
* `I`: opens inventory( press key associated with item to use)
* `C`: character menu
* `Esc`: to return to menu( game automatically saves when you exit)

### Stats:
* Character Level (Choose a stat to increase every level)
* Experience (acquire from killing monsters, used to gain levels)
* Max Health (size of health pool)
* Attack (how much damage you deal to monsters)
* Defense (how much damage you negate from monster attacks)
 
### Monsters:
* Centaurs (the weakest)
* Unicorn (average)
* Cthulhu (rare, avoid until strong enough to defeat)

### Items:
* Health Potion (restores 10 health)
* Lightning Scroll (deals damage to nearest enemy)
* Fire Scroll (aoe attack)
* Confusion Scroll (confuses a selected enemy)

### Gear:
* Sword (increases attack/ right handed)
* Shield (increases defense/ left handed)

## Author
* Dylan Campbell / [LinkedIn](www.linkedin.com/in/dylancharlescampbell) / [github](http://github.com/dcc023)
* Got started with help of [roguebasin](http://www.roguebasin.com)
