import hashlib
import json
import requests
import tkinter as tk
from tkinter import filedialog


def convert_to_quest():
    # Name of the info.dat and empty list
    info_file = "info.dat"
    file_list = [info_file]
    # Get difficulty list from info.dat and append each difficulty to the file list
    difficulty_beatmap_sets = json.load(open(info_file))["_difficultyBeatmapSets"]
    difficulty_beatmaps = difficulty_beatmap_sets[0]["_difficultyBeatmaps"]
    for difficulty in difficulty_beatmaps:
        file_list.append(difficulty["_beatmapFilename"])
    # Create empty bytearray
    byt_comb = bytearray()
    # Concatenate bytearray of each file in order
    for f in file_list:
        file = open(f, "rb")
        byt_comb.extend(bytearray(file.read()))
    # Hash bytearray (sha1)
    hashed = hashlib.sha1(byt_comb)
    # Return Quest song folder name
    return f"custom_level_{hashed.hexdigest()}"


def convert_to_pc(folder_name):
    # Remove custom_level_ at the start of the string
    song_hash = folder_name.replace("custom_level_", "")
    # Idk Laurie told me beat saver doesn't like it when you dont send this
    headers = {"User-Agent": "Quest to PC song converter"}
    # Pull song from BeatSaver using hash
    song = requests.get(f"https://beatsaver.com/api/maps/by-hash/{song_hash}", headers=headers)
    # Return PC song folder name
    return f'{song.json()["key"]} ({song.json()["metadata"]["songName"]} - {song.json()["metadata"]["levelAuthorName"]})'


def get_dir():
    sel_dir = filedialog.askdirectory(master=frm)
    song_dir.set(sel_dir)



# Let's make this damned GUI.
# Create the window and configure the grid
window = tk.Tk()
window.title("Beat Saber Song Converter")
window.resizable(False, False)
window.rowconfigure(0, weight=0)
window.rowconfigure(1, weight=1, minsize=50)
window.columnconfigure([0, 1], weight=1, minsize=5)
# Cute growoy frame
frm = tk.Frame(master=window, relief=tk.GROOVE, borderwidth=3)
frm.columnconfigure(0, weight=1)
frm.columnconfigure([1, 2], weight=2)
# Directory selection button
song_dir = tk.StringVar()
btn_path = tk.Button(master=frm, text="Select the custom songs folder", command=get_dir)
btn_path.grid(row=0, rowspan=2, column=0, padx=5, pady=5, sticky="wens")
# Directory selection entry
path_ent = tk.Entry(master=frm, width=100, textvariable=song_dir)
path_ent.grid(row=0, column=1, columnspan=2, padx=5, pady=5)
# Song number labels
songs_quest = tk.StringVar(value=f"0 Quest songs found")
songs_pc = tk.StringVar(value=f"0 PC songs found")
lbl_quest = tk.Label(master=frm, textvariable=songs_quest)
lbl_pc = tk.Label(master=frm, textvariable=songs_pc)
lbl_quest.grid(row=1, column=1, sticky="wens")
lbl_pc.grid(row=1, column=2, sticky="wens")
# Render Frame
frm.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="we")
# Conversion buttons
btn_quest = tk.Button(master=window, text="PC -> Quest")
btn_pc = tk.Button(master=window, text="Quest -> PC")
btn_quest.grid(row=1, column=0, padx=5, pady=5, sticky="wens")
btn_pc.grid(row=1, column=1, padx=5, pady=5, sticky="wens")
# Progress bar
# SOON:tm:
# GUI LET'S GOOOOOOOOOO
window.mainloop()
