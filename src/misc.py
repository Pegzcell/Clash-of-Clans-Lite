from src.headers import *

def dist_sq(x,y,x2,y2):
    return (x-x2)**2 + (y-y2)**2
    
def closest_building(x,y,Buildings_list):
    # print(x,y)

    t =[]
    for building in Buildings_list:
        x_target = building.pos.x  + len(building.figure)//2
        y_target = building.pos.y + len(building.figure[0])//2
        # print(building.pos.x, building.pos.y)
        t.append(dist_sq(x,y,x_target, y_target))
    # print("------------")
    # print(t)
    t=np.array(t)
    # print(np.where(t == np.amin(t))[0][0])
    return Buildings_list[np.where(t == np.amin(t))[0][0]]


def closest_troop_(x,y,Troops, Range):
    t = []
    t_objs = []
    for i in range(len(Troops)):
        t.append(0)
        t_objs.append([])
        for j in range(len(Troops[i])):
            if dist_sq(x, y, Troops[i][j].pos.x, Troops[i][j].pos.y) <= Range**2:
                t[i] +=1
                t_objs[i].append(j)
    t=np.array(t)
    p = (np.amax(t), np.where(t == np.amax(t))[0][0], t_objs[np.where(t == np.amax(t))[0][0]])
    # print(p)
    return p

def Cannon_closest_troop(x,y,Troops, Range):
    min = 99999
    min_obj = ''
    for key, val in Troops.items():
        if key != "Balloon":
            for j in range(len(val)):
                dist = dist_sq(x, y, val[j].pos.x, val[j].pos.y)
                if dist < min:
                    min = dist 
                    min_obj = [key,j]
    if min < Range**2:
        min_obj.append(Troops[key])
        return min_obj
    else:
        return -1

def Tower_closest_troop(x,y,Troops, Range):
    min = 99999
    min_obj = ''
    for key, val in Troops.items():
        for j in range(len(val)):
            dist = dist_sq(x, y, val[j].pos.x, val[j].pos.y)
            if dist < min:
                min = dist 
                min_obj = [key,j]
    if min < Range**2:
        min_obj.append(Troops[key])
        return min_obj
    else:
        return -1