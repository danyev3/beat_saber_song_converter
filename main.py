# Libraries OwO
import os
import time
import json
import hashlib
import requests
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from tkinter.ttk import Progressbar


# Generate Quest name from PC name and dir
def gen_quest_name(song_path, song):
    # Name of the info.dat and empty list
    info_file = "info.dat"
    file_list = [info_file]
    # Get difficulty list from info.dat and append each difficulty to the file list
    difficulty_beatmap_sets = json.load(open(f"{song_path}/{song}/{info_file}"))["_difficultyBeatmapSets"]
    difficulty_beatmaps = difficulty_beatmap_sets[0]["_difficultyBeatmaps"]
    for difficulty in difficulty_beatmaps:
        file_list.append(difficulty["_beatmapFilename"])
    # Create empty bytearray
    byt_comb = bytearray()
    # Concatenate bytearray of each file in order
    for f in file_list:
        file = open(f"{song_path}/{song}/{f}", "rb")
        byt_comb.extend(bytearray(file.read()))
    # Hash bytearray (sha1)
    hashed = hashlib.sha1(byt_comb)
    # Return Quest song folder name
    return f"custom_level_{hashed.hexdigest()}"


# Generate PC name from Quest name
def gen_pc_name(song):
    # Remove custom_level_ at the start of the string
    song_hash = song.replace("custom_level_", "")
    # Idk Laurie told me BeatSaver doesn't like it when you dont send this
    headers = {"User-Agent": "Quest to PC song converter"}
    # Pull song from BeatSaver using hash
    requested_song = requests.get(f"https://beatsaver.com/api/maps/by-hash/{song_hash}", headers=headers)
    # Remove unsupported characters from folder name
    unsupported_chars = '\/:*?"<>|'
    generated_name = f'{requested_song.json()["key"]} ({requested_song.json()["metadata"]["songName"]} - {requested_song.json()["metadata"]["levelAuthorName"]})'
    for char in unsupported_chars:
        generated_name = generated_name.replace(char, "")
    # Return PC song folder name
    return generated_name


# Open "Choose directory" window
def get_dir():
    # Open directory window
    sel_dir = filedialog.askdirectory()
    # Set selected dir in entry variable
    song_dir.set(sel_dir)
    # Check if there's an actual directory selected
    if song_dir.get() != "":
        # Look for PC and Quest songs and set the label variables
        set_song_number()
        # Enable the conversion buttons
        btn_quest["state"] = "normal"
        btn_pc["state"] = "normal"
    else:
        # Disable the conversion buttons
        btn_quest["state"] = "disabled"
        btn_pc["state"] = "disabled"


# Look for PC and Quest songs in the selected dir and set the label variables
def set_song_number():
    # Reset labels to 0 (Otherwise it wouldn't restart from zero when you select a new dir)
    change_song_lbl("quest", "set", 0)
    change_song_lbl("pc", "set", 0)
    change_song_lbl("unk", "set", 0)
    for f in os.listdir(song_dir.get()):
        # Only get directories
        if os.path.isdir(f"{song_dir.get()}/{f}"):
            # Add +1 to the label depending on the song name format
            if is_quest_song(f):
                change_song_lbl("quest", "add", 1)
            elif is_pc_song(f):
                change_song_lbl("pc", "add", 1)
            else:
                change_song_lbl("unk", "add", 1)


# Check if the selected folder has the Quest name format
def is_quest_song(name):
    # Check if the name starts with custom_level_
    if name.startswith("custom_level_"):
        return True
    else:
        return False


# Check if the selected folder has the PC name format
def is_pc_song(name):
    # Try splitting the key, song name and mapper, if it fails the song name is not in PC format
    try:
        key, songname_mapper = name.split(" ", 1)
        songname, mapper = songname_mapper.split(" - ", 1)
    except ValueError:
        return False
    # If the song name doesn't start with "(" and the mapper name doesn't end with ")" I have no clue how it got this far but it definetly isn't a PC format song
    if songname.startswith("(") and mapper.endswith(")"):
        return True
    else:
        return False


# Change the value in the song labels
def change_song_lbl(platform, operation, value):
    # I know it's not elegant but it works stfu
    platform_n = None
    platform_txt = None
    platform_lbl = None
    # Select the platform, unk is unused but it rapresents unkown format songs
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
    # Execute the operation on the value variable
    if operation == "add":
        platform_n.set(platform_n.get() + value)
    elif operation == "sub":
        platform_n.set(platform_n.get() - value)
    elif operation == "set":
        platform_n.set(value)
    # Update the label variable with the new value
    platform_txt.set(value=f"{platform_n.get()} {platform_lbl}")


# Convert all songs in the selected directory to Quest
def convert_to_quest():
    # Send error if there are no PC songs in the directory
    if songs_pc_n.get() == 0:
        messagebox.showerror(title="I'm afraid I can't do that sir.", message="No PC songs found in the selected directory OwO")
    else:
        # Confirmation box
        if messagebox.askokcancel(title="Chotto matte", message=f"Are you sure you want to convert {songs_pc_n.get()} PC songs to Quest?"):
            # Disable the conversion buttons
            btn_quest["state"] = "disabled"
            btn_pc["state"] = "disabled"
            # Start the prograss bar
            bar.start()
            # Check every directory in the selected song directory
            for song in os.listdir(song_dir.get()):
                if os.path.isdir(f"{song_dir.get()}/{song}") and is_pc_song(song):
                    # Generate the new name of the folder
                    new_song_name = gen_quest_name(song_dir.get(), song)
                    # Try to rename the folder, fail if a folder with the same name already exists and send an error
                    try:
                        os.rename(f"{song_dir.get()}/{song}", f"{song_dir.get()}/{new_song_name}")
                    except FileExistsError:
                        messagebox.showerror(title="This is getting out of hand! Now, there are two of them!", message=f"Could not convert {song} because {new_song_name} already exists in the same directory!")
                    # Reset song number labels
                    set_song_number()
            # Enable the conversion buttons
            btn_quest["state"] = "normal"
            btn_pc["state"] = "normal"
            # Stop the prograss bar
            bar.stop()
            # Done! Box
            messagebox.showinfo(title="Done!", message="Finished converting all the PC songs to Quest!")


# Convert all songs in the selected directory to PC
def convert_to_pc():
    # Send error if there are no Quest songs in the directory
    if songs_quest_n.get() == 0:
        messagebox.showerror(title="I'm afraid I can't do that sir.", message="No Quest songs found in the selected directory OwO")
    else:
        # Confirmation box
        if messagebox.askokcancel(title="Chotto matte", message=f"Are you sure you want to convert {songs_quest_n.get()} Quest songs to PC?\nThis will require internet access and will take around {((songs_quest_n.get()*1.5)/60)/2} minutes."):
            # Disable the conversion buttons
            btn_quest["state"] = "disabled"
            btn_pc["state"] = "disabled"
            # Start the prograss bar
            bar.start()
            # Check every directory in the selected song directory
            for song in os.listdir(song_dir.get()):
                if os.path.isdir(f"{song_dir.get()}/{song}") and is_quest_song(song):
                    # Wait so that BeatSaver API doesn't hate us
                    time.sleep(0.5)
                    # Try to generate the new name of the folder, if it returns a json error the song is not on Beat Saver
                    try:
                        new_song_name = gen_pc_name(song)
                    except json.decoder.JSONDecodeError:
                        new_song_name = song.replace("custom_level_", "quest_imported_")
                    # Try to rename the folder, fail if a folder with the same name already exists and send an error
                    try:
                        os.rename(f"{song_dir.get()}/{song}", f"{song_dir.get()}/{new_song_name}")
                    except FileExistsError:
                        messagebox.showerror(title="This is getting out of hand! Now, there are two of them!", message=f"Could not convert {song} because {new_song_name} already exists in the same directory!")
                    # Reset song number labels
                    set_song_number()
            # Enable the conversion buttons
            btn_quest["state"] = "normal"
            btn_pc["state"] = "normal"
            # Stop the prograss bar
            bar.stop()
            # Done! Box
            messagebox.showinfo(title="Done!", message="Finished converting all the Quest songs to PC!")


# Let's make this damned GUI.
# There's a lot of weights and stuff cause the GUI was supposed to be resizable, then I realized idgaf about that
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
frm.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="we")
# Directory selection button
song_dir = tk.StringVar()
btn_path = tk.Button(master=frm, text="Select the custom songs folder", command=get_dir)
btn_path.grid(row=0, rowspan=2, column=0, padx=5, pady=5, sticky="wens")
# Directory selection entry
path_ent = tk.Entry(master=frm, width=100, state='disabled', textvariable=song_dir)
path_ent.grid(row=0, column=1, columnspan=2, padx=5, pady=5)
# Song number vars (unk is unused but it gets filled up with unkown format songs)
songs_quest_n = tk.IntVar(value=0)
songs_pc_n = tk.IntVar(value=0)
songs_unk_n = tk.IntVar(value=0)
# Song number labels (unk is unused but it gets filled up with unkown format songs)
songs_quest_txt = tk.StringVar(value=f"0 Quest songs found")
songs_pc_txt = tk.StringVar(value=f"0 PC songs found")
songs_unk_txt = tk.StringVar(value=f"0 External songs found")
lbl_quest = tk.Label(master=frm, textvariable=songs_quest_txt)
lbl_pc = tk.Label(master=frm, textvariable=songs_pc_txt)
lbl_quest.grid(row=1, column=1, sticky="wens")
lbl_pc.grid(row=1, column=2, sticky="wens")
# Conversion buttons
btn_quest = tk.Button(master=win, text="PC -> Quest", command=convert_to_quest)
btn_pc = tk.Button(master=win, text="Quest -> PC", command=convert_to_pc)
btn_quest.grid(row=1, column=1, padx=5, pady=5, sticky="wens")
btn_pc.grid(row=1, column=0, padx=5, pady=5, sticky="wens")
# Disable the conversion buttons
btn_quest["state"] = "disabled"
btn_pc["state"] = "disabled"
# Progress bar
bar = Progressbar(master=win, length=100, mode='indeterminate')
bar.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="wens")
# GUI LET'S GOOOOOOOOOO
win.mainloop()
