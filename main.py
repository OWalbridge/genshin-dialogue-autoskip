from logic import GenshinImpactDialogueSkipper
from gui import SkipperGUI
import tkinter

if __name__ == "__main__":
    # Initialize the logic class
    logic = GenshinImpactDialogueSkipper()

    # Start the GUI
    app = SkipperGUI()
    app.mainloop()