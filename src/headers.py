import time, datetime
import math
import numpy as np
import os
import sys
from colorama import init, Fore, Back, Style
import random
import os

ON =0
VICTORY=1
LOSS=2

HEIGHT=40
WIDTH=100
SCREEN = 50

TOT_HUTS=5

HEALTH_COLOR = (Back.LIGHTGREEN_EX, Back.LIGHTYELLOW_EX, Back.LIGHTRED_EX)

class Timesteps:
    BARB_TIMESTEP = 1.0 * 10e3
    ARCHER_TIMESTEP = 0.5 * BARB_TIMESTEP
    BALLOON_TIMESTEP = 0.5 * BARB_TIMESTEP
    CANNON_TIMESTEP = 1.5 * 10e3
    CANNON_RECOIL_TIMESTEP = CANNON_TIMESTEP/5
    TOWER_TIMESTEP = 1.5 * 10e3
    TOWER_RECOIL_TIMESTEP = TOWER_TIMESTEP/5
    EAGLE_TIMESTEP = 1.0 * 10e3

TROOP_MAX = 6
# EDGETILE_HEIGHT = 1
# EDGETILE_WIDTH =1


def reposition_cursor(x,y):
    print("\033[%d;%dH" % (x, y))

#OBJECTS:

#BG
BGCOLOR = Back.WHITE
FGCOLOR = Fore.BLACK

#EDGE
BGTILE = BGCOLOR + " "
EDGETILE = Back.BLACK + Fore.BLACK + "."
