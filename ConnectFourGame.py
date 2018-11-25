# Jack Jones
from tkinter import *
from time import *

HEIGHT = 1300
WIDTH = 1000
DIAMETER = 100


class myBoard:
    """ provides the Connect 4 7x6 board"""
    turnCount = 0
    def __init__( self, width, height, window):
        self.width = width
        self.height = height
        self.data = [] # this will be the board
        
        for row in range ( self.height):
            boardRow = []
            for col in range( self.width ):
                boardRow += [' ']
            self.data += [boardRow]
        self.gameOver = False
        self.window = window
        self.frame = Frame(window)
        self.frame.pack()
        self.qButton = Button(self.frame, text="Quit Game",command=self.quit)
        self.qButton.pack(side=LEFT)
               
        self.draw = Canvas(window,wid = WIDTH, height = HEIGHT)
        self.draw.bind("<Button-1>",self.mouse)
         
        self.draw.pack()
        self.message = self.draw.create_text(5,710,text="Here we go!", \
                                             anchor="w",font="Courier 20")
        self.message1 = self.draw.create_text(5,730,text="Game on! Click the column you want to place your checker.", \
                                                     anchor="w",font="Courier 20")        
        
       
        
        initialColor = "yellow"
        y = 0
        self.circles = []
        self.colors = []
        for row in range (height):
            x = 0
            cRow = []
            colorRow = []
            for col in range(width):
                cRow += [self.draw.create_oval(x+5,y+5,x+DIAMETER,y+DIAMETER,fill=initialColor)]
                colorRow += [initialColor]
                x += DIAMETER
            self.circles += [cRow]
            self.colors += [colorRow]
            y += DIAMETER 
            
    def mouse(self, event):
        
        if self.gameOver == True:
            return
            
        print("x= %i, y= %i" % (event.x,event.y))
        #row = int(event.y/DIAMETER)
        col = int(event.x/DIAMETER)
        print("col = %i" % (col))
    
        row = self.addMove(col, 'X')
        self.draw.itemconfig(self.circles[row][col],fill="black")
        myMessage = "Setting color of circle (%i,%i) to %s" % (row,col,"black")
        self.draw.itemconfig(self.message,text=myMessage)
        self.window.update()
        if self.winsFor('X') == True:
            print(self)
            print('Player X Wins!')
            self.draw.itemconfig(self.message,text="X Wins")
            self.gameOver = True
                            
        elif self.isFull() == True:
            print(self)
            print('Tie Game!')
            self.gameOver = True
            
        if not self.gameOver:
            col = self.aiPlayer.nextMove(self)
            row = self.addMove(col,'O')
            self.draw.itemconfig(self.circles[row][col],fill="red")
    
            if self.winsFor('O') == True:
                print(self)
                print('Player O Wins!')
                self.draw.itemconfig(self.message,text="O Wins")
                self.gameOver = True
            
            elif self.isFull() == True:
                print(self)
                print('Tie Game!')
                self.gameOver = True
          
        if self.gameOver == True:
            self.draw.itemconfig(self.message1,text="Game Over!")
        return
            
        
        
    
    def playGUI(self,aiPlayer):
        self.aiPlayer = aiPlayer      

        
            
            
    def quit(self):

        self.window.destroy()
        
    def addMove( self, col, ox ):
        
        if self.allowsMove(col):
            for row in range( self.height):
                if self.data[row][col] !=' ':
                    self.data[row-1][col] = ox
                    return row-1
            self.data[self.height-1][col]= ox
            return self.height-1

    def allowsMove( self, col ):
        if 0 <= col < self.width:
            return self.data[0][col] == ' '
        return False
    
    def clear(self):
        for row in range(self.height):
            for col in range(self.width):
                self.data[row][col] = ' '
    
    def delMove( self, col):
        for row in range( self.height):
            if self.data[row][col] != ' ':
                self.data[row][col] = ' '
                return
    
    def isFull( self ):
        for col in range(self.width):
            if self.allowsMove(col):
                return False
        return True

    def winsFor( self, ox ):
        # check for horizontal wins
        for row in range(0,self.height):
            for col in range(0,self.width-3):
                if self.data[row][col] == ox and \
                   self.data[row][col+1] == ox and \
                   self.data[row][col+2] == ox and \
                   self.data[row][col+3] == ox:
                    return True
        for row in range(0,self.height-3):
            for col in range(0,self.width):        
                if self.data[row][col] == ox and \
                   self.data[row+1][col] == ox and \
                   self.data[row+2][col] == ox and \
                   self.data[row+3][col] == ox:
                    return True
        for row in range(3,self.height):
            for col in range(0,self.width-3):
                if self.data[row][col] == ox and \
                   self.data[row-1][col+1] == ox and \
                   self.data[row-2][col+2] == ox and \
                   self.data[row-3][col+3] == ox:
                    return True
        for row in range(0,self.height-3):
            for col in range(0,self.width-3):
                if self.data[row][col] == ox and \
                   self.data[row+1][col+1] == ox and \
                   self.data[row+2][col+2] == ox and \
                   self.data[row+3][col+3] == ox:
                    return True
        return False
    
    def __repr__ (self):
            #print out rows and cols
            s= '' # the string to return
            for row in range ( self.height ):
                s += '|' # add the separator character
                for col in range( self.width ):
                    s += self.data[row][col] + '|'
                s += '\n'
            
            s += '--'*self.width + '\n'
            
            for col in range( self.width ):
                s += ' ' + str(col % 10)
            s += '\n'
            
            return s
                #print out the horizontal separator          
     
    
    def hostGame(self):
        runGame = True
        turnCount = 0
        print("Game on!Player X you go first")
        while runGame == True:
            
            if turnCount % 2 == 0:
                print(self)
                print("Turn Number:",turnCount)
                print("Player X's turn")
                self.getMove('X')
                turnCount += 1
                if self.winsFor('X') == True:
                    print(self)
                    print('Player X Wins!')
                    break
                if self.isFull() == True:
                    print('Tie Game!')
                    break
                 
            if turnCount % 2 != 0:
                print(self)
                print("Turn Number:",turnCount)
                print("Player O's turn")
                self.getMove('O')
                turnCount += 1
                if self.winsFor('O') == True:
                    print(self)
                    print('Player O Wins!')
                    break
                if self.isFull() == True:
                    print(self)
                    print('Tie Game!')
                    break
        
    def playGameWith(self, aiPlayer):
        runGame = True
        turnCount = 0
        print("Game on!Player X you go first")
        while runGame == True:
                    
            if turnCount % 2 == 0:
                print(self)
                print("Turn Number:",turnCount)
                print("Player X's turn")
                self.getMove('X')
                turnCount += 1
                if self.winsFor('X') == True:
                    print(self)
                    print('Player X Wins!')
                    break
                if self.isFull() == True:
                    print('Tie Game!')
                    break
                
                
            if turnCount % 2 != 0:
                print(self)
                print("Turn Number:",turnCount)
                print("Player O's turn")
                oMove = aiPlayer.nextMove(self)
                self.addMove(oMove,'O')
                turnCount += 1
                if self.winsFor('O') == True:
                    print(self)
                    print('Player O Wins!')
                    break
                if self.isFull() == True:
                    print(self)
                    print('Tie Game!')
                    break        



class Player:
    
    def __init__(self, ox, tbt, ply):
        
        self.ox = ox
        self.tbt = tbt
        self.ply = ply
    
    def scoreFor(self,b,ox,ply):
        Scoredlist = []
        for col in range(b.width):
            if b.allowsMove(col) == True:
                b.addMove(col,ox)
                if b.winsFor(ox)== True:
                    Scoredlist += [100]
                elif ply == 1:
                    Scoredlist += [50]
                else:
                    if ox == "X":
                        opox = "O"
                    else:
                        opox = "X"
                    opScoredList = max(self.scoreFor(b,opox,ply-1))
                    Scoredlist += [100 - opScoredList]
                b.delMove(col)
            
            else:
                Scoredlist += [-1]
            
        return Scoredlist
        
    def nextMove(self,b):
        scoresList = self.scoreFor(b,self.ox,self.ply)
        biggest = max(scoresList)
        for i in range(len(scoresList)):
            if scoresList[i] == biggest:
                return i 

    

root = Tk()
root.title("Connect Four")
me = myBoard(7,6,root)
aiPlayer= Player('O','LEFT',3)
me.playGUI(aiPlayer)
root.mainloop()

