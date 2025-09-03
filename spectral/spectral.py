import tkinter as tk
from PIL import Image, ImageTk
import os
import random

# === SETUP ===
root = tk.Tk()
root.title("Spectral")
canvas_width, canvas_height = 512, 256
canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bg="black", highlightthickness=0)
canvas.pack()

# === FONT SETUP (Fallback to Courier if pixel font fails) ===
try:
    import tkinter.font as tkFont
    font_path = os.path.join(os.path.dirname(__file__), "fonts", "PressStart2P.ttf")
    spectral_font = tkFont.Font(family="Press Start 2P", size=8)
except:
    spectral_font = ("Courier", 10, "bold")

# === IMAGE FOLDERS ===
img_folder = os.path.join(os.path.dirname(__file__), "img")

# === GHOST FRAMES (corner ghost) ===
ghost_frames = [
    ImageTk.PhotoImage(Image.open(os.path.join(img_folder, "spectral_idle1.bmp")).resize((64, 64), Image.NEAREST)),
    ImageTk.PhotoImage(Image.open(os.path.join(img_folder, "spectral_idle2.bmp")).resize((64, 64), Image.NEAREST))
]
ghost_obj = canvas.create_image(20, canvas_height - 84, anchor=tk.NW, image=ghost_frames[0])

# === BOOT FRAMES (full screen animation) ===
boot_frames = [
    ImageTk.PhotoImage(Image.open(os.path.join(img_folder, "spectral_idle1_with_logo.bmp")).resize((512, 256), Image.NEAREST)),
    ImageTk.PhotoImage(Image.open(os.path.join(img_folder, "spectral_idle2_with_logo.bmp")).resize((512, 256), Image.NEAREST))
]
boot_image = canvas.create_image(0, 0, anchor=tk.NW, image=boot_frames[0])

# === MENU DATA ===
menu_items = ["Scan", "Quote", "Bias", "Demo", "Mods", "Info"]
selected_index = 0
current_screen = "boot"
glitch_visible = True

def get_glitched_title():
    if glitch_visible:
        return "".join(random.choice("Main Spectral Menu") if c != " " else " " for c in "Main Spectral Menu")
    else:
        return "Main Spectral Menu"

# === DRAW MENU FUNCTION ===
def draw_menu():
    canvas.delete("menu")
    title_x = canvas_width // 2
    canvas.create_text(title_x, 30, text=get_glitched_title(), fill="cyan", font=spectral_font, anchor="n", tags="menu")
    for i, item in enumerate(menu_items):
        y = 80 + i * 24
        prefix = "+ " if i == selected_index else "  "
        color = "cyan" if i == selected_index else "white"
        canvas.create_text(title_x, y, text=f"{prefix}{item}", fill=color, font=spectral_font, anchor="n", tags="menu")

# === GLITCH EFFECT TOGGLE ===
def glitch_loop():
    global glitch_visible
    if current_screen == "menu":
        glitch_visible = not glitch_visible
        draw_menu()
        delay = random.randint(300, 900) if glitch_visible else random.randint(800, 2000)
        root.after(delay, glitch_loop)

# === DRAW SCREEN FOR EACH MENU ITEM ===
def draw_screen(mode):
    canvas.delete("all")
    canvas.create_text(canvas_width // 2, canvas_height // 2 - 20, text=f"{mode} Mode", fill="cyan", font=spectral_font)
    canvas.create_text(canvas_width // 2, canvas_height // 2 + 20, text="Backspace to return", fill="white", font=spectral_font)
    canvas.create_image(20, canvas_height - 84, anchor=tk.NW, image=ghost_frames[0])

# === KEY CONTROL ===
def on_key(event):
    global selected_index, current_screen
    if current_screen == "menu":
        if event.keysym == "Down":
            selected_index = (selected_index + 1) % len(menu_items)
        elif event.keysym == "Up":
            selected_index = (selected_index - 1) % len(menu_items)
        elif event.keysym == "Return":
            current_screen = menu_items[selected_index].lower()
            draw_screen(menu_items[selected_index])
            return
        draw_menu()
    elif current_screen != "menu" and event.keysym == "BackSpace":
        current_screen = "menu"
        draw_menu()

root.bind("<Key>", on_key)

# === GHOST LOOP (bottom-left idle animation) ===
def animate_ghost(index=0):
    if current_screen == "menu":
        canvas.itemconfig(ghost_obj, image=ghost_frames[index])
        root.after(400, animate_ghost, (index + 1) % len(ghost_frames))

# === BOOT ANIMATION LOOP ===
def boot_sequence(index=0, cycles=0):
    global current_screen
    if current_screen != "boot":
        return
    canvas.itemconfig(boot_image, image=boot_frames[index])
    if cycles < 10:  # ~3 seconds total
        root.after(300, boot_sequence, (index + 1) % len(boot_frames), cycles + 1)
    else:
        canvas.delete(boot_image)
        current_screen = "menu"
        draw_menu()
        animate_ghost()
        glitch_loop()

# === RUN ===
boot_sequence()
root.mainloop()
