# Student: Branden Lee

# tilepuzzle.py
# > tilepuzzle([[2,8,3],[1,0,4],[7,6,5]],[[1,2,3],[8,0,4],[7,6,5]])
# Example takes a few seconds to complete

def tilepuzzle(start,goal):
    if not checkValidBoard(start,goal):
        print("Start state and/or goal state invalid. Make sure each state has a blank tile and"
              "contain the same tiles.")
    else:
        path = stateSearch(start,goal)
        if path == None:
            print("No solution found.")
        else:
            print("Solution found with", len(path), "moves.")
            print("Moves written to moves.txt")
            pathToFile("moves.txt", path)
    
# Orginally the instructors method used recursion, but
# this method was changed to use iteration to prevent stack overflow
# This is basically a Depth First Search of valid states.
def stateSearch(start,goal):
    path = []
    stack = []
    exploredTable = {}
    # the 2D arrays are serialized into a string
    # this makes hashing easier and allows string function use
    boardStateId = serialize(start);
    goalBoardStateId = serialize(goal);
    appendUniqueState(stack, boardStateId, "", exploredTable)
    while len(stack) > 0:
        # print("stack.length=",len(stack)) 
        currentBoardStateId = stack.pop()
        # check if serialized current and goal state match
        if currentBoardStateId == goalBoardStateId:
            break
        else:
            blankPosition = findBlankPosition(currentBoardStateId)
            # Generate new states.
            # New states are generated naively and dont check if we just
            # reversed the last move, but the O(1) hash table check
            # will find we already processed that state before.
            # Swap blank up.
            newStateId = generateSwapUp(currentBoardStateId,blankPosition)
            if newStateId != None:
                appendUniqueState(stack, newStateId, currentBoardStateId, exploredTable)
            # Swap blank down.
            newStateId = generateSwapDown(currentBoardStateId,blankPosition)
            if newStateId != None:
                appendUniqueState(stack, newStateId, currentBoardStateId, exploredTable)
            # Swap blank right.
            newStateId = generateSwapLeft(currentBoardStateId,blankPosition)
            if newStateId != None:
                appendUniqueState(stack, newStateId, currentBoardStateId, exploredTable)
            # Swap blank left.
            newStateId = generateSwapRight(currentBoardStateId,blankPosition)
            if newStateId != None:
                appendUniqueState(stack, newStateId, currentBoardStateId, exploredTable)
    # Back track through explored table to get the path
    path.append(goalBoardStateId)
    goalBoardStateId = exploredTable.get(goalBoardStateId, "")
    while goalBoardStateId != "":
        path.append(goalBoardStateId)
        goalBoardStateId = exploredTable.get(goalBoardStateId, "")
    # reverse path so it goes start to goal
    path.reverse();
    # validate path
    if path[0] == boardStateId:
        return path
    return None
    
                
# find the position of the blank in the puzzle
def findBlankPosition(currentBoardStateId):
    return currentBoardStateId.find('0')

# get unique state identifier
def serialize(currentBoardState):
    serializedString = ""
    # 0 to 2 inclusive
    for row in range(0, 3):
        for col in range(0, 3):
            serializedString += str(currentBoardState[row][col])
    return serializedString

def appendUniqueState(stack, boardStateId, parentBoardStateId, exploredTable):
    # python disctionaries are a hash table implementation
    # checking existance of state is only O(1)
    if(boardStateId in exploredTable):
        # print("Possible cycle detected. State Id:", boardStateId, "already added.")
        return False
    else:
        # table is childNode->parentNode
        # important for final path lookup
        exploredTable[boardStateId]= parentBoardStateId;
        stack.append(boardStateId)
    return True

# check if the start and goal state are valid
def checkValidBoard(start,goal):
    symbolTable = {}
    # create table of goal symbols
    for row in range(0, 3):
        for col in range(0, 3):
            symbolTable[goal[row][col]] = True
    # a blank tile must exist
    if 0 not in symbolTable:
        return False
    # the same tiles in goal state must exist in the start state
    for row in range(0, 3):
        for col in range(0, 3):
            if start[row][col] not in symbolTable:
                return False
    return True

# Generate the possible state from available moves

def generateSwapUp(boardStateId,blankPosition):
    # In python, characters cant be edited in place
    # The string must be converted into a list first
    newBoardStateList = list(boardStateId)
    if blankPosition > 2:
        newBoardStateList[blankPosition] = newBoardStateList[blankPosition-3]
        newBoardStateList[blankPosition-3] = '0'
    else:
        return None
    return ''.join(newBoardStateList)

def generateSwapDown(boardStateId,blankPosition):
    # copy board identifier
    newBoardStateList = list(boardStateId)
    if blankPosition < len(newBoardStateList)-3:
        # swap. 0 used for blank tile.
        newBoardStateList[blankPosition] = newBoardStateList[blankPosition+3]
        newBoardStateList[blankPosition+3] = '0'
    else:
        return None
    return ''.join(newBoardStateList)

def generateSwapLeft(boardStateId,blankPosition):
    # copy board identifier
    newBoardStateList = list(boardStateId)
    if blankPosition%3 > 0:
        # swap. 0 used for blank tile.
        newBoardStateList[blankPosition] = newBoardStateList[blankPosition-1]
        newBoardStateList[blankPosition-1] = '0'
    else:
        return None
    return ''.join(newBoardStateList)

def generateSwapRight(boardStateId,blankPosition):
    # copy board identifier
    newBoardStateList = list(boardStateId)
    if blankPosition%3 < 2:
        # swap. 0 used for blank tile.
        newBoardStateList[blankPosition] = newBoardStateList[blankPosition+1]
        newBoardStateList[blankPosition+1] = '0'
    else:
        return None
    return ''.join(newBoardStateList)

# Writes the moves to a file. Good for long move paths.
def pathToFile(fileName, path):
    f = open(fileName, "w")
    for i in range(0, len(path)):
        f.write("Move: "+str(i)+"\n")
        f.write(path[i][0]+path[i][1]+path[i][2]+"\n")
        f.write(path[i][3]+path[i][4]+path[i][5]+"\n")
        f.write(path[i][6]+path[i][7]+path[i][8]+"\n\n")
    f.close()
