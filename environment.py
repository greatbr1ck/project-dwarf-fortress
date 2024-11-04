#!/usr/bin/python

KINDS_OF_DUNGEON_TILES = dict([('Unknown', 'F'), ('Cave', ' '), ('Coal', '+'), ('Stone', '.'), ('Iron', '*'), ('Gold', '^'), ('Worked Stone', 'O')])

KINDS_OF_DWARFES_PROFESSIONS = {'Warrior', 'Healer'}
DIRECTIONS = dict([('North', 0), ('South', 1), ('West', 2), ('East', 3)])

INSTRUMENTS = dict([('Stone Pickaxe', 'T'), ('Wooden Pickaxe', '7'), ('Axe', 'P'), ('Wooden Stick', '/'), ('')])
BLOCKS = dict([('Worked Stone', 'O'), ('Worked Iron', '#'), ('Worked Gold', '$'), ('Coal', '*')])

#SIZE_OF_FIELD = 1000
#SIZE_OF_FIELD = 20
SIZE_OF_FIELD = 40
MAX_CAVE_RADIUS = 3
#MAX_CAVE_NUMBER = 100
MAX_CAVE_NUMBER = 5

class Tile:
    '''class representing the types of tiles as one field or dungeon unit'''
    tile_type = ' '

    def set_tile_type(self, tp):
        self.tyle_type = tp


class Environment:
    '''class representing global game characteristics'''
        
    #underground ground world part
    dungeon = [[KINDS_OF_DUNGEON_TILES['Cave']] * SIZE_OF_FIELD for _ in range(SIZE_OF_FIELD)]

    #global game timer
    timer = 0
    
    #list of all alive-dwarfs class examples
    dwarfs_list = []

    #entities list provides access to any character class example by its coords
    #level 0 stands for field, level 1 stands for dungeon
    entities = [[['None'] * SIZE_OF_FIELD for _ in range(SIZE_OF_FIELD)] for i in range(2)]

    def __init__(self, entities_list): #тут пока только добавляются дварфы
        #list of game characters class examples
        
        for entity in entities_list:
            (level, row, col) = entity.coords
            self.entities[level][row][col] = entity
            self.dwarfs_list.append(entity)

    def dwarf_exists(self, name):
        for dwarf in self.dwarfs_list:
            if dwarf.name == name:
                return True
        return False

    def get_dwarf(self, name):
        for dwarf in self.dwarfs_list:
            if dwarf.name == name:
                return dwarf
    
    def update_dwarf(self, name, updating_dwarf):
        for i in range(len(self.dwarfs_list)):
            if self.dwarfs_list[i].name == name:
                self.dwarfs_list[i] = updating_dwarf

                self.entities[self.dwarfs_list[i].coords[0]][self.dwarfs_list[i].coords[1]][self.dwarfs_list[i].coords[2]] = 'None'
                self.entities[updating_dwarf.coords[0]][updating_dwarf.coords[1]][updating_dwarf.coords[2]] = updating_dwarf
                return

    def get_entity(self, coords):
        (level, row, col) = coords
        return self.entities[level][row][col]
