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