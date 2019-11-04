# pyNPS

Before downloading any of your legally obtained (wink wink wink) game/theme/update/etc you have to update your NPS database, you don't have to do it every time you want to download something, but only once in a while to get info about new games NPS adds to their database:
* updating all system's databases:
>$ python3.7 main.py -c _all -u

<br/><br/>
* updating Playstation Vita's database:
>$ python3.7 main.py -c psv -u

<br/><br/>
* updating Playstation Portable's database:
>$ python3.7 main.py -c psp -u

<br/><br/>
* updating Playstation One's database:
>$ python3.7 main.py -c psx -u

******
## pkg2zip
This script uses pkg2zip to handle the .pkg extractions, there's a bundled binary for the version 1.8, in case you have problems with this binary or you just don't trust it you have other options:

1. You can just delete this binary and just use this software to download the pkg, if the script don't detect a binary either in its folder or installed in the system, it'll just skip the extraction totally;

2. If you're an Arch or Suse user, you can compile it from [AUR](https://aur.archlinux.org/packages/pkg2zip/)

 3. Or you just want to compile it yourself you can to their official repo and grab the sources [here](https://github.com/mmozeiko/pkg2zip/releases). 
******
* updating the PSP database and searching for a Sonic game in any region:
>$ python3.7 main.py -c psp -u -dg sonic
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
1 ) ULUS10323 | US   | GAMES | Sonic Rivals 2 | 455.7 MiB
2 ) ULES00622 | EU   | GAMES | Sonic Rivals | 195.1 MiB
3 ) ULES00940 | EU   | GAMES | Sonic Rivals 2 | 219.8 MiB
4 ) ULUS10195 | US   | GAMES | Sonic Rivals | 196.8 MiB
Enter the number for what you want to download, you can enter multiple separated by commas:
```
******
* search for an european release of spyro for PSX
>$ python3.7 main.py -c psx -r eur -dg crash
```
1 ) NPEE00074 | EU   | GAMES | Spyro 2: Gateway to Glimmer  | 343.6 MiB
2 ) NPEE00074 | EU   | GAMES | Spyro 2: Gateway to Glimmer (German store)  | 343.6 MiB
3 ) NPEE00074 | EU   | GAMES | Spyro 2: Gateway to Glimmer (Russian store)  | 343.6 MiB
4 ) NPEE00075 | EU   | GAMES | Spyro: Year of The Dragon  | 339.6 MiB
5 ) NPEE00075 | EU   | GAMES | Spyro: Year of The Dragon (German store)  | 339.7 MiB
6 ) NPEE00075 | EU   | GAMES | Spyro: Year of The Dragon (Russian store)  | 339.6 MiB
7 ) NPEE00076 | EU   | GAMES | Spyro the Dragon  | 329.8 MiB
8 ) NPEE00076 | EU   | GAMES | Spyro the Dragon (German store)  | 329.8 MiB
9 ) NPEE00076 | EU   | GAMES | Spyro the Dragon (Russian store)  | 329.8 MiB
Enter the number for what you want to download, you can enter multiple separated by commas:
```
******
* search for for themes and demos related to the word "touhou in any region:
>$ python3.7 main.py -c psv -dt -dde touhou
```
1  ) PCSE00947 | US   | THEMES | Touhou Genso Rondo Theme | 6.723 MiB
2  ) PCSE00990 | US   | THEMES | Touhou Genso Wanderer PlayStation Vita Theme | 4.514 MiB
3  ) PCSE01104 | US   | THEMES | Touhou Kobuto V: Burst Battle 4 Theme | 4.038 MiB
4  ) PCSB01039 | EU   | THEMES | Touhou Genso Wanderer PlayStation Vita Theme | 4.514 MiB
5  ) PCSB01129 | EU   | THEMES | Touhou Kobuto V: Burst Battle Theme 4 | 4.038 MiB
6  ) PCSG00999 | JP   | THEMES | Touhou Kobuto V | 2.533 MiB
7  ) PCSE01104 | US   | THEMES | Touhou Kobuto V: Burst Battle Theme 3 | 5.581 MiB
8  ) PCSE01104 | US   | THEMES | Touhou Kobuto V: Burst Battle Theme 2 | 5.174 MiB
9  ) PCSE01104 | US   | THEMES | Touhou Kobuto V: Burst Battle Theme 1 | 2.533 MiB
10 ) PCSG90252 | JP   | DEMOS  | Touhou Soujinengi V (DEMO) | 335.6 MiB
Enter the number for what you want to download, you can enter multiple separated by commas:
```
******
* search for for everything (themes, games, demos, dlcs and updates) related to the word "knight" in any region region:
>$ python3.7 main.py -c psv knight
* or if you like suffering:
>$ python3.7 main.py -c psv -dg -dd -dt -du -dde knight
```
1  ) PCSE00244 | US   | GAMES   | Valhalla Knights 3 | 897.8 MiB
13 ) PCSA00017 | US   | DLCS    | LittleBigPlanet Knights of Old Pre-Order Costume Pack | 100 KiB
49 ) PCSB00861 | EU   | THEMES  | Digimon Story Cyber Sleuth Custom Theme: Royal Knights Set | 4.999 MiB
53 ) PCSB00743 | EU   | UPDATES | Shovel Knight | 120.8 MiB
Enter the number for what you want to download, you can enter multiple separated by commas:
```
******
* I see... you just wanna everything related to Shovel Knight? Sure:
>$ python3.7 main.py -c psv "shovel knight"
```
1 ) PCSE00640 | US   | GAMES   | Shovel Knight | 132.2 MiB
2 ) PCSB00743 | EU   | GAMES   | Shovel Knight | 137.6 MiB
3 ) PCSE00640 | US   | THEMES  | Shovel Knight Theme | 4.34 MiB
4 ) PCSE00640 | US   | UPDATES | Shovel Knight | 124.1 MiB
5 ) PCSB00743 | EU   | UPDATES | Shovel Knight | 120.8 MiB
Enter the number for what you want to download, you can enter multiple separated by commas:
```
******
* wanna return every single american DLC for the psvita? Sure, it's slow but it's a free country:
>$ python3.7 main.py -c psv -r usa -dd _all
```
that's too big to output here, mate :<
```
******


For more information just run:
>$ python3.7 main.py -h

```
usage: main.py [-h] -c {psv,psp,psx} [-r {usa,eur,jap,asia}] [-dg] [-dd] [-dt]
               [-du] [-dde] [-u]
               [search]

positional arguments:
  search                search something to download, you can search by name
                        or ID.

optional arguments:
  -h, --help            show this help message and exit
  -c {psv,psp,psx}, --console {psv,psp,psx}
                        the console you wanna get content with NPS.
  -r {usa,eur,jap,asia}, --region {usa,eur,jap,asia}
                        the region for the pkj you want.
  -dg, --games          to download games.
  -dd, --dlcs           to download dlcs.
  -dt, --themes         to download themes.
  -du, --updates        to download updates.
  -dde, --demos         to download demos.
  -u, --update          update database.
```
