#
#  Client.py
#
#  Created by Thomas Johannesmeyer on 02/02/2016.
#  Copyright (c) 2016 Thomas Johannesmeyer. All rights reserved.
#

#!/usr/bin/python

import socket
import time
import sys

from Logger import *


# Client Configuration - Edit according to your settings
#  HOST = "192.168.2.114"        # Insert HOST IP / name here
HOST = "127.0.0.1"        # Insert HOST IP / name here
PORT = 12421                   # PORT this client is communicating on
DELAY = 2                      # DELAY between retries in seconds
MAX_ATTEMPT_COUNT = 5            # Max number of attempts
##
# Use this for debugging
#  HOST = "127.0.0.1"        # Insert HOST IP / name here

# Configuration End


def send(msg):
    """
    This function attempts to establish a connection to the server,
    sends the message provided as parameter 'msg' and closes the
    connection. It also returns a BOOL which is True, if the message
    has been sent successfully.
    """

    successful = True
    clientSocket = socket.socket()         # Create a socket object
    clientSocket.settimeout(5)


    # Attempting to connect to server
    try:
        log("Connecting...\n")
        clientSocket.connect((HOST, PORT))
        response = clientSocket.recv(1024)
        log(response)
    except socket.error, exc:
        log("Caught exception socket.error : %s" % exc)
        successful = False


    # Attempting to send message to server
    try:
        log("Trying to send message: " + msg + " to " + HOST + ":" + str(PORT))
        clientSocket.send(msg)
    except socket.error, exc:
        log("Caught exception socket.error : %s" % exc)
        successful = False

    # Attempting to close connection
    try:
        log("Closing connection.\n")
        clientSocket.close()                     # Close the socket when done
    except socket.error, exc:
        log("Caught exception socket.error : %s" % exc)
        successful = False

    return successful


def executeCommand(comm):
    """
    Tries to send provided parameter 'comm' to server
    Will retry if message has not been delivered successfully.
    """

    current_attempt_count = 0                   # Resetting for each command
    successful = send(comm)                   # Attempts to send message and saves result

    if successful:                            # Message has been sent successfully
        log("Message sent successfully.\n\n")
    else:                                     # Some error appeared while sending the message
        last_try_time = time.time()             # Save timestamp

        while ((successful == False) and (current_attempt_count < MAX_ATTEMPT_COUNT)):
        # Still unsuccessful and within maximum attempt threshold
            delta_time = time.time() - last_try_time # Calculate time delta between now and last attempt

            if delta_time >= DELAY:                # time delta between now and last try is >= timeout
                log("Could not send message. Retry: " + str(current_attempt_count) + "/" + str(MAX_ATTEMPT_COUNT))
                last_try_time = time.time()         # set last try timestamp to now
                successful = send(comm)           # retry sending -> Saving success-flag
                current_attempt_count += 1          # increase attempt count


argCount = len(sys.argv)
if argCount > 1:                             # Arguments from commandline available
  for index in range(1,argCount):
    command = str(sys.argv[index]).upper()
    log("Sending: '" + command + "' provided as argument from commandline.")
    executeCommand(command)


# You can add commands here:
#executeCommand("DR(traceroute 8.8.8.8)")    
#executeCommand(COMMAND0)

