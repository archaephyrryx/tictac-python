# Import from libraries
from tkinter import *
from tkinter.filedialog import *
import ast
import sys

# Macros
WIDTH = 43
HEIGHT = 32
FONT= 'standard 14'
#attachment points for metabord frames
sticker = [NW, N, NE, W, None, E, SW, S, SE]
# Marks and names of the players
markers = ["X","O"]
players = ["Player X", "Player O"]

# x-coordinate ordered triples necessary and sufficient (up to ycor) for win vector
xcor = [(a, (a+c)/2, c) for c in range((a%2),3,2) for a in range(0,3)]
# y-coordinate orderede triples necessary and sufficient (up to xcor) for win vector
ycor = [(a, (a+c)/2, c) for c in range((a%2),3,2) for a in [0,1]]
# Tuple of 3-tuples representing linear coordinates of win vectors
vect = tuple(tuple(a + 3*b for a, b in zip(trip_x, trip_y)) for trip_x, trip_y in zip(xcor, ycor))

# Subboard class
class Subboard(index):
    def __init__(self):
	self.data = [0]*9

    def win(self): # Determines the identity of the winning player
	for i,j,k in tuple(map(lambda x: map(lambda y: self.data[y], x), vect)):
	    if i * (i + j + k) == 3: # Only true if all are equal, nonzero
		return i # The owner of the vector
	return 0 # Unclaimed

    def countOpen(self): # Number of unfilled squares
	count = 0
	for i in range(0,9):
	    if (board[i] == 0):
		count += 1
	return count

    def isUnclaimed(self): # boolean for claimed (won/unwon)
	return (self.win() == 0)

    def isUnfilled(self): # boolean for filled (complete/incomplete)
	return (self.countOpen() == 0)

    # class method isOpen():
    # Returns a boolean value indicating whether the board can be played on,
    # forced or unforced, determined by taking the logical AND operation of its
    # isUnclaimed() value and isUnfilled() value.
    def isOpen(self):
	return (self.isUnclaimed() and self.isUnfilled())

    # class method allValid():
    # Returns a list containing the universal indices of all positions in which
    # moves can be made, regardless of whether the subboard itself is valid for
    # any move.
    def allValid(self):
	return map(lambda i: 9*index + i, filter(lambda i: self.data[i] == 0, range(9)))

    def move(self, pos, newstate):
	if self.isOpen:
	    if pos in self.allValid():
		self.data[pos] = newstate
		return True
	    else:
		return False
		


    
# Full boardstate class
class State:
    def __init__(self):
	self.data = [Subboard(i) for i in range(9)] # Array of subboards
	self.history = list()
	self.hasMoved = False
 
    def win(self): # Determines the identity of the winning player
	for i,j,k in tuple(map(lambda x: map(lambda y: self.data,[y], x), vect)):
	    if i * (i + j + k) == 3: # Only true if all are equal, nonzero
		return i # The owner of the vector
	return 0 # Unclaimed
   
    def lastMove(self):
	return self.history[-1]
    
    def allOpen(self):
	return filter(lamdba i: self.data[i].isOpen(), range(9))

    def subStates(self):
	return [a.win() for a in self.data]

    def allValid(self):
	if self.hasMoved():
	    force = self.lastMove()
	    force %= 9

	    if self.data[force].isOpen():
		return self.data[force].allValid()

	    else: 
		return [self.data[b].allValid() for self.allOpen[b] for b in range(9)]
	else:
	    return range(81)


    def isValid(self, move):
	return (move in self.allValid)

    def move(self, pos, newstate):
	if not self.hasMoved:
	    self.hasMoved = True
	if isValid(self, i):
	    
	
##TKINTER##

class SubFrame(index):
    def __init__(self, master):
	self.index = index
	self.master = master
	self.active = True
	self.buttons = dict()
	self.draw()

    def draw(self):
        self.frame = Frame(self.master, bg="Black")
        for i in range(9):
            self.buttons[9*index + i] = Button(self.frame, height=2, width=2, text="",
					       font="systemfixed 14", state=ACTIVE,
					       command = ( lambda i = i: self.press(i)),
					       relief="raised", activeforeground="Black",
					       disabledforeground="Black")
            self.buttons[i].grid(padx=1, pady=1, row = int((i/9)%3), column = int(i % 3))
    
    def forbid(self):
	for i in range(9):
	    self.buttons[9*index + i]["state"] = DISABLED
	    self.buttons[9*index + i]["relief"] = "sunken"
	    self.buttons[9*index + i]["bg"] = "Dark Gray"
    
    def permit(self):
	for i in range(9):
	    self.buttons[9*index + i]["state"] = ACTIVE
	    self.buttons[9*index + i]["relief"] = "raised"
	    self.buttons[9*index + i]["bg"] = "White"
    
    def disable(self):
	self.active = False
        self.frame.grid_forget()
	for i in range(9):
	    self.buttons[9*index + i].destroy()
	



class Application:
    def __init__(self, master=None):
        self.master = master
        self.master.title("Super TkTacToe ~ Python GUI by Peter Duchovni")
        self.top = Toplevel(self.master)
        self.top.title("TkTacToe Game")
	self.globalButtons()
	self.playerLabels()

    def playerLabels(self):
        self.playerOneName = StringVar()
        self.playerOneName.set(players[0])
        self.playerOneNameEntry = Entry(self.master, font=FONT, textvar=self.playerOneName)

        self.playerTwoName = StringVar()
        self.playerTwoName.set(players[1])
        self.playerTwoNameEntry = Entry(self.master, font=FONT, textvar=self.playerTwoName)

        self.playerOneNameEntry.pack()
        self.playerTwoNameEntry.pack()


    def globalButtons(self):
	buttonQuitAll  = Button(self.master, font=FONT, text="Quit All" , anchor=W, command=self.end)
	buttonNewGame  = Button(self.master, font=FONT, text="New Game" , anchor=W, command=self.new)
	buttonLoadGame = Button(self.master, font=FONT, text="Load Game", anchor=W, command=self.load)
	buttonSaveGame = Button(self.master, font=FONT, text="Save Game", anchor=W, command=self.save)
	buttonUndoMove = Button(self.master, font=FONT, text="Undo Move", anchor=W, command=self.undo)

	buttonQuitAll.pack()
	buttonNewGame.pack()
	buttonLoadGame.pack()
	buttonSaveGame.pack()
        buttonUndoMove.pack()

    def save(self):
        savefile = asksaveasfilename(title="Save your game:")
        s = open(savefile,'w')
        s.write(str(self.history))
        s.close()

    def load(self):
        loadfile = askopenfilename(title="Open a savegame file:")
        l = open(loadfile,'r')
        rawhistory = l.read()
        l.close()
        self.history = ast.literal_eval(rawhistory)

    def new(self):
    def process(self):
    def press(self,i):
        if self.player >= len(self.history):
            self.history.append(i)
        self.m.set(i)
        self.data[self.m.get()] = markers[self.player % 2]

    def gameFrame(self):
    def end(self):


class GameWindow(master):
    def __init__(self):



class Game:
    def __init__(self):
    def loadFrom(self, init_state):
    def run(self):
    def undo(self):
    def restart(self):

def validate(history):

