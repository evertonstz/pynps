# pyNPS
<p align="center">
<img src="https://octodex.github.com/images/pythocat.png" width="448" height="448">
</p>

PyNPS is a [Nopaystation](https://beta.nopaystation.com/) client writen in python 3.7 that, with the help of [wget](https://www.gnu.org/software/wget/) and [pkg2zip](https://github.com/mmozeiko/pkg2zip/), can search, download and decrypt/extract PSVita, PSP, PSX and PSM games from Nopaystation database. It's basically a command line version of [NPSBrowser](https://nopaystation.com/vita/npsReleases/) writen by a moron (aka me).

# Table of Contents

- [Installation](#Installation)
  * [Manual](#Manual)
  * [Fedora](#Fedora)
  * [Arch/Manjaro](#Arch/Manjaro)
  * [Using dotpy file](#Using%20dotpy%20file)
  * [pkg2zip](#pkg2zip)
  * [wget](#wget)
- [Updating database](#Updating%20database)
- [Configuration file](#Configuration%20file)
- [Examples](#Examples)
  * [Searching](#Searching)
  * [Syntax for selecting files to download](#Syntax%20for%20selecting%20files%20to%20download)
  * [More information](#More%20information)
- [Make a donation](#Make%20a%20donation)
  * [Paypal](#Paypal)
  * [Crypto](#Crypto)
******
# Installation
There are tree methods you can install pyNPS:

## Manual
This is only for 64bits systems.

You can grab the latest x86/usr/bin/_64 binary file at [releases](https://github.com/evertonstz/pyNPS/releases). The binary is made with pyinstaller, so there's no need to deal with python dependencies, just download it and use it (ofc you'll still need pkg2zip and wget installed or inside ~/.config/pynps/lib)

If you want to just use it by typing "pynps" in your terminal, you have to copy your binary to /usr/bin/

Here's a full guide:
- download the latest release [here](https://github.com/evertonstz/pyNPS/releases), last time time this readme was updated it was the v0.5, so you'll need to download the file named  pynps-v0.5-linux-x86_64;

- enter your terminal and cd to were you downloaded the file, usually it's:
>$ cd ~/Download

- move the downloaded file to the /usr/bin folder by runing (don't forget to change the version if you're installing a newer release):
>$ sudo mv pynps-v0.5-linux-x86_64 /usr/bin/pynps

- make sure the moved file is marked as executable:
>$ sudo chmod +x /usr/bin/pynps

- test the newly installed binary, pynps should output the version:
>$ pynps --version

After this proceed to the [pkg2zip](#pkg2zip) section, you'll also need to install that.

## Fedora
This is for both 32 and 64bits systems.

There's a .rpm installer in [releases](https://github.com/evertonstz/pyNPS/releases), just grab the latest one and double click it to install.

## Arch/Manjaro
This is only for 64bits systems.

AUR is deprecated since I simply can't maintain it. If anyone is interested in maintaning it, go ahead!

A pkg.tar.xz installer for Arch/Manjaro can be found at [releases](https://github.com/evertonstz/pyNPS/releases). Arch users problably know how to handle it, Manjaro users can just double click it to install.

## Using dotpy file
This is for both 32 and 64bits systems.

First of all you'll need python3.7+

You'll also need Prompt Toolkit
```
$ pip install prompt_toolkit
```
You can get the source files from github and use the pynps.py file as any other python script.
```
$ git clone https://github.com/evertonstz/pyNPS
$ cd pynNPS
$ python pynps.py
```

******
# pkg2zip
This script uses lusid1's pkg2zip, as [recomended by NoPayStation](https://twitter.com/NoPayStation/status/1096508850080043010), to handle the .pkg extractions, you have 3 options:

1. Use pre-compied binary, compiled by myelf (version 2.2) [here](https://pixeldrain.com/u/qJ05A7Si), just drop it inside /home/USER/.config/pyNPS/lib/ and make it executable by runing:

> chmod -R +x /home/USER/.config/pyNPS/lib/pkg2zip


2. If you're an Arch or Suse user, you can compile it from [AUR](https://aur.archlinux.org/packages/pkg2zip-fork/) after you install it pyNPS will autodetect and use it automatically, no need to add the path to your config file, the yay command is:

>$ yay -S pkg2zip-fork/

3. Or you can just grab the sources from lusid1's repo and compile it yourself [here](https://github.com/lusid1/pkg2zip/releases) and move  the binary into this folder /home/USER/.config/pyNPS/lib/ (USER is your username);

For methods 1 and 3 pyNPS will autodetect and use it automatically, so there's no need to add the path to your config file

In case you decide to store your binary outside /home/USER/.config/pyNPS/lib/ you'll need to specify this folder in your config file unde the "pkg2zip_location" option.

******
# wget
This software uses wget to make the downloads therefore it won't work if you don't have it installed in your system, most distros already come with wget installed, if you don't have it chances are you're on some crazy non-userfriendly distro and you probably know your way around for installing it. If you don't just google.

You can drop a wget binary at /home/USER/.config/pyNPS/lib/ after that pyNPS will autodetect and use it automatically, no need to add the path to your config file.

In case you decide to store your binary outside /home/USER/.config/pyNPS/lib/ you'll need to specify this folder in your config file unde the "wget_location" option.

******
# Updating database
Before downloading any of your legally obtained (wink wink wink) pkg file you have to update your NPS database, you don't have to do it every time you want to download something, but only in your first run to construct your initial database and after that just once in a while to get info about new pkgs NPS adds to their database:

Updating all system's databases:
>$ pynps -u

<br/>
Updating database per console:

>$ pynps -c psv -u #updates only vita's db

>$ pynps -c psp -u #updates only psp's db

>$ pynps -c psv -u #updates only psx's db

>$ pynps -c psv -c psm -u #updates only psx's and psm's db

Database is located by default at: /home/USER/.config/pyNPS/database
******
# Configuration file
Configuration file is created at: /home/USER/.config/pyNPS/settings.ini

If you delete it, it'll be recreated with default parameters in the next run. The options are pretty much self explanatory.

******
# Examples
## Searching
If you wanna update the PSP's database before searching for a PSP Sonic game in any region:
>$ pynps -c psp -u -dg sonic
```
Updating Database for Playstation Portable:
Downloading File: PSP_GAMES.tsv [###################-] 98% 550K @ 71.4K/s
renaming file: ./DATABASE/PSP/PSP_GAMES.tsv ./DATABASE/PSP/GAMES.tsv
Downloading File: PSP_DLCS.tsv [####################] 100% 450K @ 100%/s
renaming file: ./DATABASE/PSP/PSP_DLCS.tsv ./DATABASE/PSP/DLCS.tsv
Downloading File: PSP_THEMES.tsv [####################] 100% 0K @ 100%/s
renaming file: ./DATABASE/PSP/PSP_THEMES.tsv ./DATABASE/PSP/THEMES.tsv
Downloading File: PSP_UPDATES.tsv [####################] 100% 0K @ 928K=0.02s/s
renaming file: ./DATABASE/PSP/PSP_UPDATES.tsv ./DATABASE/PSP/UPDATES.tsv
1 ) PSP | ULUS10323 | US   | GAMES | Sonic Rivals 2 | 455.7 MiB
2 ) PSP | ULES00622 | EU   | GAMES | Sonic Rivals | 195.1 MiB
3 ) PSP | ULES00940 | EU   | GAMES | Sonic Rivals 2 | 219.8 MiB
4 ) PSP | ULUS10195 | US   | GAMES | Sonic Rivals | 196.8 MiB
Enter the number for what you want to download, you can enter multiple separated by commas:
```
******
Search for an european release of Crash for PSX and PSP
>$ pynps -c psp -c psx -r eur -dg crash
```
1  ) PSP | NPEG00020 | EU   | GAMES   | Gravity Crash Portable | 46.09 MiB
2  ) PSP | NPEZ00305 | EU   | GAMES   | 3,2,1…SuperCrash! (Minis) | 22.4 MiB
3  ) PSX | NPEE00001 | EU   | GAMES   | Crash Bandicoot  | 461.2 MiB
4  ) PSX | NPEE00001 | EU   | GAMES   | Crash Bandicoot (German store)  | 461.2 MiB
5  ) PSX | NPEE00008 | EU   | GAMES   | Crash Bandicoot 2: Cortex Strikes Back  | 133.6 MiB
6  ) PSX | NPEE00008 | EU   | GAMES   | Crash Bandicoot 2: Cortex Strikes Back (German store)  | 133.6 MiB
7  ) PSX | NPEE00014 | EU   | GAMES   | Crash Bandicoot 3: Warped  | 133.7 MiB
8  ) PSX | NPEE00014 | EU   | GAMES   | Crash Bandicoot 3: Warped (German store)  | 133.7 MiB
9  ) PSX | NPEE00014 | EU   | GAMES   | Crash Bandicoot 3: Warped (Italian Store)  | 133.7 MiB
10 ) PSX | NPEE00014 | EU   | GAMES   | Crash Bandicoot 3: Warped (Spanish)  | 133.7 MiB
11 ) PSX | NPEE00026 | EU   | GAMES   | Crash Team Racing  | 323.2 MiB
12 ) PSX | NPEE00026 | EU   | GAMES   | Crash Team Racing (German Store)  | 323.3 MiB
13 ) PSX | NPEE00026 | EU   | GAMES   | Crash Team Racing (Italian Store)  | 323.3 MiB
Enter the number for what you want to download, you can enter multiple numbers using commas: 
```
******
Search for for themes and demos related to the word "touhou in any region:
>$ pynps -c psv -dt -dde touhou
```
1  ) PSV | PCSE00947 | US   | THEMES | Touhou Genso Rondo Theme | 6.723 MiB
2  ) PSV | PCSE00990 | US   | THEMES | Touhou Genso Wanderer PlayStation Vita Theme | 4.514 MiB
3  ) PSV | PCSE01104 | US   | THEMES | Touhou Kobuto V: Burst Battle 4 Theme | 4.038 MiB
4  ) PSV | PCSB01039 | EU   | THEMES | Touhou Genso Wanderer PlayStation Vita Theme | 4.514 MiB
5  ) PSV | PCSB01129 | EU   | THEMES | Touhou Kobuto V: Burst Battle Theme 4 | 4.038 MiB
6  ) PSV | PCSG00999 | JP   | THEMES | Touhou Kobuto V | 2.533 MiB
7  ) PSV | PCSE01104 | US   | THEMES | Touhou Kobuto V: Burst Battle Theme 3 | 5.581 MiB
8  ) PSV | PCSE01104 | US   | THEMES | Touhou Kobuto V: Burst Battle Theme 2 | 5.174 MiB
9  ) PSV | PCSE01104 | US   | THEMES | Touhou Kobuto V: Burst Battle Theme 1 | 2.533 MiB
10 ) PSV | PCSG90252 | JP   | DEMOS  | Touhou Soujinengi V (DEMO) | 335.6 MiB
Enter the number for what you want to download, you can enter multiple separated by commas:
```
******
Search for for everything (themes, games, demos, dlcs and updates) related to the word "knight" in any region region on the psvita database:
>$ pynps -c psv knight

<br/>
Or if you like suffering (I cropped the output because it returned 53 results):

>$ pynps -c psv -dg -dd -dt -du -dde knight
```
1  ) PSV | PCSE00244 | US   | GAMES   | Valhalla Knights 3 | 897.8 MiB
13 ) PSV | PCSA00017 | US   | DLCS    | LittleBigPlanet Knights of Old Pre-Order Costume Pack | 100 KiB
49 ) PSV | PCSB00861 | EU   | THEMES  | Digimon Story Cyber Sleuth Custom Theme: Royal Knights Set | 4.999 MiB
53 ) PSV | PCSB00743 | EU   | UPDATES | Shovel Knight | 120.8 MiB
Enter the number for what you want to download, you can enter multiple separated by commas:
```
******
If you just wanna everything related to God of War in all systems (psp, psv, psx and psm)? Sure, you can omit "-c/--console" and it will assume you want every gaming system:
>$ pynps "god of war"

Or

>$ pynps -c psv -c psp -c psx -c psm "god of war"
```
1  ) PSV | PCSA00017 | US   | DLCS    | LittleBigPlanet PS Vita God of War Kratos Costume | 100 KiB
2  ) PSV | PCSA00069 | US   | DLCS    | PS All-Stars PS Vita God of War's Zeus | 100 KiB
3  ) PSV | PCSA00069 | US   | DLCS    | PS All-Stars PS Vita God of War's Warrior of Apollo Costume | 100 KiB
4  ) PSV | PCSA00069 | US   | DLCS    | PS All-Stars PS Vita God of War's Hades Minion | 100 KiB
5  ) PSV | PCSF00021 | EU   | DLCS    | God of War - Level Kit (PS Vita) | 100 KiB
6  ) PSV | PCSA00017 | US   | DLCS    | LittleBigPlanet™ PS Vita God of War™ minipack | 100 KiB
7  ) PSV | PCSA00126 | US   | GAMES   | God of War Collection | 3.108 GiB
8  ) PSV | PCSC00059 | JP   | GAMES   | God of War Collection | 2.435 GiB
9  ) PSV | PCSF00438 | EU   | GAMES   | God of War Collection | 3.301 GiB
10 ) PSP | NPJH50170 | JP   | GAMES   | God of War: Rakujitsu no Hisoukyoku | 1.278 GiB
11 ) PSP | NPEG00023 | EU   | GAMES   | God of War: Chains of Olympus | 1.095 GiB
12 ) PSP | NPEG00044 | EU   | GAMES   | God of War: Ghost of Sparta | 1.117 GiB
13 ) PSP | NPHG00027 | ASIA | GAMES   | God of War: Chains of Olympus | 1.289 GiB
14 ) PSP | NPHG00092 | ASIA | GAMES   | God of War: Ghost of Sparta | 1.078 GiB
15 ) PSP | NPEG00045 | EU   | GAMES   | God of War®: Ghost of Sparta | 1024 MiB
16 ) PSP | NPUG80325 | US   | GAMES   | God of War: Chains of Olympus | 1.287 GiB
17 ) PSP | NPUG80508 | US   | GAMES   | God of War Ghost of Sparta | 1.087 GiB
18 ) PSP | NPHG00091 | ASIA | GAMES   | God of War™ Ghost of Sparta 體驗版 | 96.54 MiB
19 ) PSP | NPEW00072 | EU   | THEMES  | God of War: Ghost of Sparta Theme (pre-order bundle) | 370.5 KiB
20 ) PSP | NPEW00072 | EU   | THEMES  | God of War Ghost of Sparta PSP Theme | 370.5 KiB
Enter the number for what you want to download, you can enter multiple numbers using commas:                                                                       
```
******
Wanna return every single american DLC for the psvita? Sure, it's slow but it's a free country:
>$ pynps -c psv -r usa -dd _all
```
that's too big to output here, mate :<
```
******
## Syntax for selecting files to download
After you make your search you'll probably want to download something, if it's a single file that's pretty easy, just type the number when asked and it'll start the download for you. If you wanna multiple downloads, you can always separate the numbers by commas. But there's an even more advance (and cool) way for downloading things, and that's using "slices", here's how to do it with some examples:
>$ pynps -c psv -dt -dde touhou
```
1  ) PSV | PCSE00947 | US   | THEMES  | Touhou Genso Rondo Theme | 6.723 MiB
2  ) PSV | PCSE00990 | US   | THEMES  | Touhou Genso Wanderer PlayStation Vita Theme | 4.514 MiB
3  ) PSV | PCSE01104 | US   | THEMES  | Touhou Kobuto V: Burst Battle 4 Theme | 4.038 MiB
4  ) PSV | PCSB01039 | EU   | THEMES  | Touhou Genso Wanderer PlayStation Vita Theme | 4.514 MiB
5  ) PSV | PCSB01129 | EU   | THEMES  | Touhou Kobuto V: Burst Battle Theme 4 | 4.038 MiB
6  ) PSV | PCSG00999 | JP   | THEMES  | Touhou Kobuto V | 2.533 MiB
7  ) PSV | PCSE01104 | US   | THEMES  | Touhou Kobuto V: Burst Battle Theme 3 | 5.581 MiB
8  ) PSV | PCSE01104 | US   | THEMES  | Touhou Kobuto V: Burst Battle Theme 2 | 5.174 MiB
9  ) PSV | PCSE01104 | US   | THEMES  | Touhou Kobuto V: Burst Battle Theme 1 | 2.533 MiB
10 ) PSV | PCSG90252 | JP   | DEMOS   | Touhou Soujinengi V (DEMO) | 335.6 MiB
Enter the number for what you want to download, you can enter multiple numbers using commas:
```
* To download files 1 to 9, the masochist method, you type: 1,2,3,4,5,6,7,8,9
* To download files 1 to 9, the cool-kid method, you type: 1-9
* To download files 1 to 5 and files 8 to 10: 1-5,8-10
* To download files 1, 4 and files 6 to 10: 1,4,6-10
* To download files 1, 4 and files 6 to 10, the crazy way, as the software doesn't care about order or duplicates: 10-6,1,4,6

******
## More information
Just run:
>$ pynps -h

```
usage: pynps    [-h] [-c {psv,psp,psx,psm}] [-r {usa,eur,jap,asia}] [-dg]
                [-dd] [-dt] [-du] [-dde] [-eb] [-cso {1,2,3,4,5,6,7,8,9}] [-u]
                [--version]
                [search]

pyNPS is a Nopaystation client writen in python 3.7 that, with the help of
wget and pkg2zip, can search, download and decrypt/extract PSVita, PSP, PSX
and PSM games from Nopaystation database.

positional arguments:
  search                search something to download, you can search by name
                        or ID or use '_all' to return everythning.

optional arguments:
  -h, --help            show this help message and exit
  -c {psv,psp,psx,psm}, --console {psv,psp,psx,psm}
                        the console you wanna get content with NPS.
  -r {usa,eur,jap,asia}, --region {usa,eur,jap,asia}
                        the region for the pkj you want.
  -dg, --games          to download PSV/PSP/PSX/PSM games.
  -dd, --dlcs           to download PSV/PSP dlcs.
  -dt, --themes         to download PSV/PSP themes.
  -du, --updates        to download PSV/PSP game updates.
  -dde, --demos         to download PSV demos.
  -eb, --eboot          use this argument to unpack PSP games as EBOOT.PBP
  -cso {1,2,3,4,5,6,7,8,9}, --compress_cso {1,2,3,4,5,6,7,8,9}
                        use this argument to unpack PSP games as a compressed
                        .cso file. You can use any number beetween 1 and 9 for
                        compression factors, were 1 is less compressed and 9
                        is more compressed.
  -u, --update          update database.
  --version             show program's version number and exit

```
******
# Make a donation
kaching kaching

## Paypal
[![paypal](https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=HX93DYLRCWG2W)

## Crypto
BTC: bc1qh53mg0gm6hfjsaphw3x4ct3753rr949lfpere7

LTC: ltc1qp6230jydx7hyht7tu5cuxkk3t7j3t8s0f5wgy8

ETN: etnjyromPydDjvE6m64mvTTrtzd2k7wm3hFCAAsYBc9kdX3N5PHRA3nTescTqq7xGVBrsk8uJXwN5RnwvdbQH2KR6DbHPzE9Ey