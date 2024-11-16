#!/usr/bin/python

import environment

INF = environment.SIZE_OF_FIELD * environment.SIZE_OF_FIELD + 1

class Thing:
    '''class representing the things that can be pu in inventory'''
    
    #damage when owner uses it in fight
    damage = 0

  	#if owner marked it as a garbage
    is_garbage = False

    def __init__(self, name):
        self.name = name

        if name in {environment.INSTRUMENTS['Wooden Pickaxe'], environment.INSTRUMENTS['Stone Pickaxe']}:
            self.damage = 1
        elif name == environment.INSTRUMENTS['Axe']:
            self.damage = 3


class Inventory:
    '''class repersenting dwarfs inventory'''
    
    #max size
    max_size = 20

    #inventory content
    content = []

    #size of filled part
    size = 0
    
    #show if there is any empty place
    def is_filled(self):
        return self.size == self.max_size

    #mark items of environment as a garbage to through out
    def mark_garbage(self, name):
        for i in range(len(self.content)):
            if self.content[i].name == name:
                self.content[i].is_garbage = True
                break
    
    #show inventory
    def show_items(self):
        for i in range(len(self.content)):
            print(self.content[i].name, end=' ')
            if self.content[i].is_garbage:
                print("garbage")
            else:
                print("using")

    #through out all garbage
    def throw_garbage(self):
        content_updated = []
        for i in range(self.size):
            if not self.content[i].is_garbage:
                content_updated.append(self.content[i])

        self.content = content_updated
    
    #find the item in content
    def contains(self, item_name):
        for c in self.content:
            if c.name == item_name and not c.is_garbage:
                return True
        return False

    #put the item in content    
    def put_item(self, item_name):
        item = Thing(item_name)

        if self.size < self.max_size:
            self.content.append(item)
            self.size += 1
    
    def can_mine_item(self, item):
        if item == environment.KINDS_OF_DUNGEON_TILES['Coal'] or item == environment.KINDS_OF_DUNGEON_TILES['Stone']:
            return not self.is_filled() and (self.contains(environment.INSTRUMENTS['Wooden Pickaxe']) or self.contains(environment.INSTRUMENTS['Stone Pickaxe']))
        else:
            return not self.is_filled() and self.contains(environment.INSTRUMENTS['Stone Pickaxe'])
    
    def is_garbage_thrown(self):
        for c in self.content:
            if c.is_garbage:
                return False
        return True

    def throw_next(self):
        content_updated = []

        for i in range(self.size):
            if self.content[i].is_garbage:
                index = i
                res = self.content[i]
        
        for i in range(self.size):
            if i != index:
                content_updated.append(self.content[i])

        self.content = content_updated
        return res.name

    def extract_item(self, item):
        content_updated = []

        for i in range(self.size):
            if self.content[i].name == item and not self.content[i].is_garbage:
                index = i
        
        for i in range(self.size):
            if i != index:
                content_updated.append(self.content[i])

        self.content = content_updated

class Dwarf:
    '''class representing dwarf characters'''

    #race
    race = 'dwarf'
    
    #radius of field/dungeon that dwarf can see
    radius_to_see = 3
    
    #radius of field/dungeon that dwarf with torch can see --- пока без него и вообще без факелов
    radius_to_see_with_torch = 5

    #max health
    max_health = 5

    #current health
    health = max_health

    #dwarfs inventory
    inventory = Inventory()

    #shows is dwarfs is alive
    is_alive = True

    #type of tile the dwarf is standing on
    standing_tile = environment.KINDS_OF_DUNGEON_TILES['Cave']

    def __init__(self, profession, name, coords):
        #dwarf main work type
        self.profession = profession
        
        #dwarf name
        self.name = name

        #dwarf coords - turple of (level, row, col)
        self.coords = coords

        self.inventory.put_item(environment.INSTRUMENTS['Wooden Pickaxe'])

    #is dwarf doing any long-period activity
    doing_command = 'Nothing'

    #destination coords where dwarf moves if doing command == 'Move'
    destination_coords = (1, -1, -1)

    #coords of mining area
    coords1 = (1, -1, -1)
    coords2 = (1, -1, -1)

    #coords of dump area
    dump_coords1 = (1, -1, -1)
    dump_coords2 = (1, -1, -1)

    #where the dwarf sees - <North, West, East, South>
    direction = 'North'

    #map of dungeon where dwarf saw 'Cave' type tiles
    caves_map = [[environment.KINDS_OF_DUNGEON_TILES['Unknown']] * environment.SIZE_OF_FIELD for _ in range(environment.SIZE_OF_FIELD)]

    #get what dwarf sees
    def get_visibility(self, env):
      if self.coords[0] == 1:
          game_field = env.dungeon

      visible = [[environment.KINDS_OF_DUNGEON_TILES['Unknown']] * (self.radius_to_see * 2 + 3) for _ in range(2 * self.radius_to_see + 3)]
      (row, col) = self.coords[1:]

      q = []
      q.append((row, col, self.radius_to_see, self.radius_to_see, 0))
      visited = [[False] * len(visible) for _ in range(len(visible))]
      visited[self.radius_to_see][self.radius_to_see] = True
      visible[self.radius_to_see][self.radius_to_see] = 'D'

      while not len(q) == 0:
          (row, col, rrow, ccol, dist) = q.pop(0)
          for step in ((-1, 0), (0, -1), (1, 0), (0, 1)):
              (r, c) = (row + step[0], col + step[1])
              if dist + 1 <= self.radius_to_see and not visited[rrow + step[0]][ccol + step[1]] and 0 <= r and r < environment.SIZE_OF_FIELD and 0 <= c and c < environment.SIZE_OF_FIELD:
                  q.append((r, c, rrow + step[0], ccol + step[1], dist + 1))
                  visited[rrow + step[0]][ccol + step[1]] = True
                  visible[rrow + step[0]][ccol + step[1]] = game_field[r][c]
      
      return visible

    #show what dwarf sees
    def show_visibility(self, env):
        visible = self.get_visibility(env)
        
        for i in range(len(visible)):
            for j in range(len(visible)):
                print(visible[i][j], end='')
            print()
    
    #get the damage value as max{damage of any instrument of inventory}
    def get_damage(self):
        damage = 1
        for instrument in self.inventory.content:
            if damage < instrument.damage:
                damage = instrument.damage

        return damage            

    #attack enemies
    def fight(self, env):
        '''dwarf attacks enemies when he sees them, that's why the user does not rules whether to attack or not. Fight may happen only in dungeon'''

        damage = self.get_damage()
        if self.profession == 'Healer':
            damage = 1
        print("DAMAGE: ", damage)
        (row, col) = self.coords[1:]
        for step in ((-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)):
            r = row + step[0]
            c = col + step[1]
            if 0 <= r and r < environment.SIZE_OF_FIELD and 0 <= c and c < environment.SIZE_OF_FIELD and env.dungeon[r][c] in {'D', 'G'}:
                #in future: G, not D. Now dwarfs attack dwarfs
                env.entities[1][r][c].hit(damage, env)

    #hit with damage
    def hit(self, damage, environment):
        if damage < self.health:
            self.health -= damage
        else:
            self.die(environment)

    #die
    def die(self, environment):
        print(self.name, ' is killed')

        self.health = 0
        self.is_alive = False

        dwarfs_list = []
        for dwarf in environment.dwarfs_list:
            if dwarf.name != self.name:
                dwarfs_list.append(dwarf)
        environment.dwarfs_list = dwarfs_list
        environment.entities[1][self.coords[1]][self.coords[2]] = 'None'
        environment.dungeon[self.coords[1]][self.coords[2]] = self.standing_tile
    
    '''
    пусть дварфы ходят с помощью bfs. Когда дварф находится в точке coords,
    он видит вокруг себя некоторую область visible. Пусть дварфы обладают хорошей памятью и запоминают, где находится каждый увиденный
    им тайл типа Cave (пусть дварф представляет это в виде карты подземелья, на которой отмечены тайлы типа "Caves"). 
    Если пользователь говорит дварфу добраться до какой-то точки, предполагается что дварф мог бы дойти до нее по тайлам типа 'Cave', 
    если никто из других дварфов не ставил блоки типа 'Worked Stone'. 
    Предполагаю, что пользователь за ход может совершить передвижение на <= 1 тайла, сломать <= 8 тайлов вокруг себя и поставить <= 8 
    тайлов вокруг себя.
    Тогда если дварф встречает 'Worked Stone', он предпочтет сломать, пройти и восстановить обратно 
    (считаю, что в этом и только этом случае вещь не попадает в инвентарь при добычи тайла).

    Если пользователь задал такую координату назначения, что дварф не может ее достичь указанным способом, дварф не обязан ее достигать
    '''

    #move to tile with given coords
    def move(self, coords, env):
        if self.coords[1:] == coords:
            return

        visible = self.get_visibility(env)
       
        (row, col) = self.coords[1:]
        row_in_visible = self.radius_to_see
        col_in_visible = self.radius_to_see

        #update caves_map
        for i in range(len(visible)):
            for j in range(len(visible)):
                r = i + row - row_in_visible
                c = j + col - col_in_visible

                if self.coords[0] == 1 and 0 <= r and r < environment.SIZE_OF_FIELD and 0 <= c and c < environment.SIZE_OF_FIELD and \
                   (visible[i][j] in {'D', 'G', environment.KINDS_OF_DUNGEON_TILES['Cave'], environment.KINDS_OF_DUNGEON_TILES['Worked Stone']}):
                    self.caves_map[r][c] = environment.KINDS_OF_DUNGEON_TILES['Cave']
                #сделать аналогичную caves_map штуку для наземного уровня

        #find shortest path
        q = []
        q.append((row, col))
        visited = [[False] * environment.SIZE_OF_FIELD for _ in range(environment.SIZE_OF_FIELD)]
        visited[row][col] = True

        dist = [[INF] * environment.SIZE_OF_FIELD for _ in range(environment.SIZE_OF_FIELD)]
        dist[row][col] = 0

        parent = [[(-1, -1)] * environment.SIZE_OF_FIELD for _ in range(environment.SIZE_OF_FIELD)]

        while not len(q) == 0:
            (row, col) = q.pop(0)
            for step in ((-1, 0), (0, -1), (1, 0), (0, 1)):
                (r, c) = (row + step[0], col + step[1])
                if 0 <= r and r < environment.SIZE_OF_FIELD and 0 <= c and c < environment.SIZE_OF_FIELD and not visited[r][c] and \
                   self.caves_map[r][c] == environment.KINDS_OF_DUNGEON_TILES['Cave'] and dist[r][c] > dist[row][col] + 1:
                    i = r - (row - row_in_visible)
                    j = c - (col - col_in_visible)

                    if visible[i][j] in {'G', 'D'}:
                        continue

                    q.append((r, c))
                    dist[r][c] = dist[row][col] + 1
                    visited[r][c] = True
                    parent[r][c] = (row, col)
        
        (row, col) = self.coords[1:]
        (next_row, next_col) = coords
        
        if (next_row, next_col) != (row, col):  
            if dist[next_row][next_col] < INF:
                while parent[next_row][next_col] != self.coords[1:]:
                    (next_row, next_col) = parent[next_row][next_col]
            else:
                (next_row, next_col) = (row, col)
          
        if next_row == row - 1:
            self.direction = 'North'
        elif next_row == row + 1:
            self.direction = 'South'
        elif next_col == col + 1:
            self.direction = 'East'
        else:
            self.direction = 'West'
        
        env.dungeon[self.coords[1]][self.coords[2]] = self.standing_tile
        env.entities[1][self.coords[1]][self.coords[2]] = 'None'
        self.coords = (self.coords[0], next_row, next_col)
        self.standing_tile = env.dungeon[next_row][next_col]
        env.dungeon[next_row][next_col] = 'D' 
        env.entities[1][next_row][next_col] = self

    #mine the tile with coords tile_coords
    def mine(self, tile_coords, env):
        tile = env.dungeon[tile_coords[1]][tile_coords[2]]
        if self.inventory.can_mine_item(tile):
            env.dungeon[tile_coords[1]][tile_coords[2]] = environment.KINDS_OF_DUNGEON_TILES['Cave']
            
            if tile == environment.KINDS_OF_DUNGEON_TILES['Coal']:
                self.inventory.put_item(environment.BLOCKS['Coal'])
            elif tile == environment.KINDS_OF_DUNGEON_TILES['Gold']:
                self.inventory.put_item(environment.BLOCKS['Worked Gold'])
            elif tile == environment.KINDS_OF_DUNGEON_TILES['Iron']:
                self.inventory.put_item(environment.BLOCKS['Worked Iron'])
            else:
                self.inventory.put_item(environment.BLOCKS['Worked Stone'])

    #throw next garbage item from inventory
    def throw(self, tile_coords, env):
        if env.dungeon[tile_coords[1]][tile_coords[2]] != environment.KINDS_OF_DUNGEON_TILES['Cave']:
            return
                
        tile = self.inventory.throw_next()
        env.dungeon[tile_coords[1]][tile_coords[2]] = tile
        env.update_dwarf(self.name, self)        

    #build one Worked Stone block behind the dwarf
    def build(self, env):
        if not self.inventory.contains(environment.BLOCKS['Worked Stone']):
            print("There is no Worked Stone blocks in dwarf's inventory")
            return
        
        (row, col) = (self.radius_to_see, self.radius_to_see)
        if self.direction == 'North':
            row -= 1
        elif self.direction == 'South':
            row += 1
        elif self.direction == 'West':
            col -= 1
        else:
            col += 1
        
        if env.dungeon[row][col] == environment.KINDS_OF_DUNGEON_TILES['Cave']:
            env.dungeon[row][col] = environment.KINDS_OF_DUNGEON_TILES['Worked Stone']

        self.inventory.extract_item(environment.KINDS_OF_DUNGEON_TILES['Worked Stone'])
        env.update_dwarf(self.name, self)
    
    #mark the item as garbage
    def mark_garbage(self, item):
        if not self.inventory.contains(item):
            print("The dwarf's inventory does not contain this particular item")
            return

        self.inventory.mark_garbage(item)