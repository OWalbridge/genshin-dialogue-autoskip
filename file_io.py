#Author(s): Owen Walbridge, 2023 | 
# This file handles the reading and writing of the config.txt and customise.txt 
# files.

import os
import utils

def read(file):
    file = open(file, "r")
    temp = file.read().split("|")
    file.close()
    return temp

def write_default_config(screen_width, screen_height):
    # Make default config file
    file = open("config.txt", "w")
    file.write(str(screen_width) + "|" + str(screen_height) + "|Keyboard")
    file.close()

def write_default_custom():
    # Make default customisation file
    file = open("custom.txt", "w")
    file.write("System|100%|White|#1f6aa5|#134870")
    file.close()

def export_console(console):
    file_name = utils.current_time("-") + "_" + utils.current_date("-") + ".log"
    file = open("./console_logs/" + file_name, "w")
    file.write(console)
    file.close()

def write_update_resolution(width, height):
    temp = read("config.txt")
    file = open("config.txt", "w")
    file.write(width + "|" + height + "|" + temp[2])
    file.close()

def write_update_input(new_input_type):
    temp = read("config.txt")
    file = open("config.txt", "w")
    file.write(temp[0] + "|" + temp[1] + "|" + new_input_type)
    file.close()

#todo 
def write_update_theme(new_appearance_mode):
    temp = read("custom.txt")
    file = open("custom.txt", "w")
    file.write(new_appearance_mode + "|" + temp[1] + "|" + temp[2] + "|" + temp[3] + "|" + temp[4])
    file.close()

def write_update_scale(new_scaling):
    temp = read("custom.txt")
    file = open("custom.txt", "w")
    file.write(temp[0] + "|" + new_scaling + "|" + temp[2] + "|" + temp[3] + "|" + temp[4])
    file.close()

def write_update_text_theme(text_theme):
    temp = read("custom.txt")
    file = open("custom.txt", "w")
    file.write(temp[0] + "|" + temp[1] + "|" + text_theme + "|" + temp[3] + "|" + temp[4])
    file.close()

def write_update_button_theme(butt_theme):
    temp = read("custom.txt")
    file = open("custom.txt", "w")
    file.write(temp[0] + "|" + temp[1] + "|" + temp[2] + "|" + butt_theme + "|" + temp[4])
    file.close()

def write_update_button_hover_theme(butt_hover_theme):
    temp = read("custom.txt")
    file = open("custom.txt", "w")
    file.write(temp[0] + "|" + temp[1] + "|" + temp[2] + "|" + temp[3] + "|" + butt_hover_theme)
    file.close()