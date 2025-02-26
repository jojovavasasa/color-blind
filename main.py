import tkinter as tk
import pyautogui
import keyboard

def update_color():
    x, y = pyautogui.position()
    color = pyautogui.screenshot().getpixel((x, y))  # Kleur onder de muis
    hex_color = f"#{color[0]:02x}{color[1]:02x}{color[2]:02x}"  # RGB → HEX
    
    color_label.config(text=f"Kleur: {color}", bg=hex_color, fg="white" if sum(color) < 383 else "black")
    root.after(100, update_color)  # Elke 100ms updaten

def toggle_window():
    global root, color_label
    
    if hasattr(root, "running") and root.running:  # Sluit het venster als het al open is
        root.running = False
        root.destroy()
        return
    
    root = tk.Tk()
    root.running = True
    root.title("Kleurkiezer")
    root.geometry("200x80+1720+950")  # Positie rechts onderaan (pas aan als nodig)
    root.overrideredirect(True)  # Geen standaard vensterrand
    root.attributes("-topmost", True)  # Altijd bovenop

    color_label = tk.Label(root, text="Kleur: (0, 0, 0)", font=("Arial", 12), bg="black", fg="white")
    color_label.pack(fill="both", expand=True)

    update_color()
    root.mainloop()

# Sneltoets instellen (bijv. Ctrl+Shift+C)
keyboard.add_hotkey("ctrl+shift+c", toggle_window)

print("Druk op Ctrl+Shift+C om de kleurkiezer te openen/sluiten...")
keyboard.wait()  # Houdt het script draaiende
