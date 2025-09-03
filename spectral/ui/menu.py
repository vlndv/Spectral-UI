# ui/menu.py

import random
from assets.resources import canvas, canvas_width, canvas_height, spectral_font

# === MENU CONFIGURATION ===
menu_items = ["Scan", "Quote", "Bias", "Demo", "Mods", "Info"]  # List of menu options
glitch_visible = {"value": True}  # Controls whether the title is in glitched mode or normal

# === GENERATE GLITCHED TITLE TEXT ===
# Randomly replaces characters to simulate a glitch effect
def get_glitched_title():
    if glitch_visible["value"]:
        return "".join(
            random.choice("Main Spectral Menu") if c != " " else " "  # keep spaces
            for c in "Main Spectral Menu"
        )
    return "Main Spectral Menu"

# === DRAW THE MAIN MENU SCREEN ===
# This function renders the title and all menu items on the canvas
def draw_menu(selected_index):
    canvas.delete("menu")  # Clear previous menu drawings

    title_x = canvas_width // 2  # Center of screen horizontally

    # Draw the glitched or normal title
    canvas.create_text(
        title_x, 30,
        text=get_glitched_title(),
        fill="cyan",
        font=spectral_font,
        anchor="n",
        tags="menu"  # allows us to delete or update it later
    )

    # Draw each menu item in a list
    for i, item in enumerate(menu_items):
        y = 80 + i * 24  # vertical spacing for each item
        prefix = "+ " if i == selected_index else "  "  # highlight selected with '+'
        color = "cyan" if i == selected_index else "white"

        canvas.create_text(
            title_x, y,
            text=f"{prefix}{item}",
            fill=color,
            font=spectral_font,
            anchor="n",
            tags="menu"
        )

# === START THE GLITCH EFFECT LOOP ===
# Flickers the title between normal and glitched versions
def glitch_loop(selected_index):
    from assets.resources import root

    glitch_visible["value"] = not glitch_visible["value"]  # toggle glitch mode
    draw_menu(selected_index["value"])  # re-render menu with glitch state

    # Schedule the next glitch update with random timing
    root.after(random.randint(400, 1200), glitch_loop, selected_index)

# === HANDLE KEYBOARD CONTROLS IN MENU ===
# Controls navigation using Up/Down arrows and Enter
def handle_menu_keys(event, selected_index, current_screen):
    if event.keysym == "Down":
        # Move selection down (wraps around)
        selected_index["value"] = (selected_index["value"] + 1) % len(menu_items)

    elif event.keysym == "Up":
        # Move selection up (wraps around)
        selected_index["value"] = (selected_index["value"] - 1) % len(menu_items)

    elif event.keysym == "Return":
        # Enter pressed: change screen state to selected menu item
        current_screen["value"] = menu_items[selected_index["value"]].lower()
