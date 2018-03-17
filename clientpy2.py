import socket
import sys
    
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

def run(user, password, *commands):
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

def subscribe(user, password):
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
    status = run("Theboys", "vmarutha", "STATUS")
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

run("Theboys", "vmarutha", "ACCELERATE 3.14 1")
status()
print statusDict
#run("Theboys", "vmarutha", "BOMB "+statusDict["X"]+' ' +statusDict["Y"])

