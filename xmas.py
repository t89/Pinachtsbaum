#  Pinachtsbaum
#  Copyright 2017 Thomas Johannesmeyer
#
#  Licensed under the "THE BEER-WARE LICENSE" (Revision 42):
#  Thomas Johannesmeyer wrote this file. As long as you retain this notice you
#  can do whatever you want with this stuff. If we meet some day, and you think
#  this stuff is worth it, you can buy me a beer or coffee in return


from source.Pinachtsbaum import Pinachtsbaum
from signal import pause
from time import sleep

import sys, tty, os, termios

import inspect


##
# For Demo implementations take a look at the bottom of the file


def getkey():
    old_settings = termios.tcgetattr(sys.stdin)
    tty.setcbreak(sys.stdin.fileno())
    try:
        while True:
            b = os.read(sys.stdin.fileno(), 3).decode()
            if len(b) == 3:
                k = ord(b[2])
            else:
                k = ord(b[0])
            key_mapping = {
                    127: 'backspace',
                    10: 'return',
                    32: 'space',
                    9: 'tab',
                    27: 'esc',
                    65: 'up',
                    66: 'down',
                    67: 'right',
                    68: 'left'
                    }
            return key_mapping.get(k, chr(k))
    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)


def demo_quarters():
    print(inspect.stack()[0][3])
    duration = 1
    for n in range(0, 3):
        tree.on(tree.qmap["FRONT_LEFT"]);
        sleep(duration/8.0)
        tree.on(tree.qmap["FRONT_RIGHT"]);
        sleep(duration/8.0)
        tree.on(tree.qmap["BACK_RIGHT"]);
        sleep(duration/8.0)
        tree.on(tree.qmap["BACK_LEFT"]);
        sleep(duration/8.0)
        tree.off(tree.qmap["BACK_LEFT"]);
        sleep(duration/8.0)
        tree.off(tree.qmap["BACK_RIGHT"]);
        sleep(duration/8.0)
        tree.off(tree.qmap["FRONT_RIGHT"]);
        sleep(duration/8.0)
        tree.off(tree.qmap["FRONT_LEFT"]);
        sleep(duration/8.0)


def demo_height_map():
    print(inspect.stack()[0][3])
    #illuminate_led(led_ids, status, delay, auto_off)
    duration = 1
    for times in range(0, 3):
        for n in range(0, 4):
            tree.illuminate_led(tree.hmap[n], True, 0.0, duration/2.0)
            sleep(duration/4.0)
        sleep(duration/2.0)


def demo_swirl():
    print(inspect.stack()[0][3])
    # swirl(duration, chain_length, ascending(BOOL))
    for n in range(0, 3):
        tree.swirl(4, 4, True)
    sleep(1)


def demo_blinking():
    print(inspect.stack()[0][3])
    for n in range(0, 3):
        tree.start_blinking(tree.all, 0.2, 0.6)

    ##
    # Alternative Demo:
    #  tree.start_blinking(tree.hmap[0], 0.25, 0.125)
    #  tree.start_blinking(tree.hmap[1], 0.5, 0.25)
    #  tree.start_blinking(tree.hmap[2], 1, 0.5)
    #  tree.start_blinking(tree.hmap[3], 2, 1)


def demo_all():
    print(inspect.stack()[0][3])
    tree.on(tree.all)


def demo_ping():
    print(inspect.stack()[0][3])
    for n in range(0,24):
        tree.ping(0.5)
        sleep(0.5)


def demo_beat():
    print(inspect.stack()[0][3])
    tree.random_with_beat(116.0) # 116 BPM - Daft Punk - Get Lucky


def demo_keystrokes():
    print(inspect.stack()[0][3])
    print("Hit any key to ping a random LED and fire with RETURN. Stay away from Umlauts! Cancel with ctrl - c or esc")
    try:
        while True:
            k = getkey()
            if k == 'esc':
                quit()
            elif k == 'return':
                # Shine, Shine little twinkle Star
                tree.illuminate_led(0, True, 0, 0.2)
                tree.swirl(0.4, 3, False)
            else:
                ##
                # This fills the tree randomly and returns a token which can later be used to
                # reference the lamp: tree.off(token)
                token = tree.ping_with_token()
                print(token)

                ##
                # Alternative: Just blink a random lamp for 0.2 seconds:
                #  tree.ping(0.2)

    except (KeyboardInterrupt, SystemExit):
        os.system('stty sane')
        print('stopping.')


def demo_patterns():
    print(inspect.stack()[0][3])
    patterns = [tree.smap["LEFT_FRONT"],
            tree.smap["LEFT_BACK"],
            tree.smap["FRONT_LEFT"],
            tree.smap["FRONT_RIGHT"],
            tree.smap["RIGHT_FRONT"],
            tree.smap["RIGHT_BACK"],
            tree.smap["BACK_LEFT"],
            tree.smap["BACK_RIGHT"],
            tree.smap["LEFT_FRONT"]]



    for pattern in patterns:
        tree.illuminate_led(pattern, True, 0, 0.5)
        sleep(1)


def demo_dim():
    print(inspect.stack()[0][3])
    tree.dim(tree.all, 0.5, 0.0, 1, False)
    tree.dim(tree.all, 0.1, 0.2, 0.25, True)
    tree.dim(tree.all, 1.0, 0.0, 0.55, True)


def demo_step_brightness():
    print(inspect.stack()[0][3])
    tree.increase_brightness(tree.smap["FRONT_LEFT"], 0.5, 0)
    sleep(1)
    tree.increase_brightness(tree.hmap[0], 0.5, 0.0)
    sleep(1)
    tree.decrease_brightness(tree.hmap[1], 0.25, 0.0)
    sleep(1)
    tree.decrease_brightness(tree.hmap[2], 0.5, 0.0)
    sleep(1)

    tree.off(tree.all)

    for n in range(0, 5):
        tree.increase_brightness(tree.all, 0.2, 0.05)
        sleep(0.2)

# Create Pinachtsbaum Object
tree = Pinachtsbaum()

#Switch everything off - including the Star
tree.illuminate_all(False)

demo_keystrokes()
sleep(1)
demo_dim()
sleep(1)
demo_quarters()
sleep(1)
demo_step_brightness()
sleep(1)
demo_height_map()
sleep(1)
demo_swirl()
sleep(1)
demo_ping()
sleep(1)
demo_all()
sleep(1)
demo_patterns()
sleep(1)
demo_beat()
sleep(1)
demo_blinking()


##
# Leave this at the end of your implementation. When the
# program terminates, your tree gets reset otherwise:
pause()

