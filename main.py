#!/usr/bin/python3
# Created by evertonstz
import os, sys
from csv import DictReader
import subprocess
import urllib.request
from math import log2
import argparse
import hashlib

#leaving None will use the same folder the script is currently inside
MAIN_DOWNLOAD_FOLDER=None

if MAIN_DOWNLOAD_FOLDER is None:
	MAIN_DOWNLOAD_FOLDER = os.path.dirname(os.path.realpath(__file__))+"/"


PKG2ZIP=MAIN_DOWNLOAD_FOLDER+'pkg2zip'
DBFOLDER=MAIN_DOWNLOAD_FOLDER+'DATABASE'
DLFOLDER=MAIN_DOWNLOAD_FOLDER+"DOWNLOADS"

database_psv_links = {"games":"https://beta.nopaystation.com/tsv/PSV_GAMES.tsv", \
					"dlcs":"https://beta.nopaystation.com/tsv/PSV_DLCS.tsv", \
					"themes":"https://beta.nopaystation.com/tsv/PSV_THEMES.tsv", \
					"updates":"https://beta.nopaystation.com/tsv/PSV_UPDATES.tsv", \
					"demos":"https://beta.nopaystation.com/tsv/PSV_DEMOS.tsv", \
					}

database_psp_links = {"games":"https://beta.nopaystation.com/tsv/PSP_GAMES.tsv", \
					"dlcs":"https://beta.nopaystation.com/tsv/PSP_DLCS.tsv", \
					"themes":"https://beta.nopaystation.com/tsv/PSP_THEMES.tsv", \
					"updates":"https://beta.nopaystation.com/tsv/PSP_UPDATES.tsv", \
					}

database_psx_links = {"games":"https://beta.nopaystation.com/tsv/PSX_GAMES.tsv"}

def create_folder( location ):
	try:
		os.makedirs(location)
	except:
		pass

def save_file( file, string ):
	with open(file, 'w') as file:
	    file.write(string)

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

def updatedb( dict, system ):
	#detect gaming system#
	if system == "PSV":
		system_name = "Playstation Vita"
	elif system == "PSP":
		system_name = "Playstation Portable"
	elif system == "PSX":
		system_name = "Playstation"
	print("Updating Database for", system_name+":")
	
	for t in dict:
		#detect file#
		file = t.upper()+".tsv"
		url = dict[t]

		filename = url.split("/")[-1]
		process = subprocess.Popen( [ "wget", "-c", "-P", DBFOLDER+"/"+system+"/", url ], \
									stdout=subprocess.PIPE, stderr=subprocess.STDOUT )
		
		saved = False
		for line in iter(process.stdout.readline, b''):
			line = line.decode("utf-8").split(" ")
			
			#test if downloaded#
			if "saved" in line:
				saved = True
			
			line = [x for x in line if x != ""]
			if '..........' in line:
				line = [x for x in line if x != '..........']
				#variables#
				try:
					percentage = int(line[1].replace("%",""))
				except:
					percentage = 100
				downloaded = line[0]
				speed = line[2].replace("\n","")

				print_string = "Downloading File: " + filename + " " + progress_bar(percentage) + " " + str(percentage) + "% " + \
								downloaded + " @ " + speed+"/s"
				# print("", end = '')
				sys.stdout.write("\r"+print_string)
				sys.stdout.flush()
		if saved:
			print("\nrenaming file:", DBFOLDER+"/"+system+"/"+filename, DBFOLDER+"/"+system+"/"+file)
			os.rename(DBFOLDER+"/"+system+"/"+filename, DBFOLDER+"/"+system+"/"+file)
		else:
			print("\nunable to download file, try again later!")

def dl_file( dict, system ):
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

	print("\nDownloading:")

	dl_folder = DLFOLDER + "/PKG/" + system + "/" + dict['Type']

	process = subprocess.Popen( [ "wget", "-c", "-P", dl_folder, url], \
							stdout=subprocess.PIPE, stderr=subprocess.STDOUT )
	
	saved = False
	downloaded = False
	for line in iter(process.stdout.readline, b''):
		# print(line)
		line = line.decode("utf-8")
		
		#test if downloaded#
		if "saved" in line:
			saved = True
		if "The file is already fully retrieved" in line:
			downloaded = True
		
		line = line.split(" ")

		line = [x for x in line if x != ""]
		if '..........' in line:
			line = [x for x in line if x != '..........']
			#variables#
			try:
				percentage = int(line[1].replace("%",""))
			except:
				percentage = 100
			downloaded = line[0]
			speed = line[2].replace("\n","")

			print_string = "[" + title_id+ "] " + name + " " + progress_bar(percentage) + " " + str(percentage) + "% " + \
							downloaded + " @ " + speed+"/s"
			# print("", end = '')
			sys.stdout.write("\r"+print_string)
			sys.stdout.flush()
	if saved:
		print("\nsaved at:", dl_folder+"/"+filename+"\n" )
		return(saved)
	if downloaded:
		print("file already in disk:", dl_folder+"/"+filename+"\n")
		return(downloaded)

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

def process_search( out, index, lenght=None ):
	if index == True:
		ind = 1
		lenght_str = len(str(lenght))

		for i in out:
			print(crop_print(str(ind), lenght_str),")",i['Title ID'], "|", crop_print(i['Region'], 4),\
				 "|", crop_print(i['Type'],7), "|", i['Name'], "|", file_size(i['File Size']) )
			ind += 1
			# print(i['Title ID'], i['Region'], i['Type'], i['Name'], i['File Size'] )
	elif index == False:
		for i in out:
			print(i['Title ID'], "|", crop_print(i['Region'], 4), "|", crop_print(i['Type'],7), "|", i['Name'], \
				"|", file_size(i['File Size']) )
		
def search_db(system, type, query, region):
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
	files_to_search = []
	for r, d, f in os.walk( DBFOLDER+"/"+system.upper()+"/" ):
		for file in f:
			if '.tsv' in file and "_" not in file:
				files_to_search.append(os.path.join(r, file))

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

def check_pkg2zip( location ):
	#check if the binary is inside de script's folder
	if os.path.isfile(location) == False:
		#try to search for a binary inside the sysem
		if os.path.isfile("/usr/bin/pkg2zip"):
			new_location = "/usr/bin/pkg2zip"
			return(new_location)
		else:
			return(False)
	else:
		return(location)

def run_pkg2zip( file, output_location, zrif=False):
	create_folder(output_location)
	
	if zrif == False:
		process = subprocess.run( [PKG2ZIP,"-x",file] , cwd=output_location)
	else:
		process = subprocess.run( [PKG2ZIP,"-x",file, zrif] , cwd=output_location)


	

###MAIN STARTS HERE###

parser = argparse.ArgumentParser()

parser.add_argument("search", type=str, nargs="?",
                    help="search something to download, you can search by name or ID.")
parser.add_argument("-c", "--console", help="the console you wanna get content with NPS.",
                    type=str, required = True, choices=["psv", "psp", "psx"])
parser.add_argument("-r", "--region", help="the region for the pkj you want.",
                    type=str, required = False, choices=["usa","eur","jap","asia"])
parser.add_argument("-dg", "--games", help="to download games.",
                    action="store_true")
parser.add_argument("-dd", "--dlcs", help="to download dlcs.",
                    action="store_true")
parser.add_argument("-dt", "--themes", help="to download themes.",
                    action="store_true")
parser.add_argument("-du", "--updates", help="to download updates.",
                    action="store_true")	
parser.add_argument("-dde", "--demos", help="to download demos.",
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

if args.update == True:
	if system == "PSV":
		updatedb(database_psv_links, system)
	if system == "PSP":
		updatedb(database_psp_links, system)
	if system == "PSX":
		updatedb(database_psx_links, system)

	if args.search is None:
		print("DONE!")
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

maybe_download = search_db(args.console, what_to_dl, args.search, reg)

#print possible mathes to the user

process_search(maybe_download, 1, len(maybe_download))
index_to_download = input("Enter the number for what you want to download, you can enter multiple separated by commas:")

index_to_download = index_to_download.replace(" ","").split(",")
try:
	index_to_download = [int(x)-1 for x in index_to_download]
except:
	print("Please, only use numbers.")
	exit(1)

files_to_download = [maybe_download[i] for i in index_to_download]

print("\nYou're going to download the following files:")
process_search(files_to_download, 0)

if input("\nDownload files? [y/n]:") != "y":
	exit(0)

files_downloaded = []
for i in files_to_download:
	#download file
	dl_result = dl_file(i, args.console)
	downloaded_file_loc = DLFOLDER + "/PKG/" + system + "/" + i['Type']+"/"+i['PKG direct link'].split("/")[-1]
	
	#checksum
	if dl_result:
		if "SHA256" in i.keys():
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
					print("CHECKSUM: downloaded file is ok!")
		files_downloaded.append(i)
	else:
		print("ERROR: skipping file, wget was unable to download, try again latter...")

#autoextract with pkg2zip
PKG2ZIP = check_pkg2zip(PKG2ZIP)
if PKG2ZIP != False:
	for i in files_downloaded:
		if i['Type'] not in ["THEMES"]:
			zrif=""
			dl_dile_loc = DLFOLDER + "/PKG/" + system + "/" + i['Type'] + "/" + i['PKG direct link'].split("/")[-1]
			dl_location = DLFOLDER+"/Extracted"

			try:
				zrif = i['zRIF']
			except:
				pass
			print("\nEXTRACTION:",i['Name'])
			print("\nEXTRACTION: extracting files to:",DLFOLDER+"/Extracted/")

			if system == "PSV" and zrif !="":
				run_pkg2zip(dl_dile_loc, dl_location, zrif)
			else:
				run_pkg2zip(dl_dile_loc, dl_location)
		else:
			print("\nEXTRACTION: this type of file can't be extracted by pkg2zip:",i['Type'].lower())
else:
	print("\nEXTRACTION: skipping extraction since there's no pkg2zip binary in your system...")
	exit(0)