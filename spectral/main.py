# main.py

# === IMPORT SHARED RESOURCES AND MODULES ===
from assets.resources import root, canvas  # Tkinter root window and canvas
from ui.boot import boot_sequence          # Boot animation logic
from ui.menu import draw_menu, glitch_loop, handle_menu_keys  # Menu rendering + input
from ui.ghost import animate_ghost         # Ghost idle animation in corner
import tkinter as tk

# === APP STATE (SHARED ACROSS MODULES) ===
# We use dictionaries so we can modify these values from any module (mutable by reference)
current_screen = {"value": "boot"}         # Tracks which screen we’re on: 'boot', 'menu', 'scan', etc.
selected_index = {"value": 0}              # Which menu item is currently selected

# === KEYBOARD EVENT HANDLER ===
def on_key(event):
    screen = current_screen["value"]

    # If on menu screen, use arrow keys + enter to navigate
    if screen == "menu":
        handle_menu_keys(event, selected_index, current_screen)  # update selected index or screen
        draw_menu(selected_index["value"])  # redraw menu to reflect changes

    # If inside another screen, allow user to press Backspace to return to the menu
    elif screen != "menu" and event.keysym == "BackSpace":
        current_screen["value"] = "menu"
        draw_menu(selected_index["value"])  # redraw menu after returning

# === BIND KEYBOARD INPUT ===
# Tells Tkinter to run `on_key()` every time a key is pressed
root.bind("<Key>", on_key)

# === START THE BOOT ANIMATION ===
# This plays the boot logo animation, then runs the menu when done
boot_sequence(
    current_screen=current_screen,
    selected_index=selected_index,
    
    # Once boot finishes, show the menu, animate ghost, and start glitch flicker
    on_complete=lambda: (
        draw_menu(selected_index["value"]),
        animate_ghost(),
        glitch_loop(selected_index)
    )
)

# === RUN THE MAIN EVENT LOOP ===
# Keeps the window open and updates the UI as needed
root.mainloop()
