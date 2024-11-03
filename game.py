#!/usr/bin/python

import random
import environment
import dwarfs


def get_initial_dwarf_coords(number_of_dwarfes):
    initial_dwarf_coords = []

    (row, col) = (environment.SIZE_OF_FIELD // 2, environment.SIZE_OF_FIELD // 2)

    q = []
    q.append((row, col))

    #на самом деле дварфы появляются не в подземелье, а над землей, так что надо будет писать (0, row, col)
    initial_dwarf_coords.append((1, row, col))
    
    visited = [[False] * environment.SIZE_OF_FIELD for _ in range(environment.SIZE_OF_FIELD)]
    visited[row][col] = True

    cnt = 1

    while cnt < number_of_dwarfes and not len(q) == 0:
        (row, col) = q.pop(0)
        for step in ((-1, 0), (0, -1), (1, 0), (0, 1)):
            (r, c) = (row + step[0], col + step[1])
            if 0 <= r and r < environment.SIZE_OF_FIELD and 0 <= c and c < environment.SIZE_OF_FIELD and not visited[r][c]:
                q.append((r, c))
                visited[r][c] = True

                initial_dwarf_coords.append((1, r, c))
                
                cnt += 1
                if cnt == number_of_dwarfes:
                    break

    return initial_dwarf_coords 

def fill_area(field, start, color, radius):
    q = []
    for (row, col) in start:
        q.append((row, col))
    
    visited = [[False] * environment.SIZE_OF_FIELD for _ in range(environment.SIZE_OF_FIELD)]
    for (row, col) in start:
        visited[row][col] = True

    dist = [[dwarfs.INF] * environment.SIZE_OF_FIELD for _ in range(environment.SIZE_OF_FIELD)]
    for (row, col) in start:
        dist[row][col] = 0

    while not len(q) == 0:
        (row, col) = q.pop(0)
        for step in ((-1, 0), (0, -1), (1, 0), (0, 1)):
            (r, c) = (row + step[0], col + step[1])
            if 0 <= r and r < environment.SIZE_OF_FIELD and 0 <= c and c < environment.SIZE_OF_FIELD and not visited[r][c] and \
                dist[r][c] > dist[row][col] + 1 and dist[row][col] + 1 <= radius:
                q.append((r, c))
                dist[r][c] = dist[row][col] + 1
                visited[r][c] = True
                field[r][c] = color
    return field

def generate_dungeon(initial_coords):
    #generate stone slice
    game_field = [[environment.KINDS_OF_DUNGEON_TILES["Stone"]] * environment.SIZE_OF_FIELD for _ in range(environment.SIZE_OF_FIELD)]

    #generate caves
    number_of_experiments = random.randint(environment.MAX_CAVE_NUMBER // 2, environment.MAX_CAVE_NUMBER)
    for _ in range(number_of_experiments):
        caves_number = random.randint(environment.MAX_CAVE_NUMBER // 2, environment.MAX_CAVE_NUMBER)
        cave_radius = random.randint(environment.MAX_CAVE_RADIUS // 2, environment.MAX_CAVE_RADIUS)

        local_field = [[environment.KINDS_OF_DUNGEON_TILES["Unknown"]] * environment.SIZE_OF_FIELD for _ in range(environment.SIZE_OF_FIELD)]
        caves_center = []

        for i in range(caves_number):
            row = random.randint(0, environment.SIZE_OF_FIELD - 1)
            col = random.randint(0, environment.SIZE_OF_FIELD - 1)
            local_field[row][col] = environment.KINDS_OF_DUNGEON_TILES["Cave"]
            caves_center.append((row, col))
        
        caves_center.append((initial_coords[0][1], initial_coords[0][2]))
        
        sorted(caves_center)

        for i in range(caves_number - 1):
            (row, col) = caves_center[i]
            (frow, fcol) = caves_center[i + 1]

            row_diff = 1
            if frow - row < 0:
                row_diff = -1

            col_diff = 1
            if fcol - col < 0:
                col_diff = -1    

            while row != frow:
                local_field[row][col] = environment.KINDS_OF_DUNGEON_TILES["Cave"]
                row += row_diff
            while col != fcol:
                local_field[row][col] = environment.KINDS_OF_DUNGEON_TILES["Cave"]
                col += col_diff
        
        for i in range(environment.SIZE_OF_FIELD):
            for j in range(environment.SIZE_OF_FIELD):
                if local_field[i][j] == environment.KINDS_OF_DUNGEON_TILES["Cave"]:
                    game_field[i][j] = environment.KINDS_OF_DUNGEON_TILES["Cave"]
        
        fill_area(game_field, caves_center, environment.KINDS_OF_DUNGEON_TILES["Cave"], cave_radius)       

    #generate coal slice
    number_of_experiments = random.randint(environment.SIZE_OF_FIELD, int((environment.SIZE_OF_FIELD * environment.SIZE_OF_FIELD)**0.5))
    for _ in range(number_of_experiments):
        row = random.randint(0, environment.SIZE_OF_FIELD - 1)
        col = random.randint(0, environment.SIZE_OF_FIELD - 1)
        radius = random.randint(0, environment.MAX_CAVE_RADIUS // 2)
        fill_area(game_field, [(row, col)], environment.KINDS_OF_DUNGEON_TILES["Coal"], radius)

    #generate iron slice
    number_of_experiments = random.randint(int(environment.SIZE_OF_FIELD ** 0.5), environment.SIZE_OF_FIELD)
    for _ in range(number_of_experiments):
        row = random.randint(0, environment.SIZE_OF_FIELD - 1)
        col = random.randint(0, environment.SIZE_OF_FIELD - 1)
        radius = random.randint(environment.MAX_CAVE_RADIUS // 4, environment.MAX_CAVE_RADIUS // 3)
        fill_area(game_field, [(row, col)], environment.KINDS_OF_DUNGEON_TILES["Iron"], radius)
    
    #generate gold slice
    number_of_experiments = random.randint(int(environment.SIZE_OF_FIELD ** 0.5) // 2 + 1, environment.SIZE_OF_FIELD // 3)
    for _ in range(number_of_experiments):
        row = random.randint(0, environment.SIZE_OF_FIELD - 1)
        col = random.randint(0, environment.SIZE_OF_FIELD - 1)
        radius = random.randint(0, 2)
        fill_area(game_field, [(row, col)], environment.KINDS_OF_DUNGEON_TILES["Gold"], radius)    
    
    #set dwarfes positions
    for coord in initial_coords:
        game_field[coord[1]][coord[2]] = 'D'

    return game_field
    

def init_game():
    #get dwarfes list
    print('type the population of your dwarf squad')

    number_of_dwarfes = int(input())
    while True:
        if 1 <= number_of_dwarfes and number_of_dwarfes <= environment.SIZE_OF_FIELD * environment.SIZE_OF_FIELD:
            break

        print('please type the population of dwarfs in the correct way')
        number_of_dwarfes = int(input())

    initial_coords = get_initial_dwarf_coords(number_of_dwarfes)

    dwarfes_list = []
    for i in range(number_of_dwarfes):
        print('type another dwarfs name')
        name = input()

        print('type the dwarfs work responsibility')
        profession = input()
        while True:
            if profession in environment.KINDS_OF_DWARFES_PROFESSIONS:
                break

            print('please type the dwarfs work responsibility in the correct way')
            profession = input()

        coords = initial_coords[i]

        dwarf = dwarfs.Dwarf(profession, name, coords)
        dwarfes_list.append(dwarf)
    
    #generate environment
    env = environment.Environment(dwarfes_list)

    #пусть пока дварфы живут только под землей
    env.dungeon = generate_dungeon(initial_coords)
    #env.field = generate_field(initial_coords)
    
    print("DUNGEON")
    for _ in env.dungeon:
        for c in _:
            print(c, end='')
        print()

    return env

#functions for user

def get_dwarf_info(dwarf_name, env):
    print("name: ", dwarf_name)

    if not env.dwarf_exists(dwarf_name):
        print("status: dead or went missing")
        return

    print("status: alive")
    dwarf = env.get_dwarf(dwarf_name)
    print("work responsibility: ", dwarf.profession)
    print("health: ", dwarf.health)
    print("is now doing: ", dwarf.doing_command)
    print("coords: ", dwarf.coords)
    print("direction", dwarf.direction)
    print("what dwarf sees:")
    dwarf.show_visibility(env)
    print()

def show_dwarf_inventory(dwarf_name, env):
    if not env.dwarf_exists(dwarf_name):
        print("type dwarf's name correctly")
        return
    
    dwarf = env.get_dwarf(dwarf_name)
    dwarf.inventory.show_items()

def get_map(dwarf_name, env):
    '''get the map of caves seen by this particular dwarf'''

    if not env.dwarf_exists(dwarf_name):
        print("type dwarf's name correctly")
        return
    
    dwarf = env.get_dwarf(dwarf_name)
    for i in range(len(dwarf.caves_map)):
        for c in dwarf.caves_map[i]:
            print(c, end='')
        print()
    print()

def move(dwarf_name, destination_coords, env):
    '''
    Before using 'move' funtion user should check out whether this dwarf can reach the destination.
    It can be done by following the caves map, where every dwarf marks the tiles he ever visited
    '''

    if not env.dwarf_exists(dwarf_name):
        print("Type the name of existing and alive dwarf")
        return
    
    dwarf = env.get_dwarf(dwarf_name)    

    if dwarf.coords[0] != destination_coords[0]:
        print("You can move your dwarfs from one level to another only by using the portal")
        return

    while (dwarf.coords != destination_coords):
        dwarf.move(destination_coords[1:], env)
    dwarf.move(destination_coords[1:], env)

def mine(dwarf_name, env):
    if not env.dwarf_exists(dwarf_name):
        print("Type the name of existing and alive dwarf")
        return
    
    dwarf = env.get_dwarf(dwarf_name)

    (row, col) = dwarf.coords[1:]
    if dwarf.direction == 'North':
        row -= 1
    elif dwarf.direction == 'South':
        row += 1
    elif dwarf.direction == 'West':
        col -= 1
    else:
        col += 1
    
    if 0 <= row and row < environment.SIZE_OF_FIELD and 0 <= col and col < environment.SIZE_OF_FIELD:
        dwarf.mine((1, row, col), env)
    
    # print("DUNGEON")
    # for _ in env.dungeon:
    #     for c in _:
    #         print(c, end='')
    #     print()

def mine_area(dwarf_name, coords1, coords2, env):
    if not env.dwarf_exists(dwarf_name):
        print("Type the name of existing and alive dwarf")
        return
    
    dwarf = env.get_dwarf(dwarf_name)

    if dwarf.inventory.is_filled():
        print("Dwarf's inventory is filled")
        return

    print(dwarf.coords)
    if dwarf.coords[0] != coords1[0] or dwarf.coords[0] != coords2[0]:
        print("You can move your dwarfs from one level to another only by using the portal")
        return
    
    if not(coords1[1] <= coords2[1] and coords1[2] <= coords2[2]):
        print('Choose left high and right low corners of mining are')
        return
    
    get_dwarf_info(dwarf_name, env)

    #update caves_map - лучше оформить отдельной функцией
    visible = dwarf.get_visibility(env)
    
    (row, col) = dwarf.coords[1:]
    row_in_visible = dwarf.radius_to_see
    col_in_visible = dwarf.radius_to_see

    for i in range(len(visible)):
        for j in range(len(visible)):
            r = i + row - row_in_visible
            c = j + col - col_in_visible

            if dwarf.coords[0] == 1 and 0 <= r and r < environment.SIZE_OF_FIELD and 0 <= c and c < environment.SIZE_OF_FIELD and \
                (visible[i][j] in {'D', 'G', environment.KINDS_OF_DUNGEON_TILES['Cave'], environment.KINDS_OF_DUNGEON_TILES['Worked Stone']}):
                dwarf.caves_map[r][c] = environment.KINDS_OF_DUNGEON_TILES['Cave']
            #сделать аналогичную caves_map штуку для наземного уровня
    
    (finish_row, finish_col) = (-1, -1)
    for srow in range(coords1[1], coords2[1] + 1):
        for scol in range(coords1[2], coords2[2] + 1):
            q = []
            q.append((srow, scol))
    
            visited = [[False] * environment.SIZE_OF_FIELD for _ in range(environment.SIZE_OF_FIELD)]
            visited[srow][scol] = True

            while not len(q) == 0:
                (row, col) = q.pop(0)
                for step in ((-1, 0), (0, -1), (1, 0), (0, 1)):
                    (r, c) = (row + step[0], col + step[1])
                    if 0 <= r and r < environment.SIZE_OF_FIELD and 0 <= c and c < environment.SIZE_OF_FIELD and not visited[r][c] and \
                       dwarf.caves_map[r][c] == environment.KINDS_OF_DUNGEON_TILES["Cave"]:
                        q.append((r, c))
                        visited[r][c] = True
            
            if visited[dwarf.coords[1]][dwarf.coords[2]]:
                (finish_row, finish_col) = (srow, scol)
    
    print(finish_row, finish_col)
    
    if finish_row == -1:
        print('It is impossible to reach given are')
        return
    
    for step in ((-1, 0), (0, -1), (1, 0), (0, 1)):
        (r, c) = (finish_row + step[0], finish_col + step[1])
        if 0 <= r and r < environment.SIZE_OF_FIELD and 0 <= c and c < environment.SIZE_OF_FIELD and \
           dwarf.caves_map[r][c] == environment.KINDS_OF_DUNGEON_TILES["Cave"]:
            (finish_row, finish_col) = (r, c)
            break
    
    move(dwarf_name, (1, finish_row, finish_col), env)

    print('moved')
    get_dwarf_info(dwarf_name, env)

    #start mining the area

    mine(dwarf_name, env)

    if dwarf.inventory.is_filled():
        print("Dwarf's inventory is filled")
        return
    
    if dwarf.direction == 'North':
        if dwarf.caves_map[dwarf.coords[1] - 1][dwarf.coords[2]] in {'G', 'D'}:
            dwarf.fight(env)
        if not dwarf.is_alive:
            return
        move(dwarf_name, (1, dwarf.coords[1] - 1, dwarf.coords[2]), env)
    elif dwarf.direction == 'South':
        if dwarf.caves_map[dwarf.coords[1] + 1][dwarf.coords[2]] in {'G', 'D'}:
            dwarf.fight(env)
        if not dwarf.is_alive:
            return
        move(dwarf_name, (1, dwarf.coords[1] + 1, dwarf.coords[2]), env)
    elif dwarf.direction == 'West':
        if dwarf.caves_map[dwarf.coords[1]][dwarf.coords[2] - 1] in {'G', 'D'}:
            dwarf.fight(env)
        if not dwarf.is_alive:
            return    
        move(dwarf_name, (1, dwarf.coords[1], dwarf.coords[2] - 1), env)
    else:
        if dwarf.caves_map[dwarf.coords[1]][dwarf.coords[2] + 1] in {'G', 'D'}:
            dwarf.fight(env)
        if not dwarf.is_alive:
            return
        move(dwarf_name, (1, dwarf.coords[1], dwarf.coords[2] + 1), env)
    dwarf.direction = 'North'

    while dwarf.coords[1] > coords1[1]:
        mine(dwarf_name, env)
        move(dwarf_name, (1, dwarf.coords[1] - 1, dwarf.coords[2]), env)
        
        if dwarf.inventory.is_filled():
            print("Dwarf's inventory is filled")
            return

    print('moved1')
    get_dwarf_info(dwarf_name, env)

    dwarf.direction = 'West'
    while dwarf.coords[2] > coords1[2]:
        mine(dwarf_name, env)
        move(dwarf_name, (1, dwarf.coords[1], dwarf.coords[2] - 1), env)

        if dwarf.inventory.is_filled():
            print("Dwarf's inventory is filled")
            return
    
    print('moved2')
    get_dwarf_info(dwarf_name, env)

    print('reached')
    for _ in env.dungeon:
        for c in _:
            print(c, end='')
        print()
    print()

    show_dwarf_inventory(dwarf_name, env)
    
    #теперь сделать обход змейкой из левого верхнего угла в правый нижний 
    for i in range(coords1[1], coords2[1] + 1):
        dwarf.direction = 'West'
        col_diff = -1
        if i % 2 == 0:
            dwarf.direction = 'East'
            col_diff = 1

        for scol in range(coords1[2], coords2[2]):
            destination = (dwarf.coords[1] + col_diff, dwarf.coords[2])
            
            #it may happen that in destination coord stands another dwarf or goblin. Is so, dwarf attack instead of going there
            if dwarf.caves_map[destination[0]][destination[1]] in {'G', 'D'}:
                dwarf.fight(env)
            if not dwarf.is_alive:
                return

            if dwarf.caves_map[destination[0]][destination[1]] in {environment.KINDS_OF_DUNGEON_TILES['Cave'], \
                                                                     environment.KINDS_OF_DUNGEON_TILES['Worked Stone']}:
                move(dwarf_name, (1, destination[0], destination[1]), env)
            else:
                mine(dwarf_name, env)
                move(dwarf_name, (1, destination[0], destination[1]), env)
                
                if dwarf.inventory.is_filled():
                    print("Dwarf's inventory is filled")
                    return
            
        dwarf.direction = 'South'
        if dwarf.coords[1] + 1 <= coords2[1]:
            mine(dwarf_name, env)
            move(dwarf_name, (1, dwarf.coords[1] + 1, dwarf.coords[2]), env) 
            
            if dwarf.inventory.is_filled():
                print("Dwarf's inventory is filled")
                return
    
    show_dwarf_inventory(dwarf_name, env)

def build_block(dwarf_name, block_name):
    pass


#-------------------------------GAME-----------------------------

env = init_game()
while True:
    command = input()
    dwarf_name = input()

    if command == 'get_dwarf_info':
        get_dwarf_info(dwarf_name, env)
    elif command == 'mine_area':
        coords1 = map(int, input().split())
        coords2 = map(int, input().split())
        mine_area(dwarf_name, coords1, coords2, env)
    elif command == 'mine':
        mine(dwarf_name, env)    
    elif command == 'move':
        coords = map(int, input())
        move(dwarf_name, coords, env)
    elif command == 'get_map':
        get_map(dwarf_name, env)
    elif command == 'show_dwarf_inventory':
        show_dwarf_inventory(dwarf_name, env)