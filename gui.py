#Author(s): Owen Walbridge

#Notes:
#
# Adding the console to the application was a design choice as many younger 
# and/or less tech savy users might not know how to navigate to a file 
# directory. Remember kids play Genshin too! 
# This allows them to more easily submit issues to us. <3

#TODOs (More info in comments at relevent parts of code):
#
# Append time to start of console output
# Add more console error catching (if needed)

# Imports ----------------------------------------------------------------------
import tkinter as tk
import sys
import os
from datetime import datetime
from logic import GenshinImpactDialogueSkipper
import customtkinter

try: # If on Windows, use win32api to get screen dimensions
    from win32api import GetSystemMetrics
except ImportError: # If not on Windows, use dummy function to return 1920x1080
    def GetSystemMetrics(metric):
        if metric == 0:
            return 1920
        elif metric == 1:
            return 1080

# Global Variables -------------------------------------------------------------
customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

# These need to be global to load them into the UI and create init config file
# as opposed to class attributes
SCREEN_WIDTH = GetSystemMetrics(0)
SCREEN_HEIGHT = GetSystemMetrics(1)

# Config -----------------------------------------------------------------------

try: # Check for existing config
    file = open("config.txt", "r")
    file.close()
except: # If no config, create default one
    file = open("config.txt", "w")
    file.write(str(SCREEN_WIDTH) + "|" + str(SCREEN_HEIGHT) + "|Keyboard|System|#1f6aa5|#134870|White|100%")
    file.close()

# Load themes from config
file = open("config.txt", "r")
config = file.read().split("|")
butt_theme = config[4]
butt_hover_theme = config[5]
text_theme = config[6]
file.close()

class SkipperGUI(customtkinter.CTk):
    # Class attributes ---------------------------------------------------------

    # GUI ----------------------------------------------------------------------
    def __init__(self):
        super().__init__()

        global SCREEN_WIDTH
        global SCREEN_HEIGHT

        # Configure window
        self.title("Genshin Impact Dialogue Skip")
        self.deiconify()
        self.geometry(f"{380}x{430}")
        self.resizable(False, False)

        # Set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Navigation frame -----------------------------------------------------
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(3, weight=1)

        # - Navigation frame logo
        self.navigation_frame_label = customtkinter.CTkLabel(self.navigation_frame, text="Dialogue Skipper",
                                                             font=customtkinter.CTkFont(size=15, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)
        # - Start/Stop Buttons
        self.start_button = customtkinter.CTkButton(self.navigation_frame, command=self.start_button_event, text="Start", fg_color=('green'), hover_color=('darkgreen'))
        self.start_button.grid(row=1, column=0, padx=20, pady=10)
        self.stop_button = customtkinter.CTkButton(self.navigation_frame, command=self.stop_button_event, text="Stop", fg_color=('red'), hover_color=('darkred'))
        self.stop_button.grid(row=2, column=0, padx=20, pady=10)
        # - configure Button
        self.configure_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Configure",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30")
                                                   , command=self.configure_button_event)
        self.configure_button.grid(row=4, column=0, sticky="ew")
        # - Readme Button
        self.readme_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Read Me!",
                                                    fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30")
                                                    , command=self.readme_button_event)
        self.readme_button.grid(row=7, column=0, sticky="ew")
        # - Console Button
        self.console_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Console",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30")
                                                   , command=self.console_button_event)
        self.console_button.grid(row=6, column=0, sticky="ew")
        # - Customise Button
        self.customise_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Customise",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30")
                                                   , command=self.customise_button_event)
        self.customise_button.grid(row=5, column=0, sticky="ew")

        # Configure frame -----------------------------------------------------------
        self.configure_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.configure_frame.grid_columnconfigure(0, weight=0)

        # Resolution
        self.configure_resolution_label = customtkinter.CTkLabel(self.configure_frame, text="Current Resolution:\n" + str(SCREEN_WIDTH) + 'x' + str(SCREEN_HEIGHT), anchor="w")
        self.configure_resolution_label.grid(row=1, column=0, padx=30, pady=(15, 0))

        self.configure_resolution_entry_width = customtkinter.CTkEntry(self.configure_frame, placeholder_text="Enter custom width")
        self.configure_resolution_entry_width.grid(row=2, column=0, padx=30, pady=(10, 10))
        self.configure_resolution_entry_height = customtkinter.CTkEntry(self.configure_frame, placeholder_text="Enter custom height")
        self.configure_resolution_entry_height.grid(row=3, column=0, padx=30, pady=(10, 10))

        self.configure_resolution_button = customtkinter.CTkButton(self.configure_frame,command = self.update_resolution_button_event, text="Update Resolution", fg_color=butt_theme, hover_color=butt_hover_theme, text_color=text_theme )
        self.configure_resolution_button.grid(row=4, column=0, padx=20, pady=(10, 10)) 

        # Configure Input Method
        self.configure_input_method_label = customtkinter.CTkLabel(self.configure_frame, text="Input Method:", anchor="w")
        self.configure_input_method_label.grid(row=5, column=0, padx=30, pady=(10, 0))
        self.configure_input_method_optionemenu = customtkinter.CTkOptionMenu(self.configure_frame, values=["Keyboard"],
                                                                            command=self.change_input_type_event, fg_color=butt_theme, text_color=text_theme)
        self.configure_input_method_optionemenu.grid(row=6, column=0, padx=30, pady=(10, 10))

        # Save Button
        self.configure_save_label = customtkinter.CTkLabel(self.configure_frame, text="Save config:", anchor="w")
        self.configure_save_label.grid(row=7, column=0, padx=30, pady=(10, 0))
        self.configure_save_button = customtkinter.CTkButton(self.configure_frame, text="Save config", fg_color=butt_theme, hover_color=butt_hover_theme, text_color=text_theme)
        self.configure_save_button.grid(row=8, column=0, padx=20, pady=(10, 10))

        # Notice
        self.configure_input_method_label = customtkinter.CTkLabel(self.configure_frame, text="Remember to enable\nautoskip!", anchor="w")
        self.configure_input_method_label.grid(row=9, column=0, padx=30, pady=(10, 10))

        # Readme frame ---------------------------------------------------------
        self.readme_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.readme_frame.grid_columnconfigure(0, weight=0)

        # Textbox
        self.readme_frame_txtbox = customtkinter.CTkTextbox(master = self.readme_frame, corner_radius=0,height = 430, state = "disabled", wrap = "word")
        self.readme_frame_txtbox.grid(row=0, column=0)
        self.readme_frame_txtbox.grid(row=0, column=0, sticky="nsew")

        # Console frame --------------------------------------------------------
        self.console_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent") 
        self.console_frame.grid_columnconfigure(0, weight=0)

        # Textbox
        self.console_frame_txtbox = customtkinter.CTkTextbox(master = self.console_frame, corner_radius=0,height = 380, state = "disabled", wrap = "word")
        self.console_frame_txtbox.grid(row=0, column=0)
        self.console_frame_txtbox.grid(row=0, column=0, sticky="nsew")

        # Export Button
        self.console_frame_export_button = customtkinter.CTkButton(self.console_frame, command=self.export_button_event, text="Export", fg_color=butt_theme, hover_color=butt_hover_theme, text_color=text_theme)
        self.console_frame_export_button.grid(row=1, column=0, padx=20, pady=10)

        # Customise frame ------------------------------------------------------
        self.customise_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.customise_frame.grid_columnconfigure(0, weight=0)
        # Appearance Mode
        self.appearance_mode_label = customtkinter.CTkLabel(self.customise_frame, text="Appearance:", anchor="w")
        self.appearance_mode_label.grid(row=1, column=0, padx=30, pady=(15, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.customise_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event, fg_color=butt_theme, text_color=text_theme)
        self.appearance_mode_optionemenu.grid(row=2, column=0, padx=30, pady=(10, 10))
        # Theme
        self.custom_theme_label = customtkinter.CTkLabel(self.customise_frame, text="Custom Theme:\n(updates on restart)", anchor="e")
        self.custom_theme_label.grid(row=3, column=0, padx=30, pady=(10, 0))

        self.custom_theme_entry_fg_color = customtkinter.CTkEntry(self.customise_frame, placeholder_text="Button HEX")
        self.custom_theme_entry_fg_color.grid(row=4, column=0, padx=30, pady=(10, 10))

        self.custom_theme_entry_hover_color = customtkinter.CTkEntry(self.customise_frame, placeholder_text="Button hover HEX")
        self.custom_theme_entry_hover_color.grid(row=5, column=0, padx=30, pady=(10, 10))

        self.custom_theme_text_optionmenu = customtkinter.CTkOptionMenu(self.customise_frame, values=["White text", "Black text"],
                                                                          command=self.change_theme_event, fg_color=butt_theme, text_color=text_theme)
        self.custom_theme_text_optionmenu.grid(row=6, column=0, padx=30, pady=(10, 10))

        self.custom_theme_update_button = customtkinter.CTkButton(self.customise_frame, text="Update theme", command=self.change_theme_event, fg_color=butt_theme, hover_color=butt_hover_theme, text_color=text_theme)
        self.custom_theme_update_button.grid(row=7, column=0, padx=20, pady=(10, 10))

        # Scaling
        self.scaling_label = customtkinter.CTkLabel(self.customise_frame, text="Scale:", anchor="w")
        self.scaling_label.grid(row=8, column=0, padx=30, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.customise_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event, fg_color=butt_theme, text_color=text_theme)
        self.scaling_optionemenu.grid(row=9, column=0, padx=30, pady=(10, 20))

        # Set default values ---------------------------------------------------
        self.stop_button.configure(state="disabled", fg_color=('darkred'))
        self.configure_input_method_optionemenu.set("Keyboard")
        self.select_frame_by_name("configure")

        # Load custom config.txt
        try:
            file = open("config.txt", "r")
            config = file.read().split("|")

            # Set appearance mode
            self.appearance_mode_optionemenu.set(config[3]) 
            customtkinter.set_appearance_mode(config[3])

            # Set scaling
            self.scaling_optionemenu.set(config[7])
            new_scaling_float = int(config[7].replace("%", "")) / 100
            customtkinter.set_widget_scaling(new_scaling_float)
            customtkinter.set_window_scaling(new_scaling_float)

            # Set resolution
            SCREEN_WIDTH = int(config[0])
            SCREEN_HEIGHT = int(config[1])
            self.configure_resolution_label.configure(text="Current Resolution:\n" + str(SCREEN_WIDTH) + 'x' + str(SCREEN_HEIGHT))

            # Set input method
            self.configure_input_method_optionemenu.set(config[2])


        except:
            self.appearance_mode_optionemenu.set("System")
            self.scaling_optionemenu.set("100%")
        
        self.readme_frame_txtbox.configure(state='normal') # enable editing
        self.readme_frame_txtbox.insert("0.0", "WARNING: There is a possibility you get banned for using this program. Use at your own risk!\n\nHow to use:\nEnsure the \"current resolution\" and \"input method\" are correct and hit \"start\". Head back to Genshin and dialoge will be auto clicked.\n\nThis program detects pixel colors to determine when to skip dialogue. It can misfire; disable when not in dialogue.\n\nThis project is under the MIT License.\n\n Contributors:\n-Hubert Rozmarynowski\n(Git Management, Pixel Coordiantes, Dialogue Selection, Documentation)\n\n-Owen Walbridge\n(UI, All Res Support, Fixes, Documentation)\n\n-xdenotte\n(Xbox Support)\n\n-Vamqueror\n(Dialog Selection, Fixes)\n\n-vlsido\n(DS4 Support)\n\n-YotamZiv298\n(Documentation and Code Clarity)")
        self.readme_frame_txtbox.configure(state='disabled') # disable editing
        
    
        # Console Setup --------------------------------------------------------

        def console(*args, **kwargs):
            text = ' '.join(str(arg) for arg in args)

            # TODO: Append time to start of console output
            # ! Currently not working becuase it's also appending it to the end
            # ! I've tried substrings to no avail, need to look into it
            #current_time = datetime.now().strftime("%H:%M:%S")
            #output = str(current_time) + ": " + str(text)

            self.console_frame_txtbox.configure(state='normal') # enable editing
            self.console_frame_txtbox.insert("end", text)
            self.console_frame_txtbox.see("end")
            self.console_frame_txtbox.configure(state='disabled') # disable editing
        
        # TODO: Add more error catching (if needed)
        sys.stdout.write = console
        sys.stderr.write = console
        sys.excepthook = console
    
    # Functions ----------------------------------------------------------------
    def current_date(self):
        now = datetime.now()
        current_date = str(now.strftime("%d-%m-%Y"))
        return current_date

    def current_time(self):
        now = datetime.now()
        current_time = str(now.strftime("%H-%M-%S"))
        return current_time
    
    # Event handlers -----------------------------------------------------------

    def select_frame_by_name(self, name):
        self.configure_button.configure(fg_color=("gray75", "gray25") if name == "configure" else "transparent")
        self.readme_button.configure(fg_color=("gray75", "gray25") if name == "readme" else "transparent")
        self.console_button.configure(fg_color=("gray75", "gray25") if name == "console" else "transparent")
        self.customise_button.configure(fg_color=("gray75", "gray25") if name == "customise" else "transparent")

        # Show the selected frame
        if name == "configure":
            self.configure_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.configure_frame.grid_forget()
        if name == 'readme':
            self.readme_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.readme_frame.grid_forget()
        if name == 'console':
            self.console_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.console_frame.grid_forget()
        if name == 'customise':
            self.customise_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.customise_frame.grid_forget()

    # Navigation Frame Event Handlers ------------------
    def start_button_event(self):
        #print("Start button clicked")
        self.stop_button.configure(state="normal", fg_color=('red'))
        self.start_button.configure(state="disabled", fg_color=('darkgreen'))
        
    def stop_button_event(self):
        #print("Stop button clicked")
        self.stop_button.configure(state="disabled", fg_color=('darkred'))
        self.start_button.configure(state="normal", fg_color=('green'))

    def configure_button_event(self):
        #print("Configure button clicked")
        self.select_frame_by_name("configure")

    def readme_button_event(self):
        #print("Readme button clicked")
        self.select_frame_by_name("readme")
    
    def console_button_event(self):
        #print("Console button clicked")
        self.select_frame_by_name("console")

    def customise_button_event(self):
        #print("Customise button clicked")
        self.select_frame_by_name("customise")

    # configure Frame Event Handlers -------------------------
    def update_resolution_button_event(self):
       #print("Update Resolution button clicked")

        width_entry = self.configure_resolution_entry_width.get()
        height_entry = self.configure_resolution_entry_height.get()
        if width_entry and height_entry:  # Check if both entries are not empty
            try:
                global SCREEN_WIDTH
                global SCREEN_HEIGHT
                SCREEN_WIDTH = int(width_entry)
                SCREEN_HEIGHT = int(height_entry)
                print("Resolution updated to " + str(SCREEN_WIDTH) + 'x' + str(SCREEN_HEIGHT))
            except ValueError:
                print("Invalid input. Please enter valid integers for width and height.")
        else:
            print("Please enter values for both width and height.")
        self.configure_resolution_label.configure(text="Current Resolution:\n" + str(SCREEN_WIDTH) + 'x' + str(SCREEN_HEIGHT))

    def change_input_type_event(self, new_input_type: str):
        print("Input type changed to " + new_input_type)

    # Console Frame Event Handlers ---------------------
    def export_button_event(self):
        #print("Export button clicked")
        try:
            file_name = self.current_time() + "_" + self.current_date() + ".log"
            file = open("./console_logs/" + file_name, "w")
            file.write(self.console_frame_txtbox.get("0.0", "end"))
            file.close()
            print("Console output exported")
            try:
                os.startfile(os.path.realpath("./console_logs"))
            except:
                print("Error: Could not open console_logs folder")
        except:
            print("Error: Could not export console output")
        
    # Customisation Frame Event Handlers ---------------
    def change_appearance_mode_event(self, new_appearance_mode: str):
        print("Appearance changed to " + new_appearance_mode)
        customtkinter.set_appearance_mode(new_appearance_mode)
    
    def change_theme_event(self):
        #print("Theme button clicked")
        try: 
            theme = self.custom_theme_entry.get()
            print("Theme changed to " + theme)
        except:
            print("Invalid Input. Please enter a valid hex code.")
        else:
            print("Please enter a hex value")

    def change_scaling_event(elf, new_scaling: str):
        print("Scaling changed to " + new_scaling)
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)
        customtkinter.set_window_scaling(new_scaling_float)

# For testing GUI only purposes (Commented out when not in use) ----------------
#if __name__ == "__main__":
#    app = SkipperGUI()
#    app.mainloop()