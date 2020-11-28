import copy
METHOD = None
M = None
N = None
GOAL = None
GOALINDEX = None
GOALVIEW = [[], [], []]
A = None
B = None
C = None
class Node:
    parent = None
    children = []
    state = []
    cost = None
    depth = None

    def __init__(self, parent, children, state, cost, depth):
        self.parent = parent
        self.children = children
        self.cost = cost
        self.state = state
        self.depth = depth

    def printNode(self):
        # DEBUG Function
        print('|'*(self.depth+3),'>', 'Depth', self.depth)
        if self.parent != None:
            print('|'*(self.depth+4), 'Parent ' , self.parent.state)
        else:
            print('|'*(self.depth+4), 'Parent : itself')

        print('|'*(self.depth+4), 'Cost ' , self.cost)
        print('|'*(self.depth+4), 'State ' , 'A = ' , self.state[0])
        print('|'*(self.depth+4), 'State ' , 'B = ' , self.state[1])
        print('|'*(self.depth+4), 'State ' , 'C = ' , self.state[2])
        if len(self.children) > 0 :
            print('|'*(self.depth+4), 'Children:')
            for i in range(0,len(self.children)):
                self.children[i].printNode()
        else:
            print('|'*(self.depth+4), 'Children : []')

    def fillChildren(self):
        for i in range(0,3):
            for j in range(0, 3):
                if i == j:
                    continue
                else:
                    frontStart = len(self.state[i]) - 1
                    frontDest = len(self.state[j]) - 1
                    condition = (frontStart >= 0 and frontDest >= 0 and self.state[i][frontStart] < self.state[j][frontDest])
                    condition = condition | (frontStart +1 > 0 and frontDest + 1 == 0)
                    if condition:
                        childState = copy.deepcopy(self.state)
                        childState[j].append(childState[i].pop())
                        childDepth = self.depth + 1
                        childCost = childDepth + heuristic(childState)
                        child = Node(self, [], childState, childCost, childDepth)
                        self.children.append(child)

    def isGoal(self):
        return self.state == GOALVIEW       

def heuristic(state):
    global GOALINDEX, N
    x = N - len(state[GOALINDEX])
    prevIndex = (GOALINDEX - 1) % 3
    nextIndex = (GOALINDEX + 1) % 3
    y  = 0 
    currentDisk = N
    rodBottomPtr = 0
    goalLen = len(state[GOALINDEX])
    # '''
    while currentDisk > 0 and rodBottomPtr < goalLen:
        if state[GOALINDEX][rodBottomPtr] < currentDisk: 
            '''
                if the biggest element in the rod is smaller than an element in another rod, then all the remaining 
                ones will also be smaller
            '''
            y += len(state[GOALINDEX][rodBottomPtr:])
            break
        rodBottomPtr += 1
        currentDisk -= 1
  

    return x + 2*y

def readInput():
    global METHOD, M, N, GOAL, A, B, C, GOALINDEX, GOALVIEW
    METHOD = input()
    M = int(input())
    N = int(input())
    GOAL = input()
    A = input()
    B = input()
    C = input()
    if A != '':
        A = A.split(',')
        A = list(map(lambda item: int(item),A))
    else:
         A = []
    if B != '':
        B = B.split(',') 
        B = list(map(lambda item: int(item),B))
    else:
        B = []
    if C != '':
        C = C.split(',') 
        C = list(map(lambda item: int(item),C))
    else:
        C = []
    if GOAL == 'A':
        GOALINDEX = 0
    elif GOAL == 'B':
        GOALINDEX = 1
    else:
        GOALINDEX = 2
    
    GOALVIEW[GOALINDEX] = A + B + C
    GOALVIEW[GOALINDEX].sort(reverse = True)

def getMinCostItemIndex(openList):
    global M
    minCost = openList[0].cost
    index = 0
    length = len(openList)
    for i in range(1, length):
        if openList[i].cost < minCost:
            minCost = openList[i].cost
            index = i
    if minCost > M:
        index = -1
    return index

def isInList(statusList, currentChildNode):
    statusListLength = len(statusList)
    for i in range(0, statusListLength):
        if currentChildNode.state == statusList[i].state:
            return i
    return -1

def buildSolutionArray(goalNode):
    solution = []
    tmp = goalNode
    while tmp != None:
        solution.insert(0, tmp.state)
        tmp = tmp.parent
    return solution

def Astar():
    global METHOD, M, N, GOAL, A, B, C
    initialState = Node(None , [], [A , B , C] , heuristic([A , B , C]), 0)
    openList = [initialState]
    closedList = []
    while openList != []:
        popIndex = getMinCostItemIndex(openList)
        if popIndex == -1:
            return [] # M reached
        currentNode = openList.pop(popIndex)
        closedList.append(currentNode)
        if currentNode.isGoal():
            return buildSolutionArray(currentNode)
        else:
            currentNode.fillChildren()
            childCount = len(currentNode.children)
            for i in range(0, childCount):
                currentChildNode = currentNode.children[i]
                isInOpen = isInList(openList, currentChildNode)
                isInClosed = isInList(closedList, currentChildNode)
                if isInOpen == -1 and isInClosed == -1 :
                    openList.append(currentChildNode)
                elif isInOpen > -1 and currentChildNode.cost < openList[isInOpen].cost:
                    openList[isInOpen].parent = currentNode
                elif isInClosed > -1 and currentChildNode.cost < closedList[isInClosed].cost:
                    closedList.pop(isInClosed)
                    openList.append(currentChildNode)
    return []   # Empty open list

def limitedFSearch(dfsStack, fmax):
    lastNode = dfsStack.pop()
    if lastNode.cost > fmax:
        return lastNode
    if lastNode.isGoal():
        return lastNode
    retVal = lastNode
    lastNode.fillChildren()
    for i in lastNode.children:
        if isInList(dfsStack, i) == -1:
            dfsStack.append(i)
            retVal = limitedFSearch(dfsStack, fmax)
            if retVal.isGoal():
                return retVal       
    return retVal

def IDAStar():
    global M, N, GOAL, A, B, C
    initialState = Node(None , [], [A , B , C] , heuristic([A , B , C]), 0)
    fmax = initialState.cost
    i = 0
    
    while(True):
        if fmax > M:
            return []
        dfsStack = [initialState]
        result = limitedFSearch(dfsStack,fmax)
        if type(result) is Node and result.isGoal():
            return buildSolutionArray(result)
        else:
            fmax = result.cost
        i += 1
    return []

def __main__():
    global METHOD, M, N, GOAL, A, B, C
    readInput()
    result = []
    if METHOD == 'A*':
        result = Astar()
    else:
        result = IDAStar()
    
    if result == []:
        print('FAILURE')
    else:
        print('SUCCESS')
        for i in result:
            outText = "\nA->{a}\tB->{b}\tC->{c}\n".format(a = i[0], b = i[1], c = i[2])
            print(outText)
__main__()