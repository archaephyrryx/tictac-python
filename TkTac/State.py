################
# global xcor: #
# A list of ordered triples representing the x-coordinates (column number) of
# the positions of win-vectors. Membership in this list is a necessary condition
# for a 3-tuple of positions to be a possible win vector, and simultaeneous
# membership of the x-cor triples in this list and the y-cor triples in the
# [ycor] list is necessary and sufficient for win-vectors. (i.e. all win-vectors
# satisfy the conditions, and the conditions are only satisfied by win vectors).
# 
# This list contains all triples of x-coordinates constructed via the following
# algorithm:
# 
# A triple is a win-vector if its members lie in the same column or row, or span
# a diagonal. In each case, the x-coordinate of the second position must
# be the average of the x-coordinates of the first and third position, in order
# for the three to be colinear. Furthermore, the third coordinate and first
# coordinate must have the same parity, as the step between them can only be 0
# or 2, as they must either lie in the same column or lie at opposing extreme
# columns. These two conditions are both incorporated into the algorithm. As
# long as these conditions are satisfied, all positions satisfying the [ycor]
# conditions are win-vectors if and only if they also satisfy the xcor
# conditions.
xcor = [(a, (a+c)/2, c) for c in range((a%2),3,2) for a in range(0,3)]

################
# global ycor: #
# A list of ordered triples representing the y-coordinates (row number) of
# the positions of win-vectors. Membership in this list is a necessary condition
# for a 3-tuple of positions to be a possible win vector, and simultaeneous
# membership of the y-cor triples in this list and the x-cor triples in the
# [xcor] list is necessary and sufficient for win-vectors. (i.e. all win-vectors
# satisfy the conditions, and the conditions are only satisfied by win vectors).
# 
# This list contains all triples of x-coordinates constructed via the following
# algorithm:
# 
# A triple is a win-vector if its members lie in the same column or row, or span
# a diagonal. In each case, the y-coordinate of the second position must
# be the average of the x-coordinates of the first and third position, in order
# for the three to be colinear. Furthermore, the third coordinate and first
# coordinate must have the same parity, as the step between them can only be 0
# or 2, as they must either lie in the same row or lie at opposing extreme
# rows. Finally, the last y-coordinate must be greater than or equal to the
# first y-coordinate, as the triplets are ordered in ascending positional value.
# As long as these conditions are satisfied, all positions satisfying the [xcor]
# conditions are win-vectors if and only if they also satisfy the ycor
# conditions.
ycor = [(a, (a+c)/2, c) for c in range(a,3,2) for a in range(3)]

# Tuple of 3-tuples representing linear coordinates of win vectors
vect = tuple(tuple(a + 3*b for a, b in zip(trip_x, trip_y)) for trip_x, trip_y in zip(xcor, ycor))

# Class representing subboards
class Subboard(index):
    def __init__(self):
	self.data = [0]*9

    #################
    # method win(): #
    # Determines the identity of the winning player by testing every win-vector
    # for full ownership. If any win-vector is found to have an owner, the
    # identify of that owner is returned. Otherwise, 0 is returned. This method
    # does not distinguish between boards not yet won and boards fully drawn.
    #
    # The determination is made by testing the values of the positions in each
    # win-vector via the following test:
    #
    # In order for the three positions to have the same, non-zero value, their
    # sum must have absolute value of 3, as they must all be 1, or all be -1.
    # If we multiply the sum by any of the values, then we maintain a positive
    # value for positive sums, and reach a positive value for negative sums, as
    # each of the constituent positions must be -1, so the product is -1 * -3 =
    # 3. If any of the positions are 0, the sum will fall short of 3
    # (magnitude), and two opposing values equate to a single zero. When this
    # condition is met (a sum of 3 is found), the method returns any of the
    # values, as they all must be the same in order for that condition to be
    # met.
    def win(self):
	for i,j,k in tuple(map(lambda x: map(lambda y: self.data[y], x), vect)):
	    if i * (i + j + k) == 3:
		return i # The owner of the vector
	return 0 # Unclaimed

    #######################
    # method countOpen(): #
    # Returns the number of unfilled squares in the sub-board. Special cases are
    # 0, for a completely filled board; and 9, for a completely open board.
    def countOpen(self):
	count = 0
	for i in range(9):
	    if (board[i] == 0):
		count += 1
	return count

    #########################
    # method isUnclaimed(): #
    # Returns a boolean value representing whether the board is claimed or not,
    # where claimed is equivalent to "won". This method makes no distinction
    # about the identity of the winner should a winner exist, and only indicates
    # whether or not there is a winner of unspecified identity. The return
    # values are:
    # No winner (tied/open) --> True
    # Winner (claimed) --> False
    def isUnclaimed(self):
	return (self.win() == 0)

    #########################
    # method isUnfilled():  #
    # Returns a boolean value representing whether the board is filled or not.
    # This method makes no distinction about whether an unfilled (filled) board
    # is won, or open (tied). 
    # or won, or whether 
    # about the identity of the winner should a winner exist, and only indicates
    # whether or not there is a winner of unspecified identity. The return
    # values are:
    # No winner (tied/open) --> True
    # Winner (claimed) --> False

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
