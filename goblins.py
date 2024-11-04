#!/usr/bin/python

import random
import environment

INF = environment.SIZE_OF_FIELD * environment.SIZE_OF_FIELD + 1

class Goblin:
    '''class representing game characters'''

    #race
    race = 'goblin'
    
    #radius of field/dungeon that goblin can see
    radius_to_see = 3
    
    #max health
    max_health = 5

    #current health
    health = max_health
    
    #shows is creature is alive
    is_alive = True

    #type of tile the creature is standing on
    standing_tile = environment.KINDS_OF_DUNGEON_TILES['Cave']

    def __init__(self, coords):
        #goblin coords - turple of (level, row, col)
        self.coords = coords

    #get what goblin sees
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
    
    #get the damage value 
    def get_damage(self):
        damage = 2
        return damage            

    #attack enemies
    def fight(self, env):
        entities = env.entities

        (row, col) = self.coords[1:]
        for step in ((-1, -1), (-1, 0), (0, -1), (1, 0), (0, 1), (1, 1)):
            r = row + step[0]
            c = col + step[1]
            if 0 <= r and r < environment.SIZE_OF_FIELD and 0 <= c and c < environment.SIZE_OF_FIELD and env.dungeon[r][c] == 'D':
                damage = self.get_damage()
                entities[1][r][c].hit(damage, env)

    #hit with damage
    def hit(self, damage, environment):
        if damage < self.health:
            self.health -= damage
        else:
            self.die(environment)

    #die
    def die(self, environment):
        goblins_list = []
        for g in environment.goblins_list:
            if g.coords != self.coords:
                goblins_list.append(g)
        environment.goblins_list = goblins_list
    
        environment.dungeon[self.coords[1]][self.coords[2]] = self.standing_tile
    
    #move
    def move(self, env):
        ways = []
        (row, col) = self.coords[1:]
        for step in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            r = row + step[0]
            c = col + step[1]

            if 0 <= r and r < environment.SIZE_OF_FIELD and 0 <= c and c < environment.SIZE_OF_FIELD and env.dungeon[r][c] == environment.KINDS_OF_DUNGEON_TILES['Cave']:
               ways.append((r, c))

        if len(ways) == 0:
            return
        
        index = random.randint(0, len(ways))
        
        if index >= len(ways):
            return
        
        (row, col) = ways[index]
        print(index)

        env.dungeon[self.coords[1]][self.coords[2]] = self.standing_tile
        self.coords = (self.coords[0], row, col)
        self.standing_tile = env.dungeon[row][col]
        env.dungeon[row][col] = 'G' 
