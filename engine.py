players = [1,-1]

# linkMoveBoard: gives the index of the board linked to a numbered move
def linkMoveBoard(i):
  return ((i%9)/3)+3*((i%27)/9)

# onMoveBoard: gives the index of the board containing a numbered move
def onMoveBoard(i):
    return (3 * ((i % 81) / 27) + ((i % 9)/3))

# linkBoardMove: gives the positions that link to a numbered board
def linkBoardMove(i):
  # Note: The following code is a temporary bash until a better solution is found */
  values = list()
  count = 0
  for x in range(81):
    if (linkMoveBoard(x) == i):
      values.append(x)
  return values

# onBoardMove: gives the positions that a numbered board contains */
def onBoardMove(i):
  if i == 9:
    return range(81)
  # Note: The following code is a temporary bash until a better solution is found */
  values = list()
  count = 0
  for x in range(81):
    if (onkMoveBoard(x) == i):
      values.append(x)
  return values


# win: returns the winner of a given 3x3 data board, or 0 if no winner (incomplete or tie) */
def win(board):
  i = 0
  while i < 9:
    j = 0
    while j < i:
      k = 0
      while k < j:
	if (abs(board[i] + board[j] + board[i]) == 3):
	  if ((i+j+k) % 3 == 0 and (i+j+k)/3 == j):
		return board[i]
	k += 1
      j += 1
    i += 1
  return 0

class Game:
  def __init__(self):
    self.time = 0
    self.player = 1
    self.state = [0]*81
    self.boardstate = [0]*9
    self.gamestate = 0
    self.spacestate = 9
    self.gamespace = range(81)
    
  def updateMetaState(self):
    board = 0
    while board < 9:
      values = list()
      i = 0;
      while i < 9:
	values.append(state[onBoardMove(i)])
	i += 1
      self.boardstate[board] = win(values)
      board += 1
    self.gamestate = win(self.boardstate)
    return boardstate

  def play(self):
    while gamestate == 0:
      self.updateGameSpace()
      move = self.getMove()
      self.state[move] = player
      self.updateMetaState()
      if (self.boardstate[linkMoveBoard(move)] == 0) and (0 in map(lambda x: self.state[x], onBoardMove(onMoveBoard(x)))):
	self.spacestate = onMoveBoard(x)
      else:
	self.spacestate = 9
      self.time += 1
      self.player *= -1
    return gamestate
	  
    def updateGameSpace(self):
      self.gamespace = filter(lambda x: self.state[x] == 0 and self.boardstate[onBoardMove(x)] == 0, onBoardMove(self.spacestate))
      
    def getMove(self):
      return move(self.state, self.boardstate, self.gamestate, self.gamespace, self.player)
      
def move():
  return 0