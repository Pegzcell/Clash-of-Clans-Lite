
from src.headers import *
from src.misc import *

class Object:

    def __init__(self, x, y):
        self.pos = self.position(x, y)
        self.destroyed = False
        self.hitStatus = -1
        # self.figure=[]
        # self.shape=np.zeros((100), dtype='<U1000')

    class position:
        def __init__(self , x, y):
            self.x = x
            self.y = y


    def attacked(self, attack_val):
        # print('before', self.pos.x, self.pos.y, "::", self.health)
        self.health -= attack_val
        # print('after', self.pos.x, self.pos.y, "::", self.health)
        if self.health <= 0:
            self.health = 0
            self.destroyed = True ##########################
        if len(self.hitpoints) and self.health < self.hitpoints[0]:
            self.hitStatus+=1
            self.hitpoints.pop(0)
            # print(self.pos.x, self.pos.y, "=", self.hitStatus)

    def add_to_scene(self, scene):                  
        #POLYMORPHISM USED TO SHOW/DISPLAY ALL OBJECTS
        for i in range(len(self.figure)):
            for j in range(len(self.figure[0])):
                if (self.hitStatus == -1):
                    scene.grid[self.pos.x + i][self.pos.y + j]= (self.textureOut if (j==0 or j==len(self.figure[0])-1) else self.textureIn) + self.figure[i][j]
                else:
                    scene.grid[self.pos.x + i][self.pos.y + j]= (self.textureOut + HEALTH_COLOR[self.hitStatus] if (j==0 or j==len(self.figure[0])-1) else self.textureIn) + self.figure[i][j]
 

class Structure(Object):
    def __init__(self, x, y):
        Object.__init__(self,x,y)
                   

# class EdgeWall(Structure):
#     def __init__(self, x, y):
#         Structure.__init__(self,x,y, EDGETILE_WIDTH, EDGETILE_HEIGHT)

class TownHall(Structure):
    def __init__(self):
        self.textureIn = Back.LIGHTMAGENTA_EX + Fore.BLACK
        self.textureOut = BGCOLOR + FGCOLOR
        self.health = 1000
        self.hitpoints = [1000, 500, 200]
        self.figure = [list(i) for i in ("""\
/^^\\
|TH|
|__|""").split("\n")]
        Object.__init__(self, (HEIGHT - 3)//2, (WIDTH - 4)//2)


class Hut(Structure):
    def __init__(self, x, y):
        self.textureIn = Back.LIGHTMAGENTA_EX + Fore.BLACK
        self.textureOut = BGCOLOR + FGCOLOR
        self.health = 300
        self.hitpoints = [500, 200, 100]
        self.figure = [list(i) for i in ("""\
/H\\
|_|""").split("\n")]
        Object.__init__(self, x,y)


class Cannon(Structure):
    def __init__(self, x, y):
        self.shooting = -1
        self.justshot = False
        self.range = 9
        self.attack_val = 20
        self.textureIn = Back.LIGHTMAGENTA_EX + Fore.BLACK
        self.textureIn_ = Back.LIGHTMAGENTA_EX + Fore.WHITE
        self.textureOut = BGCOLOR +FGCOLOR
        self.health = 1000
        self.hitpoints = [1000, 500, 200]
        self.figure = [list(i) for i in ("""\
(C)""").split("\n")] 
        Object.__init__(self, x,y) 

    def shoot(self, game):
        if self.shooting == -1: #cannon idle
            if not game.player.destroyed and dist_sq(game.player.pos.x + (len(game.player.figure)-1)//2, game.player.pos.y + (len(game.player.figure[0])-1)//2, self.pos.x, self.pos.y + (len(self.figure[0])-1)//2) <= self.range**2:
                self.shooting = "k"
                self.justshot = True
                game.player.attacked(self.attack_val)
            else:
                for i in list(game.troops_dict.values())[:-1]:
                    if (len(i) != 0):
                        break
                else:
                    return #cannon inactive bc no troops
                closestTroop = Cannon_closest_troop(self.pos.x, self.pos.y + (len(self.figure[0])-1)//2, game.troops_dict, self.range)
                if closestTroop != -1:
                    self.shooting = closestTroop
                    self.justshot = True
                    game.troops_dict[closestTroop[0]][closestTroop[1]].attacked(self.attack_val)

        else: #cannon shooting smth => wants to continue shooting that object if it's still in range
            index = self.shooting
            self.shooting = -1
            if index =='k':
                if not game.player.destroyed and dist_sq(game.player.pos.x + (len(game.player.figure)-1)//2, game.player.pos.y + (len(game.player.figure[0])-1)//2, self.pos.x, self.pos.y + (len(self.figure[0])-1)//2) <= self.range**2:
                    self.shooting = index
                    self.justshot = True
                    game.player.attacked(self.attack_val)
            else:
                if (index[2] and index[1] < len(index[2]) and game.troops_dict[index[0]] == index[2]):
                    if dist_sq(game.troops_dict[index[0]][index[1]].pos.x, game.troops_dict[index[0]][index[1]].pos.y, self.pos.x, self.pos.y + (len(self.figure[0])-1)//2) <= self.range**2:
                        self.shooting = index
                        self.justshot = True
                        game.troops_dict[index[0]][index[1]].attacked(self.attack_val)
    
    def add_to_scene(self, scene):                  
        #POLYMORPHISM USED TO SHOW/DISPLAY ALL OBJECTS
        for i in range(len(self.figure)):
            for j in range(len(self.figure[0])):
                if (self.hitStatus == -1):
                    scene.grid[self.pos.x + i][self.pos.y + j]= (self.textureOut if (j==0 or j==len(self.figure[0])-1) else (self.textureIn_ if self.justshot else self.textureIn)) + self.figure[i][j]
                else:
                    scene.grid[self.pos.x + i][self.pos.y + j]= (self.textureOut + HEALTH_COLOR[self.hitStatus] if (j==0 or j==len(self.figure[0])-1) else (self.textureIn_ if self.justshot else self.textureIn)) + self.figure[i][j]
 
class Tower(Structure):
    def __init__(self, x, y):
        self.shooting = -1
        self.justshot = False
        self.range = 9
        self.attack_val = 20
        self.aoe = 3
        self.textureIn = Back.LIGHTMAGENTA_EX + Fore.BLACK
        self.textureIn_ = Back.LIGHTMAGENTA_EX + Fore.WHITE
        self.textureOut = BGCOLOR + FGCOLOR
        self.health = 1000
        self.hitpoints = [1000, 500, 200]
        self.figure = [list(i) for i in ("""\
<W>""").split("\n")] 
        Object.__init__(self, x,y) 

    def shoot(self, game):
        if self.shooting == -1: #tower idle
            if not game.player.destroyed and dist_sq(game.player.pos.x + (len(game.player.figure)-1)//2, game.player.pos.y + (len(game.player.figure[0])-1)//2, self.pos.x, self.pos.y + (len(self.figure[0])-1)//2) <= self.range**2:
                self.shooting = "k"
                self.justshot = True
                game.player.attacked(self.attack_val)
            else:
                for i in list(game.troops_dict.values()):
                    if (len(i) != 0):
                        break
                else:
                    return #tower inactive bc no troops
                closestTroop = Tower_closest_troop(self.pos.x, self.pos.y + (len(self.figure[0])-1)//2, game.troops_dict, self.range)
                if closestTroop != -1:
                    for key, val in game.troops_dict.items():
                        for i in range(len(val)):
                            if abs(game.troops_dict[key][i].pos.x - game.troops_dict[closestTroop[0]][closestTroop[1]].pos.x) <= self.aoe/2 and abs(game.troops_dict[key][i].pos.y - game.troops_dict[closestTroop[0]][closestTroop[1]].pos.y) <= self.aoe/2:
                                game.troops_dict[key][i].attacked(self.attack_val) 
                    self.shooting = closestTroop
                    self.justshot = True

        else: #tower shooting smth => wants to continue shooting that object if it's still in range
            index = self.shooting
            self.shooting = -1
            if index =='k':
                if not game.player.destroyed and dist_sq(game.player.pos.x + (len(game.player.figure)-1)//2, game.player.pos.y + (len(game.player.figure[0])-1)//2, self.pos.x, self.pos.y + (len(self.figure[0])-1)//2) <= self.range**2:
                    self.shooting = index
                    self.justshot = True
                    game.player.attacked(self.attack_val)
            else:
                if (index[2] and index[1] < len(index[2]) and game.troops_dict[index[0]] == index[2]):
                    if dist_sq(game.troops_dict[index[0]][index[1]].pos.x, game.troops_dict[index[0]][index[1]].pos.y, self.pos.x, self.pos.y + (len(self.figure[0])-1)//2) <= self.range**2:
                        for key, val in game.troops_dict.items():
                            for i in range(len(val)):
                                if abs(game.troops_dict[key][i].pos.x - game.troops_dict[index[0]][index[1]].pos.x) <= self.aoe/2 and abs(game.troops_dict[key][i].pos.y - game.troops_dict[index[0]][index[1]].pos.y) <= self.aoe/2:
                                    game.troops_dict[key][i].attacked(self.attack_val) 
                        self.shooting = index
                        self.justshot = True
    
    def add_to_scene(self, scene):                  
        #POLYMORPHISM USED TO SHOW/DISPLAY ALL OBJECTS
        for i in range(len(self.figure)):
            for j in range(len(self.figure[0])):
                if (self.hitStatus == -1):
                    scene.grid[self.pos.x + i][self.pos.y + j]= (self.textureOut if (j==0 or j==len(self.figure[0])-1) else (self.textureIn_ if self.justshot else self.textureIn)) + self.figure[i][j]
                else:
                    scene.grid[self.pos.x + i][self.pos.y + j]= (self.textureOut + HEALTH_COLOR[self.hitStatus] if (j==0 or j==len(self.figure[0])-1) else (self.textureIn_ if self.justshot else self.textureIn)) + self.figure[i][j]

class Wall(Structure):
    def __init__(self, x, y):
        self.textureIn = FGCOLOR
        self.textureOut = Back.LIGHTBLACK_EX
        self.health = 100
        self.hitpoints = [100, 50, 20]
        self.figure = ['.']
        Object.__init__(self, x,y)  


class Team(Object):
    def __init__(self, x, y):
        # self.health = 200
        Object.__init__(self,x,y)

class Troop(Team):
    def __init__(self, x, y):
        self.attack_val = 10  
        self.health = 100
        self.hitpoints = [100, 50, 30]
        self.healpoints = (100, 50, 30)
        Team.__init__(self, x,y)   

    def move(self, game):
        if (len(game.Buildings_list) == 0):
            return #game_won
        building = closest_building(self.pos.x,self.pos.y, game.Buildings_list)
        # print("]]]]]]]]]]]]]]]]]]]]]]]", building.pos.x, building.pos.y)
        x_target = building.pos.x  + (len(building.figure)-1)//2
        y_target = building.pos.y + (len(building.figure[0])-1)//2
        x_step = 1 if (self.pos.x - x_target) < 0 else -1
        y_step = 1 if (self.pos.y - y_target) < 0 else -1
        if abs(self.pos.x - x_target) > abs(self.pos.y - y_target):
            if (self.pos.x + x_step >= building.pos.x and self.pos.x + x_step <= building.pos.x + len(building.figure) -1) and (self.pos.y >= building.pos.y and self.pos.y <= building.pos.y + len(building.figure[0])-1):
                building.attacked(self.attack_val)
            else:
                for wall_obj in game.walls_arr:
                    if (self.pos.x + x_step >= wall_obj.pos.x and self.pos.x + x_step <= wall_obj.pos.x + len(wall_obj.figure)-1) and (self.pos.y >= wall_obj.pos.y and self.pos.y <= wall_obj.pos.y + len(wall_obj.figure[0])-1):
                        wall_obj.attacked(self.attack_val)
                        break
                else:
                    self.pos.x += x_step
        else:
            if (self.pos.x >= building.pos.x and self.pos.x <= building.pos.x + len(building.figure)-1) and (self.pos.y +y_step >= building.pos.y and self.pos.y + y_step <= building.pos.y + len(building.figure[0])-1):
                building.attacked(self.attack_val)
            else:
                for wall_obj in game.walls_arr:
                    if (self.pos.x >= wall_obj.pos.x and self.pos.x <= wall_obj.pos.x + len(wall_obj.figure)-1) and (self.pos.y + y_step >= wall_obj.pos.y and self.pos.y + y_step <= wall_obj.pos.y + len(wall_obj.figure[0])-1):
                        wall_obj.attacked(self.attack_val)
                        break
                else:
                    self.pos.y += y_step

class Barbarian(Troop):
    def __init__(self, x, y):
        self.textureIn = FGCOLOR
        self.textureOut = BGCOLOR + Fore.BLUE
        self.figure = ['^']
        Troop.__init__(self, x, y)

class Archer(Troop):
    def __init__(self, x, y):
        self.range = 5
        self.attack_val = 5
        self.health = 50
        self.hitpoints = [50, 30, 10]
        self.healpoints = (50, 30, 10)        
        self.textureIn = FGCOLOR
        self.textureOut = BGCOLOR + Fore.RED
        self.figure = ['*']
        Troop.__init__(self, x, y)

    def move(self, game):
        if (len(game.Buildings_list) == 0):
            return #game_won
        building = closest_building(self.pos.x,self.pos.y, game.Buildings_list)
        x_target = building.pos.x + (len(building.figure)-1)//2
        y_target = building.pos.y + (len(building.figure[0])-1)//2
        x_step = 1 if (self.pos.x - x_target) < 0 else -1
        y_step = 1 if (self.pos.y - y_target) < 0 else -1
        if dist_sq(x_target, y_target, self.pos.x, self.pos.y) <= self.range**2:
            building.attacked(self.attack_val)
        else:
            if abs(self.pos.x - x_target) > abs(self.pos.y - y_target):
                for wall_obj in game.walls_arr:
                    # if dist_sq(wall_obj.pos.x + (len(wall_obj.figure)-1)//2, wall_obj.pos.y + (len(wall_obj.figure[0])-1)//2, self.pos.x, self.pos.y) <= self.range**2:
                    if wall_obj.pos.y == self.pos.y and (wall_obj.pos.x - self.pos.x)*x_step <= self.range and (wall_obj.pos.x - self.pos.x)*x_step > 0:
                        wall_obj.attacked(self.attack_val)
                        break
                else:
                    self.pos.x += x_step

            else:
                for wall_obj in game.walls_arr:
                    # if (self.pos.x >= wall_obj.pos.x and self.pos.x <= wall_obj.pos.x + len(wall_obj.figure)-1) and (self.pos.y + y_step >= wall_obj.pos.y and self.pos.y + y_step <= wall_obj.pos.y + len(wall_obj.figure[0])-1):
                    if wall_obj.pos.x == self.pos.x and (wall_obj.pos.y - self.pos.y)*y_step <= self.range and (wall_obj.pos.y - self.pos.y)*y_step > 0:    
                        wall_obj.attacked(self.attack_val)
                        break
                else:
                    self.pos.y += y_step

class Balloon(Troop):
    def __init__(self, x, y):
        self.attack_val = 20
        self.textureIn = FGCOLOR
        self.textureOut = BGCOLOR + Fore.MAGENTA
        self.figure = ['!']
        Troop.__init__(self, x, y)

    def move(self, game):
        if (len(game.Buildings_list) == 0):
            return #game_won
        if (len(game.Defensive_buildings_list) != 0):
            building = closest_building(self.pos.x,self.pos.y, game.Defensive_buildings_list)
        else:
            building = closest_building(self.pos.x,self.pos.y, game.Buildings_list)
    
        x_target = building.pos.x  + (len(building.figure)-1)//2
        y_target = building.pos.y + (len(building.figure[0])-1)//2
        x_step = 1 if (self.pos.x - x_target) < 0 else -1
        y_step = 1 if (self.pos.y - y_target) < 0 else -1
        if abs(self.pos.x - x_target) > abs(self.pos.y - y_target):
            if (self.pos.x == x_target) and (self.pos.y == y_target):
                building.attacked(self.attack_val)
            else:
                self.pos.x += x_step
        else:
            if (self.pos.x == x_target) and (self.pos.y == y_target):
                building.attacked(self.attack_val)
            else:
                self.pos.y += y_step
class King(Team):
    healpoints = (500, 200, 100)
    attack_val = 20
    def __init__(self,x,y):
        self.textureIn = BGCOLOR + Fore.GREEN
        self.textureOut = BGCOLOR + Fore.GREEN
        self.health = 500
        self.hitpoints = [500, 200, 100]
        self.range = 5
        self.figure = [list(i) for i in ("""\
 O 
/U\\
 A """).split("\n")]
        Object.__init__(self, x,y)        
    
    def health_bar(self, length):
        self.hp = (int)((self.health/self.healpoints[0])*length)//1
        print(("King's health: " + (str(self.health) if self.health>=0 else str(0)) + " " + Back.LIGHTGREEN_EX + " "*self.hp + Style.RESET_ALL + Back.LIGHTWHITE_EX + " "*(length-self.hp) + Style.RESET_ALL).center(WIDTH))
        print()
    
    def moveup(self, game):
        if self.pos.x - 1 >= 0:
            for j in range(len(self.figure[0])):
                if game.screen.grid[self.pos.x - 1][self.pos.y + j] != BGTILE:
                    break
            else:
                self.pos.x -=1

    def movedown(self, game):
        if self.pos.x + len(self.figure)<= HEIGHT:
            for j in range(len(self.figure[0])):
                if game.screen.grid[self.pos.x + len(self.figure)][self.pos.y + j] != BGTILE:
                    break
            else:
                self.pos.x +=1

    def moveleft(self, game):
        if self.pos.y -1 >=0:
            for i in range(len(self.figure[0])):
                if game.screen.grid[self.pos.x + i][self.pos.y -1 ] != BGTILE:
                    break
            else:
                self.pos.y -=1

    def moveright(self, game):
        if self.pos.y + len(self.figure[0])<= WIDTH:
            for i in range(len(self.figure)):
                if game.screen.grid[self.pos.x + i][self.pos.y + len(self.figure[0])] != BGTILE:
                    break
            else:
                self.pos.y +=1

    def attack(self, game):
        self.center_x = self.pos.x + (len(self.figure)-1)//2
        self.centre_y = self.pos.y + (len(self.figure[0])-1)//2
        for building in game.Buildings_list:
            if dist_sq(self.center_x, self.centre_y, building.pos.x + (len(building.figure)-1)//2, building.pos.y + (len(building.figure[0])-1)//2) <= self.range**2:
                building.attacked(self.attack_val)
        for wall in game.walls_arr:
            if dist_sq(self.center_x, self.centre_y, wall.pos.x + (len(wall.figure)-1)//2, wall.pos.y + (len(wall.figure[0])-1)//2) <= self.range**2:
                wall.attacked(self.attack_val)

class Queen(Team):
    healpoints = (500, 200, 100)
    attack_val = 15
    def __init__(self,x,y):
        self.eagle_shot = False
        self.lastMove = 'd'
        self.textureIn = BGCOLOR + Fore.RED
        self.textureOut = BGCOLOR + Fore.RED
        self.health = 500
        self.hitpoints = [500, 200, 100]
        self.range = 8
        self.eagle_range = 16
        self.aoe = 5
        self.eagle_aoe = 9
        self.figure = [list(i) for i in ("""\
/O\\
-|-
/|\\""").split("\n")]
        Object.__init__(self, x,y)        
    
    def health_bar(self, length):
        self.hp = (int)((self.health/self.healpoints[0])*length)//1
        print(("Queen's health: " + (str(self.health) if self.health>=0 else str(0)) + " " + Back.LIGHTGREEN_EX + " "*self.hp + Style.RESET_ALL + Back.LIGHTWHITE_EX + " "*(length-self.hp) + Style.RESET_ALL).center(WIDTH))
        print()
    
    def moveup(self, game):
        if self.pos.x - 1 >= 0:
            for j in range(len(self.figure[0])):
                if game.screen.grid[self.pos.x - 1][self.pos.y + j] != BGTILE:
                    break
            else:
                self.pos.x -=1
                self.lastMove = 'w'

    def movedown(self, game):
        if self.pos.x + len(self.figure)<= HEIGHT:
            for j in range(len(self.figure[0])):
                if game.screen.grid[self.pos.x + len(self.figure)][self.pos.y + j] != BGTILE:
                    break
            else:
                self.pos.x +=1
                self.lastMove = 's'

    def moveleft(self, game):
        if self.pos.y -1 >=0:
            for i in range(len(self.figure[0])):
                if game.screen.grid[self.pos.x + i][self.pos.y -1 ] != BGTILE:
                    break
            else:
                self.pos.y -=1
                self.lastMove = 'a'

    def moveright(self, game):
        if self.pos.y + len(self.figure[0])<= WIDTH:
            for i in range(len(self.figure)):
                if game.screen.grid[self.pos.x + i][self.pos.y + len(self.figure[0])] != BGTILE:
                    break
            else:
                self.pos.y +=1
                self.lastMove = 'd'

    def attack(self, game):
        self.range_center_x = self.pos.x + (len(self.figure)-1)//2
        self.range_center_y = self.pos.y + (len(self.figure[0])-1)//2
        if self.lastMove == 'w':
            self.range_center_x -= self.range
        elif self.lastMove == 's':
            self.range_center_x += self.range
        elif self.lastMove == 'a':
            self.range_center_y -= self.range
        elif self.lastMove == 'd':
            self.range_center_y += self.range

        for building in game.Buildings_list:
            if abs(self.range_center_x - building.pos.x + (len(building.figure)-1)//2) <= self.aoe/2 and abs(self.range_center_y - building.pos.y + (len(building.figure[0])-1)//2) <= self.aoe/2:
                building.attacked(self.attack_val)
        for wall in game.walls_arr:
            if abs(self.range_center_x - wall.pos.x + (len(wall.figure)-1)//2) <= self.aoe/2 and abs(self.range_center_y - wall.pos.y + (len(wall.figure[0])-1)//2) <= self.aoe/2:
                wall.attacked(self.attack_val)

    def eagle_attack_start(self, game):
        self.eagle_shot = True
        self.shotTime = game.tot_time
        self.eagle_range_center_x = self.pos.x + (len(self.figure)-1)//2
        self.eagle_range_center_y = self.pos.y + (len(self.figure[0])-1)//2
        if self.lastMove == 'w':
            self.eagle_range_center_x -= self.eagle_range
        elif self.lastMove == 's':
            self.eagle_range_center_x += self.eagle_range
        elif self.lastMove == 'a':
            self.eagle_range_center_y -= self.eagle_range
        elif self.lastMove == 'd':
            self.eagle_range_center_y += self.eagle_range

    def eagle_attack_end(self, game):
        self.eagle_shot = False
        for building in game.Buildings_list:
            if abs(self.eagle_range_center_x - building.pos.x + (len(building.figure)-1)//2) <= self.eagle_aoe/2 and abs(self.eagle_range_center_y - building.pos.y + (len(building.figure[0])-1)//2) <= self.eagle_aoe/2:
                building.attacked(self.attack_val)
        for wall in game.walls_arr:
            if abs(self.eagle_range_center_x - wall.pos.x + (len(wall.figure)-1)//2) <= self.eagle_aoe/2 and abs(self.eagle_range_center_y - wall.pos.y + (len(wall.figure[0])-1)//2) <= self.eagle_aoe/2:
                wall.attacked(self.attack_val)

class Spell:
    def __init__():
        pass


class Rage(Spell):
    def __init__(self, game):
        Timesteps.BARB_TIMESTEP//=2
        Timesteps.ARCHER_TIMESTEP//=2
        Timesteps.BALLOON_TIMESTEP//=2
        for i in game.troops_dict.values():
            for j in i:
                j.attack_val*=2
        game.player.attack_val*=2
        Spell.__init__()

class Heal(Spell):
    def __init__(self, game):
        for i in game.troops_dict.values():
            for j in i:
                j.health=(1.5*j.health)//1 if (1.5*j.health)//1 < 100 else 100
                j.health = int(j.health)
                x=-1
                for t in j.healpoints:
                    if j.health > t:
                        break
                    else:
                        x+=1
                j.hitstatus = x

        game.player.health = (1.5*game.player.health)//1 if (1.5*game.player.health)//1 < 500 else 500
        game.player.health = int(game.player.health)
        x=-1
        for t in game.player.healpoints:
            if game.player.health > t:
                break
            else:
                x+=1
        game.player.hitstatus = x
        Spell.__init__()
