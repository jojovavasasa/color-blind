import tkinter as tk
import pyautogui
import keyboard
import math

root = None
color_label = None

# Verbeterde kleurlijst
kleuren = {
    "rood": (255, 0, 0), "lichtrood": (255, 102, 102), "donkerrood": (139, 0, 0),
    "groen": (0, 255, 0), "lichtgroen": (144, 238, 144), "donkergroen": (0, 100, 0),
    "blauw": (0, 0, 255), "lichtblauw": (173, 216, 230), "donkerblauw": (0, 0, 139),
    "hemelsblauw": (135, 206, 235), "marineblauw": (0, 0, 128), "staalblauw": (70, 130, 180),
    "geel": (255, 255, 0), "lichtgeel": (255, 255, 153), "donkergeel": (204, 204, 0),
    "oranje": (255, 165, 0), "lichtoranje": (255, 200, 120), "donkeroranje": (204, 102, 0),
    "paars": (128, 0, 128), "lichtpaars": (216, 191, 216), "donkerpaars": (75, 0, 130),
    "magenta": (255, 0, 255), "cyaan": (0, 255, 255), "turkoois": (64, 224, 208),
    "roze": (255, 192, 203), "lichtroze": (255, 182, 193), "donkerroze": (231, 84, 128),
    "bruin": (165, 42, 42), "lichtbruin": (210, 180, 140), "donkerbruin": (101, 67, 33),
    "kastanjebruin": (139, 69, 19), "beige": (245, 245, 220), "goud": (255, 215, 0),
    "zilver": (192, 192, 192), "olijfgroen": (107, 142, 35), "limegroen": (50, 205, 50),
    "zeegroen": (46, 139, 87), "nachtblauw": (25, 25, 112), "diepblauw": (0, 51, 102),
    "zwart": (0, 0, 0), "grijs": (128, 128, 128), "lichtgrijs": (200, 200, 200),
    "donkergrijs": (64, 64, 64), "wit": (255, 255, 255)
}

def gewogen_afstand(c1, c2):
    """ Bereken de kleurafstand met gewichten voor rood, groen en blauw. """
    r_diff = (c1[0] - c2[0]) ** 2 * 0.3  # Rood weegt minder
    g_diff = (c1[1] - c2[1]) ** 2 * 0.59  # Groen weegt het zwaarst (mensen zien dit het best)
    b_diff = (c1[2] - c2[2]) ** 2 * 0.11  # Blauw weegt het minst
    return math.sqrt(r_diff + g_diff + b_diff)

def get_basic_color(r, g, b):
    """ Zoek de dichtstbijzijnde kleur met gewogen afstand. """
    dichtsbijzijnde = min(kleuren, key=lambda kleur: gewogen_afstand((r, g, b), kleuren[kleur]))
    
    # Extra check voor neutrale kleuren
    if abs(r - g) < 15 and abs(g - b) < 15:
        if sum([r, g, b]) > 600:
            return "wit"
        elif sum([r, g, b]) < 100:
            return "zwart"
        elif sum([r, g, b]) < 300:
            return "donkergrijs"
        else:
            return "grijs" if sum([r, g, b]) < 500 else "lichtgrijs"

    return dichtsbijzijnde

def update_color():
    if root is None:
        return
    x, y = pyautogui.position()
    color = pyautogui.screenshot().getpixel((x, y))  # RGB onder de muis
    hex_color = f"#{color[0]:02x}{color[1]:02x}{color[2]:02x}"
    basiskleur = get_basic_color(*color)

    color_label.config(
        text=f"Kleur: {color} ({basiskleur})", 
        bg=hex_color, 
        fg="white" if sum(color) < 383 else "black"
    )
    root.after(100, update_color)  # Elke 100ms updaten

def open_window():
    global root, color_label
    
    if root is not None:  # Sluit het venster als het al open is
        return
    
    root = tk.Tk()
    root.title("Kleurkiezer")
    root.geometry("230x80+1700+950")  # Positie rechts onderaan
    root.overrideredirect(True)  # Geen standaard vensterrand
    root.attributes("-topmost", True)  # Altijd bovenop

    color_label = tk.Label(root, text="Kleur: (0, 0, 0)", font=("Arial", 12), bg="black", fg="white")
    color_label.pack(fill="both", expand=True)

    close_button = tk.Button(root, text="X", command=close_window)
    close_button.pack(side="top", anchor="ne")

    update_color()
    root.mainloop()

def close_window():
    global root
    if root is not None:
        root.destroy()
        root = None

# Sneltoets instellen (Ctrl + Alt + Shift + N)
keyboard.add_hotkey("ctrl+alt+shift+n", open_window)
keyboard.add_hotkey("ctrl+alt+shift+n", close_window, trigger_on_release=True)

print("Houd Ctrl + Alt + Shift + N ingedrukt om de kleurkiezer te openen en laat los om te sluiten...")
keyboard.wait()  # Houdt het script draaiende
