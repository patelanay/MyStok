#MyStok 
#Team: Project 3 Group 55
#Members: James Jean Philipe, Ignatius Martin, Anay Patel


import sys
import os
from src.interface.cli import MyStokCLI

# Try to import pygame GUI, but make it optional
try:
    from src.interface.pygame_interface import MyStokGUI
    GUI_AVAILABLE = True
except ImportError:
    GUI_AVAILABLE = False


def main():
    try:
        csv_path = "resources/World-Stock-Prices-Dataset.csv"
        if not os.path.exists(csv_path):
            print("Error: CSV file not found!")
            return 1

        # Try GUI first, go to CLI if not available
        if GUI_AVAILABLE:
            gui = MyStokGUI(csv_path)
            gui.run()
        else:
            print("GUI not available. Going back to CLI...")
            cli = MyStokCLI(csv_path)
            cli.run()
        
        return 0
        
    except KeyboardInterrupt:
        print("\n\nApplication interrupted by user.")
        return 0
    except Exception as x:
        print(f"\nUnexpected error: {x}")
        return 1


if __name__ == "__main__":
    sys.exit(main()) 