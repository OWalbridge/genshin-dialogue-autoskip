import os
import sys

import tkinter as tk
import customtkinter

import file_io
import utils
import logic

class EventHandlers:
    def __init__(self, gui_instance, screen_dimensions):
        self.gui_instance = gui_instance
        self.screen_dimensions = screen_dimensions
        self.logic = logic.logic(self.screen_dimensions)

    def select_frame_by_name(self, name):
        """
        Change GUI frame
        :param name: Name of the frame to show
        :return: None
        """
        self.gui_instance.configure_button.configure(fg_color=("gray75", "gray25") if name == "configure" else "transparent")
        self.gui_instance.readme_button.configure(fg_color=("gray75", "gray25") if name == "readme" else "transparent")
        self.gui_instance.console_button.configure(fg_color=("gray75", "gray25") if name == "console" else "transparent")
        self.gui_instance.customise_button.configure(fg_color=("gray75", "gray25") if name == "customise" else "transparent")

        # Show the selected frame
        if name == "configure":
            self.gui_instance.configure_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.gui_instance.configure_frame.grid_forget()
        if name == 'readme':
            self.gui_instance.readme_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.gui_instance.readme_frame.grid_forget()
        if name == 'console':
            self.gui_instance.console_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.gui_instance.console_frame.grid_forget()
        if name == 'customise':
            self.gui_instance.customise_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.gui_instance.customise_frame.grid_forget()

    # Navigation Frame Event Handlers ------------------------------------------

    # Start/ Stop --------------------------------------------------------------
    def start_button_event(self):
        self.gui_instance.stop_button.configure(state="normal", fg_color=('red'))
        self.gui_instance.start_button.configure(state="disabled", fg_color=('darkgreen'))

        self.logic.start()
        
    def stop_button_event(self):
        self.gui_instance.stop_button.configure(state="disabled", fg_color=('darkred'))
        self.gui_instance.start_button.configure(state="normal", fg_color=('green'))

        self.logic.stop()

    # --------------------------------------------------------------------------

    def reset_button_event(self):
        certain = tk.messagebox.askyesno("Reset Settings?", "Are you sure you want to reset settings?")  
        if certain:
            detected_height = self.screen_dimensions.detect_height()
            detected_width = self.screen_dimensions.detect_width()
            file_io.write_default_config(detected_width, detected_height)
            file_io.write_default_custom()
            utils.restart_program()

    def configure_button_event(self):
        self.select_frame_by_name("configure")

    def readme_button_event(self):
        self.select_frame_by_name("readme")
    
    def console_button_event(self):
        self.select_frame_by_name("console")

    def customise_button_event(self):
        self.select_frame_by_name("customise")

    # Configure Frame Event Handlers -------------------------------------------
    def update_resolution_button_event(self):
        width_entry = self.gui_instance.configure_resolution_entry_width.get()
        height_entry = self.gui_instance.configure_resolution_entry_height.get()
        if width_entry and height_entry:  # Check both entries are not empty
            try:
                # TODO Add error handling
                self.screen_dimensions.set_width(int(width_entry))
                self.screen_dimensions.set_height(int(height_entry))
                self.screen_dimensions.update_pixels()
                width_entry = str(self.screen_dimensions.get_width())
                height_entry = str(self.screen_dimensions.get_height())
                # Update config.txt
                file_io.write_update_resolution(width_entry, height_entry)
                self.gui_instance.configure_resolution_label.configure(text="Current Resolution:\n" + width_entry + 'x' + height_entry)
            except ValueError:
                print("Invalid input. Please enter valid integers for width and height.")
        else:
            print("Please enter values for both width and height.")

    def change_input_type_event(self, new_input_type: str):
        # Update config.txt
        file_io.write_update_input_type(new_input_type)
    
    # Console Frame Event Handlers ---------------------------------------------
    def export_button_event(self):
        try:
            file_io.export_console(self.gui_instance.console_frame_txtbox.get("0.0", "end"))
            print("Console output exported")
            try:
                os.startfile(os.path.realpath("./console_logs"))
            except:
                print("However, could not open console_logs folder; you'll need to go there manually")
        except:
            print("Error: Could not export console output")
        
    # Customisation Frame Event Handlers ---------------------------------------
    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)
        # Update config.txt
        file_io.write_update_theme(new_appearance_mode)

    def change_theme_event(self):
        # Update fg theme
        butt_theme = self.gui_instance.custom_theme_entry_fg_color.get()
        if utils.is_valid_hex_code(butt_theme):
            file_io.write_update_button_theme(butt_theme)
        else:
            print("Invalid hex code for button color")


        # Update hover theme
        butt_hover_theme = self.gui_instance.custom_theme_entry_hover_color.get()
        if utils.is_valid_hex_code(butt_hover_theme):
            file_io.write_update_button_hover_theme(butt_hover_theme)
        else:
            print("Invalid hex code for button hover color")
        
        # Update text theme
        text_theme = self.gui_instance.custom_theme_text_optionmenu.get()
        if text_theme == "White text":
            text_theme = "White"
        elif text_theme == "Black text":
            text_theme = "Black"
        file_io.write_update_text_theme(text_theme)
        
    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)
        customtkinter.set_window_scaling(new_scaling_float)
        file_io.write_update_scale(new_scaling)