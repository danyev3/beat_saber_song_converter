# Beat Saber Song Converter
An executable to... well... _convert Beat Saber songs_?\
You can use this to change the names of your PC song's folders to use your song library on Quest!\
You can also convert from Quest to PC in case you like your songs folder to look nice and tidy.

### Installation
Just download the latest `BSSC.exe` from [the realease tab](https://github.com/danyev3/beat_saber_song_converter/releases/latest) and run it!\
Windows may warn you about the file being a virus or stright up delete it when you try to run it, to prevent this, you can temporarily disable Windows Defender's Real Time Protection.

If you think the program is a virus, **don't use it**. It's open source and the code is very simple and filled to the brim with comments to make it easier to read. The reason Windows flags it is because it's not signed with a certificate, and signing an executable is _extremely_ expensive.

### How to use BSSC
Once you run BSSC you'll be greeted with a very simple GUI, hit the `Select the custom songs folder` button and select your custom songs folder (The folder must be on your PC, not on your Quest).\
Once you selected a folder, the program will tell you how many PC songs and how many Quest songs it has detected, from here, just hit the `Convert to Quest` button or the `Convert to PC` button to convert all your songs!

There is also a third `Unknown format songs` label that will tell you how many songs the program found that don't follow the Quest or PC naming scheme.\
If you also want to convert these `Unknown format songs` just hit the checkbox next to the label and then one of the convert buttons.

Converting to Quest is very quick, doesn't require internet access and is a required step to use your PC library on Quest.

Converting to PC on the other end is very slow and requires an internet connection, this isn't something I can fix as I am limited by the BeatSaver API.\
If you don't really want to wait to convert your Quest songs to PC... just don't! PC Beat Saber doesn't care how your custom song folders are named (but converting them makes it much easier to know which song is which)

### How to move the converted songs to your Quest
At the moment BMBF does not support uploading multiple songs from a single `.zip` file, so you will have to manually move the songs in your Quest's songs folder and reload it through BMBF.\
To do this, plug your Quest into your PC, open SideQuest and wait for your Quest to connect successfully. (if you don't know what SideQuest is, how the hell did you get here? There's plenty of good tutorials to set it up, just google it.) After your Quest is connected, close Sidequest and hit the `Exit SideQuest` button. After you do this, your Quest will appear in your File Explorer (just like if it was a USB stick!), navigate to `sdcard/BMBFData/CustomSongs` and if you already have some custom songs on your Quest, here you will find many `custom_level_xxxxx` folders. Just select the songs you converted to Quest using BSSC (which should also be in the `custom_level_xxxxx` format) and move them in the Quest's `CustomSongs` folder! If you get a popup while moving your songs, you most likely already have the song you are trying to move on your Quest, just hit `Ok`.\
After you are done moving your songs, put your headset on, head into BMBF, go in the `Tools` tab and hit `Reload songs folder`. This may take a little bit and give some errors if you have a lot of songs, this is not something I can control.

### Does BSSC work on Linux?
BSSC technically works on Linux, but obviously not with the same `.exe` file as on Windows. I am currently working to release a stable version for Linux, but if you want to use it right now, just download the source code, extract the `main.py` and edit it. Comment out (or delete) the `os.chdir(sys._MEIPASS)` and the `win.iconbitmap("icon.ico")` lines (use `CTRL + F` to search for them) and save. Now if you run `sudo python3 main.py` in the same directory where you extracted the code, the program *should* start correctly and work just fine, if it doesn't just DM me on Discord and we will figure it out. You need to have the `tkinter` python library installed, if you don't know how to do that just look it up on google

### Can you add X feature to BSSC?
Yes! *I think*\
I am always trying to improve BSSC, so if you have any good ideas shoot me a DM on Discord and I'll see if I can add it!
This is a list of what I'm working on:
- [x] Make BSSC convert unknown song formats
- [ ] Add a "Converting XXX song" label above the progress bar
- [ ] Generate a single BMBF-compatible zip file to upload songs to Quest more easily
- [ ] Linux version
- [ ] Option to convert only songs marked as favorite in-game

#### If you need help or have any questions, DM me on discord at dany_ev3#0001
