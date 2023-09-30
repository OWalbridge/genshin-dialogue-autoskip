#Author(s): Owen Walbridge, 2023 | 

from typing import Tuple, Union

import os
import time

import pyautogui
from pynput.mouse import Controller
from pynput.keyboard import Key, KeyCode, Listener
from threading import Thread
from random import randint, uniform

import utils

class logic:
    def __init__(self, screen_dimensions):
        self.screen_dimensions = screen_dimensions
        self.stop_flag = False
        self.mouse = Controller()

    def start(self):
        self.stop_flag = False
        Thread(target=self.run).start()

    def stop(self):
        self.stop_flag = True

    def get_pixel(self, x: int, y: int) -> Tuple[int, int, int]:
        """
        Return the RGB value of a pixel.
        :param x: The x coordinate of the pixel.
        :param y: The y coordinate of the pixel.
        :return: The RGB value of the pixel.
        """

        return pyautogui.pixel(x, y)

    def random_interval(self) -> float:
        """
        Return a random interval between 0.12 and 0.18 seconds, or 0.18 and 0.2 seconds if a 6 is rolled.
        :return: A random interval between 0.12 and 0.18 seconds, or 0.18 and 0.3 seconds if a 6 is rolled.
        """

        return uniform(0.18, 0.2) if randint(1, 6) == 6 else uniform(0.12, 0.18)

    def random_cursor_position(self) -> Tuple[int, int]:
        """
        The cursor is moved to a random position in the bottom dialogue option.
        :return: A random (x, y) in range of the bottom dialogue option.
        """
        x = randint(self.screen_dimensions.BOTTOM_DIALOGUE_MIN_X, self.screen_dimensions.BOTTOM_DIALOGUE_MAX_X)
        y = randint(self.screen_dimensions.BOTTOM_DIALOGUE_MIN_Y, self.screen_dimensions.BOTTOM_DIALOGUE_MAX_Y)
        print(x, y)
        return x, y

    def run(self):
        """
        Skip Genshin Impact dialogue when it's present based on the colors of 3 specific pixels.
        :return: None
        """

        def is_dialogue_option_available():
            # Confirm loading screen is not white
            if self.get_pixel(self.screen_dimensions.LOADING_SCREEN_X, self.screen_dimensions.LOADING_SCREEN_Y) == (255, 255, 255):
                return False

            # Check if lower dialogue icon pixel is white
            if self.get_pixel(self.screen_dimensions.DIALOGUE_ICON_X, self.screen_dimensions.DIALOGUE_ICON_LOWER_Y) == (255, 255, 255):
                return True

            # Check if higher dialogue icon pixel is white
            if self.get_pixel(self.screen_dimensions.DIALOGUE_ICON_X, self.screen_dimensions.DIALOGUE_ICON_HIGHER_Y) == (255, 255, 255):
                return True

            return False

        last_reposition: float = 0.0
        time_between_repositions: float = self.random_interval() * 40

        while not self.stop_flag:
            if is_dialogue_option_available():
                if time.time() - last_reposition > time_between_repositions:
                    current_time = utils.current_time(":")
                    print(str(current_time) + ': Selecting dialogue')
                    last_reposition = time.time()
                    time_between_repositions = self.random_interval() * 40
                    self.mouse.position = self.random_cursor_position()
                    pyautogui.click()
                    print("Clicked")
