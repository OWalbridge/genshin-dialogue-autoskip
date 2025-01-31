# genshin-dialogue-autoskip

This fork of "genshin-dialogue-autoskip" includes my KBM only version which supports all resolutions. See the issue i've left on the original repo for more info.

Below is the projects original readme:

## Overview
This script automatically skips dialogue in Genshin Impact, always chooses the bottom dialogue option.

*This is for educational purposes only. I advice against relying on the script in daily gameplay, as it will ruin your story experience.*

## Requirements
- The game running on Main Display 1 in 1920x1080
- The script run as Admin to allow key and mouse emulation
- Required Python packages installed with `pip install -r requirements.txt`

## Usage
1. Run `autoskip_dialogue.py` with Admin privileges
	-  Tip: You can right-click the handy `run.bat` file and select "Run as administrator"
2. When you're ready, press F8 on your keyboard to start the main loop

## DualShock 4 Support
- The script automatically defines the UI version, currently autodetects ENG/RUS keyboard+mouse UI and ENG/RUS DualShock 4 gamepad UI
- To use with DS4 gamepad, the autoplay button must be activated using the square button

## Xbox Gamepads Support
- The script works in the same way as with DS4
- To use with Xbox Gamepad, the autoplay button must be activated using the "X" button

## Keyboard and Mouse Only Version
- If you're just using keyboard and mouse to play the game and don't need the gamepad support, you may prefer to use the `kbm_only` branch. That way you'll only use what you need, without the added complexity of additional input device support.
