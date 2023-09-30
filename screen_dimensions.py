#Author(s): Owen Walbridge, 2023 | 

try: # If on Windows, use win32api to get screen dimensions
    from win32api import GetSystemMetrics
except ImportError: # If not on Windows, use dummy function to return 1920x1080
    def GetSystemMetrics(metric):
        if metric == 0:
            return 1920
        elif metric == 1:
            return 1080

class ScreenDimensions:
    def __init__(self):
        self.width = GetSystemMetrics(0)
        self.height = GetSystemMetrics(1)

        # Dimensions of bottom dialogue option.
        self.BOTTOM_DIALOGUE_MIN_X: int = self.width_adjust(1300)
        self.BOTTOM_DIALOGUE_MAX_X: int = self.width_adjust(1700)
        self.BOTTOM_DIALOGUE_MIN_Y: int = self.height_adjust(790)
        self.BOTTOM_DIALOGUE_MAX_Y: int = self.height_adjust(800)

        # Pixel coordinates for white part of the speech bubble in bottom dialogue option.
        self.DIALOGUE_ICON_X = self.width_adjust(1301)
        self.DIALOGUE_ICON_LOWER_Y = self.height_adjust(808)
        self.DIALOGUE_ICON_HIGHER_Y = self.height_adjust(790)

        # Pixel coordinates near middle of the screen known to be white while the game is loading.
        self.LOADING_SCREEN_X: int = self.width_adjust(1200)
        self.LOADING_SCREEN_Y: int = self.height_adjust(700)

    def detect_width(self):
        return GetSystemMetrics(0)

    def detect_height(self):
        return GetSystemMetrics(1)

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def set_width(self, width):
        self.width = width

    def set_height(self, height):
        self.height = height

    # Pixel Adjustments
    def update_pixels(self):
       # Dimensions of bottom dialogue option.
        self.BOTTOM_DIALOGUE_MIN_X: int = self.width_adjust(1300)
        self.BOTTOM_DIALOGUE_MAX_X: int = self.width_adjust(1700)
        self.BOTTOM_DIALOGUE_MIN_Y: int = self.height_adjust(790)
        self.BOTTOM_DIALOGUE_MAX_Y: int = self.height_adjust(800)

        # Pixel coordinates for white part of the autoplay button.
        self.PLAYING_ICON_X = self.width_adjust(84)
        self.PLAYING_ICON_Y = self.height_adjust(46)

        # Pixel coordinates for white part of the speech bubble in bottom dialogue option.
        self.DIALOGUE_ICON_X = self.width_adjust(1301)
        self.DIALOGUE_ICON_LOWER_Y = self.height_adjust(808)
        self.DIALOGUE_ICON_HIGHER_Y = self.height_adjust(790)

        # Pixel coordinates near middle of the screen known to be white while the game is loading.
        self.LOADING_SCREEN_X: int = self.width_adjust(1200)
        self.LOADING_SCREEN_Y: int = self.height_adjust(700)

    def width_adjust(self, x: int) -> int:
        return int(x/1920 * self.get_width())

    def height_adjust(self, y: int) -> int:
        return int(y/1080 * self.get_height())
