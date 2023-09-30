#Author(s): Owen Walbridge, 2023 | 

import screen_dimensions

class logic:
    def __init__(self, screen_dimensions):
        self.screen_dimensions = screen_dimensions

    # Adjust variables to the width and height of the screen
    def width_adjust(self, x: int) -> int:
        """
        Adjust variables to the width of the screen
        """
        return int(x/1920 * self.screen_dimensions.get_width())

    def height_adjust(self, y: int) -> int:
        """
        Adjust variables to the height of the screen
        """
        return int(y/1080 * self.screen_dimensions.get_height())

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