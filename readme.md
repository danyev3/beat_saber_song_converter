# Beat Saber Song Converter
An executable to... well... _convert Beat Saber songs_?\
You can use this to change the names of your PC song's folders to use your song library on Quest!\
You can also convert from Quest to PC in case you like your songs folder to look nice and tidy.

### Installation
Just download the latest `BSSC.exe` from the realease tab and run it!\
Windows may warn you about the file being a virus or stright up delete it when you try to run it, to prevent this, you can temporarily disable Windows Defender's Real Time Protection.\
If you think the program is a virus, **don't use it**. It's open source and the code is very simple. The reason Windows flags it is because it's not signed with a certificate, and signing an executable is _extremely_ expensive.

### How to use BSSC
Once you run BSSC you'll be greeted with a very simple GUI, hit the `Select the custom songs folder` button and select your custom songs folder (The folder must be on your PC, not on your Quest).\
Once you selected a folder, the program will tell you how many PC songs and how many Quest songs it has detected, from here, just hit the `Quest -> PC` button or the `PC -> Quest` button to convert all your songs!\
Converting to Quest is very quick, doesn't require internet access and it will conver **all** songs to make them work on Quest.\
Converting to PC on the other end is very slow and requires an internet connection, this isn't something I can fix as I am limited by the BeatSaver API. Also if you try converting to PC a song that is not on BeatSaver It will just be called `quest_imported_XXX`. This will probably change in the future to something like `(song_name - song_mapper)`.\
If you don't want to wait to convert your Quest songs to PC... just don't! PC Beat Saber doesn't care how your custom song folders are named.

#### If you need help or have any questions, DM me on discord at dany_ev3#0001