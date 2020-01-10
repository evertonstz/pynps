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
# from functions import *
from pynps.functions import *
# import variables
import pynps.variables as variables

#external imports
from uuid import uuid4 as id_gen

def cli_main(maindir=""):
    """implement pynps cli interface"""

    if get_system() == 'Linux':
        CONFIGFOLDER = f"{os.getenv('HOME')}/.config/pyNPS"
        config_file = f"{CONFIGFOLDER}/settings.ini"
    elif get_system() == 'Windows':
        CONFIGFOLDER = f"{maindir}/pynps_config/"
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
    DBFOLDER = fix_folder_syntax(config['pyNPS']['databasefolder'], maindir)
    DLFOLDER = fix_folder_syntax(config['pyNPS']['downloadfolder'], maindir)
    PKG2ZIP = fix_folder_syntax(config['BinaryLocations']['pkg2zip_location'], maindir)
    WGET = fix_folder_syntax(config['BinaryLocations']['wget_location'], maindir)

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
    args, parser = create_args()

    limit_rate = args.limit_rate
    keepkg = args.keepkg
    system = args.console
    cso_factor = args.compress_cso
    
    if args.resume_session:
        # in this case args.search will be considered a tag to fast resume a session

        input_tag = args.search
        if input_tag is not None:
            if input_tag.isalnum() is False:
                printft(HTML("<orange>[DOWNLOAD] Tags can only be alphanumeric without spaces</orange>"))
                input_tag = None
           
        ##load download db
        with SqliteDict(f"{DBFOLDER}/downloads.db", autocommit=False) as database:
            try:
                db = database['resumes']
                if len(db) == 0:
                    raise
            except:
                printft(HTML("<orange>[DOWNLOAD] There are no saved download sessions to resume</orange>"))
                sys.exit(0)

        checker = next((item for item in db if item['session_tag'] == input_tag), None)
        
        ## if tag is prvided and there's a match in the db
        if input_tag is not None and checker is not None:
            # has something in db
            session = checker

        elif checker is None or input_tag is None:
            if input_tag is not None:
                printft(HTML("<orange>[DOWNLOAD] There's no such tag in download sessions</orange>"))

                # validation resume input
                class Check_resume_input_y_n(Validator):
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
                    yn_check = prompt("Wanna see all currently download sessions? [y/n]: ",
                                    validator=Check_resume_input_y_n())
                    if yn_check.lower() != "y":
                        raise
                except KeyboardInterrupt:
                    printft(HTML("<grey>Interrupted by user</grey>"))
                    sys.exit(0)
                except:
                    printft(HTML("<grey>Interrupted by user</grey>"))
                    sys.exit(0)
            
            printft(HTML("<grey>%s</grey>") %fill_term())
            
            p_db = []
            for index_file, i in enumerate(db):
                i["Index"] = index_file + 1
                p_db.append(i)

            
            process_resumes(p_db)

            # validating input
            class Check_resume_input(Validator):
                def validate(self, document):
                    text = document.text
                    if len(text) > 0:
                        if text.isdigit():

                            # test if number being typed is bigger than the biggest number from game list
                            num_p = len(db)
                            if num_p == 1 and text != "1":
                                raise ValidationError(message="Your only option is to type 1.",
                                                    cursor_position=0)
                            if int(text) > num_p:
                                raise ValidationError(
                                    message=f"There are no entries past {num_p}.")
                        else:
                            raise ValidationError(message="Please only use numbers",
                                                    cursor_position=0)
                    else:
                        raise ValidationError(message='Enter something or press Ctrl+C to close. Press "h" for help.',
                                            cursor_position=0)


            try:
                session_index = prompt("Enter the number for the download session you want to resume: ", 
                                                validator=Check_resume_input())
            except KeyboardInterrupt:
                printft(HTML("<grey>Interrupted by user</grey>"))
                sys.exit(0)
            except:
                printft(HTML("<grey>Interrupted by user</grey>"))
                sys.exit(0)

            session = db[int(session_index) - 1]

        files_to_download = session["session_dict"]

    else:

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


        # check region
        if args.region == None:
            reg = ["usa", "eur", "jap", "asia", "int"]
        else:
            reg = args.region

        # maybe_download = []
        maybe_download = search_db(system, what_to_dl, args.search, reg, DBFOLDER)

        # test if the result isn't empty
        if len(maybe_download) == 0:
            printft(HTML("<orange>[SEARCH] No results found, try searching for something else or updating your database</orange>"))
            sys.exit(0)

        # adding indexes to maybe_download
        for i in range(0, len(maybe_download)):
            # maybe_download[i]["Index"] = str(i)
            maybe_download[i]["Index"] = str(i + 1)

        # print possible mathes to the user
        if len(maybe_download) > 1:
            if args.print is True:
                for i in maybe_download:
                    print(f"{i['Index']} {i['System']} | {i['Title ID']} | {variables.REGION_DICT[i['Region']]} | {i['Type']} | {i['Name']} | [{file_size(i['File Size'])}]".encode("utf-8"))
                sys.exit(0)
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

####### skip all inputs to here in case of a resume :)
    """fully process game by game inside a single "for"
    # this is useful to change the state for every game in the resume list
    # proposed "Status" key in the dictionary will be as follow:
    
    # 0 - PKG not downloaded:
    #         this is already checked by the dl_file() fucntion!
    #         Also, this should be the default parameter?
    
    # 1 - PKG downloaded, but not extracted:
    #         the status will be updated to 1 after the download passes checksum
    #         a good place to do it could be around ### 1 HERE
    
    # 2 - PKG downloaded and extracted!
    #         the package should be removed from the resume dictionary when it reaches this status
    #         a good place to do it could be around ### 2 HERE

    'files_downloaded' starts with no itens
    'files_to_download' starts with all itens to be downloaded

    for i in files_to_download:
        downloads i

        if dl_results is False:
            do processing for resuming download latter
        
        save download locationg into 'downloaded_file_loc' var

        call pkg_checksum() function (WIP) into 'chekcsum' var

        if checksum is True:
            if PKG2ZIP == False:
                append i to 'files_downloaded' list
            else:
                proceed to extract pkg with pkg2zip

                if extraction is ok:
                    delete pkg file if needed
                    append i to 'files_downloaded' list
                    
                remove i from list in the database!!! 
        else:
            skip file
    """
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
            # TODO: alert about closing with control + c to not save session
            # TODO don't let duplicate tags
            
            printft(HTML("<grey>%s</grey>") %fill_term())
            # tag save validation
            class Check_tag_save(Validator):
                def validate(self, document):
                    text = document.text
                    if text.isalnum() is False and text != "": #only let alphanumeric
                        # break
                        raise ValidationError(message='Only alphanumeric characters, without spaces, are supported for tag naming.',
                                            cursor_position=0)

            try:
                tag = prompt("If you wanna save this download session to easily resume it latter, give this session a tag (you can use control+c to not save it or just leave blank to use a generated tag): ",
                                validator=Check_tag_save())
            except KeyboardInterrupt:
                printft(HTML("<grey>Interrupted by user</grey>"))
                sys.exit(0)
            
            if tag == "":
                tag = False

            # check if the current session already has a loaded UUID
            try:
                session_id = session['session_id']
                if tag == False:
                    tag = session['session_tag']
            except:
                # this means it's a new session!
                session_id = str(id_gen())
            download_save_state(resume_dict, DBFOLDER, id=session_id,  tag=tag)

            sys.exit(0)

        downloaded_file_loc = f"{DLFOLDER}/PKG/{i['System']}/{i['Type']}/{i['PKG direct link'].split('/')[-1]}"

        # checksum
        # TODO: transform into function?
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
                    printft(HTML("<red>[CHECKSUM] corrupted file location: %s</red>") %loc)
                    break # skip file
                else:
                    printft(HTML("<green>[CHECKSUM] downloaded is not corrupted!</green>"))
        
        ### 1 HERE
        

        printft(HTML("<grey>%s</grey>") %fill_term())

        if PKG2ZIP != False:
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
                    if cso_factor == None and args.eboot == False:
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
            if cso_factor != None and i["Type"] == "GAMES" and i['System'] == "PSP":
                pkg2zip_args.append("-c"+cso_factor)
            elif cso_factor != None and i["Type"] != "UPDATES" and i['System'] != "PSP":
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

            ### 2 HERE
            files_downloaded.append(i)
        else:
            printft(HTML("<orange>[EXTRACTION] skipping extraction since there's no pkg2zip binary in your system</orange>"))
            
            ### 2 HERE
            files_downloaded.append(i)

    printft(HTML("<grey>%s</grey>") %fill_term())
    printft(HTML("<blue>Done!</blue>"))

