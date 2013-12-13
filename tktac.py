FOO = 43
BAR = 32

from tkinter import *
from tkinter.filedialog import *
import ast
import sys

sticker = [NW, N, NE, W, None, E, SW, S, SE]
markers = ["X","O"]
players = ["Player X", "Player O"]

map = list()
for i in [0,0,0,3,3,3,6,6,6]: map.extend(range(i,i+3))
map *= 3

def which_board(x): return (3 * (int((x % 81) / 27)) + (int((x % 9)/3)))

def is_win(b):
    for mark in markers:
        if [mark]*3 in [[b[0],b[1],b[2]],[b[0],b[3],b[6]],[b[0],b[4],b[8]],[b[1],b[4],b[7]],[b[2],b[5],b[8]],[b[2],b[4],b[6]],[b[3],b[4],b[5]],[b[6],b[7],b[8]]]:
            return mark
    return ""


class Game:
    def __init__(self, master=None):
        self.master = master
        self.master.title("Super TkTacToe ~ Peter Duchovni")
        self.top = Toplevel(self.master)
        self.top.title("TkTacToe Game")

        quitbutton = Button(self.master, font="standard 14", text="Quit", anchor=W, command=end)
        quitbutton.pack()
        new_game = Button(self.master, font="standard 14", text="New Game", anchor=W, command=self.new)
        new_game.pack()
        load_save = Button(self.master, font="standard 14", text="Load Game", anchor=W, command=self.load)
        load_save.pack()
        save_game = Button(self.master, font="standard 14", text="Save Game", anchor=W, command=self.save)
        save_game.pack()
        undo_move = Button(self.master, font="standard 14", text="Undo Move", anchor=W, command=self.undo)
        undo_move.pack()
        self.p0 = StringVar()
        self.p0.set(players[0])
        p0en = Entry(self.master, font="standard 14", textvar=self.p0)
        p0en.pack()
        self.p1 = StringVar()
        self.p1.set(players[1])
        p1en = Entry(self.master, font="standard 14", textvar=self.p1)
        p1en.pack()

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
        self.clear()
        self.play()

    def new(self):
        self.clear()
        self.history = list()
        self.play()

    def undo(self):
        if len(self.history) != 0:
            self.history.pop()
            self.clear()
            self.play()

    def play(self):
        self.player = 0
        self.histmove = iter(self.history)
        self.data = [""]*81
        self.boardstate = [""]*9
        self.gamestate = [""]
        self.space = range(81)
        self.m = IntVar()
        self.buttons = [0]*81
        self.draw()

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

    def draw(self):
        self.main_frame = Frame(self.top, bg="Black")
        self.main_frame.pack()

        self.status = StringVar()
        self.statusbar = Label(self.top, textvar=self.status, bd=1, anchor=W, font="systemfixed 14")
        self.statusbar.pack()

        self.sub_frames = [0]*9
        self.board_frames = [0]*9

        for i in range(9):
            self.sub_frames[i] = Frame(self.main_frame,bg="Black")
            self.sub_frames[i].grid(row = int(i/3), column = int(i%3), padx = 2, pady = 2, sticky = sticker[i])
        for i in range(81):
            self.buttons[i] = Button(self.sub_frames[3*int(i/27) + int((i%9)/3)],
                                     height=2, width=2, command = ( lambda i = i: self.press(i)),
                                     text="", font="systemfixed 14", state=ACTIVE, relief="raised",
                                     activeforeground="Black", disabledforeground="Black"
                                    )
            self.buttons[i].grid(padx=1, pady=1, row = int((i/9)%3), column = int(i % 3))



def end():
    root.destroy()
    root.quit()
    sys.exit(0)

root = Tk()
app = Game(root)
root.mainloop()
