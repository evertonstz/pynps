#!/usr/bin/python3
# coding=utf-8
# Created by evertonstz
""" This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>. """

##IMPORTS##
import os
import sys
import re
import inspect
import subprocess
import argparse
import hashlib
import configparser
from json import dumps
from shutil import copyfile, which
from csv import DictReader
from math import log2
from sqlitedict import SqliteDict
from prompt_toolkit.validation import Validator, ValidationError
from prompt_toolkit import prompt, HTML, print_formatted_text as printft
from tempfile import TemporaryDirectory as TmpFolder

# Versioning
VERSION = '1.3.1'

##STATIC DICTS AND LISTS##
_FULL_SYSTEM_NAME = {"PSV": "Playstation Vita", "PSP": "Playstation Portable",
                     "PSX": "Playstation", "PSM": "Playstation Mobile"}

_SUFFIXES = ['bytes', 'KiB', 'MiB', 'GiB',
             'TiB', 'PiB', 'EiB', 'ZiB', 'YiB']

_TYPE_DICT = {"GAMES": "Game", "THEMES": "Theme",
              "DLCS": "DLC", "DEMOS": "Demo", "UPDATES": "Update"}

_REGION_DICT = {"US": "USA", "EU": "EUR", "JP": "JAP", "ASIA": "ASIA",
                "INT": "INT", "usa": "US", "jap": "JP", "eur": "EU",
                "asia": "ASIA", "int": "INT", "all":"all"}

_CONF_PSV_LINKS = {'games': 'http://nopaystation.com/tsv/PSV_GAMES.tsv',
                   'dlcs': 'http://nopaystation.com/tsv/PSV_DLCS.tsv',
                           'themes': 'http://nopaystation.com/tsv/PSV_THEMES.tsv',
                           'updates': 'http://nopaystation.com/tsv/PSV_UPDATES.tsv',
                           'demos': 'http://nopaystation.com/tsv/PSV_DEMOS.tsv'
                   }

_CONF_PSP_LINKS = {'games': 'http://nopaystation.com/tsv/PSP_GAMES.tsv',
                   'dlcs': 'http://nopaystation.com/tsv/PSP_DLCS.tsv',
                           'themes': 'http://nopaystation.com/tsv/PSP_THEMES.tsv',
                           'updates': 'http://nopaystation.com/tsv/PSP_UPDATES.tsv'
                   }

_CONF_PSX_LINKS = {'games': 'http://nopaystation.com/tsv/PSX_GAMES.tsv'
                   }

_CONF_PSM_LINKS = {'games': 'http://nopaystation.com/tsv/PSM_GAMES.tsv'
                   }


##FUNCTIONS##

def create_folder(location):
    try:
        os.makedirs(location)
        return True
    except:
        return False

def get_terminal_columns():
    """this function returns the columns' 
    numbers in the terminal"""

    return(os.get_terminal_size().columns)


def fill_term(symbol="-"):
    """this function fills a line in the 
    terminal with given symbol"""

    return(get_terminal_columns()*symbol)

def progress_bar(number, symbol="#", fill_width=20, open_symbol="[", close_symbol="]", color=False, unfilled_symbol="-"):
    if color == 0:
        slice = int(number*fill_width/100)
        return(open_symbol+symbol*slice+unfilled_symbol*(fill_width-slice)+close_symbol)
    # else:

    #     slice = int(number*fill_width/100)
    #     if fill_width % 4 == 0:
    #         chunks = int(fill_width/4)
    #         chunks_dir = ""
    #         for i in range(0, slice):
    #             if i in range(0, chunks):
    #                 chunks_dir += LBLUE+symbol
    #             elif i in range(chunks, chunks*2):
    #                 chunks_dir += LGREEN+symbol
    #             elif i in range(chunks*2, chunks*3):
    #                 chunks_dir += YELLOW+symbol
    #             elif i in range(chunks*3, chunks*4):
    #                 chunks_dir += LRED+symbol

    #         return(open_symbol+chunks_dir+GREY+unfilled_symbol*(fill_width-slice)+close_symbol+NC)
    #     else:
    #         print('ERROR: Use a number divisible by 4 in "fill_width".')
    #         sys.exit(1)


def updatedb(dict, system, DBFOLDER, WGET, types):
    """this function downloads the tsvs databases from nps' website"""

    #detect gaming system#
    system_name = _FULL_SYSTEM_NAME[system]

    # dict = ['/home/everton/.config/pyNPS/database/PSV/PSV_GAMES.tsv',
    #         '/home/everton/.config/pyNPS/database/PSV/PSV_DLCS.tsv'] #remove

    # db_dict = SqliteDict(_DB, autocommit=False)
    def insert_into_DB(tsv, DB, type):
        with open(tsv, 'r') as file:
            # read source tsv file
            file = [i for i in DictReader(file, delimiter='\t')]

            # write ordered dicsts to new db
        # opens db
        with SqliteDict(DB, autocommit=False) as database:
            #checks for console and make a [] in case it doesn't exist
            if system not in database:
                database[system] = []
            system_database = database[system]
            # if next((item for item in file if item['Title ID'] == "Tom" and item["age"] == 11), None) is not None:
            
            for index_file, i in enumerate(file):
                
                print(f"Processing {type}: {progress_bar( int(index_file/(len(file) - 1) * 100) )}", 
                                            f"({index_file}/{len(file) - 1})", 
                                            end="\r")
                
                i["Type"] = type.upper()
                i['System'] = system
                # check if keys part of the dict are already in the database 'Title ID' 'Region' 'Type' 'System'
                try: 
                    checker = next((item for item in system_database if item['Title ID'] == i['Title ID'] and item['Region'] == i['Region'] and item['System'] == i['System'] and item['Type'] == i['Type'] and item['Content ID'] == i['Content ID']), None)
                except:
                    checker = next((item for item in system_database if item['Title ID'] == i['Title ID'] and item['Region'] == i['Region'] and item['System'] == i['System'] and item['Type'] == i['Type']), None)

                if checker is not None:
                    # this means there's already a entry, only updates the last entry
                    if checker != i:
                        # print("Updated database existing entry:", i['Title ID'], i['Region'], i['Type'], i['System'], i['Name'])
                        checker_index = system_database.index(checker)
                        system_database[checker_index].update(i)
                else:
                    # this means it's a new entry
                    # print("New database entry:", i['Title ID'], i['Region'], i['Type'], i['System'], i['Name'])
                    system_database.append(i)
            print() # escapes \r from print above

            # commit changes
            database[system] = system_database
            database.commit()

    with TmpFolder() as tmp:
        dl_tmp_folder = f"{tmp}/"

        for t in dict:
            if t in types:
                # detect file#
                file = f"{t.upper()}.tsv"
                url = dict[t]

                filename = url.split('/')[-1]

                dl_folder = f"{DBFOLDER}/{system}/"

                # create folder
                create_folder(dl_folder)
                process = subprocess.run([WGET, "-q", "--show-progress", url], cwd=dl_tmp_folder)

                #read file and feed to database
                DB = f"{DBFOLDER}/pynps.db"
                insert_into_DB(f"{dl_tmp_folder}{filename}", DB, t) #pass downloaded tsv here in local


def dl_file(dict, system, DLFOLDER, WGET, limit_rate):
    """this function downloads the games"""

    system_name = _FULL_SYSTEM_NAME[system.upper()]

    url = dict['PKG direct link']
    filename = url.split('/')[-1]
    name = dict['Name']
    title_id = dict['Title ID']

    printft(HTML("<grey>%s</grey>") %fill_term())
    printft(HTML("<green>[DOWNLOAD] %s (%s) [%s] for %s</green>") %(name, dict['Region'], title_id, system))

    dl_folder = f"{DLFOLDER}/PKG/{system}/{dict['Type']}"

    # making folder
    create_folder(dl_folder)

    # check if file exists
    if os.path.isfile(f"{dl_folder}/{filename}"):
        printft(HTML("<orange>[DOWNLOAD] file exists, wget will decide if the file is completely downloaded, if it's not the download will be resumed</orange>"))

    try:
        if limit_rate is None:
            process = subprocess.run([WGET, "-q", "--show-progress", "-c",
                                    dl_folder, url], cwd=dl_folder)
        else:
            process = subprocess.run([WGET, "-q", "--show-progress", "-c", "--limit-rate", limit_rate,
                                    dl_folder, url], cwd=dl_folder)           
    except KeyboardInterrupt:
        printft(HTML("\n<orange>[DOWNLOAD] File was partially downloaded, you can resume this download by searching for same pkg again</orange>"))
        printft(HTML("<orange>[DOWNLOAD] File location:</orange> <grey>%s/%s</grey>") %(dl_folder, filename))
        printft(HTML("<grey>Download interrupted by user</grey>"))
        sys.exit(0)
    return True


def file_size(size):
    """this function formats bytes into 
    human readable"""

    if type(size) != int:
        try:
            size = int(size)
        except:
            size = 0
    # determine binary order in steps of size 10
    # (coerce to int, // still returns a float)
    order = int(log2(size) / 10) if size else 0
    # format file size
    # (.4g results in rounded numbers for exact matches and max 3 decimals,
    # should never resort to exponent values)
    return '{:.4g} {}'.format(size / (1 << (order * 10)), _SUFFIXES[order])


def crop_print(text, leng, center=False, align="left"):
    """this function is helper for process_search()"""

    if len(text) < leng:
        if center == False:
            if align == "left":
                add = (leng-len(text))*" "
                return(f"{text}{add}")
            elif align == "right":
                add = (leng-len(text))*" "
                return(f"{add}{text}")
        else:
            if True:
                add1 = int((leng - len(text)) / 2)
                add2 = (leng - len(text)) - add1
                return(f"{add1*' '}{text}{add2*' '}") 
    elif len(text) == leng:
        return text


def process_search(out):
    """this function prints the search result for the 
    user in a human friendly format"""

    # look for the biggest Index value
    biggest_index = sorted([int(x["Index"]) for x in out])
    lenght_str = len(str(biggest_index[-1]))
    try:
        biggest_type = sorted([len(x['Type']) for x in out])[-1] - 1
    except:
        biggest_type = 2 - 1

    try:
        if sorted([len(x['Region']) for x in out])[-1] in [2, 3]:
            biggest_reg = 3
        elif sorted([len(x['Region']) for x in out])[-1] == 4:
            biggest_reg = 4
    except:
        biggest_reg = 2

    for i in out:
        number_str = crop_print(str(i['Index']), lenght_str)
        system_str = i['System']
        id_str = i['Title ID']

        reg_str = crop_print(_REGION_DICT[i['Region']], biggest_reg, center=True)
        type_str = crop_print(_TYPE_DICT[i['Type']], biggest_type, center=False)
        size_str = crop_print(file_size(i['File Size']), 9, center=False, align="right")

        head = f"{number_str}) {system_str} | {id_str} | {reg_str} | {type_str} | "

        tail = f" [{size_str}]"

        head_name = f"{head}{i['Name']}"

        term_cols = get_terminal_columns()

        if len(head_name + tail) <= term_cols:  # no neet to crop
            rest = term_cols - len(head_name + tail)
            print(head_name + rest*" " + tail)
        else:
            thats_more = len(head_name + tail) - term_cols

            remove = len(i['Name']) - thats_more

            if remove > 10:
                head_name = head + i['Name'][:remove]
                head_name = head + i['Name'][:remove]
            else:
                head_name = f"{head}{i['Name']}"
            
            print(f"{head_name}{tail}")


def search_db(systems, type, query, region, DBFOLDER):
    """this function searchs in the tsv databases 
    provided by nps"""

    # start = time.time()

    query = query.upper()
    #process query#
    region = [_REGION_DICT[x] for x in region]

    DB = f"{DBFOLDER}/pynps.db"

    # parse types to search
    types = [x.upper() for x in type if type[x] == True]
    
    
    # read database
    with SqliteDict(DB, autocommit=False) as database:
        # return everything
        result = []
        for system in systems:
            system_database = database[system]
            if query == "_ALL":
                result = result + [item for item in system_database if 
                                    (item['System'] == system and item['Region'] in region and item['Type'] in types) and
                                    (item['PKG direct link'] not in ["", "MISSING", None])
                                    ]
            else:
                result = result + [item for item in system_database if 
                                    (item['System'] == system and item['Region'] in region and item['Type'] in types) and 
                                    (query.lower() in item['Name'].lower() or query.lower() in item['Title ID']) and
                                    (item['PKG direct link'] not in ["", "MISSING", None])
                                    ]
    # end = time.time()
    # print(end - start)

    # exit()
    return(result)

def checksum_file(file):
    """this fuction is used to calculate a sha256 
    checksum for a file"""

    BUF_SIZE = 65536  # lets read stuff in 64kb chunks!

    sha256 = hashlib.sha256()

    with open(file, 'rb') as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            sha256.update(data)
    return(sha256.hexdigest())


def is_tool(name):
    """Check whether `name` is on PATH and marked 
    as executable."""

    ret = which(name)
    if ret == None:
        return False
    else:
        return ret


def check_wget(location, CONFIGFOLDER):
    """this fuction is used to detect a wget 
    installation in the users system"""

    # check if wget is on path and prefer this one
    if is_tool("wget") != False:
        # can be run as wget
        return(is_tool("wget"))
    else:
        # if not on patch, check if it's on lib and prefer this one
        if os.path.isfile(f"{CONFIGFOLDER}/lib/wget"):
            return(f"{CONFIGFOLDER}/lib/wget")
        else:
            # last resort is check for user provided binary in settings.ini
            # check if exists
            if os.path.isfile(location):
                return(location)
            else:
                return False


def check_pkg2zip(location, CONFIGFOLDER):
    """this function is used to detect a pkg2zip 
    installation in the users system"""

    if is_tool("pkg2zip") != False:
        return(is_tool("pkg2zip"))
    else:
        if os.path.isfile(f"{CONFIGFOLDER}/lib/pkg2zip"):
            return(f"{CONFIGFOLDER}/lib/pkg2zip")
        else:
            if os.path.isfile(location):
                return(location)
            else:
                return False


def run_pkg2zip(file, output_location, PKG2ZIP, args, extraction_folder, zrif=False):  # OK!
    """this fuction is used to extract a pkg with pkg2zip"""
    def runner( list, cwd):

        p = subprocess.Popen(list, cwd=cwd,
                     stdout=subprocess.PIPE,
                     stderr=subprocess.STDOUT)
        
        r = re.compile('pkg2zip v\\d.\\d')
        full_out = ''
        for line in iter(p.stdout.readline, b''):
            out = line.rstrip().decode()
            full_out += f"{out}\n"
            if out.startswith("ERROR") == False and r.match(out) is None:
                print(out)
        
        # test if file exist
        
        # test for corrupted and file not being a pkg
        if "ERROR: not a pkg file" in full_out:
            # corrupted file and feeding inexistent file
            if os.path.isfile(file):
                if file.endswith(".pkg"):
                    printft(HTML("<red>[PKG2ZIP] The provided file is is a .pkg, but seems to be corrupted</red>"))
                else:
                    printft(HTML("<red>[PKG2ZIP] The provided file is is not a .pkg</red>"))
            else:
                printft(HTML("<red>[PKG2ZIP] Provided file doesn't exist</red>"))
            return False
        elif "ERROR: pkg file is too small" in full_out:
            # download not ended
            printft(HTML("<red>[PKG2ZIP] The provided file is too small, it's probably corrupted or didn't fully downloaded</red>"))
            return False
        elif "ERROR: failed to read 256 bytes from file" in full_out:
            # feeded a folder to pkg2zip
            if os.path.isdir(file):
                printft(HTML("<red>[PKG2ZIP] The provided file seems to be a folder</red>"))
            else:
                printft(HTML("<red>[PKG2ZIP] Unknown extraction error</red>"))
            return False
        else:
            printft(HTML("<green>[PKG2ZIP] File extracted to: </green><grey>%s</grey>") %extraction_folder)
            return True
    
    # create extraction folder
    create_folder(output_location)

    # reversing list
    args.reverse()

    if zrif == False:
        run_lst = [PKG2ZIP, file]
        for x in args:
            run_lst.insert(1, x)
        process = runner(run_lst, cwd=output_location)
    else:
        run_lst = [PKG2ZIP, file, zrif]
        for x in args:
            run_lst.insert(1, x)
        process = runner(run_lst, cwd=output_location)

    return process


def fix_folder_syntax(folder):
    """this function is used to fix slashes in the 
    directories provided by the user's settings.ini"""

    new_folder = folder
    if "\\" in folder:
        new_folder = folder.replace('\\', '/')
    if folder.endswith('/'):
        new_folder = folder[:-1]
    return new_folder


def save_conf(file, conf):
    """this function is used to save files"""

    # TODO remove create folder from function!
    create_folder(os.path.dirname(file))
    with open(file, 'w') as file:
        conf.write(file)


def create_config(file, folder):
    """this function is used to create a configuration 
    file on first run"""

    config = configparser.ConfigParser()
    config['pyNPS'] = {'DownloadFolder': folder.replace("/.config/pyNPS", "/Downloads/pyNPS/"), 
                        'DatabaseFolder': f"{folder}/database/"}

    config['PSV_Links'] = _CONF_PSV_LINKS
    config['PSP_Links'] = _CONF_PSP_LINKS
    config['PSX_Links'] = _CONF_PSX_LINKS
    config['PSM_Links'] = _CONF_PSM_LINKS

    config['BinaryLocations'] = {'Pkg2zip_Location': f"{folder}/lib/pkg2zip",
                                'Wget_location': f"{folder}/lib/wget"}
    # saving file
    save_conf(file, config)


def get_theme_folder_name(loc):
    """this function helps to print the exact folder 
    name for extracted PSV themes"""

    a = os.listdir(loc)
    a = sorted([int(x) for x in a])
    comp = list(range(1, a[-1] + 1))
    diff = list(set(comp) - set(a))

    if len(diff) > 0:
        selected = diff[0]
    else:  # == 0
        selected = a[-1] + 1
    # put the zeros in the name 00000005 len = 8
    selected = str(selected)
    zero_lst = [0]*(8 - len(selected))
    return_lst = [str(x) for x in zero_lst]
    return_lst.append(selected)
    return(''.join(return_lst))


def main():
    """main function"""

    CONFIGFOLDER = f"{os.getenv('HOME')}/.config/pyNPS"
    config_file = f"{CONFIGFOLDER}/settings.ini"

    # create conf file
    if os.path.isfile(config_file) == False:
        create_config(config_file, CONFIGFOLDER)
        create_folder(CONFIGFOLDER+"/lib/")

    # read conf file
    config = configparser.ConfigParser()
    config.read(config_file)

    # test sections
    if sorted(config.sections()) != sorted(['pyNPS', 'PSV_Links', 'PSP_Links', 'PSX_Links', 'PSM_Links', 'BinaryLocations']):
        printft(HTML("<red>[ERROR] config file: missing sections</red>"))
        print("You need the following sections in your config file: 'PSV_Links', 'PSP_Links', 'PSX_Links', 'PSM_Links', 'BinaryLocations'")
        sys.exit(1)
    if sorted(list(config["PSV_Links"])) != sorted(['games', 'dlcs', 'themes', 'updates', 'demos']):
        printft(HTML("<red>[ERROR] config file: missing options in the PSV_Links section</red>"))
        print("You need the following options in your PSV_Links section: 'games', 'dlcs', 'themes', 'updates', 'demos'")
        sys.exit(1)
    if sorted(list(config["PSP_Links"])) != sorted(['games', 'dlcs', 'themes', 'updates']):
        printft(HTML("<red>[ERROR] config file: missing options in the PSP_Links section</red>"))
        print("You need the following options in your PSP_Links section: 'games', 'dlcs', 'themes', 'updates'")
        sys.exit(1)
    if sorted(list(config["PSX_Links"])) != sorted(['games']):
        printft(HTML("<red>[ERROR] config file: missing options in the PSX_Links section</red>"))
        print("You need the following options in your PSX_Links section: 'games'")
        sys.exit(1)
    if sorted(list(config["PSM_Links"])) != sorted(['games']):
        printft(HTML("<red>[ERROR] config file: missing options in the PSM_Links section</red>"))
        print("You need the following options in your PSM_Links section: 'games'")
        sys.exit(1)

    # making vars
    DBFOLDER = fix_folder_syntax(config['pyNPS']['databasefolder'])
    DLFOLDER = fix_folder_syntax(config['pyNPS']['downloadfolder'])
    PKG2ZIP = fix_folder_syntax(config['BinaryLocations']['pkg2zip_location'])
    WGET = fix_folder_syntax(config['BinaryLocations']['wget_location'])

    # tests existence of pkg2zip
    PKG2ZIP = check_pkg2zip(PKG2ZIP, CONFIGFOLDER)
    if PKG2ZIP == False:
        printft(HTML("<orange>[PKG2ZIP] you don't have a valid pkg2zip installation or binary in your system, extraction will be skipped</orange>"))
        # sys.exit(1)

    # tests existence of wget
    WGET = check_wget(WGET, CONFIGFOLDER)
    if WGET == False:
        printft(HTML("<red>[ERROR] you don't have a valid wget installation or binary in your system, this program can't work without it</red>"))
        sys.exit(1)

    # makin dicts for links
    database_psv_links = {}
    for key in config["PSV_Links"]:
        database_psv_links[key] = config["PSV_Links"][key]

    database_psp_links = {}
    for key in config["PSP_Links"]:
        database_psp_links[key] = config["PSP_Links"][key]

    database_psx_links = {}
    for key in config["PSX_Links"]:
        database_psx_links[key] = config["PSX_Links"][key]

    database_psm_links = {}
    for key in config["PSM_Links"]:
        database_psm_links[key] = config["PSM_Links"][key]

    # create args
    parser = argparse.ArgumentParser(
        description='pyNPS is a Nopaystation client writen in python 3.7 that, with the help of wget and pkg2zip, can search, download and decrypt/extract PSVita, PSP, PSX and PSM games from Nopaystation database.')

    parser.add_argument("search",help="search something to download, you can search by name or ID or use '_all' to return everythning.", 
                        type=str, nargs="?")
    parser.add_argument("-c", "--console", help="the console you wanna get content with NPS.",
                        type=str, required=False, action='append', choices=["psv", "psp", "psx", "psm"])
    parser.add_argument("-r", "--region", help="the region for the pkj you want.",
                        type=str, required=False, action='append', choices=["usa", "eur", "jap", "asia", "int"])
    parser.add_argument("-G", "-dg", "--games", help="to download PSV/PSP/PSX/PSM games.",
                        action="store_true")
    parser.add_argument("-D", "-dd", "--dlcs", help="to download PSV/PSP dlcs.",
                        action="store_true")
    parser.add_argument("-T", "-dt", "--themes", help="to download PSV/PSP themes.",
                        action="store_true")
    parser.add_argument("-U", "-du", "--updates", help="to download PSV/PSP game updates.",
                        action="store_true")
    parser.add_argument("-E", "-dde", "--demos", help="to download PSV demos.",
                        action="store_true")
    parser.add_argument("-k", "--keepkg", help="using this flag will keep the pkg after the extraction",
                        action="store_true")
    parser.add_argument("-eb", "--eboot", help="use this argument to unpack PSP games as EBOOT.PBP",
                        action="store_true")
    parser.add_argument("-cso", "--compress_cso", help="use this argument to unpack PSP games as a compressed .cso file. You can use any number beetween 1 and 9 for compression factors, were 1 is less compressed and 9 is more compressed.",
                        type=str, required=False, choices=[str(x) for x in range(1, 10)])
    parser.add_argument("-l", "--limit_rate", help="limit download speed, input is the same as wget's.",
                        type=str, required=False)
    parser.add_argument("-u", "--update", help="update database.",
                        action="store_true")
    parser.add_argument('--version', action='version',
                        version=f"%(prog)s version {VERSION}")
    
    args = parser.parse_args()

    keepkg = args.keepkg

    #check limit rate string
    limit_rate = args.limit_rate
    if limit_rate is not None:
        # check how it ends
        if limit_rate[:-1].isdigit() is False or limit_rate[-1].lower() not in ["k","m","g","t"]:
            printft(HTML("<red>[ERROR] invalid format for --limit_rate</red>"))
            sys.exit(1)

    if args.console is not None:
        system = list({x.upper() for x in args.console})
    else:
        system = ["PSV", "PSP", "PSX", "PSM"]
    
    if args.eboot is True and args.compress_cso is not None:
        printft(HTML("<red>[ERROR] you can't use --eboot and --compress_cso at the same time</red>"))

    if args.compress_cso is not None:
        cso_factor = args.compress_cso
    else:
        cso_factor = False

    what_to_dl = {"games": args.games, "dlcs": args.dlcs, "themes": args.themes,
                  "updates": args.updates, "demos": args.demos}

    if set(what_to_dl.values()) == set([False]):
        for i in what_to_dl:
            what_to_dl[i] = True

    if args.update == True:
        if [args.region, args.search, args.eboot, args.compress_cso] != [None, None, False, None]:
            printft(HTML("<red>[UPDATEDB] you can't search while updating the database</red>"))
            sys.exit(1)

        printft(HTML("<grey>%s</grey>") %fill_term())
        what_to_up = [x for x in what_to_dl if what_to_dl[x] == True]

        for i in system:
            printft(HTML("<green>[UPDATEDB] %s:</green>") %_FULL_SYSTEM_NAME[i])
            if i == "PSV":
                db = database_psv_links
            elif i == "PSP":
                db = database_psp_links
            elif i == "PSX":
                db = database_psx_links
            elif i == "PSM":
                db = database_psm_links
            
            # parsing supported
            what_to_up_parsed = [x for x in what_to_up if x in db.keys()]
            
            if len(what_to_up_parsed) > 0:
                updatedb(db, i, DBFOLDER, WGET, what_to_up_parsed)
            else:
                printft(HTML("<blue>Nothing to do!</blue>"))

        printft(HTML("<blue>Done!</blue>"))
        sys.exit(0)

    elif args.update == False and args.search is None:
        printft(HTML("<red>[SEARCH] No search term provided, you need to search for something</red>"))
        parser.print_help()
        sys.exit(1)

    # checking for database's existense:
    if os.path.isfile(f"{DBFOLDER}/pynps.db") is False:
        printft(HTML("<red>[UPDATEDB] theres no database in your system, please update your database and try again</red>"))
        sys.exit(1)

    # check if unsupported downloads were called
    if "PSP" in system and args.demos == True:
        printft(HTML("<oragen>[SEARCH] NPS has no support for demos with the Playstation Portable (PSP)</oragen>"))
    if "PSX" in system and True in [args.dlcs, args.themes, args.updates, args.demos]:
        printft(HTML("<oragen>[SEARCH] NPS only supports game downlaods for the Playstation (PSX)</oragen>"))

    # check region
    if args.region == None:
        reg = ["usa", "eur", "jap", "asia", "int"]
    else:
        reg = args.region

    # maybe_download = []
    maybe_download = search_db(system, what_to_dl, args.search, reg, DBFOLDER)

    # test if the result isn't empty
    if len(maybe_download) == 0:
        printft(HTML("<oragen>[SEARCH] No results found, try searching for something else or updating your database</oragen>"))
        sys.exit(0)

    # adding indexes to maybe_download
    for i in range(0, len(maybe_download)):
        # maybe_download[i]["Index"] = str(i)
        maybe_download[i]["Index"] = str(i + 1)

    # print possible mathes to the user
    if len(maybe_download) > 1:
        printft(HTML("<grey>%s</grey>") %fill_term())
        printft(HTML("<green>[SEARCH] here are the matches:</green>"))
        process_search(maybe_download)

    # validating input
    class Check_game_input(Validator):
        def validate(self, document):
            text = document.text
            if len(text) > 0:
                # test if number being typed is bigger than the biggest number from game list
                num_p = len(maybe_download)
                if num_p == 1 and text != "1":
                    raise ValidationError(message="Your only option is to type 1.",
                                          cursor_position=0)
                text_processed = text.replace(
                    "-", " ").replace(",", " ").split(" ")
                last_texttext_processed = [
                    x for x in text_processed if x != ""]
                last_text = text_processed[-1]

                if "0" in text_processed:
                    raise ValidationError(message='Zero is an invalid entry.')

                if last_text.isdigit():
                    last_text = int(last_text)
                    if last_text > num_p:
                        raise ValidationError(
                            message=f"There are no entries past {num_p}.")

                if text.startswith("-") or text.startswith(","):
                    # break
                    raise ValidationError(message='Start the input with a number. Press "h" for help.',
                                          cursor_position=0)

                if "--" in text or ",," in text or ",-" in text or "-," in text:
                    raise ValidationError(
                        message='Use only one symbol to separate numbers. Press "h" for help.')

                text = text.replace("-", "").replace(",", "")
                if text.isdigit() is False and text != "h":
                    raise ValidationError(
                        message='Do not use leters. Press "h" for help.')
            else:
                raise ValidationError(message='Enter something or press Ctrl+C to close. Press "h" for help.',
                                      cursor_position=0)

    if len(maybe_download) > 1:
        try:
            index_to_download_raw = prompt("Enter the number for what you want to download, you can enter multiple numbers using commas: ", 
                                            validator=Check_game_input())
        except KeyboardInterrupt:
            printft(HTML("<grey>Interrupted by user</grey>"))
            sys.exit(0)
        except:
            printft(HTML("<grey>Interrupted by user</grey>"))
            sys.exit(0)
    else:
        index_to_download_raw = "1"

    # provides help
    if index_to_download_raw.lower() == "h":
        printft(HTML("<grey>\tSuppose you have 10 files to select from:</grey>"))
        printft(HTML("<grey>\tTo download file 2, you type: 2</grey>"))
        printft(HTML("<grey>\tTo download files 1 to 9, the masochist method, you type: 1,2,3,4,5,6,7,8,9</grey>"))
        printft(HTML("<grey>\tTo download files 1 to 9, the cool-kid method, you type: 1-9</grey>"))
        printft(HTML("<grey>\tTo download files 1 to 5 and files 8 to 10: 1-5,8-10</grey>"))
        printft(HTML("<grey>\tTo download files 1, 4 and files 6 to 10: 1,4,6-10</grey>"))
        printft(HTML("<grey>\tTo download files 1, 4 and files 6 to 10, the crazy way, as the software doesn't care about order or duplicates: 10-6,1,4,6</grey>"))
        printft(HTML("<grey>Exiting</grey>"))
        sys.exit(0)

    # parsing indexes
    index_to_download_raw = index_to_download_raw.replace(" ", "").split(",")
    index_to_download = []
    for i in index_to_download_raw:
        if "-" in i and i.count("-") == 1:
            # spliting range
            range_0, range_1 = i.split("-")
            # test if is digit
            if range_0.isdigit() == True and range_1.isdigit() == True:
                # test if there's a zero
                range_0 = int(range_0)
                range_1 = int(range_1)

                if range_0 < 1 or range_1 < 1:
                    print("ERROR: Invalid syntax, please only use non-zero positive integer numbers")
                    sys.exit(1)
                # test if digit 0 is bigger than digit 1
                if range_0 < range_1:
                    # populate the index list
                    for a in range(range_0, range_1+1):
                        if a not in index_to_download:
                            index_to_download.append(a)
                elif range_0 > range_1:
                    for a in range(range_1, range_0+1):
                        if a not in index_to_download:
                            index_to_download.append(a)
                else:  # range_0 == range_1
                    if range_0 not in index_to_download:
                        index_to_download.append(range_0)
            else:
                print("ERROR: Invalid syntax, please only use non-zero positive integer numbers")
                sys.exit(1)
        elif i.isdigit() == True:
            if int(i) not in index_to_download:
                index_to_download.append(int(i))
        else:
            print("ERROR: Invalid syntax, please only use non-zero positive integer numbers")
            sys.exit(1)

    # fixing indexes for python syntax and sorting the list
    index_to_download = sorted([int(x)-1 for x in index_to_download])

    files_to_download = [maybe_download[i] for i in index_to_download]

    # if index_to_download_raw == "1":
    printft(HTML("<grey>%s</grey>") %fill_term())
    printft(HTML("<green>[SEARCH] you're going to download the following files:</green>"))

    process_search(files_to_download)

    # validation 2
    class Check_game_input_y_n(Validator):
        def validate(self, document):
            text = document.text
            if len(text) > 0:
                if text.lower() not in ['y', 'n']:
                    # break
                    raise ValidationError(message='Use "y" for yes and "n" for no',
                                          cursor_position=0)
            else:
                raise ValidationError(message='Enter something or press Ctrl+C to close.',
                                      cursor_position=0)

    try:
        accept = prompt("Download files? [y/n]: ",
                        validator=Check_game_input_y_n())
        if accept.lower() != "y":
            raise
    except KeyboardInterrupt:
        printft(HTML("<grey>Interrupted by user</grey>"))
        sys.exit(0)
    except:
        printft(HTML("<grey>Interrupted by user</grey>"))
        sys.exit(0)

    files_downloaded = []
    for i in files_to_download:
        # download file
        dl_result = dl_file(i,  i['System'], DLFOLDER, WGET, limit_rate)
        downloaded_file_loc = f"{DLFOLDER}/PKG/{i['System']}/{i['Type']}/{i['PKG direct link'].split('/')[-1]}"

        # checksum
        if dl_result:
            if "SHA256" in i.keys():
                printft(HTML("<grey>%s</grey>") %fill_term())
                if i["SHA256"] == "":
                    printft(HTML("<orange>[CHECKSUM] No checksum provided by NPS, skipping check</orange>"))
                else:

                    sha256_dl = checksum_file(downloaded_file_loc)

                    try:
                        sha256_exp = i["SHA256"]
                    except:
                        sha256_exp = ""

                    if sha256_dl != sha256_exp:
                        loc = f"{DLFOLDER}/PKG/{i['System']}/{i['Type']}/{i['PKG direct link'].split('/')[-1]}"
                        printft(HTML("<red>[CHECKSUM] checksum not matching, pkg file is probably corrupted, delete it at your download folder and redownload the pkg</red>"))
                        printft(HTML("<red>[CHECKSUM] corrupted file location: </red>") %loc)
                        break
                    else:
                        printft(HTML("<green>[CHECKSUM] downloaded is not corrupted!</green>"))
            files_downloaded.append(i)
        else:
            print("ERROR: skipping file, wget was unable to download, try again latter")

    # autoextract with pkg2zip
    # PKG2ZIP = check_pkg2zip(PKG2ZIP)
    # print(PKG2ZIP)
    printft(HTML("<grey>%s</grey>") %fill_term())
    if PKG2ZIP != False:
        for i in files_downloaded:
            zrif = ""
            dl_dile_loc = f"{DLFOLDER}/PKG/{i['System']}/{i['Type']}/{i['PKG direct link'].split('/')[-1]}"
            dl_location = f"{DLFOLDER}/Extracted"

            try:
                zrif = i['zRIF']
            except:
                pass

            # expose the exact directory were the pkg was extracted!
            extraction_folder = ""
            if i['System'] == "PSV":
                if i["Type"] in ["GAMES", "DEMOS"]:
                    extraction_folder = f"{DLFOLDER}/Extracted/app/{i['Title ID']}"
                    # printft(HTML(f"<green>[EXTRACTION] {i['Name']} ➔ {DLFOLDER}/Extracted/app/{i['Title ID']}</green>"))
                if i["Type"] == "UPDATES":
                    extraction_folder = f"{DLFOLDER}/Extracted/patch/{i['Title ID']}"
                    # printft(HTML(f"<green>[EXTRACTION] {i['Name']} ➔ {DLFOLDER}/Extracted/patch/{i['Title ID']}</green>"))
                if i["Type"] == "DLCS":
                    extraction_folder = f"{DLFOLDER}/Extracted/addcont/{i['Title ID']}"
                    # printft(HTML(f"<green>[EXTRACTION] {i['Name']} ➔ {DLFOLDER}/Extracted/addcont/{i['Title ID']}</green>"))
                if i["Type"] == "THEMES":
                    theme_folder_name = get_theme_folder_name(f"{DLFOLDER}/Extracted/bgdl/t/")
                    extraction_folder = f"{DLFOLDER}/Extracted/bgdl/t/{theme_folder_name}/{i['Title ID']}"
                    # printft(HTML(f"<green>[EXTRACTION] {i['Name']} ➔ {DLFOLDER}/Extracted/bgdl/t/{theme_folder_name}/{i['Title ID']}</green>"))

            if i['System'] == "PSP":
                if i["Type"] == "GAMES":
                    if cso_factor == False and args.eboot == False:
                        extraction_folder = f"{DLFOLDER}/Extracted/pspemu/ISO/<i>game_name</i> [{i['Title ID']}].iso"
                        # printft(HTML(f"<green>[EXTRACTION] {i['Name']} ➔ {DLFOLDER}/Extracted/pspemu/ISO/<i>game_name</i> [{i['Title ID']}].iso</green>"))
                    elif cso_factor in [str(x) for x in range(1, 10)]:
                        extraction_folder = f"{DLFOLDER}/Extracted/pspemu/ISO/<i>game_name</i> [{i['Title ID']}].cso"
                        # printft(HTML(f"<green>[EXTRACTION] {i['Name']} ➔ {DLFOLDER}/Extracted/pspemu/ISO/<i>game_name</i> [{i['Title ID']}].cso</green>"))
                    elif args.eboot == True:
                        extraction_folder = f"{DLFOLDER}/Extracted/pspemu/PSP/GAME/{i['Title ID']}"
                        # printft(HTML(f"<green>[EXTRACTION] {i['Name']} ➔ {DLFOLDER}/Extracted/pspemu/PSP/GAME/{i['Title ID']}</green>"))
                if i["Type"] == "DLCS":
                    extraction_folder = f"{DLFOLDER}/Extracted/pspemu/PSP/GAME/{i['Title ID']}"
                    # printft(HTML(f"<green>[EXTRACTION] {i['Name']} ➔ {DLFOLDER}/Extracted/pspemu/PSP/GAME/{i['Title ID']}</green>"))
                if i["Type"] == "THEMES":
                    extraction_folder = f"{DLFOLDER}/Extracted/pspemu/PSP/THEME/<i>theme_name</i>.PTF"
                    # printft(HTML(f"<green>[EXTRACTION] {i['Name']} ➔ {DLFOLDER}/Extracted/pspemu/PSP/THEME/<i>theme_name</i>.PTF</green>"))
                if i["Type"] == "UPDATES":
                    extraction_folder = f"{DLFOLDER}/Extracted/pspemu/PSP/GAME/{i['Title ID']}"
                    # printft(HTML(f"<green>[EXTRACTION] {i['Name']} ➔ {DLFOLDER}/Extracted/pspemu/PSP/GAME/{i['Title ID']}</green>"))

            if i['System'] == "PSX":
                extraction_folder = f"{DLFOLDER}/Extracted/pspemu/PSP/GAME/{i['Title ID']}"
                # printft(HTML(f"<green>[EXTRACTION] {i['Name']} ➔ {DLFOLDER}/Extracted/pspemu/PSP/GAME/{i['Title ID']}</green>"))

            if i['System'] == "PSM":
                extraction_folder = f"{DLFOLDER}/Extracted/psm/{i['Title ID']}"
                # printft(HTML(f"<green>[EXTRACTION] {i['Name']} ➔ {DLFOLDER}/Extracted/psm/{i['Title ID']}</green>"))

            # -x is default argument to not create .zip files
            pkg2zip_args = ["-x"]
            if cso_factor != False and i["Type"] == "GAMES" and i['System'] == "PSP":
                pkg2zip_args.append("-c"+cso_factor)
            elif cso_factor != False and i["Type"] != "UPDATES" and i['System'] != "PSP":
                printft(HTML("<orange>[EXTRACTION] cso is only supported for PSP games, since you're extracting a %s %s the compression will be skipped</orange>") %(i['System'], i['Type'][:-1].lower()))

            if args.eboot == True and i["Type"] == "GAMES" and i['System'] == "PSP":
                pkg2zip_args.append("-p")
            # append more commands here if needed!

            printft(HTML("<green>[PKG2ZIP] Attempting to extract [%s]%s</green>") %(i['Title ID'], i['Name']))

            if i['System'] == "PSV" and zrif not in ["", "MISSING", None]:
                delete = run_pkg2zip(dl_dile_loc, dl_location, PKG2ZIP, pkg2zip_args, extraction_folder, zrif)
            else:
                delete = run_pkg2zip(dl_dile_loc, dl_location, PKG2ZIP, pkg2zip_args, extraction_folder)

            #testing if extraction was completion and delete file if needed
            if delete == True and keepkg == False:
                # delete file
                printft(HTML("<green>[EXTRACTION] Attempting to delete .pkg file</green>"))
                try:
                    os.remove(dl_dile_loc)
                    printft(HTML("<green>[EXTRACTION] Success, the compressed .pkg was deleted</green>"))
                except:
                    printft(HTML("<red>[EXTRACTION] Unable to delete, you may want to it manually at: </red><grey>%s</grey>") %dl_dile_loc)

    else:
        printft(HTML("<orange>[EXTRACTION] skipping extraction since there's no pkg2zip binary in your system</orange>"))
        sys.exit(0)
    printft(HTML("<grey>%s</grey>") %fill_term())
    printft(HTML("<blue>Done!</blue>"))


if __name__ == '__main__':
    main()