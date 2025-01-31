#Author(s): Owen Walbridge, 2023 | 

import os
import sys
import os.path
import file_io
from screen_dimensions import ScreenDimensions
from gui import GUI

# Todo: Add error handling
# We need to check what we're loading. If a user modifies an app file, 
# it's corrupted or the app updates it wrongly, the whole app doesnt run and the 
# user needs to delete the config.txt & customise.txt files.
def initialise():
    """
    Initialise the app by loading settings from config.txt and customise.txt.
    return: screen_dimensions, input_type, theme, scale, text_theme, butt_theme, butt_hover_theme
    """
    screen_dimensions = ScreenDimensions()
    # Check if config.txt exists, if not, make it
    if (os.path.isfile("config.txt") == False):
        screen_width = screen_dimensions.get_width() # Detected screen width
        screen_height = screen_dimensions.get_height() # Detected screen height
        file_io.write_default_config(screen_width, screen_height)
    
    # Set config variables from file
    temp = file_io.read("config.txt")
    screen_dimensions.set_width(int(temp[0]))
    screen_dimensions.set_height(int(temp[1])) 
    input_type = temp[2] 
    
    # Check if custom.txt exists, if not, make it
    if (os.path.isfile("custom.txt") == False):
        file_io.write_default_custom()

    # Set customisation variables from file
    temp = file_io.read("custom.txt")
    theme = temp[0] 
    scale = temp[1]
    text_theme = temp[2]
    butt_theme = temp[3]
    butt_hover_theme = temp[4]

    return screen_dimensions, input_type, theme, scale, text_theme, butt_theme, butt_hover_theme

def main():
    """
    Main function. Initialises the app and starts the GUI.
    return: None
    """
    screen_dimensions, input_type, theme, scale, text_theme, butt_theme, butt_hover_theme = initialise()
    app = GUI(screen_dimensions, input_type, theme, scale, text_theme, butt_theme, butt_hover_theme)
    app.mainloop()

if __name__ == "__main__":
    main()