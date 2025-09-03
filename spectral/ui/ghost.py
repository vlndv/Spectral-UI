# ui/ghost.py

from assets.resources import canvas, ghost_frames, canvas_height, root
import tkinter as tk

# === CREATE THE GHOST OBJECT (BOTTOM-LEFT CORNER) ===
# This places the ghost image at a fixed position on the canvas
ghost_obj = canvas.create_image(
    20,                    # X position from the left (near the corner)
    canvas_height - 84,    # Y position near the bottom
    anchor=tk.NW,          # Align from top-left corner of the image
    image=ghost_frames[0]  # Start with the first ghost frame
)

# === ANIMATE THE GHOST IN A LOOP ===
# This function cycles between ghost frames to simulate movement
def animate_ghost(index=0):
    # Update the image on the canvas to the current frame
    canvas.itemconfig(ghost_obj, image=ghost_frames[index])

    # Schedule the next frame change after 400 milliseconds
    root.after(
        400,                      # Wait 400 ms
        animate_ghost,           # Function to call again
        (index + 1) % len(ghost_frames)  # Next frame index (loops)
    )
