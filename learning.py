import random
import pickle

load = open("table","rb+")
tree = pickle.load(load)

datastates = ["X","O",""]
markers = ["X","O"]
win_conditions = [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]]

def random_move(data):
    possible = [ x for x in range(9) if data[x] == ""]
    return random.choice(possible)

def enemy(who):
    if who == "X": return "O" 
    if who == "O": return "X"

def make_move(who, data):
    optimal = winning_moves(data)
    offense = optimal[who]
    defense = optimal[enemy(who)]
    move = decide(offense,defense)
    if move:
        return move
    return random_move(data)

def winning_moves(data):
    control = dict()
    optimal = dict()
    for state in datastates:
        control[state] = list()
    for state in markers:
        optimal[state] = list()
    for square in range(9):
        control[data[square]].append(square)
    for position in win_conditions:
        for player in markers:
            blocked = [ x for x in position if x in control[enemy(player)]]
            if not blocked:
                optimal[player].append([ x for x in position if x in control[""]])
    for player in markers:
        optimal[player] = organize(optimal[player])
    return optimal

def decide(offense,defense):
    mygoal = [[[seq for seq in offense[i] if move in seq] for move in range(9)] for i in range(3)]
    hisgoal = [[[seq for seq in defense[i] if move in seq] for move in range(9)] for i in range(3)]
    i = 0
    for move in range(9):
        if len(mygoal[i][move]) >= 1:
            return move
    for move in range(9):
        if len(hisgoal[i][move]) >= 1:
            return move
    i = 1
    for ways in [4,3,2]:
        for move in range(9):
            if len(mygoal[i][move]) >= ways:
                return move
        for move in range(9):
            if len(hisgoal[i][move]) >= ways:
                return move
    for move in range(9):
        if len(mygoal[i][move]) == 1:
            forces = mygoal[i][move][0]
            force = forces[1 - forces.index(move)]
            if len(hisgoal[i][force]) <= 1:
                return move
    i = 2
    for ways in [4,3,2]:
        for move in range(9):
            if len(mygoal[i][move]) >= ways:
                return move
        for move in range(9):
            if len(hisgoal[i][move]) >= ways:
                return move
    return False
             

def organize(optimal):
    organized = dict()
    for i in range(3):
        organized[i] = list(filter(lambda x: len(x) == i+1, optimal))
    return organized

def is_win(b):
    for mark in markers:
        if [mark]*3 in [ [b[x] for x in y] for y in win_conditions ]:
            return mark
    return ""


class Tree():
    def __init__(self):
        self.children = list()
        self.terminus = False

class Node(object):
    def __init__(self):
        self.parent = None
        self.terminus = False
        self.state = None
        self.children = list()

def ends(node):
    states = dict.fromkeys(["win","loss","tie"],0)
    count = 0
    if node.terminus:
        states[node.state] += 1
    else:
        for child in node.children:
            count += ends(child)
    return count

def plant(root,sequence,finalstate):
    node = root
    i = 1
    termin = False
    while True:
        parent = node
        parent.terminus = (i == len(sequence) + 1)
        if parent.terminus:
            parent.state = finalstate
        else:
            node = Node(sequence[:i]) 
            if child not in parent.children:
                parent.children.append(child)
                child.parent = parent
        i += 1
    return root,finalstate

def forever(parity,tries):
    trials = 0
    win = 0
    loss = 0
    tie = 0
    while trials <= tries:
        player = 0
        data = [""]*9
        gamestate = ""
        history = []
        while True: 
            if gamestate != "":
                if gamestate == markers[parity]:
                    result = "win"
                    break
                elif gamestate == markers[1 - parity]:
                    result = "lose"
                    break
            elif not ("" in data):
                result = "tie"
                break
            if player % 2 == parity:
                m = make_move(markers[parity],data)
            if player % 2 != parity:
                m = random_move(data)
            data[m] = markers[player % 2]
            history.append(m)
            gamestate = is_win(data)
            player += 1
        if result == "lose"
            lose += 1
            print(history)
        if result == "win":
            win += 1
        if result == "tie":
            tie += 1 
        trials += 1
        tree = plant(tree,history,result)
    return "Wins: %d Losses: %d Ties: %d" % (wins,lose,ties)
