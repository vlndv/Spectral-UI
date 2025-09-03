# assets/resources.py

import tkinter as tk
from tkinter import font as tkFont
from PIL import Image, ImageTk
import os

# === SETUP WINDOW AND CANVAS ===

# Define canvas dimensions (used consistently throughout the UI)
canvas_width, canvas_height = 512, 256

# Create the main window for the Spectral interface
root = tk.Tk()
root.title("Spectral")  # Window title

# Create a canvas that acts as the drawing area for all UI elements
canvas = tk.Canvas(
    root,
    width=canvas_width,
    height=canvas_height,
    bg="black",              # Background color
    highlightthickness=0     # No border around the canvas
)
canvas.pack()  # Attach canvas to window

# === LOAD CUSTOM FONT (Fallback to Courier) ===

try:
    # Attempt to load the pixel-style font from the 'fonts' folder
    font_path = os.path.join(os.path.dirname(__file__), "..", "fonts", "PressStart2P.ttf")
    spectral_font = tkFont.Font(family="Press Start 2P", size=8)
except:
    # If loading fails, fallback to built-in Courier font
    spectral_font = ("Courier", 10, "bold")

# === LOAD IMAGE ASSETS ===

# Folder where all bitmap images are stored
img_folder = os.path.join(os.path.dirname(__file__), "..", "img")

# Load ghost idle frames (for the small animated ghost in the corner)
ghost_frames = [
    ImageTk.PhotoImage(
        Image.open(os.path.join(img_folder, "spectral_idle1.bmp")).resize((64, 64), Image.NEAREST)
    ),
    ImageTk.PhotoImage(
        Image.open(os.path.join(img_folder, "spectral_idle2.bmp")).resize((64, 64), Image.NEAREST)
    )
]

# Load boot logo frames (used for the full-screen startup animation)
boot_frames = [
    ImageTk.PhotoImage(
        Image.open(os.path.join(img_folder, "spectral_idle1_with_logo.bmp")).resize((512, 256), Image.NEAREST)
    ),
    ImageTk.PhotoImage(
        Image.open(os.path.join(img_folder, "spectral_idle2_with_logo.bmp")).resize((512, 256), Image.NEAREST)
    )
]

# === EXPORTED RESOURCES ===
# These are the shared components used across all modules (menu, boot, ghost, etc.)
__all__ = [
    "root", "canvas", "canvas_width", "canvas_height",
    "spectral_font", "ghost_frames", "boot_frames"
]
