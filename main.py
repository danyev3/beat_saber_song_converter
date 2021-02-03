import os
import json
import hashlib
import requests
import tkinter as tk
from tkinter import filedialog
from tkinter.ttk import Progressbar


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
    sel_dir = filedialog.askdirectory()
    song_dir.set(sel_dir)
    set_song_number()


def set_song_number():
    change_song_lbl("quest", "set", 0)
    change_song_lbl("pc", "set", 0)
    change_song_lbl("unk", "set", 0)
    if song_dir.get() != "":
        for f in os.listdir(song_dir.get()):
            if os.path.isdir(f"{song_dir.get()}/{f}"):
                if is_quest_song(f):
                    change_song_lbl("quest", "add", 1)
                elif is_pc_song(f):
                    change_song_lbl("pc", "add", 1)
                else:
                    change_song_lbl("unk", "add", 1)


def is_quest_song(name):
    if name.startswith("custom_level_"):
        return True
    else:
        return False


def is_pc_song(name):
    try:
        key, songname_mapper = name.split(" ", 1)
        songname, mapper = songname_mapper.split(" - ", 1)
    except ValueError:
        return False
    if songname.startswith("(") and mapper.endswith(")"):
        return True
    else:
        return False


def change_song_lbl(platform, operation, value):
    # I know it's not elegant but it works stfu
    if platform == "quest":
        platform_n = songs_quest_n
        platform_txt = songs_quest_txt
        platform_lbl = "Quest songs found"
    elif platform == "pc":
        platform_n = songs_pc_n
        platform_txt = songs_pc_txt
        platform_lbl = "PC songs found"
    elif platform == "unk":
        platform_n = songs_unk_n
        platform_txt = songs_unk_txt
        platform_lbl = "External songs found"
    if operation == "add":
        platform_n.set(platform_n.get() + value)
    elif operation == "set":
        platform_n.set(value)
    platform_txt.set(value=f"{platform_n.get()} {platform_lbl}")


# Let's make this damned GUI.
# Create the window and configure the grid
win = tk.Tk()
win.title("Beat Saber Song Converter")
win.resizable(False, False)
win.rowconfigure(0, weight=0)
win.rowconfigure(1, weight=1, minsize=50)
win.columnconfigure([0, 1], weight=1, minsize=5)
# Cute growoy frame
frm = tk.Frame(master=win, relief=tk.GROOVE, borderwidth=3)
frm.columnconfigure(0, weight=1)
frm.columnconfigure([1, 2], weight=2)
# Directory selection button
song_dir = tk.StringVar()
btn_path = tk.Button(master=frm, text="Select the custom songs folder", command=get_dir)
btn_path.grid(row=0, rowspan=2, column=0, padx=5, pady=5, sticky="wens")
# Directory selection entry
path_ent = tk.Entry(master=frm, width=100, state='disabled', textvariable=song_dir)
path_ent.grid(row=0, column=1, columnspan=2, padx=5, pady=5)
# Song number labels
songs_quest_n = tk.IntVar(value=0)
songs_pc_n = tk.IntVar(value=0)
songs_unk_n = tk.IntVar(value=0)
songs_quest_txt = tk.StringVar(value=f"0 Quest songs found")
songs_pc_txt = tk.StringVar(value=f"0 PC songs found")
songs_unk_txt = tk.StringVar(value=f"0 External songs found")
lbl_quest = tk.Label(master=frm, textvariable=songs_quest_txt)
lbl_pc = tk.Label(master=frm, textvariable=songs_pc_txt)
lbl_quest.grid(row=1, column=1, sticky="wens")
lbl_pc.grid(row=1, column=2, sticky="wens")
# Render Frame
frm.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="we")
# Conversion buttons
btn_quest = tk.Button(master=win, text="PC -> Quest")
btn_pc = tk.Button(master=win, text="Quest -> PC")
btn_quest.grid(row=1, column=0, padx=5, pady=5, sticky="wens")
btn_pc.grid(row=1, column=1, padx=5, pady=5, sticky="wens")
# Progress bar
bar = Progressbar(master=win, length=100, mode='determinate')
bar.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="wens")
#bar.start()
# GUI LET'S GOOOOOOOOOO
win.mainloop()
