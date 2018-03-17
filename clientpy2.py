import socket
import sys
from random import randint
from time import sleep

# Status dictionary 
statusDict = {
  "COMMAND": "",
  "X": "",
  "Y": "",
  "DX": "",
  "DY" : "",
  "NUM_MINES": "",
  "MINES_POS": [],
  "NUM_PLAYERS": "",
  "PLAYER_POS": [],
  "NUM_BOMBS": "",
  "BOMBS_POS": [],
  "NUM_WORMHOLES": "",
  "WORMHOLES_POS": []
}

def calculateDistance(x1, y1, x2, y2):
    return sqrt((x1-x2)^2 + (y1-y2)^2)

def calculateAngleBetweenPoints(x1, y1, x2, y2):
    print math.atan2(y2-y1, x2-x1)
    return math.atan2(y2-y1, x2-x1)

user = "Theboys"
password = "vmarutha"

def run(*commands):
    HOST, PORT = "codebb.cloudapp.net", 17429
    
    data=user + " " + password + "\n" + "\n".join(commands) + "\nCLOSE_CONNECTION\n"
    returnList = [] 
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        sock.connect((HOST, PORT))
        sock.sendall(data)
        sfile = sock.makefile()
        rline = sfile.readline()
        while rline:
	    returnList.append(rline.strip())
            print(rline.strip())
            rline = sfile.readline()
    finally:
        sock.close()
    return returnList

def subscribe():
    HOST, PORT = "codebb.cloudapp.net", 17429
    
    data=user + " " + password + "\nSUBSCRIBE\n"

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        sock.connect((HOST, PORT))
        sock.sendall(data)
        sfile = sock.makefile()
        rline = sfile.readline()
        while rline:
            #print(rline.strip())
            rline = sfile.readline()
    finally:
        sock.close()

def status():
    status = run("STATUS")
    for s in xrange(len(status)):
    	splitStatus = status[s].split()
	numOfPlayers = 0;
	numOfMines = 0;
	numOfBombs = 0
	numOfWormholes = 0;
	x = 0
    	while (x < len(splitStatus)):
		if (numOfPlayers > 0):
			statusDict["PLAYER_POS"].append((splitStatus[x], splitStatus[x+1], splitStatus[x+2], splitStatus[x+3]))
			x = x + 4
			numOfPlayers = numOfPlayers - 1
		elif (numOfMines > 0):
			statusDict["MINES_POS"].append((splitStatus[x], splitStatus[x+1], splitStatus[x+2]))
			x = x + 3
			numOfMines = numOfMines - 1
		elif (numOfBombs > 0):
			statusDict["BOMBS_POS"].append((splitStatus[x], splitStatus[x+1]))
			x = x + 2
			numOfBombs = numOfBombs - 1
		elif (numOfWormholes > 0):
			statusDict["WORMHOLES_POS"].append((splitStatus[x], splitStatus[x+1], splitStatus[x+2], splitStatus[x+3], splitStatus[x+4]))
			x = x + 5
			numOfWormholes = numOfWormholes - 1
		else:
    			if (x == 0):
    				statusDict["COMMAND"] = splitStatus[x]
    			elif (x == 1):
    				statusDict["X"] = splitStatus[x]
    			elif (x == 2):
    				statusDict["Y"] = splitStatus[x]
   	 		elif (x == 3):
    				statusDict["DX"] = splitStatus[x]
    			elif (x == 4):
    				statusDict["DY"] = splitStatus[x]
    			elif (x == 6):
    				statusDict["NUM_MINES"] = splitStatus[x]
				numOfMines = int(splitStatus[x])
			elif (splitStatus[x] == "PLAYERS"):
				x = x + 1
				statusDict["NUM_PLAYERS"] = splitStatus[x]
				numOfPlayers = int(splitStatus[x])
			elif (splitStatus[x] == "BOMBS"):
				x = x + 1
				statusDict["NUM_BOMBS"] = splitStatus[x]
				numOfBombs = int(splitStatus[x])
			elif (splitStatus[x] == "WORMHOLES"):
				x = x + 1
				statusDict["NUM_WORMHOLES"] = splitStatus[x]
				numOfWormholes = int(splitStatus[x])
			x  = x + 1


def gotoPoints(coords):
    while coords:
        point = coords.pop()
        radians = calculateAngleBetweenPoints(statusDict["X"], statusDict["Y"], point[1], point[2])
        run("ACCELERATE " + radians + " 1")
        run("BOMB "+statusDict["X"]+' ' +statusDict["Y"])

        while(float(statusDict["X"] != point[1]) or float(statusDict["Y"] != point[2])):
                status()

        run("BRAKE")
        while(float(statusDict["DX"]) or float(statusDict["DY"])):
                status()
                print("random")


direction = {
    1: ["WEST", "3.14"],
    2: ["EAST", "0"],
    3: ["NORTH", "1.57"],
    4: ["SOUTH", "4.71"],
}

status()

while 1:
    status()
    # Find all the mines in our visible radius that is not ours
    # if (int(statusDict["NUM_MINES"])):
    if(1):
        not_ours = []
        statusDict["MINES_POS"] = [("rand", statusDict["X"], statusDict["Y"])]
        for mine in statusDict["MINES_POS"]:
            if mine[0] != user:
                not_ours.append(mine)
        print("FMLFMLFMLMFLFM")
        print(not_ours)
        if not_ours: 
            print("BRAKINGGGGG11111")
            run("BRAKE")


            # find when we stop
            while(float(statusDict["DX"]) != 0.0 or float(statusDict["DY"]) != 0.0):
                status()
                print("BRAKINGGGGG")
            exit()    
            # gotoPoints(not_ours)
        
    dir = randint(1, 4)
    print dir, direction[dir][0]
    run("ACCELERATE " + direction[dir][1] + " 1")
    run("BOMB "+statusDict["X"]+' ' +statusDict["Y"])
    sleep(3)
#run("Theboys", "vmarutha", "BOMB "+statusDict["X"]+' ' +statusDict["Y"])

