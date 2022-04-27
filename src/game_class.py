
from cgitb import reset
from src.headers import *
from src.screen import *
from src.objects import *

class Game:
    def __init__(self, scene):
        self.level = 0

        self.filename = ""
        self.inputs = []

        self.state = ON

        self.tot_time = 0
        self.start_time = 0

        self.barb_frame = 0
        self.archer_frame = 0
        self.balloon_frame = 0

        self.cannon_frame = 0
        self.cannon_recoil_frame = 0

        self.tower_frame = 0
        self.tower_recoil_frame = 0

        self.screen = scene

        self.playerType =''
        self.reset()
    
    Troops_ids = {1: ("Barb", Barbarian), 2: ("Archer", Archer), 3: ("Balloon", Balloon)}
    Spawn_points = {1 : (2, WIDTH - 10), 2: (HEIGHT - 4, WIDTH - 10), 3 : (HEIGHT - 3, 8)}
    
    # class Limits:
    #     BARB = 6
    #     ARCHER = 6
    #     BALLOON = 6

    def reset(self):
        # Timesteps.BARB_TIMESTEP = 1.0 * 10e3
        # Timesteps.ARCHER_TIMESTEP = 0.5 * Timesteps.BARB_TIMESTEP
        # Timesteps.BALLOON_TIMESTEP = 0.5 * Timesteps.BARB_TIMESTEP
        # Timesteps.CANNON_TIMESTEP = 1.5 * 10e3
        # Timesteps. CANNON_RECOIL_TIMESTEP = Timesteps.CANNON_TIMESTEP/5
        # Timesteps. TOWER_TIMESTEP = 1.5 * 10e3
        # Timesteps. TOWER_RECOIL_TIMESTEP = Timesteps.TOWER_TIMESTEP/5
        self.troop_limits = {1:TROOP_MAX, 2:TROOP_MAX, 3:TROOP_MAX}

        self.townHall_obj = ''
        self.huts_arr = []
        self.cannons_arr =[]
        self.towers_arr =[]
        self.Buildings_list = []
        self.Defensive_buildings_list = []

        self.walls_arr = []

        self.player = ''
        self.troops_dict = {
            self.Troops_ids[1][0] : [],
            self.Troops_ids[2][0] : [],
            self.Troops_ids[3][0] : []
        }

    def wall_enclosure(self, x_min, y_min, x_max, y_max):
        for i in range(x_min,x_max):
            self.walls_arr.append(Wall(i, y_min))
            self.walls_arr.append(Wall(i, y_max))

        for j in range(y_min, y_max):
            self.walls_arr.append(Wall(x_min, j))
            self.walls_arr.append(Wall(x_max, j))

        self.walls_arr.append(Wall(x_max, y_max))
    

    def remove_destroyed(self):
        # buildings
        i=0
        while (i < len(self.Buildings_list)):
            if self.Buildings_list[i].destroyed:
                self.Buildings_list = np.delete(self.Buildings_list, i)
            else:
                i+=1
        # defensive buildings
        i=0
        while (i < len(self.Defensive_buildings_list)):
            if self.Defensive_buildings_list[i].destroyed:
                self.Defensive_buildings_list = np.delete(self.Defensive_buildings_list, i)
            else:
                i+=1

        ##cannons
        i = 0
        while (i < len(self.cannons_arr)):
            if self.cannons_arr[i].destroyed:
                self.cannons_arr.pop(i)
            else:
                i+=1

        ##towers
        i = 0
        while (i < len(self.towers_arr)):
            if self.towers_arr[i].destroyed:
                self.towers_arr.pop(i)
            else:
                i+=1

        ##huts
        i = 0
        while (i < len(self.huts_arr)):
            if self.huts_arr[i].destroyed:
                self.huts_arr.pop(i)
            else:
                i+=1

        # ##townhall
        # if self.townHall_obj.destroyed:
        #     del self.townHall_obj

        # walls
        i = 0
        while (i < len(self.walls_arr)):
            if self.walls_arr[i].destroyed:
                self.walls_arr.pop(i)
            else:
                i+=1

        # troops
        for i in self.troops_dict.values():
            j=0
            while (j < len(i)):
                if i[j].destroyed:
                    i.pop(j)
                else:
                    j+=1

    def move(self):
        # Barbarians
        if self.barb_frame < self.tot_time//Timesteps.BARB_TIMESTEP:
            self.barb_frame+=1
            for barb_obj in self.troops_dict["Barb"]:
                barb_obj.move(self)        

        # Archers
        if self.archer_frame < self.tot_time//Timesteps.ARCHER_TIMESTEP:
            self.archer_frame+=1
            for archer_obj in self.troops_dict["Archer"]:
                archer_obj.move(self)    

        # Ballons
        if self.balloon_frame < self.tot_time//Timesteps.BALLOON_TIMESTEP:
            self.balloon_frame+=1
            for balloon_obj in self.troops_dict["Balloon"]:
                balloon_obj.move(self)           

        # Cannons
        if self.cannon_frame < self.tot_time//Timesteps.CANNON_TIMESTEP:
            self.cannon_frame+=1
            for cannon_obj in self.cannons_arr:
                cannon_obj.shoot(self)

        # Cannon_blink
        if Timesteps.CANNON_RECOIL_TIMESTEP < self.tot_time % Timesteps.CANNON_TIMESTEP:
            self.cannon_recoil_frame+=1
            for cannon_obj in self.cannons_arr:
                cannon_obj.justshot = False       

        # Towers
        if self.tower_frame < self.tot_time//Timesteps.TOWER_TIMESTEP:
            self.tower_frame+=1
            for tower_obj in self.towers_arr:
                tower_obj.shoot(self)

        # Tower_blink
        if Timesteps.CANNON_RECOIL_TIMESTEP < self.tot_time % Timesteps.CANNON_TIMESTEP:
            self.cannon_recoil_frame+=1
            for tower_obj in self.towers_arr:
                tower_obj.justshot = False       

        # Archer Queen’s Eagle Arrow
        if self.playerType == 'a' and self.player.eagle_shot:
            if Timesteps.EAGLE_TIMESTEP < self.tot_time - self.player.shotTime:
                self.player.eagle_attack_end(self)


    def add(self):
        for wall_obj in self.walls_arr:
            if not wall_obj.destroyed:
                wall_obj.add_to_scene(self.screen)

        for building_obj in self.Buildings_list:
            if not building_obj.destroyed:
                building_obj.add_to_scene(self.screen)

        
        for i in self.troops_dict.values():
            for barb_obj in i:
                if not barb_obj.destroyed:
                    barb_obj.add_to_scene(self.screen)

        if not self.player.destroyed:
            self.player.add_to_scene(self.screen)

    def leveller(self):
        self.reset()

        # TownHall
        self.townHall_obj = TownHall()
        self.Buildings_list = np.array([self.townHall_obj])

        # Huts
        self.huts_arr.append(Hut(18,4))
        self.huts_arr.append(Hut(18,14))
        self.huts_arr.append(Hut(18,24))
        self.huts_arr.append(Hut(18,72))
        self.huts_arr.append(Hut(18,82))
        self.huts_arr.append(Hut(18,92))    
        self.Buildings_list = np.append(self.Buildings_list, self.huts_arr)

        # Walls
        x_min = self.townHall_obj.pos.x - 2
        y_min = self.townHall_obj.pos.y - 2
        x_max = self.townHall_obj.pos.x + len(self.townHall_obj.figure) + 2
        y_max = self.townHall_obj.pos.y + len(self.townHall_obj.figure[0]) + 2

        self.wall_enclosure(x_min, y_min, x_max, y_max)
        self.wall_enclosure(1, 1, 6, 11)
        self.wall_enclosure(1, WIDTH - 12, 6, WIDTH - 2)
        self.wall_enclosure(HEIGHT - 7, 1, HEIGHT - 2, 11)
        self.wall_enclosure(HEIGHT - 7, WIDTH - 12, HEIGHT - 2, WIDTH - 2)

        # Vertical walls
        for i in range(1, HEIGHT -1):
            for j in range(WIDTH//3 - 3, WIDTH//3 + 3):
                self.walls_arr.append(Wall(i, j))

        for i in range(1, HEIGHT -1):
            for j in range((WIDTH*2)//3 - 3, (WIDTH*2)//3 + 3):
                self.walls_arr.append(Wall(i, j))

        # Horizontal Walls
        for i in range(HEIGHT//3 - 2, HEIGHT//3 +2):
            for j in range(1, WIDTH//3 - 3):
                self.walls_arr.append(Wall(i, j))         
            
        for i in range((HEIGHT*2)//3 - 2, (HEIGHT*2)//3 +2):
            for j in range(1, WIDTH//3 - 3):
                self.walls_arr.append(Wall(i, j))    

        for i in range(HEIGHT//3 - 2, HEIGHT//3 + 2):
            for j in range((WIDTH*2)//3 + 3, WIDTH - 1):
                self.walls_arr.append(Wall(i, j)) 

        for i in range((HEIGHT*2)//3 - 2, (HEIGHT*2)//3 + 2):
            for j in range((WIDTH*2)//3 + 3, WIDTH - 1):
                self.walls_arr.append(Wall(i, j)) 

        # Player
        self.player = King(3, 3) if self.playerType == 'k' else Queen(3,3)

        # Cannons and Towers
        if self.level >= 1:
            self.cannons_arr.append(Cannon(4,48))
            self.cannons_arr.append(Cannon(36,48))
            self.towers_arr.append(Tower(10,48))
            self.towers_arr.append(Tower(30,48))

        if self.level >= 2:
            self.cannons_arr.append(Cannon(4,27))
            self.cannons_arr.append(Cannon(36,69))
            self.towers_arr.append(Tower(4,69))
            self.towers_arr.append(Tower(36,27))

        if self.level == 3:
            self.cannons_arr.append(Cannon(10,80))
            self.cannons_arr.append(Cannon(28,15))
            self.towers_arr.append(Tower(10,15))
            self.towers_arr.append(Tower(28,80))

        self.Buildings_list = np.append(self.Buildings_list, self.cannons_arr)
        self.Defensive_buildings_list = np.append(self.Defensive_buildings_list, self.cannons_arr)   
        self.Buildings_list = np.append(self.Buildings_list, self.towers_arr)
        self.Defensive_buildings_list = np.append(self.Defensive_buildings_list, self.towers_arr)

    def loss(self):
        print(Back.RED + "Defeat".center(WIDTH) + Style.RESET_ALL)

    def victory(self):
        print(Back.GREEN + "Victory".center(WIDTH) + Style.RESET_ALL)
