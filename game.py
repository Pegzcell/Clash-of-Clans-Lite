from src.headers import *
from src.game_class import *
from src.input import *

game = Game(Screen(HEIGHT, WIDTH))
input_char = Get()   


def troops_init(index):
    spawn_point = index%3 + 1
    troop_id = math.ceil(index/3)
    if game.troop_limits[troop_id] == 0:
        return
    game.troop_limits[troop_id] -= 1
    game.troops_dict[Game.Troops_ids[troop_id][0]].append(Game.Troops_ids[troop_id][1](Game.Spawn_points[spawn_point][0],Game.Spawn_points[spawn_point][1]))

def initit():
    init(autoreset=True)
    os.system("clear")
    game.start_time = ((time.time()*10e3)//1)%10e7
    game.tot_time = ((time.time()*10e3)//1)%10e7 - game.start_time
    print(Back.BLACK + "COC Lite".center(WIDTH) + Style.RESET_ALL)
    playerChooser = [
        "Choose Player",
        "K for King" + " (Health-" + str(King.healpoints[0]) + ", Attack-" + str(King.attack_val) + ")",
        "A for Archer Queen" + " (Health-" + str(Queen.healpoints[0]) + ", Attack-" + str(Queen.attack_val) + ")", 
        ""         
    ]
    print("\n".join(line.center(WIDTH) for line in playerChooser))
    pt = input()
    while pt not in 'kaKA':
        pt = input("Incorrect input. Try again \"K/A\"".center(WIDTH))
    game.playerType = pt.lower()
    game.inputs.append(pt)
    reposition_cursor(1 ,0)
    for i in range(SCREEN):
        print(" "*WIDTH)

def reposition_cursor(x,y):
    print("\033[%d;%dH" % (x, y))

def handle_inputs():
    ch = input_to(input_char)
    game.inputs.append(ch)

    if not ch:
        return

    # quit
    if ch.lower() == 'q':
        reposition_cursor(SCREEN, 0)
        wrapit()
    
    # player
    if not game.player.destroyed:
        if ch.lower() == 'w':
            game.player.moveup(game)    
        elif ch.lower() == 'a':
            game.player.moveleft(game)  
        elif ch.lower() == 's':
            game.player.movedown(game)  
        elif ch.lower() == 'd':
            game.player.moveright(game)
        elif ch == ' ':
            game.player.attack(game)
        elif ch == 'e' and game.playerType == 'a':
            game.player.eagle_attack_start(game)

    # troops
    if ch.isdigit() and int(ch) in range(1,10):
        troops_init(int(ch))

    # spells
    elif ch.lower() =='r':
        r = Rage(game)
    elif ch.lower() =='h':
        h = Heal(game)

def update():
    reposition_cursor(1,0)
    print("Time: ", int(game.tot_time//10e3))
    print("Level: ", game.level)
    print("".center(20) + "Left".center(20) + "Active".center(20) + "Dead".center(20))
    print("Barbarians [^]: ".ljust(20) + str(game.troop_limits[1]).center(20) + str(len(game.troops_dict["Barb"])).center(20) + str(TROOP_MAX - game.troop_limits[1]- len(game.troops_dict["Barb"])).center(20))
    print("Archers [*]: ".ljust(20) + str(game.troop_limits[2]).center(20) + str(len(game.troops_dict["Archer"])).center(20) + str(TROOP_MAX - game.troop_limits[2]- len(game.troops_dict["Archer"])).center(20))  
    print("Balloons [!]: ".ljust(20) + str(game.troop_limits[3]).center(20) + str(len(game.troops_dict["Balloon"])).center(20) + str(TROOP_MAX - game.troop_limits[3]- len(game.troops_dict["Balloon"])).center(20))
    game.screen.setit()
    game.remove_destroyed()
    game.move()
    game.add()
    game.screen.printit()
    game.player.health_bar(40)
    # for i in game.cannons_arr:
    #     print(i,":",i.shooting if i.shooting>=0 else 'x',":", 'T' if i.justshot else '')
    

def wrapit():
    game.filename = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
    
    f = open("replays/"+game.filename,"w")
    for i in game.inputs:
        f.write(str(i)+"\n")
    f.close()
    exit(0)
    

initit()

# game.level =2
while game.level !=3: 
    game.level+=1
    game.leveller()
    while game.state == ON:
        game.tot_time = ((time.time()*10e3)//1)%10e7 - game.start_time
        handle_inputs()
        update()
        if (len(game.Buildings_list) == 0):
            break

        if (game.troop_limits[1] == 0 and game.troop_limits[2] == 0 and game.troop_limits[3] == 0 and game.player.destroyed):
            for i in game.troops_dict.values():
                if len(i) != 0:
                    break
            else:
                game.state = LOSS
                break
    if game.state == LOSS:
        game.loss()
        break
else:
    game.state = VICTORY
    game.victory()

wrapit()