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

# local imports
from functions import *
import variables

def cli_main():
    """implement pynps cli interface"""

    if get_system() == 'Linux':
        CONFIGFOLDER = f"{os.getenv('HOME')}/.config/pyNPS"
        config_file = f"{CONFIGFOLDER}/settings.ini"
    elif get_system() == 'Windows':
        CONFIGFOLDER = f"{get_script_dir()}/pynps_config/"
        config_file = f"{CONFIGFOLDER}/settings.ini"
    else:
        CONFIGFOLDER = ""
        config_file = ""      

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
    parser.add_argument("-R", "--resume_session", help="update database.",
                        action="store_true")
    parser.add_argument('--version', action='version',
                        version=f"%(prog)s version {variables.VERSION}")
    
    args = parser.parse_args()

    #check limit rate string
    limit_rate = args.limit_rate
    if limit_rate is not None:
        # check how it ends
        if limit_rate[:-1].isdigit() is False or limit_rate[-1].lower() not in ["k","m","g","t"]:
            printft(HTML("<red>[ERROR] invalid format for --limit_rate</red>"))
            sys.exit(1)
            
    if args.resume_session:
        # in this case args.search will be considered a tag to fast resume a session

        ##check if a tag is not None
            ##make a var calleg tag with the provided tag
        input_tag = args.search
        ##load download db
        with SqliteDict(f"{DLFOLDER}/downloads.db", autocommit=False) as database:
            db = database['resumes']

        checker = next((item for item in db if item['session_tag'] == input_tag), None)
        ## if tag is not None
        if input_tag is not None and checker is not None:
            # has something in db
            session = checker

        elif (input_tag is not None and checker is None) or input_tag is None:
            if input_tag is not None and checker:
                yn_check = input("error no such tag, wanna see all sessions?")
                if yn_check is "n": # TODO: prompt_toolkit
                    sys.exit(0)
            
            p_db = []
            for index_file, i in enumerate(db):
                i["Index"] = index_file + 1
                p_db.append(i)

            
            process_resumes(p_db)
            session_index = input("what session?") # TODO prompt

            session = db[int(session_index) - 1]

        files_to_download = session["session_dict"]

    else:
        keepkg = args.keepkg

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
                printft(HTML("<green>[UPDATEDB] %s:</green>") %variables.FULL_SYSTEM_NAME[i])
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

####### skip all inputs to here!'
    files_downloaded = []
    for i in files_to_download:
        # download file
        dl_result = dl_file(i,  i['System'], DLFOLDER, WGET, limit_rate)

        if dl_result is False:
            # interrupted by user
            resume_dict = []
            for i in files_to_download:
                if i not in files_downloaded:
                    resume_dict.append(i)
            
            # run saving function
            # TODO: ask user for tag
            # TODO don't let duplicate tags
            tag = input("tag:") #TODO prompt
            if tag == "":
                tag = False

            download_save_state(resume_dict, DLFOLDER, tag=tag)

            sys.exit(0)


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

