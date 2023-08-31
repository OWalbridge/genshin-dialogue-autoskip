# Imports ----------------------------------------------------------------------
from typing import Tuple, Union
from datetime import datetime
import os
import time

import pyautogui
from pynput.mouse import Controller
from pynput.keyboard import Key, KeyCode, Listener

try: # If on Windows, use win32api to get screen dimensions
    from win32api import GetSystemMetrics
except ImportError: # If not on Windows, use dummy function to return 1920x1080
    def GetSystemMetrics(metric):
        if metric == 0:
            return 1920
        elif metric == 1:
            return 1080

from random import randint, uniform
from threading import Thread

# Setup ------------------------------------------------------------------------
os.system('cls' if os.name == 'nt' else 'clear') # Clear terminal

# Get screen dimensions
SCREEN_WIDTH = GetSystemMetrics(0)
SCREEN_HEIGHT = GetSystemMetrics(1)

#Incase the resolution is not correct
print ('\nWelcome to Genshin Impact Dialogue Skipper')
print('Detected Resolution: ' + str(SCREEN_WIDTH) + 'x' + str(SCREEN_HEIGHT))
print('\nIs the resolution correct? (y/n)')
input = input()
if input == 'n' or input == 'N':
    print('Enter resolution width: ')
    SCREEN_WIDTH = int(input())
    print('Enter resolution height: ')
    SCREEN_HEIGHT = int(input())
    print('\nNew resolution set to ' + str(SCREEN_WIDTH) + 'x' + str(SCREEN_HEIGHT) + '\n')

# 'Constants' ------------------------------------------------------------------

menu = ('-------------\n'
          'Press:\n'
          'F8 to start\n'
          'F9 to stop\n'
          'F10 for help\n'
          'F12 to quit\n'
          '-------------\n')

# Adjust variables to the width and height of the screen
def width_adjust(x: int) -> int:
    """
    Adjust variables to the width of the screen
    """
    return int(x/1920 * SCREEN_WIDTH)

def height_adjust(y: int) -> int:
    """
    Adjust variables to the height of the screen
    """
    return int(y/1080 * SCREEN_HEIGHT)

# Dimensions of bottom dialogue option.
BOTTOM_DIALOGUE_MIN_X: int = width_adjust(1300)
BOTTOM_DIALOGUE_MAX_X: int = width_adjust(1700)
BOTTOM_DIALOGUE_MIN_Y: int = height_adjust(790)
BOTTOM_DIALOGUE_MAX_Y: int = height_adjust(800)

# Pixel coordinates for white part of the autoplay button.
PLAYING_ICON_X = width_adjust(84)
PLAYING_ICON_Y = height_adjust(46)

# Pixel coordinates for white part of the speech bubble in bottom dialogue option.
DIALOGUE_ICON_X = width_adjust(1301)
DIALOGUE_ICON_LOWER_Y = height_adjust(808)
DIALOGUE_ICON_HIGHER_Y = height_adjust(790)

# Pixel coordinates near middle of the screen known to be white while the game is loading.
LOADING_SCREEN_X: int = width_adjust(1200)
LOADING_SCREEN_Y: int = height_adjust(700)

# Functions --------------------------------------------------------------------
def get_pixel(x: int, y: int) -> Tuple[int, int, int]:
    """
    Return the RGB value of a pixel.
    :param x: The x coordinate of the pixel.
    :param y: The y coordinate of the pixel.
    :return: The RGB value of the pixel.
    """

    return pyautogui.pixel(x, y)


def random_interval() -> float:
    """
    Return a random interval between 0.12 and 0.18 seconds, or 0.18 and 0.2 seconds if a 6 is rolled.
    :return: A random interval between 0.12 and 0.18 seconds, or 0.18 and 0.3 seconds if a 6 is rolled.
    """

    return uniform(0.18, 0.2) if randint(1, 6) == 6 else uniform(0.12, 0.18)


def random_cursor_position() -> Tuple[int, int]:
    """
    The cursor is moved to a random position in the bottom dialogue option.
    :return: A random (x, y) in range of the bottom dialogue option.
    """

    x = randint(BOTTOM_DIALOGUE_MIN_X, BOTTOM_DIALOGUE_MAX_X)
    y = randint(BOTTOM_DIALOGUE_MIN_Y, BOTTOM_DIALOGUE_MAX_Y)

    return x, y



def exit_program() -> None:
    """
    Listen for keyboard input to start, stop, or exit the program.
    :return: None
    """

    def on_press(key: (Union[Key, KeyCode, None])) -> None:
        """
        Start, stop, or exit the program based on the key pressed.
        :param key: The key pressed.
        :return: None
        """

        key_pressed: str = str(key)

        if key_pressed == 'Key.f8':
            main.status = 'run'
            print('RUNNING')
        elif key_pressed == 'Key.f9':
            main.status = 'pause'
            print('PAUSED')
        elif key_pressed == 'Key.f10':
            print(menu)
        elif key_pressed == 'Key.f12':
            main.status = 'exit'
            exit()

    with Listener(on_press=on_press) as listener:
        listener.join()


# Main program -----------------------------------------------------------------
def main() -> None:
    """
    Skip Genshin Impact dialogue when it's present based on the colors of 3 specific pixels.
    :return: None
    """
    def is_dialogue_playing():
        return get_pixel(PLAYING_ICON_X, PLAYING_ICON_Y) == (236, 229, 216)

    def is_dialogue_option_available():
        # Confirm loading screen is not white
        if get_pixel(LOADING_SCREEN_X, LOADING_SCREEN_Y) == (255, 255, 255):
            return False

        # Check if lower dialogue icon pixel is white
        if get_pixel(DIALOGUE_ICON_X, DIALOGUE_ICON_LOWER_Y) == (255, 255, 255):
            return True

        # Check if higher dialogue icon pixel is white
        if get_pixel(DIALOGUE_ICON_X, DIALOGUE_ICON_HIGHER_Y) == (255, 255, 255):
            return True

        return False

    main.status = 'pause'
    last_reposition: float = 0.0
    time_between_repositions: float = random_interval() * 40
    print(menu)

    while True:
        while main.status == 'pause':
            sleep(0.5)

        if main.status == 'exit':
            print('Main program closing')
            break

        if is_dialogue_playing() or is_dialogue_option_available():
            if time() - last_reposition > time_between_repositions:
                current_time = datetime.now().strftime("%H:%M:%S")
                print(str(current_time) + ': Selecting dialogue')
                last_reposition = time()
                time_between_repositions = random_interval() * 40
                mouse.position = random_cursor_position()
                pyautogui.click()


if __name__ == "__main__":
    mouse = Controller()
    Thread(target=main).start()
    Thread(target=exit_program).start()