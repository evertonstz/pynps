#!/usr/bin/python3
# Created by evertonstz
import os, sys
from csv import DictReader
import subprocess
import urllib.request
from math import log2
import argparse

#./ will use the same folder the script is currently inside
MAIN_DOWNLOAD_FOLDER="./"


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

# def create_folder( location ):
# 	try:
# 		os.makedirs(location)
# 		print(location,"created")
# 	except:
# 		pass

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
	url = dict['PKG direct link']
	#detect file#
	system = system.upper()
	
	if system == "PSV":
		system_name = "Playstation Vita"

	# print("Updating Database for", system_name+":", file)

	process = subprocess.run( [ "wget", "-c", "-P", DLFOLDER+"/"+system+"/", url ] )
	# os.rename(DBFOLDER+"/"+system+"/"+url.split("/")[-1], DBFOLDER+"/"+system+"/"+file)

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

def process_search( out, index ):
	if index == True:
		ind = 1
		for i in out:
			print(ind,")",i['Title ID'], "|", crop_print(i['Region'], 4), "|", i['Type'], i['Name'], \
				"|", file_size(i['File Size']) )
			ind += 1
			# print(i['Title ID'], i['Region'], i['Type'], i['Name'], i['File Size'] )
	elif index == False:
		for i in out:
			print(i['Title ID'], "|", crop_print(i['Region'], 4), "|", i['Type'], i['Name'], \
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
	for i in type.keys():
		if type[i] == True:
			files_to_search.append(DBFOLDER+"/"+system.upper()+"/"+i.upper()+".tsv")
	
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

# search_db("psv","games", "Sonic", "all", 0)

##DOWNLOADING##

def download_pkg(system, id_list):
	system = system.upper()
	#test if dl folder exists
	create_folder(DLFOLDER+"/"+system)

	to_dl = []

	for i in id_list:
		to_dl.append(search_db(system, "all", i, "all", 1)[0])

	for i in to_dl:
		print("Downloading:", i['Title ID'], i['Region'], i['Name'])
		# filename = wget.download(i['PKG direct link'], out=DLFOLDER+"/"+system)
		print( 'Downloading DLC', end="\r" )
		process = subprocess.run( [ "wget", "-c", "-P", \
			DLFOLDER+"/"+system+"/"+i['Name']+" "+ i['Title ID'], i['PKG direct link'] ] )

###MAIN STARTS HERE###

# download_pkg("psv", ["PCSE00383"])

parser = argparse.ArgumentParser()
parser.add_argument("search", type=str, nargs="?",
                    help="name what you want to download.")
parser.add_argument("-c", "--console", help="the console you wanna use with NPS.",
                    type=str, required = True, choices=["psv", "psp"])
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

# create_folder(DBFOLDER+"/PSV")

#check if updating db is needed
if args.update == True:
	if args.console == "psv":
		updatedb(database_psv_links, "PSV")
	elif args.console == "psp":
		updatedb(database_psp_links, "PSP")

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
process_search(maybe_download, 1)
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
print(files_to_download)

if input("\nProceed to download files? [y/n]:") != "y":
	exit(0)

for i in files_to_download:
	dl_file(i, args.console)