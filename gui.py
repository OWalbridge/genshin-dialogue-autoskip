#Author(s): Owen Walbridge, 2023 | 

#TODOs (More info in comments at relevent parts of code):
#
# Add more error handling
# Append time to start of console output (facing issues, see below)
# Add more console error catching (if possible)
# Find a way to update the theme without a restart needed? (uncertain if possible)

# Imports ----------------------------------------------------------------------
import sys

import tkinter as tk
import customtkinter

import event_handlers

class GUI(customtkinter.CTk):
    def __init__(self, screen_dimensions, input_type, theme, scale, text_theme, butt_theme, butt_hover_theme):
        """
        Initialise the GUI.
        :return: None
        """
        
        super().__init__()
        self.event_handlers = event_handlers.EventHandlers(self, screen_dimensions)
        self.screen_dimensions = screen_dimensions

        # UI Settings ----------------------------------------------------------

        # Set appearance mode
        customtkinter.set_appearance_mode(theme)

        # Configure window -----------------------------------------------------
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
        self.navigation_frame_label = customtkinter.CTkLabel(
            self.navigation_frame, text="Dialogue Skipper",
            font=customtkinter.CTkFont(size=15, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)
        # - Start/Stop Buttons
        self.start_button = customtkinter.CTkButton(self.navigation_frame, 
            command=self.event_handlers.start_button_event, text="Start", fg_color=('green'),
            hover_color=('darkgreen')) 
            # TODO text_color=(text_theme) <- Can add this, if users req ^
            # if you'd like but looks weird with black text, we need to make a 
            # text_color_disabled option if we want this featue
        self.start_button.grid(row=1, column=0, padx=20, pady=10)
        self.stop_button = customtkinter.CTkButton(self.navigation_frame, 
            command=self.event_handlers.stop_button_event, text="Stop", fg_color=('red'), 
            hover_color=('darkred'), text_color=(text_theme))
            # TODO text_color=(text_theme) <- Can add this, if users req^
            # if you'd like but looks weird with black text, we need to make a 
            # text_color_disabled option if we want this featue
        self.stop_button.grid(row=2, column=0, padx=20, pady=10)
        # - Reset Button
        self.reset_button = customtkinter.CTkButton(self.navigation_frame,
            command=self.event_handlers.reset_button_event, text="Reset ALL Settings", fg_color=butt_theme,
            hover_color=butt_hover_theme, text_color=(text_theme))
        self.reset_button.grid(row=3, column=0, padx=20, pady=(10,0))
        # - configure Button
        self.configure_button = customtkinter.CTkButton(self.navigation_frame, 
            corner_radius=0, height=40, border_spacing=10, text="Configure",
            fg_color="transparent", text_color=("gray10", "gray90"), 
            hover_color=("gray70", "gray30"), command=self.event_handlers.configure_button_event)
        self.configure_button.grid(row=6, column=0, sticky="ew")
        # - Readme Button
        self.readme_button = customtkinter.CTkButton(self.navigation_frame, 
            corner_radius=0, height=40, border_spacing=10, text="Read Me!",
            fg_color="transparent", text_color=("gray10", "gray90"), 
            hover_color=("gray70", "gray30"), command=self.event_handlers.readme_button_event)
        self.readme_button.grid(row=9, column=0, sticky="ew")
        # - Console Button
        self.console_button = customtkinter.CTkButton(self.navigation_frame, 
            corner_radius=0, height=40, border_spacing=10, text="Console",
            fg_color="transparent", text_color=("gray10", "gray90"), 
            hover_color=("gray70", "gray30"), command=self.event_handlers.console_button_event)
        self.console_button.grid(row=8, column=0, sticky="ew")
        # - Customise Button
        self.customise_button = customtkinter.CTkButton(self.navigation_frame, 
            corner_radius=0, height=40, border_spacing=10, text="Customise",
            fg_color="transparent", text_color=("gray10", "gray90"), 
            hover_color=("gray70", "gray30"), command=self.event_handlers.customise_button_event)
        self.customise_button.grid(row=7, column=0, sticky="ew")

        # Configure frame -----------------------------------------------------------
        self.configure_frame = customtkinter.CTkFrame(self, corner_radius=0, 
            fg_color="transparent")
        self.configure_frame.grid_columnconfigure(0, weight=0)

        # Resolution
        self.detected_resolution_label = customtkinter.CTkLabel(self.configure_frame, 
            text="Detected Resolution:\n" + str(self.screen_dimensions.detect_width()) + 'x' + str(self.screen_dimensions.detect_height()), anchor="w")
        self.detected_resolution_label.grid(row=1, column=0, padx=30, pady=(30, 0))

        self.configure_resolution_label = customtkinter.CTkLabel(self.configure_frame, 
            text="Current Resolution:\n" + str(self.screen_dimensions.get_width()) + 'x' + str(self.screen_dimensions.get_height()), anchor="w")
        self.configure_resolution_label.grid(row=2, column=0, padx=30, pady=(15, 0))

        self.configure_resolution_entry_width = customtkinter.CTkEntry(self.configure_frame, 
            placeholder_text="Enter custom width")
        self.configure_resolution_entry_width.grid(row=3, column=0, padx=30, pady=(10, 10))
        self.configure_resolution_entry_height = customtkinter.CTkEntry(self.configure_frame, 
            placeholder_text="Enter custom height")
        self.configure_resolution_entry_height.grid(row=4, column=0, padx=30, pady=(10, 10))

        self.configure_resolution_button = customtkinter.CTkButton(self.configure_frame,
            command = self.event_handlers.update_resolution_button_event, text="Update Resolution", 
            fg_color=butt_theme, hover_color=butt_hover_theme, text_color=text_theme )
        self.configure_resolution_button.grid(row=5, column=0, padx=20, pady=(10, 10)) 

        # Configure Input Method
        self.configure_input_method_label = customtkinter.CTkLabel(self.configure_frame, 
            text="Input Method:", anchor="w")
        self.configure_input_method_label.grid(row=6, column=0, padx=30, pady=(10, 0))
        self.configure_input_method_optionemenu = customtkinter.CTkOptionMenu(self.configure_frame, 
            values=["Keyboard"],command=self.event_handlers.change_input_type_event, fg_color=butt_theme, 
            text_color=text_theme, button_color=butt_hover_theme, button_hover_color=butt_theme)
        self.configure_input_method_optionemenu.grid(row=7, column=0, padx=30, pady=(10, 10))

        # Notice
        self.configure_input_method_label = customtkinter.CTkLabel(self.configure_frame, 
            text="Remember to enable\nautoskip in-game!", anchor="w")
        self.configure_input_method_label.grid(row=8, column=0, padx=30, pady=(25, 10))
        # Readme frame ---------------------------------------------------------
        self.readme_frame = customtkinter.CTkFrame(self, corner_radius=0, 
            fg_color="transparent")
        self.readme_frame.grid_columnconfigure(0, weight=0)

        # Textbox
        self.readme_frame_txtbox = customtkinter.CTkTextbox(master = self.readme_frame, 
            corner_radius=0,height = 430, state = "disabled", wrap = "word")
        self.readme_frame_txtbox.grid(row=0, column=0)
        self.readme_frame_txtbox.grid(row=0, column=0, sticky="nsew")

        # Console frame --------------------------------------------------------
        self.console_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent") 
        self.console_frame.grid_columnconfigure(0, weight=0)

        # Textbox
        self.console_frame_txtbox = customtkinter.CTkTextbox(master = self.console_frame, 
            corner_radius=0,height = 380, state = "disabled", wrap = "word")
        self.console_frame_txtbox.grid(row=0, column=0)
        self.console_frame_txtbox.grid(row=0, column=0, sticky="nsew")

        # Export Button
        self.console_frame_export_button = customtkinter.CTkButton(self.console_frame, 
            command=self.event_handlers.export_button_event, text="Export", fg_color=butt_theme, hover_color=butt_hover_theme, text_color=text_theme)
        self.console_frame_export_button.grid(row=1, column=0, padx=20, pady=10)

        # Customise frame ------------------------------------------------------
        self.customise_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.customise_frame.grid_columnconfigure(0, weight=0)
        # Appearance Mode
        self.appearance_mode_label = customtkinter.CTkLabel(self.customise_frame,
            text="Appearance:", anchor="w")
        self.appearance_mode_label.grid(row=1, column=0, padx=30, pady=(15, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.customise_frame, 
            values=["Light", "Dark", "System"],command=self.event_handlers.change_appearance_mode_event, 
            fg_color=butt_theme, text_color=text_theme, button_color=butt_hover_theme, 
            button_hover_color=butt_theme)
        self.appearance_mode_optionemenu.grid(row=2, column=0, padx=30, pady=(10, 10))
        # Theme
        self.custom_theme_label = customtkinter.CTkLabel(self.customise_frame, 
            text="Custom Theme:\n(updates on restart)", anchor="e")
        self.custom_theme_label.grid(row=3, column=0, padx=30, pady=(10, 0))

        self.custom_theme_entry_fg_color = customtkinter.CTkEntry(self.customise_frame,
            placeholder_text="Button HEX")
        self.custom_theme_entry_fg_color.grid(row=4, column=0, padx=30, pady=(10, 10))

        self.custom_theme_entry_hover_color = customtkinter.CTkEntry(self.customise_frame, 
            placeholder_text="Button hover HEX")
        self.custom_theme_entry_hover_color.grid(row=5, column=0, padx=30, pady=(10, 10))

        self.custom_theme_text_optionmenu = customtkinter.CTkOptionMenu(self.customise_frame, 
            values=["White text", "Black text"], fg_color=butt_theme, 
            text_color=text_theme, button_color=butt_hover_theme, button_hover_color=butt_theme)
        self.custom_theme_text_optionmenu.grid(row=6, column=0, padx=30, pady=(10, 10))

        self.custom_theme_update_button = customtkinter.CTkButton(self.customise_frame, 
            text="Update theme", command=self.event_handlers.change_theme_event, fg_color=butt_theme, 
            hover_color=butt_hover_theme, text_color=text_theme)
        self.custom_theme_update_button.grid(row=7, column=0, padx=20, pady=(10, 10))

        # Scaling
        self.scaling_label = customtkinter.CTkLabel(self.customise_frame, text="Scale:", anchor="w")
        self.scaling_label.grid(row=8, column=0, padx=30, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.customise_frame, 
            values=["80%", "90%", "100%", "110%", "120%"], command=self.event_handlers.change_scaling_event, 
            fg_color=butt_theme, text_color=text_theme, button_color=butt_hover_theme, 
            button_hover_color=butt_theme)
        self.scaling_optionemenu.grid(row=9, column=0, padx=30, pady=(10, 20))

        # Set defaults ---------------------------------------------------------
        self.stop_button.configure(state="disabled", fg_color=('darkred'))
        self.event_handlers.select_frame_by_name("configure")

        # Passed from initialisation
        # Set input method
        self.configure_input_method_optionemenu.set(input_type)
        # Set theme
        self.appearance_mode_optionemenu.set(theme) 
        # Set scaling
        new_scaling_float = int(scale.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)
        customtkinter.set_window_scaling(new_scaling_float)
        self.scaling_optionemenu.set(scale)
        # Set text
        if text_theme == "White":
            self.custom_theme_text_optionmenu.set("White text") 
        elif text_theme == "Black":
            self.custom_theme_text_optionmenu.set("Black text")
        # todo: readme from file
        self.readme_frame_txtbox.configure(state='normal') # enable editing
        self.readme_frame_txtbox.insert("0.0", "WARNING: There is a possibility you get banned for using this program. Use at your own risk!\n\nHow to use:\nEnsure the \"current resolution\" and \"input method\" are correct and hit \"start\". Head back to Genshin and dialoge will be auto clicked.\n\nThis program detects pixel colors to determine when to skip dialogue. It can misfire; disable when not in dialogue.\n\nThis project is under the MIT License.\n\n Contributors:\n-Hubert Rozmarynowski\n(Git Management, Pixel Coordiantes, Dialogue Selection, Documentation)\n\n-Owen Walbridge\n(User Interface, All Res Support, Customisation Options, Fixes, Documentation)\n\n-xdenotte\n(Xbox Support)\n\n-Vamqueror\n(Dialog Selection, Fixes)\n\n-vlsido\n(DS4 Support)\n\n-YotamZiv298\n(Documentation and Code Clarity)")
        self.readme_frame_txtbox.configure(state='disabled') # disable editing
    
        # Console Setup --------------------------------------------------------

        def console(*args, **kwargs):
            """
            Redirect console to the in app console frame.
            :param args: The arguments to print.
            :param kwargs: The keyword arguments to print.
            :return: None
            """
            text = ' '.join(str(arg) for arg in args)

            # TODO: Append time to start of console output
            # ! Currently not working becuase it's also appending it to the end
            # ! I've tried substrings to no avail, need to look into it
            #current_time = utils.current_time(":")
            #text = str(current_time) + ": " + str(text)

            self.console_frame_txtbox.configure(state='normal') # enable editing
            self.console_frame_txtbox.insert("end", text)
            self.console_frame_txtbox.see("end")
            self.console_frame_txtbox.configure(state='disabled') # disable editing
        
        # TODO: Add more error catching (if needed)
        sys.stdout.write = console
        sys.stderr.write = console
        sys.excepthook = console