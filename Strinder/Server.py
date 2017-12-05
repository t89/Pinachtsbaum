#
#  Server.py
#
#  Created by Thomas Johannesmeyer on 02/02/2016.
#  Copyright (c) 2016 Thomas Johannesmeyer. All rights reserved.
#

#!/usr/bin/python


import socket
import os
import sys
import inspect

from threading import Thread
from Logger import *

from time import sleep


##
# Importing from parent directory without being a module
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

from source.Pinachtsbaum import Pinachtsbaum

is_running = True


# Setup
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
HOST = ""                       # Leaving it empty fixes bug on Windows Machines
PORT = 12421                    # PORT this server is listening to
serverSocket.bind((HOST, PORT)) # Bind to the PORT
serverSocket.listen(5)          # Await client connection.


# Pre- / Suffix for direct commands. 
DIRECT_RUN_PREFIX = "DR("
DIRECT_RUN_SUFFIX = ")"

##
# This is your command central. Here you can add, delete and assign the different commands.
# Assign the names of your commands:

C_ON = "ON"
C_OFF =  "OFF"
C_STOP_SERVER = "STOP_SERVER"
C_AMBIENT_GLOW = "AMBIENT_GLOW"
C_FLUSH = "FLUSH"
C_PING = "PING"


# Server monitoring
def log_status():
    """
    Logs the server status
    """

    if is_running:
        log("Server is running.")
        ip_address = (([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")] or [[(s.connect(("8.8.8.8", 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) + ["no IP found"])[0]

	log("Address: " + ip_address + ":" + str(PORT))
    else:
        log("Server is not running.")


def run_server():
    """
    Starts server loop
    """

    while is_running:
        try:
            clientSocket, addr = serverSocket.accept()   # Establish connection with client.
            log('Received connection from:' + str(addr))
            clientSocket.send('Connection Established.')

            receivedMessage = clientSocket.recv(1024)

            log("Received Message: " + receivedMessage)
            run_command(receivedMessage) # Execute command
            clientSocket.close()         # Closing the connection
        except socket.error, exc:
            log("Caught exception socket.error : %s" % exc)
        sleep(0.1) # greatly frees up processing time


def stop_server():
    """
    Stops server
    """

    is_running = False
    log_status()


##
# Tell the server what it should be doing
# You can execute shell commands following this sample:
# os.system("echo 'hello world'") # Writes "hello world" to console
# os.system("ping 8.8.8.8") # Pings Google's DNS
# os.system("speaker-test -c2") # Linux sound test for 2 Channels (Not tested)

def direct_run(msg):
    """
    Directly run command on server.
    """

    log("Tried executing command:" + msg + ". This feature is deactivated")
    #  log("Executing system command: " + msg)
    #  os.system(msg)


def flush():
    """
    Swirl Tree from top to bottom, leaving all LEDs off
    """

    log("Flush")
    tree.illuminate_led(0, True, 0, 0.2)
    tree.swirl(0.4, 3, False)


def ping():
    """
    Pings one random LED for 0.2 seconds
    """

    log("Ping")
    tree.ping(0.2)


def ambient_glow():
    """
    Starts Ambient Glow
    """

    log("Start Ambient Glow")
    tree.ambient_glow(0.75, 2.0)


def on():
    """
    Switches on every LED on tree
    """

    log("Status: On")
    tree.illuminate_all(True)


def off():
    """
    Switches off every LED on tree
    """

    log("Status: Off")
    tree.illuminate_all(False)


def run_command(comm):
    """
    Links commands to methods and executes them
    """

    if isinstance(comm, basestring):
        # Is of type basestring

        # Evaluating commands
        if comm == C_STOP_SERVER:
            stop_server()
        elif comm == C_ON:
            on()
        elif comm == C_OFF:
            off()
        elif comm == C_AMBIENT_GLOW:
            ambient_glow()
        elif comm == C_FLUSH:
            flush()
        elif comm == C_PING:
            ping()
        elif comm.startswith(DIRECT_RUN_PREFIX) and comm.endswith(DIRECT_RUN_SUFFIX):
            direct_run(comm[3:len(comm) - 1])
        else:
            log("Invalid Command: " + comm)
    else:
        log("Warning. Not a string.")


##
# Entry point

# Create Pinachtsbaum Object
tree = Pinachtsbaum()

#Switch everything off - including the Star
off()

if __name__ == "__main__":
    """
    Run the server
    """

    log_status()

    threadServer = Thread(target = run_server)
    threadServer.setDaemon(True)
    threadServer.start()

    while True:
        pass
