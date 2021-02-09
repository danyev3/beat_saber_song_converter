# Libraries OwO
import os
import sys
import time
import json
import hashlib
import requests
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from tkinter.ttk import Progressbar
from threading import *


# Changing the working directory to the temporary one created by pyinstaller (mainly for the .ico) (UNCOMMENT BEFORE BUILDING THE EXE YOU IDIOT)
os.chdir(sys._MEIPASS)


# Release version
release_version = "1.1.1"


# Beat Saver User Agent
headers = {"User-Agent": f"Beat Saber Song Converter / {release_version}"}


# Name of the info file to find song folders
info_file = "info.dat"


# Generate Quest name from PC name and dir
def gen_quest_name(song_path, song):
    # File list with info file at the beginning
    file_list = [info_file]
    # Get difficulty list from info.dat and append each difficulty to the file list
    difficulty_beatmap_sets = json.load(open(info_file, encoding="utf8"))["_difficultyBeatmapSets"]
    for characteristic in range(0, len(difficulty_beatmap_sets)):
        difficulty_beatmaps = difficulty_beatmap_sets[characteristic]["_difficultyBeatmaps"]
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
def gen_pc_name(song_path, song):
    # Remove custom_level_ at the start of the string
    song_hash = song.replace("custom_level_", "")
    # Try to pull song from BeatSaver using hash
    try:
        requested_song = requests.get(f"https://beatsaver.com/api/maps/by-hash/{song_hash}", headers=headers)
        generated_name = f'{requested_song.json()["key"]} ({requested_song.json()["metadata"]["songName"]} - {requested_song.json()["metadata"]["levelAuthorName"]})'
        beatsaver = True
    # If it fails, the song is not on BeatSaver, generate a name from the info file
    except json.decoder.JSONDecodeError:
        song_info = json.load(open(f"{song_path}/{song}/{info_file}", encoding="utf8"))
        generated_name = f'({song_info["_songName"]} - {song_info["_levelAuthorName"]})'
        beatsaver = False
    # Remove unsupported characters from folder name
    unsupported_chars = '\/:*?"<>|'
    for char in unsupported_chars:
        generated_name = generated_name.replace(char, "")
    # Return PC song folder name and if BeatSaver was used
    return generated_name, beatsaver


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
        check_unk["state"] = "normal"
        btn_quest["state"] = "normal"
        btn_pc["state"] = "normal"
    else:
        # Disable the conversion buttons
        check_unk["state"] = "disabled"
        btn_quest["state"] = "disabled"
        btn_pc["state"] = "disabled"


# Look for PC and Quest songs in the selected dir and set the label variables
def set_song_number():
    # Reset labels to 0 (Otherwise it wouldn't restart from zero when you select a new dir)
    change_song_lbl("quest", "set", 0)
    change_song_lbl("pc", "set", 0)
    change_song_lbl("unk", "set", 0)
    for folder in os.listdir(song_dir.get()):
        # Only get directories
        if os.path.isdir(f"{song_dir.get()}/{folder}"):
            # Check if it's a song folder by finding the info file
            if os.path.isfile(f"{song_dir.get()}/{folder}/{info_file}"):
                # Add +1 to the label depending on the song name format
                if is_quest_song(folder):
                    change_song_lbl("quest", "add", 1)
                elif is_pc_song(folder):
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
        # Split the key and song name from the mapper
        key_songname, mapper = name.split(" - ", 1)
        # If the mapper end with ) it may be in PC format
        if mapper.endswith(")"):
            # If the key+songname starts with ( it's the custom PC format for songs not on BeatSaver
            if key_songname.startswith("("):
                return True
            else:
                # Split the key and song name
                key, songname = key_songname.split(" ", 1)
                # If the song name starts with ( it's in PC format
                if songname.startswith("("):
                    return True
        # If none of the above are true it's not PC format
        return False
    except ValueError:
        return False


# Check if the selected folder is in an unknown format and return false if unk songs shouldn't be converted
def is_unk_song(name):
    # If we are not converting unk songs, return false
    if not convert_unk.get():
        return False
    else:
        # If they are Quest or Pc songs, return false, else true
        if is_quest_song(name) or is_pc_song(name):
            return False
        else:
            return True


# Change the value in the song labels
def change_song_lbl(platform, operation, value):
    # I know it's not elegant but it works stfu
    platform_n = None
    platform_txt = None
    platform_str = None
    # Select the platform, unk is unused but it rapresents unkown format songs
    if platform == "quest":
        platform_n = songs_quest_n
        platform_txt = songs_quest_txt
        platform_str = "Quest songs found"
    elif platform == "pc":
        platform_n = songs_pc_n
        platform_txt = songs_pc_txt
        platform_str = "PC songs found"
    elif platform == "unk":
        platform_n = songs_unk_n
        platform_txt = songs_unk_txt
        platform_str = "unknown format songs found"
    # Execute the operation on the value variable
    if operation == "add":
        platform_n.set(platform_n.get() + value)
    elif operation == "sub":
        platform_n.set(platform_n.get() - value)
    elif operation == "set":
        platform_n.set(value)
    # Update the label variable with the new value
    platform_txt.set(value=f"{platform_n.get()} {platform_str}")


# Get total number of songs to convert adding the unk format songs if the checkbox is selected
def n_songs_to_convert(platform):
    if platform == "quest":
        if convert_unk.get():
            return songs_quest_n.get() + songs_unk_n.get()
        else:
            return songs_quest_n.get()
    elif platform == "pc":
        if convert_unk.get():
            return songs_pc_n.get() + songs_unk_n.get()
        else:
            return songs_pc_n.get()


# Convert all songs in the selected directory to Quest
def convert_to_quest():
    # Get total number of songs to convert
    songs_n = n_songs_to_convert("pc")
    # Send error if there are no PC songs in the directory
    if songs_n == 0:
        messagebox.showerror(title="I'm afraid I can't do that sir.", message="No PC songs found in the selected directory OwO")
    else:
        # Confirmation box
        if messagebox.askokcancel(title="Chotto matte", message=f"Are you sure you want to convert {songs_n} songs to Quest?"):
            # Disable the conversion buttons and checkbox
            check_unk["state"] = "disabled"
            btn_quest["state"] = "disabled"
            btn_pc["state"] = "disabled"
            # Setup the prograss bar
            converted_songs = 0
            bar["maximum"] = songs_n
            bar["value"] = converted_songs
            # For every directory in the selected song directory
            for song in os.listdir(song_dir.get()):
                # Only get directories
                if os.path.isdir(f"{song_dir.get()}/{song}"):
                    # Check if it's a song folder by finding the info file
                    if os.path.isfile(f"{song_dir.get()}/{song}/{info_file}"):
                        # Check if it's a pc song or and unk song if they are being converted
                        if is_pc_song(song) or is_unk_song(song):
                            # Generate the new name of the folder
                            new_song_name = gen_quest_name(song_dir.get(), song)
                            # Try to rename the folder, fail if a folder with the same name already exists and send an error
                            try:
                                os.rename(f"{song_dir.get()}/{song}", f"{song_dir.get()}/{new_song_name}")
                                # Update the progress bar
                                converted_songs = converted_songs + 1
                                bar["value"] = converted_songs
                                # Change song number labels
                                if is_pc_song(song):
                                    change_song_lbl("pc", "sub", 1)
                                else:
                                    change_song_lbl("unk", "sub", 1)
                                change_song_lbl("quest", "add", 1)
                            except FileExistsError:
                                messagebox.showerror(title="This is getting out of hand! Now, there are two of them!", message=f"Could not convert {song} because the same song ({new_song_name}) already exists in the same directory!")
            # Enable the conversion buttons and checkbox
            check_unk["state"] = "normal"
            btn_quest["state"] = "normal"
            btn_pc["state"] = "normal"
            # Stop the prograss bar
            bar.stop()
            # Done! Box
            messagebox.showinfo(title="Done!", message="Finished converting all the PC songs to Quest!")


# Convert all songs in the selected directory to PC
def convert_to_pc():
    # Get total number of songs to convert
    songs_n = n_songs_to_convert("quest")
    # Send error if there are no Quest songs in the directory
    if songs_n == 0:
        messagebox.showerror(title="I'm afraid I can't do that sir.", message="No Quest songs found in the selected directory OwO")
    else:
        # Confirmation box
        if messagebox.askokcancel(title="Chotto matte", message=f"Are you sure you want to convert {songs_n} songs to PC?\nThis will require internet access and will take roughly {round(((songs_n*1.5)/60)/2)} minutes.\nYes, it's a very slow process, we are limited by the speed of the BeatSaver API"):
            try:
                requests.get(f"https://beatsaver.com/api/", headers=headers)
            except requests.exceptions.ConnectionError:
                messagebox.showerror(title="OwO where's my Internet?!", message="Oh no! Looks like you don't have an Internet connection or the BeatSaver API servers are offline...\nPlease try again when Internet is available or the BeatSaver API comes back online.")
                return
            # Disable the conversion buttons and checkbox
            check_unk["state"] = "disabled"
            btn_quest["state"] = "disabled"
            btn_pc["state"] = "disabled"
            # Setup the prograss bar
            converted_songs = 0
            bar["maximum"] = songs_n
            bar["value"] = converted_songs
            # For every directory in the selected song directory
            for song in os.listdir(song_dir.get()):
                # Only get directories
                if os.path.isdir(f"{song_dir.get()}/{song}"):
                    # Check if it's a song folder by finding the info file
                    if os.path.isfile(f"{song_dir.get()}/{song}/{info_file}"):
                        # Check if it's a quest song or and unk song if they are being converted
                        if is_quest_song(song) or is_unk_song(song):
                            # Generate the new name of the folder and get back if BeatSaver was used to generate it
                            new_song_name, beatsaver_used = gen_pc_name(song_dir.get(), song)
                            # Try to rename the folder, fail if a folder with the same name already exists and send an error
                            try:
                                os.rename(f"{song_dir.get()}/{song}", f"{song_dir.get()}/{new_song_name}")
                                # Update the progress bar
                                converted_songs = converted_songs + 1
                                bar["value"] = converted_songs
                                # Change song number labels
                                if is_quest_song(song):
                                    change_song_lbl("quest", "sub", 1)
                                else:
                                    change_song_lbl("unk", "sub", 1)
                                change_song_lbl("pc", "add", 1)
                            except FileExistsError:
                                messagebox.showerror(title="This is getting out of hand! Now, there are two of them!", message=f"Could not convert {song} because the same song ({new_song_name}) already exists in the same directory!")
                            # Wait so that BeatSaver API doesn't hate us
                            if beatsaver_used:
                                time.sleep(0.5)
            # Enable the conversion buttons and checkbox
            check_unk["state"] = "normal"
            btn_quest["state"] = "normal"
            btn_pc["state"] = "normal"
            # Stop the prograss bar
            bar.stop()
            # Done! Box
            messagebox.showinfo(title="Done!", message="Finished converting all the Quest songs to PC!")


# Thread get_dir()
def thread_get_dir():
    thread = Thread(target=get_dir)
    thread.start()


# Thread convert_to_quest()
def thread_quest():
    thread = Thread(target=convert_to_quest)
    thread.start()


# Thread convert_to_pc()
def thread_pc():
    thread = Thread(target=convert_to_pc)
    thread.start()


# Let's make this damned GUI.
# There's a lot of weights and stuff cause the GUI was supposed to be resizable, then I realized idgaf about that
# Create the window and configure the grid
win = tk.Tk()
win.title("Beat Saber Song Converter")
win.iconbitmap("icon.ico")
win.resizable(False, False)
win.rowconfigure([0, 1], weight=0)
win.rowconfigure(2, weight=1, minsize=75)
win.columnconfigure([0, 1], weight=1, minsize=5)

# Cute growoy frame
frm = tk.Frame(master=win, relief=tk.GROOVE, borderwidth=3)
frm.columnconfigure(0, weight=1)
frm.columnconfigure([1, 2], weight=2)
frm.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="we")
# Directory selection button
song_dir = tk.StringVar()
btn_path = tk.Button(master=frm, text="Select the custom songs folder", command=thread_get_dir)
btn_path.grid(row=0, rowspan=2, column=0, padx=5, pady=5, sticky="wens")
# Directory selection entry
path_ent = tk.Entry(master=frm, width=100, state='disabled', textvariable=song_dir)
path_ent.grid(row=0, column=1, columnspan=2, padx=5, pady=5)
# Song number labels
songs_quest_n = tk.IntVar(value=0)
songs_pc_n = tk.IntVar(value=0)
songs_quest_txt = tk.StringVar(value=f"0 Quest songs found")
songs_pc_txt = tk.StringVar(value=f"0 PC songs found")
lbl_quest = tk.Label(master=frm, textvariable=songs_quest_txt)
lbl_pc = tk.Label(master=frm, textvariable=songs_pc_txt)
lbl_quest.grid(row=1, column=1, sticky="wens")
lbl_pc.grid(row=1, column=2, sticky="wens")

# Unknown format flat frame
frm_unk = tk.Frame(master=win)
frm_unk.grid(row=1, column=0, columnspan=2, padx=8, sticky="we")
frm_unk.columnconfigure(1, weight=1)
# Unknown format label
songs_unk_n = tk.IntVar(value=0)
songs_unk_txt = tk.StringVar(value=f"0 unknown format songs found")
lbl_unk = tk.Label(master=frm_unk, textvariable=songs_unk_txt)
lbl_unk.grid(row=0, column=0, sticky="w")
# Unknown format checkbox
convert_unk = tk.BooleanVar(value=0)
check_unk = tk.Checkbutton(master=frm_unk, text="Convert all unknown format songs to the selected platform", variable=convert_unk, padx=10)
check_unk.grid(row=0, column=1, columnspan=1, sticky="w")
# Disable Unknown format conversion checkbox
check_unk["state"] = "disabled"

# Conversion buttons
btn_quest = tk.Button(master=win, text="Convert to Quest", command=thread_quest)
btn_pc = tk.Button(master=win, text="Convert to PC", command=thread_pc)
btn_quest.grid(row=2, column=0, padx=5, pady=5, sticky="wens")
btn_pc.grid(row=2, column=1, padx=5, pady=5, sticky="wens")
# Disable the conversion buttons
btn_quest["state"] = "disabled"
btn_pc["state"] = "disabled"

# Progress bar
bar = Progressbar(master=win, length=50, mode='determinate')
bar.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky="wens")

# GUI LET'S GOOOOOOOOOO
win.mainloop()
