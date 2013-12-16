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

class Frame(index):
    def __init__(self, master):
	self.index = index
	self.master = master
	self.active = True
	self.buttons = dict()
	self.draw()

    def draw(self):
        self.frame = Frame(self.master, bg="Black")
        for i in range(9):
            self.buttons[9*index + i] = Button(self.frame,
                                     height=2, width=2, command = ( lambda i = i: self.press(i)),
                                     text="", font="systemfixed 14", state=ACTIVE, relief="raised",
                                     activeforeground="Black", disabledforeground="Black"
                                    )
            self.buttons[i].grid(padx=1, pady=1, row = int((i/9)%3), column = int(i % 3))






class Game:
    def __init__(self, master=None):
        self.master = master
        self.master.title("Super TkTacToe ~ Python GUI by Peter Duchovni")
        self.top = Toplevel(self.master)
        self.top.title("TkTacToe Game")
	self.inPlay = False

	self.globalButtons()

        self.playerOneName = StringVar()
        self.playerOneName.set(players[0])
        self.playerOneNameEntry = Entry(self.master, font=FONT, textvar=self.playerOneName)
        self.playerOneNameEntry.pack()

        self.playerTwoName = StringVar()
        self.playerTwoName.set(players[1])
        self.playerTwoNameEntry = Entry(self.master, font=FONT, textvar=self.playerTwoName)
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


    def clear(self):
        try:
            self.main_frame.destroy()
            self.main_frame.forget()
            self.statusbar.destroy()
            self.statusbar.forget()
        except AttributeError:
            pass

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
	if self.inPlay:
	    self.clear()
        self.play()

    def new(self):
	if self.inPlay:
	    self.clear()
        self.play()

    def undo(self):
        if len(self.history) != 0:
            last = self.history.pop()
            self.clear()
            self.play()

    def play(self):
        self.inPlay = True
        self.player = 0
        self.state = State()
        self.m = IntVar()
        self.gameButtons()

        while True: 
            pl0 = self.p0.get()
            pl1 = self.p1.get()
            if self.gamestate[0] != "":
                self.status.set("%s has won." % ([pl0,pl1][ markers.index(self.gamestate[0])]))
                for i in range(81): self.buttons[i]["state"] = DISABLED
            elif not ("" in [ self.boardstate[x] for x in range(9) ]):
                self.status.set("Tie.")
                for i in range(81): self.buttons[i]["state"] = DISABLED
            else:
                self.status.set("%s to move." % ([pl0,pl1][ self.player % 2 ]))
            try:
                self.press(next(self.histmove))
            except StopIteration:
                self.master.wait_variable(self.m)
            self.process()
            self.player += 1


    def process(self):
        self.mbn = which_board(self.m.get())
        self.mb = list(filter(lambda x: which_board(x) == self.mbn, range(81)))
        self.mbd = [ self.data[x] for x in self.mb ]
        win = is_win(self.mbd)
        if (win == "") and (not ("" in self.mbd)):
                self.boardstate[self.mbn] = "T"
        else:
            self.boardstate[self.mbn] = win
        self.gamestate[0] = is_win(self.boardstate)
        
        for i in [x for x in range(9) if self.boardstate[x] != ""]:
            if len(self.sub_frames[i].grid_slaves()) == 9:
                for button in self.sub_frames[i].grid_slaves():
                    button.grid_forget()
                    button.destroy()
                    self.buttons[self.buttons.index(button)] = False
                if self.boardstate[i] == "T":
                    Label(self.sub_frames[i], text="", font="systemfixed 72").grid(row=0, column=0, ipadx=FOO, ipady=BAR, sticky="nesw")
                else:
                    Label(self.sub_frames[i], text=self.boardstate[i], font="systemfixed 72").grid(row=0, column=0, ipadx=FOO, ipady = BAR, sticky="nesw")
        self.newspace = [ x for x in range(81) if which_board(x) == map[self.m.get()]]
        if (not ("" in [self.data[x] for x in self.newspace])) or (not ("" in [self.boardstate[which_board(x)] for x in self.newspace])):
            self.newspace = range(81)
        self.newspace = list(filter(lambda x: self.data[x] == "" and self.boardstate[which_board(x)] == "", self.newspace))
        self.space = self.newspace
        for i in [x for x in range(81) if self.buttons[x]]:
            self.buttons[i]["text"] = self.data[i]
            if i in self.space:
                self.buttons[i]["state"] = ACTIVE
                self.buttons[i]["relief"] = "raised"
                self.buttons[i]["bg"] = "White"
            else:
                self.buttons[i]["state"] = DISABLED
                self.buttons[i]["relief"] = "sunken"
                self.buttons[i]["bg"] = "Dark Gray"
        self.top.update()
    

    def press(self,i):
        if self.player >= len(self.history):
            self.history.append(i)
        self.m.set(i)
        self.data[self.m.get()] = markers[self.player % 2]

    def gameFrame(self):
        self.main_frame = Frame(self.top, bg="Black")
        self.main_frame.pack()

        self.status = StringVar()
        self.statusbar = Label(self.top, textvar=self.status, bd=1, anchor=W, font="systemfixed 14")
        self.statusbar.pack()

        for i in range(9):
            self.sub_frames[i] = Frame(self.main_frame,bg="Black")
            self.sub_frames[i].grid(row = int(i/3), column = int(i%3), padx = 2, pady = 2, sticky = sticker[i])






    def end(self):
	root.destroy()
	root.quit()
	sys.exit(0)

root = Tk()
app = Game(root)
root.mainloop()
