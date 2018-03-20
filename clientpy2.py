import socket
import sys
from random import randint
from time import sleep
import math

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
    t = math.atan2(y1-y2, x2-x1)
    t = 2*(3.14159) - t
    if (t < 0):
        t = t + 2*(3.14159)
    return t

user = "Theboys"
password = "vmarutha"

def run(*commands):
    HOST, PORT = "localhost", 17429
    
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
            #print(rline.strip())
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
    3: ["WEST", "3.14"],
    1: ["EAST", "0"],
    4: ["SOUTH", "1.57"],
    2: ["NORTH", "4.71"],
}

status()
counter = 0
tickCounter = 0
captureLimit = 0
while 1:
    status()
    # Find all the mines in our visible radius that is not ours
    #print "Num of mines " + statusDict["NUM_MINES"] 
    if (int(statusDict["NUM_MINES"])):
    #if 1:
    # if(1):
        not_ours = []
        #statusDict["MINES_POS"] = [("rand", "5000.0", "5000.0")]
        print counter
        if (counter < len(statusDict["MINES_POS"])):
            for mine in statusDict["MINES_POS"]:
                if (captureLimit > 2):
                    captureLimit = 0
                    break
                if mine[0] != user:
                    if mine not in not_ours:
                        not_ours.append(mine)
                        print("+++")
                        print not_ours
                        run("BRAKE")
                        print "SLEEPING"
                        sleep(10)
                        status()
                        print statusDict["X"], statusDict["Y"]
                        print str(calculateAngleBetweenPoints(float(statusDict["X"]), float(statusDict["Y"]), float(mine[1]), float(mine[2])))
                        run("ACCELERATE " + str(calculateAngleBetweenPoints(float(statusDict["X"]), float(statusDict["Y"]), float(mine[1]), float(mine[2]))) + " 1")
                        print "Second SLEEP"
                        sleep(5)
                        captureLimit = captureLimit + 1
                        #Should have gotten mine now
                        break
                else:
                    print "Own this already!"
                    print mine
                    counter = counter + 1
        else:
            #Go in a random direction
            counter = 0
            dir = randint(2, 2)
            print dir, direction[dir][0]
            run("ACCELERATE " + direction[dir][1] + " 1")
            run("BOMB "+statusDict["X"]+' ' +statusDict["Y"])
            sleep(3)
            tickCounter = 0



    else:
        tickCounter = tickCounter + 1
        if (tickCounter >= 800):
            tickCounter = 0
        t = (tickCounter / 200) + 1
        print tickCounter
        dir = randint(t, t)
        #print dir, direction[dir][0]
        run("ACCELERATE " + direction[dir][1] + " 1")
        run("BOMB "+statusDict["X"]+' ' +statusDict["Y"])
        #sleep(1)

#run("Theboys", "vmarutha", "BOMB "+statusDict["X"]+' ' +statusDict["Y"])

