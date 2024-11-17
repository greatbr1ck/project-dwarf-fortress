#!/usr/bin/python

import random
import environment
import dwarfs
import goblins

def get_initial_dwarf_coords(number_of_dwarfes):
    initial_dwarf_coords = []

    (row, col) = (environment.SIZE_OF_FIELD // 2, environment.SIZE_OF_FIELD // 2)

    q = []
    q.append((row, col))

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
    goblins_list = []

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

            while (1, row, col) in initial_coords:
                row = random.randint(0, environment.SIZE_OF_FIELD - 1)
                col = random.randint(0, environment.SIZE_OF_FIELD - 1)
    
            local_field[row][col] = environment.KINDS_OF_DUNGEON_TILES["Cave"]
            caves_center.append((row, col))
            goblins_list.append(goblins.Goblin((row, col)))
        
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
        
        #for checker - useful tu uncomment while checking the fight process
        #game_field[coord[1] - 1][coord[2]] = 'G'
        #game_field[coord[1]][coord[2] - 1] = 'G'

    #set goblins positions
    for goblin in goblins_list:
        (row, col) = goblin.coords
        game_field[row][col] = 'G'

    return game_field

def init_game():
    #get dwarfes list
    print('type the population of your dwarf squad')
    
    s = input()
    while True:
        is_number = True
        for c in s:
            if not c in '0123456789':
                is_number = False
        if not is_number:
            print('Error! Dwarfs population must be an integer value')
            s = input()
            continue

        number_of_dwarfes = int(s)
        if 1 <= number_of_dwarfes and number_of_dwarfes <= environment.SIZE_OF_FIELD * environment.SIZE_OF_FIELD:
            break

        print('Error! Dwarfs population must be greater than 0 and no greater than', environment.SIZE_OF_FIELD * environment.SIZE_OF_FIELD)
        s = input()

    initial_coords = get_initial_dwarf_coords(number_of_dwarfes)

    dwarfes_list = []
    for i in range(number_of_dwarfes):
        print('type another dwarfs name')
        name = input()

        print('type the dwarfs work responsibility ("Warrior" or "Healer")')
        profession = input()
        while True:
            profession = profession.lower()
            profession = chr(ord(profession[0]) - 32) + profession[1::]

            if profession in environment.KINDS_OF_DWARFES_PROFESSIONS:
                break

            print('please type "Warrior" or "Healer"')
            profession = input()

        coords = initial_coords[i]

        dwarf = dwarfs.Dwarf(profession, name, coords)
        dwarfes_list.append(dwarf)

    #generate environment
    env = environment.Environment(dwarfes_list)
    env.dungeon = generate_dungeon(initial_coords)

    goblins_list = []
    for i in range(environment.SIZE_OF_FIELD):
        for j in range(environment.SIZE_OF_FIELD):
            if env.dungeon[i][j] == 'G':
                goblins_list.append(goblins.Goblin((1, i, j)))
    
    env.goblins_list = goblins_list
    env.update_entities()

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
    print("damage:", dwarf.get_damage())
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
    
    dwarf = env.get_dwarf(dwarf_name)    
    dwarf.move(destination_coords[1:], env)
    dwarf.destination_coords = destination_coords

    if dwarf.coords == destination_coords:
        if dwarf.doing_command == 'Move':
            dwarf.doing_command = 'Nothing'
            dwarf.destination_coords = (1, -1, -1)
        elif dwarf.doing_command == 'Mine:Move':
            dwarf.doing_command = 'Mine:Reached'
            dwarf.destination_coords = (1, -1, -1)
        elif dwarf.doing_command == 'Throw:Move':
            dwarf.doing_command = 'Throw:Reached'
            dwarf.destination_coords = (1, -1, -1)
    env.update_dwarf(dwarf_name, dwarf)

def mine(dwarf_name, env):
    dwarf = env.get_dwarf(dwarf_name)

    if dwarf.inventory.is_filled():
        print("Dwarf's inventory is filled")
        return

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
    
    env.update_dwarf(dwarf_name, dwarf)

def mine_area(dwarf_name, coords1, coords2, env):
    dwarf = env.get_dwarf(dwarf_name)

    if dwarf.inventory.is_filled():
        print("Dwarf's inventory is filled")
        
        dwarf.doing_command = 'Nothing'
        dwarf.coords1 = (1, -1, -1)
        dwarf.coords2 = (1, -1, -1)
        env.update_dwarf(dwarf_name, dwarf)
        return

    if dwarf.doing_command == 'Mine':
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

        if finish_row == -1:
            print('It is impossible to reach given area')
            dwarf.doing_command = 'Nothing'
            dwarf.coords1 = (1, -1, -1)
            dwarf.coords2 = (1, -1, -1)
            env.update_dwarf(dwarf_name, dwarf)
            return
        
        for step in ((-1, 0), (0, -1), (1, 0), (0, 1)):
            (r, c) = (finish_row + step[0], finish_col + step[1])
            if 0 <= r and r < environment.SIZE_OF_FIELD and 0 <= c and c < environment.SIZE_OF_FIELD and \
            dwarf.caves_map[r][c] == environment.KINDS_OF_DUNGEON_TILES["Cave"]:
                (finish_row, finish_col) = (r, c)
                break
        
        dwarf.doing_command = 'Mine:Move'
        dwarf.destination_coords = (1, finish_row, finish_col)
        env.update_dwarf(dwarf_name, dwarf)
    if dwarf.doing_command == 'Mine:Move':
        move(dwarf_name, dwarf.destination_coords, env) 
        env.update_dwarf(dwarf_name, dwarf)
    elif dwarf.doing_command == 'Mine:Reached':    
        for step in ((-1, 0), (0, -1), (1, 0), (0, 1)):
            (r, c) = (dwarf.coords[1] + step[0], dwarf.coords[2] + step[1])
            if 0 <= r and r < environment.SIZE_OF_FIELD and 0 <= c and c < environment.SIZE_OF_FIELD and \
               coords1[1] <= r and r <= coords2[1] and coords1[2] <= c and c <= coords2[2]:
                if step == (-1, 0):
                    dwarf.direction == 'North'
                elif step == (0, -1):
                    dwarf.direction == 'West'
                elif step == (1, 0):
                    dwarf.direction == 'South'
                else:
                    dwarf.direction == 'East'

        env.update_dwarf(dwarf_name, dwarf)
        
        #start mining the area    
        mine(dwarf_name, env)

        if dwarf.inventory.is_filled():
            print("Dwarf's inventory is filled")
            dwarf.doing_command = 'Nothing'
            dwarf.destination_coords = (1, -1, -1)
            dwarf.coords1 = (1, -1, -1)
            dwarf.coords2 = (1, -1, -1)
            env.update_dwarf(dwarf_name, dwarf)
            return
        
        dwarf.doing_command = 'Mine:Move in area'
        env.update_dwarf(dwarf_name, dwarf)
    elif dwarf.doing_command == 'Mine:Move in area':
        if dwarf.direction == 'North':
            move(dwarf_name, (1, dwarf.coords[1] - 1, dwarf.coords[2]), env)
        elif dwarf.direction == 'South':
            move(dwarf_name, (1, dwarf.coords[1] + 1, dwarf.coords[2]), env)
        elif dwarf.direction == 'West':
            move(dwarf_name, (1, dwarf.coords[1], dwarf.coords[2] - 1), env)
        else:
            move(dwarf_name, (1, dwarf.coords[1], dwarf.coords[2] + 1), env)
        dwarf.direction = 'North'

        dwarf.doing_command = 'Mine:Move in left corner'
        env.update_dwarf(dwarf_name, dwarf)
    elif dwarf.doing_command == 'Mine:Move in left corner':
        if dwarf.coords[1] > coords1[1]:
            if dwarf.caves_map[dwarf.coords[1] - 1][dwarf.coords[2]] != environment.KINDS_OF_DUNGEON_TILES['Cave']:
                mine(dwarf_name, env)
            move(dwarf_name, (1, dwarf.coords[1] - 1, dwarf.coords[2]), env)
            env.update_dwarf(dwarf_name, dwarf)
            
            if dwarf.inventory.is_filled():
                print("Dwarf's inventory is filled")
                dwarf.destination_coords = (1, -1, -1)
                dwarf.coords1 = (1, -1, -1)
                dwarf.coords2 = (1, -1, -1)    
                env.update_dwarf(dwarf_name, dwarf)
                return
        else:       
            dwarf.direction = 'West'
            env.update_dwarf(dwarf_name, dwarf)
            
            if dwarf.coords[2] > coords1[2]:
                if dwarf.caves_map[dwarf.coords[1]][dwarf.coords[2] - 1] != environment.KINDS_OF_DUNGEON_TILES['Cave']:
                    mine(dwarf_name, env)
                move(dwarf_name, (1, dwarf.coords[1], dwarf.coords[2] - 1), env)
                env.update_dwarf(dwarf_name, dwarf)

                if dwarf.inventory.is_filled():
                    print("Dwarf's inventory is filled")
                    dwarf.destination_coords = (1, -1, -1)
                    dwarf.coords1 = (1, -1, -1)
                    dwarf.coords2 = (1, -1, -1)
                    env.update_dwarf(dwarf_name, dwarf)    
                    return
            else:
                dwarf.doing_command = 'Mine:Reached in left corner'
                env.update_dwarf(dwarf_name, dwarf)
    elif dwarf.doing_command == 'Mine:Reached in left corner':
        dwarf.direction = 'West'
        env.update_dwarf(dwarf_name, dwarf)
        
        col_diff = -1
        if (dwarf.coords[1] - dwarf.coords1[1]) % 2 == 0:
            dwarf.direction = 'East'
            env.update_dwarf(dwarf_name, dwarf)
            col_diff = 1
        
        destination = (dwarf.coords[1], dwarf.coords[2] + col_diff)
        if destination[1] > dwarf.coords2[2] or destination[1] < dwarf.coords1[2]:
            dwarf.direction = 'South'
            env.update_dwarf(dwarf_name, dwarf)
        
            if dwarf.coords[1] + 1 <= coords2[1]:
                if dwarf.caves_map[dwarf.coords[1] + 1][dwarf.coords[2]] != environment.KINDS_OF_DUNGEON_TILES['Cave']:
                    mine(dwarf_name, env)
                move(dwarf_name, (1, dwarf.coords[1] + 1, dwarf.coords[2]), env) 
                env.update_dwarf(dwarf_name, dwarf)
                
                if dwarf.inventory.is_filled():
                    print("Dwarf's inventory is filled")
                    dwarf.destination_coords = (1, -1, -1)
                    dwarf.coords1 = (1, -1, -1)
                    dwarf.coords2 = (1, -1, -1)
                    env.update_dwarf(dwarf_name, dwarf)
                    return
            else:
                dwarf.doing_command = 'Nothing'
                dwarf.destination_coords = (1, -1, -1)
                dwarf.coords1 = (1, -1, -1)
                dwarf.coords2 = (1, -1, -1)
                env.update_dwarf(dwarf_name, dwarf)
                return
        else:
            if dwarf.caves_map[destination[0]][destination[1]] != environment.KINDS_OF_DUNGEON_TILES['Cave']:
                mine(dwarf_name, env)
            move(dwarf_name, (1, destination[0], destination[1]), env)            
            env.update_dwarf(dwarf_name, dwarf)

def throw(dwarf_name, env):
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
        dwarf.throw((1, row, col), env)
    
    env.update_dwarf(dwarf_name, dwarf)

def turn_around(dwarf_name, env):
    dwarf = env.get_dwarf(dwarf_name)
    if dwarf.direction == 'North':
        dwarf.direction = 'South'
    elif dwarf.direction == 'South':
        dwarf.direction = 'North'
    elif dwarf.direction == 'West':
        dwarf.direction = 'East'
    else:
        dwarf.direction = 'West'
    env.update_dwarf(dwarf_name, dwarf)

def throw_area(dwarf_name, coords1, coords2, env):
    dwarf = env.get_dwarf(dwarf_name)

    if dwarf.inventory.is_garbage_thrown():
        dwarf.doing_command = 'Nothing'
        dwarf.coords1 = (1, -1, -1)
        dwarf.coords2 = (1, -1, -1)
        env.update_dwarf(dwarf_name, dwarf)
        return

    if dwarf.doing_command == 'Throw':
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

        if finish_row == -1:
            print('It is impossible to reach given area')
            dwarf.doing_command = 'Nothing'
            dwarf.dump_coords1 = (1, -1, -1)
            dwarf.dump_coords2 = (1, -1, -1)
            env.update_dwarf(dwarf_name, dwarf)
            return
        
        for step in ((-1, 0), (0, -1), (1, 0), (0, 1)):
            (r, c) = (finish_row + step[0], finish_col + step[1])
            if 0 <= r and r < environment.SIZE_OF_FIELD and 0 <= c and c < environment.SIZE_OF_FIELD and \
            dwarf.caves_map[r][c] == environment.KINDS_OF_DUNGEON_TILES["Cave"]:
                (finish_row, finish_col) = (r, c)
                break
        
        dwarf.doing_command = 'Throw:Move'
        dwarf.destination_coords = (1, finish_row, finish_col)
        env.update_dwarf(dwarf_name, dwarf)
    if dwarf.doing_command == 'Throw:Move':
        move(dwarf_name, dwarf.destination_coords, env) 
        env.update_dwarf(dwarf_name, dwarf)
    elif dwarf.doing_command == 'Throw:Reached':    
        for step in ((-1, 0), (0, -1), (1, 0), (0, 1)):
            (r, c) = (dwarf.coords[1] + step[0], dwarf.coords[2] + step[1])
            if 0 <= r and r < environment.SIZE_OF_FIELD and 0 <= c and c < environment.SIZE_OF_FIELD and \
               coords1[1] <= r and r <= coords2[1] and coords1[2] <= c and c <= coords2[2]:
                if step == (-1, 0):
                    dwarf.direction == 'North'
                elif step == (0, -1):
                    dwarf.direction == 'West'
                elif step == (1, 0):
                    dwarf.direction == 'South'
                else:
                    dwarf.direction == 'East'

        env.update_dwarf(dwarf_name, dwarf)
        
        #start throwing in area    
        turn_around(dwarf_name, env)
        throw(dwarf_name, env)
        turn_around(dwarf_name, env)

        dwarf.doing_command = 'Throw:Move in area'
        env.update_dwarf(dwarf_name, dwarf)
    elif dwarf.doing_command == 'Throw:Move in area':
        if dwarf.direction == 'North':
            move(dwarf_name, (1, dwarf.coords[1] - 1, dwarf.coords[2]), env)
        elif dwarf.direction == 'South':
            move(dwarf_name, (1, dwarf.coords[1] + 1, dwarf.coords[2]), env)
        elif dwarf.direction == 'West':
            move(dwarf_name, (1, dwarf.coords[1], dwarf.coords[2] - 1), env)
        else:
            move(dwarf_name, (1, dwarf.coords[1], dwarf.coords[2] + 1), env)
        dwarf.direction = 'North'

        dwarf.doing_command = 'Throw:Move in left corner'
        env.update_dwarf(dwarf_name, dwarf)
    elif dwarf.doing_command == 'Throw:Move in left corner':
        if dwarf.coords[1] > coords1[1]:
            turn_around(dwarf_name, env)
            throw(dwarf_name, env)
            turn_around(dwarf_name, env)

            move(dwarf_name, (1, dwarf.coords[1] - 1, dwarf.coords[2]), env)
            env.update_dwarf(dwarf_name, dwarf)
        else:       
            dwarf.direction = 'West'
            env.update_dwarf(dwarf_name, dwarf)
            
            if dwarf.coords[2] > coords1[2]:
                turn_around(dwarf_name, env)
                throw(dwarf_name, env)
                turn_around(dwarf_name, env)

                move(dwarf_name, (1, dwarf.coords[1], dwarf.coords[2] - 1), env)
                env.update_dwarf(dwarf_name, dwarf)
            else:
                dwarf.doing_command = 'Throw:Reached in left corner'
                env.update_dwarf(dwarf_name, dwarf)
    elif dwarf.doing_command == 'Throw:Reached in left corner':
        dwarf.direction = 'West'
        env.update_dwarf(dwarf_name, dwarf)
        
        col_diff = -1
        if (dwarf.coords[1] - dwarf.coords1[1]) % 2 == 0:
            dwarf.direction = 'East'
            env.update_dwarf(dwarf_name, dwarf)
            col_diff = 1
        
        destination = (dwarf.coords[1], dwarf.coords[2] + col_diff)
        if destination[1] > dwarf.coords2[2] or destination[1] < dwarf.coords1[2]:
            dwarf.direction = 'South'
            env.update_dwarf(dwarf_name, dwarf)
        
            if dwarf.coords[1] + 1 <= coords2[1]:
                turn_around(dwarf_name, env)
                throw(dwarf_name, env)
                turn_around(dwarf_name, env)

                move(dwarf_name, (1, dwarf.coords[1] + 1, dwarf.coords[2]), env) 
                env.update_dwarf(dwarf_name, dwarf)
            else:
                dwarf.doing_command = 'Nothing'
                dwarf.destination_coords = (1, -1, -1)
                dwarf.dump_coords1 = (1, -1, -1)
                dwarf.dump_coords2 = (1, -1, -1)
                env.update_dwarf(dwarf_name, dwarf)
                return
        else:
            turn_around(dwarf_name, env)
            throw(dwarf_name, env)
            turn_around(dwarf_name, env)

            move(dwarf_name, (1, destination[0], destination[1]), env)            
            env.update_dwarf(dwarf_name, dwarf)            

def build_block(dwarf_name, env):
    dwarf = env.get_dwarf(dwarf_name)
    dwarf.build(env)
    env.update_dwarf(dwarf_name, dwarf)  

def mark_as_garbage(dwarf_name, item_name, env):
    dwarf = env.get_dwarf(dwarf_name)
    dwarf.mark_garbage(environment.BLOCKS[item_name])
    env.update_dwarf(dwarf_name, dwarf)

def heal(dwarf_name, other_name):
    dwarf = env.get_dwarf(dwarf_name)
    other = env.get_dwarf(other_name)

    if not dwarf.inventory.contains(environment.BLOCKS['Worked Gold']):
        print("Dwarf", dwarf_name, "cannot heal another dwarf due to the lack of gold")
        return

    dwarf.inventory.extract_item(environment.BLOCKS['Worked Gold'])
    other.health += 2
    if other.health > other.max_health:
        other.health= other.max_health
    env.update_dwarf(dwarf_name, dwarf)
    env.update_dwarf(other_name, other)


#-------------------------------GAME-----------------------------

TURN_COMMANDS = dict([('Turn North', 'w'), ('Turn West', 'a'), ('Turn South', 's'), ('Turn East', 'd')])
MOVE_COMMANDS = dict([('Move', 'mv')])
MINE_COMMANDS = dict([('Mine', 'mn'), ('Mine Area', 'mna')])
INFO_COMMANDS = dict([('Show Inventory', 'inv'), ('Get Map', 'map'), ('Get Info', 'inf')])
BUILD_COMMANDS = dict([('Build', 'b')])
THROW_COMMANDS = dict([('Mark as garbage', 'mk'), ('Throw', 't')])
FINISH_COMMANDS = dict([('Move on to another dwarf', 'f')])
BUY_COMMANDS = dict([('Buy for gold', 'g')])
HEAL_COMMANDS = dict([('Heal', 'h')])

def help():
    print("You can turn dwarf's direction as much as you want in any single move")
    for key in TURN_COMMANDS:
        print('if you want to', key, 'you should type:', TURN_COMMANDS[key])
    print()

    print("You can move a dwarf to any cell of a field with coords (coords.row, coords.column) by typing: ")
    print(MOVE_COMMANDS['Move'])
    print('row col #where row and col are integer numbers in 0..', environment.SIZE_OF_FIELD, sep='')
    print()

    print("Dwarf can mine a tile in front of him by typing: ", MINE_COMMANDS['Mine'])
    print()

    print("Dwarf can mine an area with left high corner (coords1.row, coords1.column) and right low corner (coords2.row, coords2.column) by typing: ")
    print(MINE_COMMANDS['Mine Area'])
    print("row1 col1")
    print("row2 col2 #where row1, 2 and col1, 2 are integer numbers in 0..", environment.SIZE_OF_FIELD, " and are the corners of area mentioned higher", sep='')
    print()

    print("You can see dwarf's inventory by typing: ", INFO_COMMANDS['Show Inventory'])
    print()

    print("You can see what dwarf remembers about the parts of field it is possible to go by typing: ", INFO_COMMANDS['Get Map'])
    print()

    print("You can see basic information abiut this particular dwarfs by typing", INFO_COMMANDS['Get Info'])
    print()

    print("Dwarf can build a Worked Stone block in front of him if the tile in front of him is empty by typing: ", BUILD_COMMANDS['Build'])
    print()

    print("You can mark the things of dwarfs inventory as a garbage to throw later by typing: ")
    print(THROW_COMMANDS['Mark as garbage'])
    print("name #where name is 'Worked Stone', 'Worked Iron', 'Worked Gold' or 'Coal'")
    print()

    print("Dwarf can throw all marked as garbage from his inventory in an area with left high corner (coords1.row, coords1.column) and right low corner (coords2.row, coords2.column) by typing:")
    print(THROW_COMMANDS['Throw'])
    print("row1 col1")
    print("row2 col2 #where row1, 2 and col1, 2 are integer numbers in 0..", environment.SIZE_OF_FIELD, " and are the corners of area mentioned higher", sep='')
    print()
    
    print("You can finish playing for this particular dwarf on this particular game move by typing: ", FINISH_COMMANDS['Move on to another dwarf'])
    print()

    print("Dwarf can exchange one Worked Gold item from his inventory for one particular item from from <'Stone Pickaxe', 'Wooden Pickaxe', 'Axe', 'Wooden Stick'> by typing:")
    print(BUY_COMMANDS['Buy for gold'])
    print("name #where name is the name of any single instrument mentioned higher")

def describe():
    print("field symbols:")
    for key in list(environment.KINDS_OF_DUNGEON_TILES.keys()):
        print(environment.KINDS_OF_DUNGEON_TILES[key], "stands for", key)
    print()
    
    print("inventory symbols")
    for key in list(environment.INSTRUMENTS.keys()):
        print(environment.INSTRUMENTS[key], "stands for", key)
    for key in list(environment.BLOCKS.keys()):
        print(environment.BLOCKS[key], "stands for", key)
    print()

    print("G stands for goblin")
    print("D stands for dwarf")

def can_be_parsed_into_coords(data):
    for c in data:
        if not c in ' 0123456789':
            return False
    return True

print('''
    Welcome to the world of dwarf and goblins!\n
    !!!Type "help" whenever you want to know the commands you can use playing for dwarfs!!!
    First, you should form a dwarf squad.
      ''')

env = init_game()

print('''
    As you have formed the dwarf squad, the game starts:
    On each stage you have to make a move for each alive dwarf.
    Type the name of any alive dwarf and type the command you want him to do.
    After that finish the move for this particular dwarf by the command 'f'.
    If you dont remember what any simbol of field or inventory means, you can type "describe"
    ''')

while True:
    used_dwarfs = set()

    for i in range(len(env.dwarfs_list)):
        print("Type the name of alive dwarf you have not played for in this particular move")
        dwarf_name = input()

        while True:
            if not env.dwarf_exists(dwarf_name):
                print("Type the name of existing and alive dwarf")
            elif dwarf_name in used_dwarfs:
                print('You have already used this dwarf in this move')
            else:
                used_dwarfs.add(dwarf_name)
                break

            dwarf_name = input()

        dwarf = env.get_dwarf(dwarf_name)

        is_mine_area_used = False
        is_move_used = False
        is_throw_used = False

        while True:
            print("Type another command to do")
            command = input()

            command_exists = False
            is_finished = False

            if command == "describe":
                describe()
                command_exists = True

            if command == "help":
                help()
                command_exists = True

            #command for checker - to see the whole field
            if command == "D":
                for _ in env.dungeon:
                    for c in _:
                        print(c, end='')
                    print()
                command_exists = True    

            #command for checker - put one Worked Gold in dwarf's inventory
            if command == "E":
                dwarf.inventory.put_item(environment.BLOCKS['Worked Gold'])
                command_exists = True    

            for c in tuple(TURN_COMMANDS.keys()):
                if TURN_COMMANDS[c] == command:
                    command_exists = True
                    dwarf.direction = c[5:]
                    env.update_dwarf(dwarf_name, dwarf)
            for c in tuple(MOVE_COMMANDS.keys()):
                if MOVE_COMMANDS[c] == command:
                    if is_move_used:
                        print("You can move each dwarf only once at single game stage")
                        continue

                    data = input()
                    if not can_be_parsed_into_coords(data):
                        print("Unnacceptable coords format")
                        continue

                    coords = tuple(map(int, data.split()))
                    if len(coords) != 2:
                        print("Unnacceptable coords format")
                        continue

                    coords_ = (1, coords[0], coords[1])
                    dwarf.doing_command = 'Move'
                    env.update_dwarf(dwarf_name, dwarf)
                    move(dwarf_name, coords_, env)
                    env.update_dwarf(dwarf_name, dwarf)

                    is_move_used = True
                    command_exists = True
            for c in list(MINE_COMMANDS.keys()):
                if MINE_COMMANDS[c] == command:
                    if c == 'Mine Area':
                        if is_mine_area_used:
                            print("Each dwarf can mine area only once at single game stage")
                            continue

                        data = input()
                        if not can_be_parsed_into_coords(data):
                            print("Unnacceptable coords format")
                            continue
                            
                        coords1 = tuple(map(int, data.split()))
                        if len(coords1) != 2:
                            print("Unnacceptable coords format")
                            continue
                        coords1_= (1, coords1[0], coords1[1])

                        data = input()
                        if not can_be_parsed_into_coords(data):
                            print("Unnacceptable coords format")
                            continue

                        coords2 = tuple(map(int, data.split()))
                        if len(coords2) != 2:
                            print("Unnacceptable coords format")
                            continue
                        coords2_ = (1, coords2[0], coords2[1])

                        if not(coords1_[1] <= coords2_[1] and coords1_[2] <= coords2_[2]):
                            print('Choose LEFT HIGH and RIGHT LOW corners of mining area') 
                            continue
                    
                        dwarf.doing_command = 'Mine'
                        dwarf.coords1 = coords1_
                        dwarf.coords2 = coords2_
                        
                        env.update_dwarf(dwarf_name, dwarf)
                        mine_area(dwarf_name, coords1_, coords2_, env)
                        env.update_dwarf(dwarf_name, dwarf)
                        is_mine_area_used = True
                    else:                         
                        if is_mine_area_used:
                            print("Each dwarf can mine area only once at single game stage")
                            continue 

                        mine(dwarf_name, env)

                    command_exists = True
            for c in list(INFO_COMMANDS.keys()):
                if INFO_COMMANDS[c] == command:
                    if c == 'Get Map':
                        get_map(dwarf_name, env)
                    elif c == 'Get Info':
                        get_dwarf_info(dwarf_name, env)
                    else:
                        show_dwarf_inventory(dwarf_name, env)

                    command_exists = True
            for c in list(BUILD_COMMANDS.keys()):
                if BUILD_COMMANDS[c] == command:
                    if dwarf.inventory.contains(environment.BLOCKS['Worked Stone']):
                        build_block(dwarf_name, env)
                        env.update_dwarf(dwarf_name, dwarf)

                    command_exists = True
            for c in list(THROW_COMMANDS.keys()):
                if THROW_COMMANDS[c] == command:
                    if c == 'Mark as garbage':
                        item_name = input()
                        is_name_correct = False

                        for name in list(environment.BLOCKS.keys()):
                            if name == item_name:
                                is_name_correct = True
                        
                        if not is_name_correct:
                            print("Type the item name correctly")
                            continue
                            
                        mark_as_garbage(dwarf_name, item_name, env)
                        env.update_dwarf(dwarf_name, dwarf)
                    else:
                        if is_throw_used:
                            print("Each dwarf can throw items only once at single game stage")
                            continue

                        data = input()
                        if not can_be_parsed_into_coords(data):
                            print("Unnacceptable coords format")
                            continue

                        coords1 = tuple(map(int, data.split()))
                        if len(coords1) != 2:
                            print("Unnacceptable coords format")
                            continue
                        coords1_ = (1, coords1[0], coords1[1])

                        data = input()
                        if not can_be_parsed_into_coords(data):
                            print("Unnacceptable coords format")
                            continue

                        coords2 = tuple(map(int, data.split()))
                        if len(coords2) != 2:
                            print("Unnacceptable coords format")
                            continue
                        coords2_ = (1, coords2[0], coords2[1])

                        if not(coords1_[1] <= coords2_[1] and coords1_[2] <= coords2_[2]):
                            print('Choose LEFT HIGH and RIGHT LOW corners of dump area')
                            continue
                    
                        dwarf.doing_command = 'Throw'
                        dwarf.dump_coords1 = coords1_
                        dwarf.dump_coords2 = coords2_
                        
                        env.update_dwarf(dwarf_name, dwarf)
                        throw_area(dwarf_name, coords1_, coords2_, env)
                        env.update_dwarf(dwarf_name, dwarf)
                        is_throw_used = True

                    command_exists = True
            for c in list(FINISH_COMMANDS.keys()):
                if FINISH_COMMANDS[c] == command:
                    is_finished = True
                    command_exists = True
            for c in list(BUY_COMMANDS.keys()):
                if BUY_COMMANDS[c] == command:
                    command_exists = True

                    if not dwarf.inventory.contains(environment.BLOCKS['Worked Gold']):
                        print("There is not gold in dwarf's inventory to exchange")
                        continue

                    exchanging_item = input()
                    if exchanging_item in list(environment.INSTRUMENTS.keys()):
                        dwarf.inventory.extract_item(environment.BLOCKS['Worked Gold'])
                        dwarf.inventory.put_item(environment.INSTRUMENTS[exchanging_item])
                        env.update_dwarf(dwarf_name, dwarf)
            
            for c in list(HEAL_COMMANDS.keys()):
                if HEAL_COMMANDS[c] == command:
                    command_exists = True

                    other_dwarf_name = input()
                    if not env.dwarf_exists(other_dwarf_name):
                        print("There is no dwarf named", other_dwarf_name, "in your dwarf squad")
                        continue

                    heal(dwarf_name, other_dwarf_name)

            if is_finished:
                if not is_mine_area_used:
                    if dwarf.doing_command[:4:] == 'Mine':
                        mine_area(dwarf_name, dwarf.coords1, dwarf.coords2, env)
                        env.update_dwarf(dwarf_name, dwarf)
                
                if not is_throw_used:
                    if dwarf.doing_command[:5:] == 'Throw':
                        throw_area(dwarf_name, dwarf.dump_coords1, dwarf.dump_coords2, env)
                        env.update_dwarf(dwarf_name, dwarf)

                if not is_move_used:
                    if dwarf.doing_command == 'Move':
                        move(dwarf_name, dwarf.destination_coords, env)
                        env.update_dwarf(dwarf_name, dwarf)
                
                break

            if not command_exists:
                print('Type the command correctly')
                continue
        
        dwarf.fight(env)
        env.update_dwarf(dwarf_name, dwarf)
    
    env.timer += 1
    for i in range(len(env.goblins_list)):
        env.goblins_list[i].fight(env)
        env.goblins_list[i].move(env)

    if len(env.dwarfs_list) == 0:
        print("All your dwarfs were killed... Game over")
        break