class Tree():
    def __init__(self):
        self.children = list()
        self.terminus = False

class Node(object):
    def __init__(self):
        self.parent = None
        self.terminus = False
        self.children = list()

def ends(node):
    count = 0
    if node.terminus:
        count += 1
    else:
        for child in node.children:
            count += ends(child)
    return count

def plant(sequence,finalstate):
    root = Tree()
    child = root
    for i in range(1,len(sequence)+1)
        parent = child
        child = Node(sequence[:i]) 
        if child not in parent.children:
             parent.children.append(child)
             child.parent = parent
    return root,finalstate
