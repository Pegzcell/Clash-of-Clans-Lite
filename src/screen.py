from src.headers import *

class Screen:

    #Creates the entire screen for the game

    #constructor function
    def __init__(self, height, width):
        self.rows=height
        self.cols=width
        self.grid=[]
        self.__flag=0

    def setit(self):
        self.grid=[]
        for i in range(self.rows):
            temp=[]
            for j in range(self.cols):
                if i==0 or j==0 or i==self.rows - 1 or j == self.cols -1:
                    temp.append(EDGETILE)
                    continue
                temp.append(BGTILE)
            self.grid.append(temp)
        # self.grid=np.array(self.grid)
        

    #function to print the playing screen
    def printit(self):
            for i in self.grid:
                for j in i:                    
                    # print(Back.LIGHTBLACK_EX +self.grid[i][j] + Back.RESET, end='')
                    print(j,end='')                    
                print()

        

