#
#  Logger.py
#
#  Created by Thomas Johannesmeyer on 02/02/2016.
#  Copyright (c) 2016 Thomas Johannesmeyer. All rights reserved.
#

#!/usr/bin/python

import time

def log(text):
  """
  Prints a string with current date & time to console.
  """

  current_time = time.strftime("%H:%M:%S")
  if isinstance(text, basestring):
      print("[Pinachtsbaum <" + current_time + ">]: " + text)
  else:
      print("[Pinachtsbaum <" + current_time + ">]: Warning. Not a string.")
