import hashlib
import json
import requests


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


print(convert_to_pc(convert_to_quest()))
