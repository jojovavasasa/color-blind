import tkinter as tk
import pyautogui
import keyboard

root = None
color_label = None

def get_basic_color(r, g, b):
    kleuren = {
        "rood": (255, 0, 0),
        "groen": (0, 255, 0),
        "blauw": (0, 0, 255),
        "geel": (255, 255, 0),
        "oranje": (255, 165, 0),
        "paars": (128, 0, 128),
        "roze": (255, 192, 203),
        "bruin": (165, 42, 42),
        "zwart": (0, 0, 0),
        "wit": (255, 255, 255),
        "grijs": (128, 128, 128)
    }

    def afstand(c1, c2):
        return sum((a - b) ** 2 for a, b in zip(c1, c2))

    return min(kleuren, key=lambda kleur: afstand((r, g, b), kleuren[kleur]))

def update_color():
    if root is None:
        return
    x, y = pyautogui.position()
    color = pyautogui.screenshot().getpixel((x, y))  # Kleur onder de muis
    hex_color = f"#{color[0]:02x}{color[1]:02x}{color[2]:02x}"  # RGB → HEX
    basiskleur = get_basic_color(*color)  # RGB omzetten naar basisnaam

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
    root.geometry("200x80+1720+950")  # Positie rechts onderaan (pas aan als nodig)
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
