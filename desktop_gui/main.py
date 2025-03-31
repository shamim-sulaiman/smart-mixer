import json
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import tkinter as tk
from tkinter import messagebox, filedialog
from simulation.simulation import run_simulation

CONFIG_FILE = "config.json"

def save_last_folder(path):
    with open(CONFIG_FILE, "w") as f:
        json.dump({"last_folder": path}, f)

def load_last_folder():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                data = json.load(f)
                return data.get("last_folder", "")
        except (json.JSONDecodeError, IOError):
            print("⚠️ Config file corrupted or empty. Resetting.")
            return ""
    return ""

def start_simulation():
    try:
        target = float(entry_target.get())
        duration = int(entry_duration.get())
        kp = float(entry_kp.get())
        ki = float(entry_ki.get())
        kd = float(entry_kd.get())

        try:
            disturb_time = int(entry_disturb_time.get())
            new_conc_in = float(entry_new_conc.get())
        except ValueError:
            disturb_time = None
            new_conc_in = None

        save_to = folder_path.get() or None
        run_simulation(target, duration, kp, ki, kd,
               save_folder=save_to,
               disturbance_time=disturb_time,
               new_salt_conc=new_conc_in)

    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numbers!")

# GUI setup
root = tk.Tk()
root.title("Smart Mixing Tank Simulation")

# Input Fields
tk.Label(root, text="Target Concentration (g/L):").grid(row=0, column=0, sticky='e')
tk.Label(root, text="Simulation Duration (min):").grid(row=1, column=0, sticky='e')
tk.Label(root, text="Kp:").grid(row=2, column=0, sticky='e')
tk.Label(root, text="Ki:").grid(row=3, column=0, sticky='e')
tk.Label(root, text="Kd:").grid(row=4, column=0, sticky='e')
tk.Label(root, text="Save Folder:").grid(row=5, column=0, sticky='e')
tk.Label(root, text="Disturbance Time (min):").grid(row=7, column=0, sticky='e')
tk.Label(root, text="New Salt Conc. In (g/L):").grid(row=8, column=0, sticky='e')

entry_target = tk.Entry(root)
entry_duration = tk.Entry(root)
entry_kp = tk.Entry(root)
entry_ki = tk.Entry(root)
entry_kd = tk.Entry(root)
entry_disturb_time = tk.Entry(root)
entry_new_conc = tk.Entry(root)

entry_target.insert(0, "10")
entry_duration.insert(0, "60")
entry_kp.insert(0, "0.05")
entry_ki.insert(0, "0.005")
entry_kd.insert(0, "0.01")
entry_disturb_time.insert(0, "30")  # default: disturb at 30 mins
entry_new_conc.insert(0, "20")      # default: drop to 20 g/L

entry_target.grid(row=0, column=1)
entry_duration.grid(row=1, column=1)
entry_kp.grid(row=2, column=1)
entry_ki.grid(row=3, column=1)
entry_kd.grid(row=4, column=1)
entry_disturb_time.grid(row=7, column=1)
entry_new_conc.grid(row=8, column=1)

folder_path = tk.StringVar()
folder_path.set(load_last_folder())


def choose_folder():
    path = filedialog.askdirectory()
    folder_path.set(path)
    save_last_folder(path)

# Button
tk.Entry(root, textvariable=folder_path, width=30).grid(row=5, column=1)
tk.Button(root, text="Browse", command=choose_folder).grid(row=5, column=2)
tk.Button(root, text="Start Simulation", command=start_simulation).grid(row=6, column=0, columnspan=2, pady=10)

root.mainloop()
