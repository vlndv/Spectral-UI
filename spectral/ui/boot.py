# ui/boot.py

from assets.resources import canvas, boot_frames
import tkinter as tk

# === GLOBAL HANDLE FOR BOOT IMAGE OBJECT ===
# This holds the reference to the image displayed during the boot animation
boot_image = None

# === BOOT SEQUENCE ANIMATION FUNCTION ===
# Plays an animated boot logo using 2 frames for ~3 seconds
def boot_sequence(current_screen, selected_index, on_complete, index=0, cycles=0):
    global boot_image

    # If we are no longer in "boot" mode, stop the animation immediately
    if current_screen["value"] != "boot":
        return

    # First time running — place the image on the canvas
    if boot_image is None:
        boot_image = canvas.create_image(
            0, 0,
            anchor=tk.NW,
            image=boot_frames[0]  # Start with the first boot frame
        )
    else:
        # Update the frame to animate (e.g., frame 0 → 1 → 0 → 1...)
        canvas.itemconfig(boot_image, image=boot_frames[index])

    # === ANIMATION LOOP ===
    if cycles < 10:
        # Still within animation period (~3 seconds if 10 * 300ms)
        from assets.resources import root
        root.after(
            300,  # Delay between each frame
            boot_sequence,
            current_screen,
            selected_index,
            on_complete,
            (index + 1) % len(boot_frames),  # Flip to next frame (loop)
            cycles + 1  # Increase cycle count
        )
    else:
        # === BOOT FINISHED ===
        canvas.delete(boot_image)              # Remove the boot image
        current_screen["value"] = "menu"       # Change state to menu
        on_complete()                          # Trigger menu + ghost + glitch start
