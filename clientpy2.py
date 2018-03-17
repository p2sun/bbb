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
  "NUM_PLAYERS": "",
  "PLAYER_POS": [],
  "NUM_BOMBS": "",
  "NUM_WORMHOLES": "",
  "WORMHOLES": []
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
    	for x in xrange(len(splitStatus)):
    		print x
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


run("Theboys", "vmarutha", "ACCELERATE 3.14 1")
status()
run("Theboys", "vmarutha", "BOMB "+statusDict["X"]+' ' +statusDict["Y"])

