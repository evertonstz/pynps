#!/usr/bin/python3
#Created by evertonstz
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
import os, sys, inspect
from csv import DictReader
from os.path import join as joindir
import subprocess
import urllib.request
from math import log2
import argparse
import hashlib
import configparser
from prompt_toolkit.validation import Validator, ValidationError
from prompt_toolkit import prompt
from prompt_toolkit import print_formatted_text as printft
from prompt_toolkit import HTML
from tempfile import TemporaryDirectory as TmpFolder
from shutil import copyfile

##FUNCTIONS##
def create_folder( location ):
	try:
		os.makedirs(location)
	except:
		pass

def save_file( file, string ):
	with open(file, 'w') as file:
	    file.write(string)

def get_script_dir(follow_symlinks=True):
    if getattr(sys, 'frozen', False): # py2exe, PyInstaller, cx_Freeze
        path = os.path.abspath(sys.executable)
    else:
        path = inspect.getabsfile(get_script_dir)
    if follow_symlinks:
        path = os.path.realpath(path)
    return os.path.dirname(path)

def fill_term(symbol="-"):
    term_size, __ = os.get_terminal_size()
    return(term_size*symbol)

def progress_bar(number, symbol="#", fill_width=20,open_symbol="[", close_symbol="]", color=False, unfilled_symbol="-"):
	if color == 0:
		slice = int(number*fill_width/100)
		return(open_symbol+symbol*slice+unfilled_symbol*(fill_width-slice)+close_symbol)
	else:
		
		slice = int(number*fill_width/100)
		if fill_width%4 == 0:
			chunks = int(fill_width/4)
			chunks_dir = ""
			for i in range(0, slice):
				if i in range(0, chunks):
					chunks_dir+=LBLUE+symbol
				elif i in range(chunks, chunks*2):
					chunks_dir+=LGREEN+symbol
				elif i in range(chunks*2, chunks*3):
					chunks_dir+=YELLOW+symbol
				elif i in range(chunks*3, chunks*4):
					chunks_dir+=LRED+symbol

			return(open_symbol+chunks_dir+GREY+unfilled_symbol*(fill_width-slice)+close_symbol+NC)
		else:
			print('ERROR: Use a number divisible by 4 in "fill_width".')
			exit(1)

def updatedb( dict, system, DBFOLDER, WGET):
	#detect gaming system#
	if system == "PSV":
		system_name = "Playstation Vita"
	elif system == "PSP":
		system_name = "Playstation Portable"
	elif system == "PSX":
		system_name = "Playstation"
	print("Updating Database for", system_name+":")

	#spawn temporary directory
	
	with TmpFolder() as tmp:
		dl_tmp_folder = tmp+"/"
		
		for t in dict:
			#detect file#
			file = t.upper()+".tsv"
			url = dict[t]

			filename = url.split("/")[-1]

			dl_folder = DBFOLDER+"/"+system+"/"

			#create folder
			create_folder(dl_folder)

			process = subprocess.run( [ WGET, dl_tmp_folder, url ], cwd=dl_tmp_folder)

			print(os.path.isdir(dl_tmp_folder))
			copyfile(dl_tmp_folder+filename, dl_folder+file)
		

		# process = subprocess.Popen( [ WGET, "-c", "-P", DBFOLDER+"/"+system+"/", url ], \
		# 							stdout=subprocess.PIPE, stderr=subprocess.STDOUT )
		
		# saved = False
		# for line in iter(process.stdout.readline, b''):
		# 	line = line.decode("utf-8").split(" ")
			
		# 	#test if downloaded#
		# 	if "saved" in line:
		# 		saved = True
			
		# 	line = [x for x in line if x != ""]
		# 	if '..........' in line:
		# 		line = [x for x in line if x != '..........']
		# 		#variables#
		# 		try:
		# 			percentage = int(line[1].replace("%",""))
		# 		except:
		# 			percentage = 100
		# 		downloaded = line[0]
		# 		speed = line[2].replace("\n","")

		# 		print_string = "Downloading File: " + filename + " " + progress_bar(percentage) + " " + str(percentage) + "% " + \
		# 						downloaded + " @ " + speed+"/s"
		# 		# print("", end = '')
		# 		sys.stdout.write("\r"+print_string)
		# 		sys.stdout.flush()
		# if saved:
		# 	print("\nrenaming file:", DBFOLDER+"/"+system+"/"+filename, DBFOLDER+"/"+system+"/"+file)
		# 	os.rename(DBFOLDER+"/"+system+"/"+filename, DBFOLDER+"/"+system+"/"+file)
		# else:
		# 	print("\nunable to download file, try again later!")

def dl_file( dict, system, DLFOLDER, WGET): #OK!
	system = system.upper()	
	if system == "PSV":
		system_name = "Playstation Vita"
	elif system == "PSP":
		system_name = "Playstation Portable"
	elif system == "PSX":
		system_name = "Playstation"

	url = dict['PKG direct link']
	filename = url.split("/")[-1]
	name = dict['Name']
	title_id = dict['Title ID']

	printft(HTML("<grey>%s</grey>" %fill_term()))
	printft(HTML("<green>[DOWNLOAD] %s</green>" % dict["Name"]))

	dl_folder = DLFOLDER + "/PKG/" + system + "/" + dict['Type']

	#making folder
	create_folder(dl_folder)

	process = subprocess.run( [ WGET, "-c", "-P", dl_folder, url], cwd=dl_folder )#TODO change CWD to a tempfolder
	return True

	#TODO: universal output warapping for wget that's not bound to the english release
	# process = subprocess.Popen( [ WGET, "-c", "-P", dl_folder, url], \
	# 						stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=dl_folder )#

	# saved = False
	# downloaded = False
	# for line in iter(process.stdout.readline, b''):
	# 	print(line)
	# 	line = line.decode("utf-8")
		
	# 	#test if downloaded#
	# 	if "saved" in line:
	# 		saved = True
	# 	if "200 OK" in line:
	# 		downloaded = True
		
	# 	line = line.split(" ")

	# 	line = [x for x in line if x != ""]
	# 	if '..........' in line:
	# 		line = [x for x in line if x != '..........']
	# 		#variables#
	# 		try:
	# 			percentage = int(line[1].replace("%",""))
	# 		except:
	# 			percentage = 100
	# 		downloaded = line[0]
	# 		speed = line[2].replace("\n","")

	# 		print_string = "[" + title_id+ "] " + name + " " + progress_bar(percentage) + " " + str(percentage) + "% " + \
	# 						downloaded + " @ " + speed+"/s"
	# 		# print("", end = '')
	# 		sys.stdout.write("\r"+print_string)
	# 		sys.stdout.flush()
	# if saved:
	# 	print("\nsaved at:", dl_folder+"/"+filename )
	# 	return(saved)
	# if downloaded:
	# 	print("file already in disk:", dl_folder+"/"+filename)
	# 	return(downloaded)

def file_size(size):
	_suffixes = ['bytes', 'KiB', 'MiB', 'GiB', 'TiB', 'PiB', 'EiB', 'ZiB', 'YiB']
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
	return '{:.4g} {}'.format(size / (1 << (order * 10)), _suffixes[order])

def crop_print(text, leng):
	if len(text) < leng:
		add = (leng-len(text))*" "
		return(text+add)
	elif len(text) == leng: 
		return(text)

def process_search( out ):
	#look for the biggest Index value
	biggest_index = sorted([int(x["Index"]) for x in out])
	lenght_str = len(str(biggest_index[-1]))

	for i in out:
		print(crop_print(str(i['Index']), lenght_str),")", i['Title ID'], "|", crop_print(i['Region'], 4), "|", crop_print(i['Type'],7), "|", i['Name'], \
		# print(str(i['Index'])+")", i['Title ID'], "|", crop_print(i['Region'], 4), "|", crop_print(i['Type'],7), "|", i['Name'], \
			"|", file_size(i['File Size']) )
		
def search_db(system, type, query, region, DBFOLDER): #OK!
	query = query.upper()
	#process query#

	if region == "usa":
		region = "US"
	if region == "jap":
		region = "JP"
	if region == "eur":
		region = "EU"
	if region == "asia":
		region = "ASIA"

	#define the files to search
	files_to_search_raw = []
	for r, d, f in os.walk( DBFOLDER+"/"+system.upper()+"/" ):
		for file in f:
			if '.tsv' in file and "_" not in file:
				files_to_search_raw.append(os.path.join(r, file))

	files_to_search =[]
	for i in files_to_search_raw:
		file_system_lst = i.split("/")[-1].replace(".tsv","").lower()
		if type[file_system_lst] == True:
			files_to_search.append(i)

	o = []
	for f in files_to_search:
		with open(f, 'r') as file:
			file = [i for i in DictReader(file, delimiter='\t')]
			# file = csv.reader(file, delimiter="\t", quotechar='"')
			for i in file:
				try:
					i["Upper Name"] = i["Name"].upper()
				except:
					i["Upper Name"] = i["Name"]
				i["Type"] = f.split("/")[-1].replace(".tsv","")
			
			if query == "_ALL":
				for row in file:
					for data in row.values():
						if data == None:
							data = "None"
						if row not in o:
							if region == "all":
								o.append(row)
							else:
								if row['Region'] == region:
									o.append(row)
			else:
				for row in file:
					for data in row.values():
						if data == None:
							data = "None"
						if query in data and row not in o:
							if row['PKG direct link'] != "MISSING":
								if region == "all":
									o.append(row)
								else:
									if row['Region'] == region:
										o.append(row)
	
	return o

def checksum_file( file ):
	
	BUF_SIZE = 65536  # lets read stuff in 64kb chunks!

	sha256 = hashlib.sha256()

	with open(file, 'rb') as f:
		while True:
			data = f.read(BUF_SIZE)
			if not data:
				break
			sha256.update(data)
	return(sha256.hexdigest())

def check_wget( location, CONFIGFOLDER ): #OK!
	#check if the binary is inside de script's folder
	if location == "wget":
		if os.path.isfile(CONFIGFOLDER+"lib/wget"):
			return(CONFIGFOLDER+"lib/wget")
		# print("Using system installed wget")
		return("wget")
	elif os.path.isfile(location) == False:
		#try to search for a binary inside the sysem
		if os.path.isfile("/usr/bin/wget"):
			# print("Using system installed wget")
			new_location = "wget"
			return(new_location)
		else:
			
			return(False)
	else:
		# print("Using user provided wget")
		return(location)

def check_pkg2zip( location, CONFIGFOLDER): #OK!
	#check if the binary is inside de script's folder
	if location == "pkg2zip":
		if os.path.isfile(CONFIGFOLDER+"lib/pkg2zip") == True:
			return(CONFIGFOLDER+"lib/pkg2zip")
		return("pkg2zip")
	elif os.path.isfile(location) == False:
		#try to search for a binary inside the sysem
		if os.path.isfile("/usr/bin/pkg2zip"):
			# print("Using system installed pkg2zip")
			new_location = "pkg2zip"
			return(new_location)
		else:
			
			return(False)
	else:
		# print("Using user provided pkg2zip")
		return(location)

def run_pkg2zip( file, output_location, PKG2ZIP, zrif=False): #OK!
	create_folder(output_location)
	
	if zrif == False:
		process = subprocess.run( [PKG2ZIP,"-x",file] , cwd=output_location)
	else:
		process = subprocess.run( [PKG2ZIP,"-x",file, zrif] , cwd=output_location)

def fix_folder_syntax( folder ):
	new_folder = folder
	if "\\" in folder:
		new_folder = folder.replace("\\", "/")
	if folder.endswith("/"):
		new_folder = folder[:-1]
	return(new_folder)

#config parser functions
def save_conf( file, conf ):
	create_folder(os.path.dirname(file))
	with open(file, 'w') as file:
	    conf.write(file)

def create_config( file, folder ):
	config = configparser.ConfigParser()
	config['pyNPS'] = {'DownloadFolder': folder.replace("/.config/pyNPS/",'/Downloads/pyNPS'), \
		'DatabaseFolder': folder+'database/'}

	config['PSV_Links'] = {'games': 'https://beta.nopaystation.com/tsv/PSV_GAMES.tsv', \
		'dlcs': 'https://beta.nopaystation.com/tsv/PSV_DLCS.tsv', \
		'themes': 'https://beta.nopaystation.com/tsv/PSV_THEMES.tsv', \
		'updates': 'https://beta.nopaystation.com/tsv/PSV_UPDATES.tsv', \
		'demos': 'https://beta.nopaystation.com/tsv/PSV_DEMOS.tsv'
		}
	config['PSP_Links'] = {'games': 'https://beta.nopaystation.com/tsv/PSP_GAMES.tsv', \
		'dlcs': 'https://beta.nopaystation.com/tsv/PSP_DLCS.tsv', \
		'themes': 'https://beta.nopaystation.com/tsv/PSP_THEMES.tsv', \
		'updates': 'https://beta.nopaystation.com/tsv/PSP_UPDATES.tsv'
		}
	config['PSX_Links'] = {'games': 'https://beta.nopaystation.com/tsv/PSX_GAMES.tsv'
		}
	config['BinaryLocations'] =	{'Pkg2zip_Location': '', \
		'Wget_location': ''}
	#saving file
	save_conf(file, config)




##MAIN##
def main():
	CONFIGFOLDER = os.getenv("HOME")+"/.config/pyNPS/"
	config_file = joindir(CONFIGFOLDER, "settings.ini")
	#create conf file
	if os.path.isfile(config_file) == False:
		create_config(config_file, CONFIGFOLDER)
		create_folder(CONFIGFOLDER+"lib/")

	#read conf file
	config = configparser.ConfigParser()
	config.read(config_file)

	#test sections
	if config.sections() != ['pyNPS', 'PSV_Links', 'PSP_Links', 'PSX_Links', 'BinaryLocations']:
		print("ERROR: config file.")
		exit(1)
	elif list(config["PSV_Links"]) != ['games', 'dlcs', 'themes', 'updates', 'demos']:
		print("ERROR: config file.")
		exit(1)		
	elif list(config["PSP_Links"]) != ['games', 'dlcs', 'themes', 'updates']:
		print("ERROR: config file.")
		exit(1)	
	elif list(config["PSX_Links"]) != ['games']:
		print("ERROR: config file.")
		exit(1)	

	#making vars
	DBFOLDER = fix_folder_syntax(config['pyNPS']['databasefolder'])
	DLFOLDER = fix_folder_syntax(config['pyNPS']['downloadfolder'])
	PKG2ZIP =  fix_folder_syntax(config['BinaryLocations']['pkg2zip_location'])
	WGET =  fix_folder_syntax(config['BinaryLocations']['wget_location'])

	#if blank use system installed binaries
	if PKG2ZIP == '':
		PKG2ZIP = check_pkg2zip("pkg2zip", CONFIGFOLDER)
	if WGET == '':
		WGET = check_wget("wget", CONFIGFOLDER)

	#makin dicts for links
	database_psv_links = {}
	for key in config["PSV_Links"]:
		database_psv_links[key] = config["PSV_Links"][key]
	
	database_psp_links = {}
	for key in config["PSP_Links"]:
		database_psp_links[key] = config["PSP_Links"][key]
	
	database_psx_links = {}
	for key in config["PSX_Links"]:
		database_psx_links[key] = config["PSX_Links"][key]
	
	#create args
	parser = argparse.ArgumentParser()

	parser.add_argument("search", type=str, nargs="?",
						help="search something to download, you can search by name or ID or use '_all' to return everythning.")
	parser.add_argument("-c", "--console", help="the console you wanna get content with NPS.",
						type=str, required = True, choices=["psv", "psp", "psx", "_all"])
	parser.add_argument("-r", "--region", help="the region for the pkj you want.",
						type=str, required = False, choices=["usa","eur","jap","asia"])
	parser.add_argument("-dg", "--games", help="to download psv/psp/psx games.",
						action="store_true")
	parser.add_argument("-dd", "--dlcs", help="to download psv/psp dlcs.",
						action="store_true")
	parser.add_argument("-dt", "--themes", help="to download psv/psp themes.",
						action="store_true")
	parser.add_argument("-du", "--updates", help="to download psv/psp game updates.",
						action="store_true")	
	parser.add_argument("-dde", "--demos", help="to download psv demos.",
						action="store_true")				

	parser.add_argument("-u", "--update", help="update database.",
						action="store_true")

	args = parser.parse_args()

	#check if updating db is needed
	
	system = args.console.upper()

	if system == "PSP" and args.demos == True:
		print("ERROR: NPS has no support for demos with the Playstation Portable (PSP), exiting...")
		exit(1)
	if system == "PSX" and True in [args.dlcs, args.themes, args.updates, args.demos]:
		print("ERROR: NPS only supports game downlaods for the Playstation (PSX), exiting...")
		exit(1)

	if system == "_ALL" and args.search != None:
		print("ERROR: you can't search for multiple systems, this option is only used to make a full update like:\n\tmain.py -c _all -u")

	if args.update == True:
		if system == "_ALL":
			print("Updating all databases:")
		if system in ["PSV", "_ALL"]:
			updatedb(database_psv_links, "PSV", DBFOLDER, WGET)
		if system in ["PSP", "_ALL"]:
			updatedb(database_psp_links, "PSP", DBFOLDER, WGET)
		if system in ["PSX", "_ALL"]:
			updatedb(database_psx_links, "PSX", DBFOLDER, WGET)
		print("DONE!")

		if args.search is None:
			if system != "_ALL":
				print("No search term provided, exiting...")
			exit(0)
		
	elif args.update == False and args.search is None:
		print("Please, you need to search for something...")
		exit(1)

	#check region
	if args.region is None:
		reg = "all"
	else:
		reg = args.region

	what_to_dl = {"games":args.games, "dlcs":args.dlcs, "themes":args.themes, \
		"updates":args.updates, "demos":args.demos}

	if list(what_to_dl.values()) == [False, False, False, False, False]:
		what_to_dl = {"games":True, "dlcs":True, "themes":True, "updates":True, "demos":True}

	maybe_download = search_db(args.console, what_to_dl, args.search, reg, DBFOLDER)

	if len(maybe_download) == 0:
		print("No results found, exiting...")
		exit(0)

	#adding indexes to maybe_download
	for i in range(0, len(maybe_download)):
		# maybe_download[i]["Index"] = str(i)
		maybe_download[i]["Index"] = str(i+1)

	#test if the result isn't empty
	if len(maybe_download) == 0:
		print("Oops, there's nothing that matches '" + args.search + "'.Try searching for something else, exiting...")
		exit(0)
	
	#print possible mathes to the user
	if len(maybe_download) > 1:
		printft(HTML("<grey>%s</grey>" %fill_term()))
		printft(HTML("<green>[SEARCH] here are the matches:</green>"))
		process_search(maybe_download)


	#validating input
	class Check_game_input(Validator):
		def validate(self, document):
			text = document.text
			if len(text) > 0:
				#test if number being typed is bigger than the biggest number from game list
				num_p = len(maybe_download)
				if num_p == 1 and text != "1":
					raise ValidationError(message="Your only option is to type 1.",
										cursor_position=0)
				text_processed = text.replace("-"," ").replace(",", " ").split(" ")
				last_texttext_processed = [x for x in text_processed if x != ""]
				last_text = text_processed[-1]

				if "0" in text_processed:
					raise ValidationError(message='Zero is an invalid entry.')

				if last_text.isdigit():
					last_text = int(last_text)
					if last_text > num_p:
						raise ValidationError(message='There are no entries past %i.' %num_p)

				if text.startswith("-") or text.startswith(","):
					# break
					raise ValidationError(message='Start the input with a number. Press "h" for help.',
										cursor_position=0)
				
				if "--" in text or ",," in text or ",-" in text or "-," in text:
					raise ValidationError(message='Use only one symbol to separate numbers. Press "h" for help.')
				
				text = text.replace("-","").replace(",","")
				if text.isdigit() is False and text != "h":
					raise ValidationError(message='Do not use leters. Press "h" for help.')
			else:
				raise ValidationError(message='Enter something or press Ctrl+C to close.',
										cursor_position=0)
	if len(maybe_download) > 1:
		index_to_download_raw = prompt("Enter the number for what you want to download, you can enter multiple numbers using commas: ", validator=Check_game_input())
	else:
		index_to_download_raw = "1"

	#TODO: remove redundant code
	#check if the user didn't sent an empty request
	# if len(index_to_download_raw) == 0:
	# 	print("ERROR: you must select something to download")
	# 	exit(1)

	if index_to_download_raw.lower() == 'h':
		printft(HTML("<grey>\tSuppose you have 10 files to select from:</grey>"))
		printft(HTML("<grey>\tTo download file 2, you type: 2</grey>"))
		printft(HTML("<grey>\tTo download files 1 to 9, the masochist method, you type: 1,2,3,4,5,6,7,8,9</grey>"))
		printft(HTML("<grey>\tTo download files 1 to 9, the cool-kid method, you type: 1-9</grey>"))
		printft(HTML("<grey>\tTo download files 1 to 5 and files 8 to 10: 1-5,8-10</grey>"))
		printft(HTML("<grey>\tTo download files 1, 4 and files 6 to 10: 1,4,6-10</grey>"))
		printft(HTML("<grey>\tTo download files 1, 4 and files 6 to 10, the crazy way, as the software doesn't care about order or duplicates: 10-6,1,4,6</grey>"))
		printft(HTML("<grey>Exiting...</grey>"))
		exit(0)

	#parsing indexes
	index_to_download_raw = index_to_download_raw.replace(" ","").split(",")
	index_to_download = []
	for i in index_to_download_raw:
		if "-" in i and i.count("-") == 1:
			#spliting range
			range_0, range_1 = i.split("-")
			#test if is digit
			if range_0.isdigit() == True and range_1.isdigit() == True:
				#test if there's a zero
				range_0 = int(range_0)
				range_1 = int(range_1)
				
				if range_0 < 1 or range_1 < 1:
					print("ERROR: Invalid syntax, please only use non-zero positive integer numbers")
					exit(1)
				#test if digit 0 is bigger than digit 1
				if range_0 < range_1:
					print(1)
					#populate the index list
					for a in range(range_0, range_1+1):
						if a not in index_to_download:
							index_to_download.append(a)
				elif range_0 > range_1:
					print(1)
					for a in range(range_1, range_0+1):
						if a not in index_to_download:
							index_to_download.append(a)
				else: #range_0 == range_1
					if range_0 not in index_to_download:
						index_to_download.append(range_0)
			else:
				print("ERROR: Invalid syntax, please only use non-zero positive integer numbers")
				exit(1)			
		elif i.isdigit() == True:
			if int(i) not in index_to_download:
				index_to_download.append(int(i))
		else:
			print("ERROR: Invalid syntax, please only use non-zero positive integer numbers")
			exit(1)
			
	#fixing indexes for python syntax and sorting the list
	index_to_download = sorted([int(x)-1 for x in index_to_download])

	files_to_download = [maybe_download[i] for i in index_to_download]

	# if index_to_download_raw == "1":
	printft(HTML("<grey>%s</grey>" %fill_term()))

	printft(HTML("<red>You're going to download the following files:</red>"))
	process_search(files_to_download)

	#validation 2
	class Check_game_input_y_n(Validator):
		def validate(self, document):
			text = document.text
			if len(text) > 0:
				if text.lower() not in ['y','n']:
					# break
					raise ValidationError(message='Use "y" for yes and "n" for no',
										cursor_position=0)
			else:
				raise ValidationError(message='Enter something or press Ctrl+C to close.',
										cursor_position=0)

	accept = prompt("Download files? [y/n]: ", validator=Check_game_input_y_n())

	if accept not in ['y','n']:
		exit(0)

	files_downloaded = []
	for i in files_to_download:
		#download file
		dl_result = dl_file(i, args.console, DLFOLDER, WGET)
		downloaded_file_loc = DLFOLDER + "/PKG/" + system + "/" + i['Type']+"/"+i['PKG direct link'].split("/")[-1]
		
		#checksum
		if dl_result:
			if "SHA256" in i.keys():
				printft(HTML("<grey>%s</grey>" %fill_term()))
				if i["SHA256"] == "":
					print("CHECKSUM: No checksum provided by NPS, skipping check...")
				else:
					
					sha256_dl = checksum_file(downloaded_file_loc)
					
					try:
						sha256_exp = i["SHA256"]
					except:
						sha256_exp = ""

					if sha256_dl != sha256_exp:
						print("CHECKSUM: checksum not matching, pkg file is probably corrupted, delete it at your download folder and redownload the pkg.")
						print("CHECKSUM: corrupted file location:", DLFOLDER + "/PKG/" + system + "/" + i['Type'] + "/" + i['PKG direct link'].split("/")[-1])
						break
					else:
										printft(HTML("<green>[CHECKSUM] downloaded file is ok!</green>"))
			files_downloaded.append(i)
		else:
			print("ERROR: skipping file, wget was unable to download, try again latter...")

	#autoextract with pkg2zip
	# PKG2ZIP = check_pkg2zip(PKG2ZIP)
	# print(PKG2ZIP)
	printft(HTML("<grey>%s</grey>" %fill_term()))
	if PKG2ZIP != False:
		for i in files_downloaded:
			# if i['Type'] not in ["THEMES"]:
			if True:
				zrif=""
				dl_dile_loc = DLFOLDER + "/PKG/" + system + "/" + i['Type'] + "/" + i['PKG direct link'].split("/")[-1]
				dl_location = DLFOLDER+"/Extracted"

				try:
					zrif = i['zRIF']
				except:
					pass
				
				printft(HTML("<green>[EXTRACTION] %s ➔ %s</green>" %(i['Name'], DLFOLDER+"/Extracted/")))
				# print("EXTRACTION:",i['Name'], "➔", DLFOLDER+"/Extracted/")

				if system == "PSV" and zrif !="":
					run_pkg2zip(dl_dile_loc, dl_location, PKG2ZIP, zrif)
				else:
					run_pkg2zip(dl_dile_loc, dl_location, PKG2ZIP)
			else:
				print("EXTRACTION: this type of file can't be extracted by pkg2zip:",i['Type'].lower())
	else:
		print("EXTRACTION: skipping extraction since there's no pkg2zip binary in your system...")
		exit(0)
	printft(HTML("<grey>%s</grey>" %fill_term()))
	printft(HTML("<grey>Done!</grey>"))

if __name__ == '__main__':
	main()