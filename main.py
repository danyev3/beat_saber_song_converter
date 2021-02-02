import hashlib
import json
import requests
import tkinter as tk


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


# Create the window and configure the grid
window = tk.Tk()
window.title("Beat Saber Song Converter")
window.rowconfigure(0, weight=0)
window.rowconfigure(1, weight=1, minsize=50)
window.columnconfigure([0, 1], weight=1, minsize=5)
# Cute groowy frame
frm = tk.Frame(master=window, relief=tk.GROOVE, borderwidth=3)
# Label and entry
path_lbl = tk.Label(master=frm, text="Path:")
path_ent = tk.Entry(master=frm, width=50)
path_lbl.grid(row=0, column=0)
path_ent.grid(row=0, column=1)
# Buttons
btn_quest = tk.Button(master=window, text="PC -> Quest")
btn_pc = tk.Button(master=window, text="Quest -> PC")
frm.grid(row=0, columnspan=2, padx=5, pady=5, sticky="we")
btn_quest.grid(row=1, column=0, padx=5, pady=5, sticky="wens")
btn_pc.grid(row=1, column=1, padx=5, pady=5, sticky="wens")

# GUI LET'S GOOOOOOOOOO
window.mainloop()
