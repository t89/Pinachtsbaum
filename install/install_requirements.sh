# Pinachtsbaum
# Copyright 2017 Thomas Johannesmeyer
#
# Licensed under the "THE BEER-WARE LICENSE" (Revision 42):
# Thomas Johannesmeyer wrote this file. As long as you retain this notice you
# can do whatever you want with this stuff. If we meet some day, and you think
# this stuff is worth it, you can buy me a beer or coffee in return

#!/bin/bash

if [ "$(uname)" == "Darwin" ]; then
  echo "Running on macOS. This script is meant to be run on Linux. Aborting."
  exit
fi

# fetches available updates
sudo apt-get update

# installs gcc compiler
sudo apt-get install gcc

# installs latest versions of python 2.x / 3
sudo apt-get install python
sudo apt-get install python3

# installs python dev header files and static libraries
sudo apt-get install python-dev
sudo apt-get install python3-dev

# installs python package-management
sudo apt-get install python-pip
sudo apt-get install python-pip3

# installs python packages
sudo pip install gpiozero
sudo pip install RPi.GPIO

# installs python3 packages
sudo pip3 install gpiozero
sudo pip3 install RPi.GPIO

# downloads latest versions
sudo apt-get dist-upgrade

