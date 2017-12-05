#  Pinachtsbaum
#  Copyright 2017 Thomas Johannesmeyer
#
#  Licensed under the "THE BEER-WARE LICENSE" (Revision 42):
#  Thomas Johannesmeyer wrote this file. As long as you retain this notice you
#  can do whatever you want with this stuff. If we meet some day, and you think
#  this stuff is worth it, you can buy me a beer or coffee in return


import collections
from gpiozero import LEDBoard
from gpiozero.tools import random_values
import time
from time import sleep
from threading import Timer
import random
from sets import Set


class Pinachtsbaum:

    # Maps the numbers written on the PCB to the actual led IDs
    led_map = {
            0: 0,
            1: 2,
            2: 13,
            3: 11,
            4: 19,
            5: 23,
            6: 6,
            7: 3,
            8: 8,
            9: 14,
            10: 15,
            11: 25,
            12: 24,
            13: 22,
            14: 7,
            15: 10,
            16: 4,
            17: 18,
            18: 17,
            19: 12,
            20: 16,
            21: 9,
            22: 5,
            23: 21,
            24: 20
            }

    # Maps Sides
    smap = {
            "LEFT_FRONT" : (4, 12, 18),
            "LEFT_BACK" : (17, 3, 9),
            "RIGHT_FRONT" : (2, 20, 11),
            "RIGHT_BACK" : (19, 1, 10),
            "FRONT_LEFT" : (15, 7, 21),
            "FRONT_RIGHT" : (22, 16, 6),
            "BACK_LEFT" : (23, 13, 5),
            "BACK_RIGHT" : (8, 24, 14) }

    # Maps Quarters
    qmap = {
            "FRONT_LEFT" : (smap["LEFT_FRONT"], smap["FRONT_LEFT"]),
            "FRONT_RIGHT" : (smap["RIGHT_FRONT"], smap["FRONT_RIGHT"]),
            "BACK_RIGHT" : (smap["BACK_RIGHT"], smap["RIGHT_BACK"]),
            "BACK_LEFT" : (smap["BACK_LEFT"], smap["LEFT_BACK"]),
            }

    ##
    # Height Map. Each surface has 3 LEDs. Maps 0 to 3 to vertical
    # layers. 0 being the bottom, 3 being the star
    hmap = {
            0: (4, 15, 22, 2, 19, 8, 23, 17),
            1: (12, 7, 16, 20, 1, 24, 13, 3),
            2: (18, 21, 6, 11, 10, 14, 5, 9),
            3: (0)
            }

    all = (22, 16, 20, 2, 19, 24, 8, 13, 23, 3, 17, 4, 15, 6, 11, 1, 10, 14, 5, 9, 18, 12, 7, 21, 0)
    #  all = (4, 19, 8, 22,)

    engaged_leds = Set([]) # Keeps track of leds currently switched on
    tree = LEDBoard(*range(2,28),pwm=True) # Contains all LEDs

    break_loops = False

    # Use Borg-Pattern in case multiple instances of this tree occur
    __shared_state = {}

    def __init__(self):
        self.__dict__ = self.__shared_state
        self.secure_random = random.SystemRandom()


    def read_indexes(self, delay):
        """
        Blinks each LED from index 0 (star) to index 25. (2 is n.a.) for 'delay' seconds.
        This function was used to create the led_map. And has no other purpose.
        """

        for led_id in range(0, 26):
            print(led_id)
            tree[led_id].on()
            sleep(delay)
            tree[led_id].off()


    def break_loops():
        """
        This breaks running loops like "Ambient Glow"
        """

        self.break_loops = True


    def __engage_led(self, led_id):
        """
        Private Method. Adds engaged LED to set.
        This function takes numbers and iterables.
        """

        if isinstance(led_id, collections.Iterable):
            # User passed a pattern
            for lid in led_id:
                self.__engage_led(lid)
        else:
            self.engaged_leds.add(led_id)
            # Debugging:
            #  print("Engaged: " + str(led_id) + " Engaged: " + str(self.engaged_leds))


    def __disengage_led(self, led_id):
        """
        Private Method. Removes disengaged LED to set.
        This function takes numbers and iterables.
        """

        if isinstance(led_id, collections.Iterable):
            # User passed a pattern
            for lid in led_id:
                self.__disengage_led(lid)
        else:
            # Debugging:
            #  print("Disengaged: " + str(led_id) + " from " + str(self.engaged_leds))
            if led_id in self.engaged_leds:
                self.engaged_leds.remove(led_id)


    def on(self, led_id):
        """
        Switches on provided led_id(s).
        This function takes numbers and iterables.
        """

        if isinstance(led_id, collections.Iterable):
            # User passed a pattern
            for lid in led_id:
                self.on(lid)
        else:
            self.tree[self.led_map[led_id]].on()
            self.__engage_led(led_id)


    def off(self, led_id):
        """
        Switches off provided led_id(s).
        This function takes numbers and iterables.
        """

        if isinstance(led_id, collections.Iterable):
            # User passed a pattern
            for lid in led_id:
                self.off(lid)
        else:
            self.tree[self.led_map[led_id]].off()
            self.__disengage_led(led_id)


    def illuminate_led(self, led_id, status, delay, auto_off):
        """
        Illuminates LED according to the numbers written on the pcb. These values are pulled
        from the led_map. This function takes numbers and iteratables
        """

        #  if type(led_id) in [list,tuple]:
        if isinstance(led_id, collections.Iterable):
            # User passed a pattern
            for lid in led_id:
                self.illuminate_led(lid, status, delay, auto_off)
        else:
            if delay > 0:
                sleep(delay) # Sleep(0) would still cause small delay
            if status:
                self.on(led_id)
                if auto_off > 0:
                    Timer(auto_off, self.off, [led_id]).start()
            else:
                self.off(led_id)
                self.__disengage_led(led_id)


    def illuminate_all(self, status):
        """
        Apply status to all LEDs.
        True = On
        False = Off
        """

        for led in self.tree:
            if status:
                led.on()
            else:
                led.off()


    def start_blinking(self, led_id, on_time, off_time):
        """
        Starts blinking for provided led_id(s).
        This function takes numbers and iterables
        """

        if isinstance(led_id, collections.Iterable):
            # User passed a pattern
            for lid in led_id:
                self.start_blinking(lid, on_time, off_time)
        else:
            self.tree[self.led_map[led_id]].blink(on_time=on_time, off_time=off_time, n=None, background=True)


    def ping(self, off_time):
        """
        Pop a random LED and kill it after 'off_time'
        """

        available_leds = Set(self.all).difference(Set([0])).difference(self.engaged_leds)
        if len(available_leds) > 0:
            random = self.secure_random.choice(list(available_leds))
            self.illuminate_led(random, True, 0, off_time)


    def ping_with_token(self):
        """
        Turns ON a random LED and returns a token which can later be used to switch it off.
        """

        available_leds = Set(self.all).difference(Set([0])).difference(self.engaged_leds)
        if len(available_leds) > 0:
            random = self.secure_random.choice(list(available_leds))
            self.illuminate_led(random, True, 0, 0)
            return random


    def swirl(self, duration, chain_length, inorder):
        """
        Performs a swirl with duration
        """

        delta = duration / float(len(self.all))
        if inorder:
            for led_id in self.all:
                self.illuminate_led(led_id, True, delta, chain_length*delta)
        else:
            for led_id in reversed(self.all):
                self.illuminate_led(led_id, True, delta, chain_length*delta)


    def random_with_beat(self, bpm):
        """
        Set random value to each LED for a beat
        """

        for led in self.tree:
            led.source_delay = 60/float(bpm)
            led.source = random_values()


    def random(self, delay):
        """
        Set random value to each LED every 'delay' seconds
        """

        for led in tree:
            led.source_delay = delay
            led.source = random_values()


    def __source_dim(self, source_value, destination_value, duration, returns):
        """
        Private Method. Only used by led.source to determine dim values.
        """
        step_count = 25
        if duration < 0.1:
            step_count = 5
        elif duration < 0.2:
            step_count = 10
        elif duration < 0.5:
            step_count = 25
        elif duration < 1.0:
            step_count = 50
        else:
            step_count = 100

        delta_time = duration/float(step_count)
        delta_step = (destination_value - source_value) / float(step_count)

        for n in range(1, step_count + 1):
            yield(min(1, source_value + delta_step * n))
            sleep(delta_time)

        if returns:
            for n in range(1, step_count + 1):
                yield(max(0, destination_value - delta_step * n))
                sleep(delta_time)


    def dim(self, led_id, value, delay, duration, returns):
        """
        Dims led_id(s) from current value over 'duration' to destination 'value'.
        If the flag 'returns' is set to True, it will dim back to original value.
        This function takes numbers and iterables.
        """

        if isinstance(led_id, collections.Iterable):
            # User passed a pattern
            for lid in led_id:
                self.dim(lid, value, delay, duration, returns)
        else:
            if delay > 0:
                sleep(delay) # Sleep(0) would still cause small delay

            source_value = self.tree[self.led_map[led_id]].value
            self.tree[self.led_map[led_id]].source = self.__source_dim(source_value, value, duration, returns)


    def increase_brightness(self, led_id, amount, delay):
        """
        Increases led(s) brightness by a fixed amount.
        This function takes numbers and iterables.
        """

        if isinstance(led_id, collections.Iterable):
            # User passed a pattern
            for lid in led_id:
                self.increase_brightness(lid, amount, delay)
        else:
            if delay > 0:
                sleep(delay) # Sleep(0) would still cause small delay

            source_value = self.tree[self.led_map[led_id]].value
            destination_value = source_value + amount
            self.tree[self.led_map[led_id]].value = min(1.0, destination_value)


    def decrease_brightness(self, led_id, amount, delay):
        """
        Decreases led(s) brightness by a fixed amount.
        This function takes numbers and iterables.
        """

        if isinstance(led_id, collections.Iterable):
            # User passed a pattern
            for lid in led_id:
                self.decrease_brightness(lid, amount, delay)
        else:
            if delay > 0:
                sleep(delay) # Sleep(0) would still cause small delay

            source_value = self.tree[self.led_map[led_id]].value
            destination_value = source_value - amount
            self.tree[self.led_map[led_id]].value = max(0.0, destination_value)


    def ambient_glow(self, intensity, period_duration):
        """
        Engages ambient mode with custom settings.
        """

        # Dim to solid 10% brightness as a starting glow
        self.dim(self.all, 0.1, 0.0, 0.5, False)
        sleep(0.6)

        while True:
            self.dim(self.all, intensity, 0.2, period_duration, True)
            sleep(period_duration)
            if self.break_loops:
                break;

        self.break_loops = False

