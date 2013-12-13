boardref = (["top left", "top middle", "top right"] +
	    ["center left", "center", "center right"] +
            ["bottom left", "bottom middle", "bottom right"])

map = list()
for i in [0,0,0,3,3,3,6,6,6]:
    map.extend(range(i,i+3))
map *= 3

markers = ["X","O"]

def which_board(x):
    return (3 * ((x % 81) / 27) + ((x % 9)/3))

def is_win(board):
    foo = range(9)
    for i in foo:
	for j in filter(lambda x: x != i, foo):
	    for k in filter(lambda x: x != i and x != j, foo):
		if [board[i],board[j],board[k]] in [ [x]*3 for x in markers]:
		     if (i+j+k) % 3 == 0 and (i+j+k)/3 in [i,j,k]:
			return board[i]
    return "."


class Game:
    def __init__(self,history=[]):
	self.init = history
	self.data = ["."]*81
	self.boardstate = ["."]*9
	self.gamestate = ["."]
	self.newspace = range(81)
	self.m = None
	self.mbn = None
	self.mb = None
	self.mbd = None
	self.player = 0
	self.movemode = "command_line"
	self.malformed = False

    def play(self):
	while self.gamestate == ["."]:
	    self.space = self.newspace
	    if self.malformed:
		__init__()
	    if self.player < len(self.init):
		self.movemode = "init"
	    else:
		self.movemode = "command_line"
		self.print_board("command_line")
    	    self.move()
	    self.newspace = filter(lambda x: which_board(x) == map[self.m], range(81))
	    self.mbn = which_board(self.m)
	    self.mb = filter(lambda x: which_board(x) == self.mbn, range(81))
	    self.mbd = [ self.data[x] for x in self.mb ]
	    win = is_win(self.mbd)
	    if win == ".":
		if not "." in self.mbd:
		    self.boardstate[self.mbn] = "T"
	    else:
		self.boardstate[self.mbn] = win
		self.gamestate = [is_win(self.boardstate)]
	    self.player += 1
	    if (not ("." in [ self.data[x] for x in self.newspace ])) or (self.boardstate[which_board(self.newspace[0])] != "."):
		self.newspace = range(81)
	if self.gamestate == ["x"]:
		end_game("x")
	elif self.gamestate == ["o"]:
		end_game("o")
	else:
		end_game("t")

    def print_board(self, how):
	if how == "command_line":
	    print "  123 456 789"
	    for metarow in range(3):
		for row in range(3):
		    out = ""
		    start = 27 * metarow + 9 * row
		    for column in range(3):
			for i in range(3):
			    out += str(self.data[start + 3*column + i])
			out += "|"
		    print str(row + 3*metarow + 1) + " " + out[:-1]
		if metarow != 2:
		    print "  ---+---+---"

    def move(self):
	moved = False
	while not moved:
	    self.m = self.get_move()
	    moved = (self.m in self.space and
		    self.data[self.m] == "." and
		    self.boardstate[which_board(self.m)] == ".")
	    if not moved:
		if self.movemode == "init":
			self.malformed = True
		else:
		    print "You cannot move there."
	self.data[self.m] = markers[ self.player % 2 ]

    def get_move(self):
	if self.movemode == "command_line":
	    x = self.space[0]
	    if len(self.space) == 9:
		movein = " on the %s board." % boardref[which_board(x)]
	    else:
		movein = " anywhere on the board." 
	    input = raw_input("Player %s: Select a move%s Enter <row><column>. " % (markers[ self.player % 2 ],movein))
	    try: move = int(input)
	    except ValueError : move = input
	    if type(move) != int:
		return len(self.data) + 100
	    return (9*((move/10)-1) + ((move%10)-1))
	if self.movemode == "init":
	    return self.init[self.player]	

def end_game(winner):
    if winner == "x":
	print "X won"
    if winner == "o":
	print "O won"
    if winner == "t":
	print "Tie"
