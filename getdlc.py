#!/usr/bin/python3
# Created by evertonstz

PKG2ZIP='./pkg2zip'
DBFOLDER='./DATABASE'
DLFOLDER="./DOWNLOADS"

import os, sys
from csv import DictReader
import subprocess
import urllib.request
# from urllib.request import urlopen

#check and create database#
def create_folder( location ):
	try:
		os.makedirs(location)
		print(location,"created")
	except:
		pass

create_folder(DBFOLDER+"/PSV")

#update and download DB

database_psv_links = ["https://beta.nopaystation.com/tsv/PSV_GAMES.tsv", \
					"https://beta.nopaystation.com/tsv/PSV_DLCS.tsv", \
					"https://beta.nopaystation.com/tsv/PSV_THEMES.tsv", \
					"https://beta.nopaystation.com/tsv/PSV_UPDATES.tsv", \
					"https://beta.nopaystation.com/tsv/PSV_DEMOS.tsv", \
					]


#download database files

def save_file( file, string ):
	with open(file, 'w') as file:
	    file.write(string)

def dl_file( url ):
	#detect file#
	system, file = url.split("/")[-1].split("_")
	
	if system == "PSV":
		system_name = "Playstation Vita"

	print("Updating Database for", system_name+":", file)

	process = subprocess.run( [ "wget", "-c", "-P", DBFOLDER+"/"+system+"/", url ] )
	os.rename(DBFOLDER+"/"+system+"/"+url.split("/")[-1], DBFOLDER+"/"+system+"/"+file)


##MAKING FUNCTIONS##

def search_db(system, type, query, region, raw):
	#process query#
	if region.lower() == "all":
		region = "all"
	if region.lower() in ["u","usa","us"]:
		region = "US"
	if region.lower() in ["j","jap","jp"]:
		region = "JP"
	if region.lower() in ["e","eur","eu"]:
		region = "EU"	
	if region.lower() in ["a","asia","as"]:
		region = "ASIA"


	o = []
	f = DBFOLDER+"/PSV/GAMES.tsv"
	with open(f, 'r') as file:
		file = [i for i in DictReader(file, delimiter='\t')]
		# file = csv.reader(file, delimiter="\t", quotechar='"')
	
		for row in file:
			for data in row.values():
				if query in data and row not in o:
					if region == "all":
						o.append(row)
					else:
						if row['Region'] == region:
							o.append(row)

	def process_search( out ):
		for i in out:
			print(i['Title ID'], i['Region'], i['Name'], str(round(float(i['File Size'])/(1024*1024*1024), 2))+"GB" )
	
	if raw == 1:
		return o
	elif raw == 0:
		return process_search(o)

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
		process = subprocess.run( [ "wget", "-c", "-P", DLFOLDER+"/"+system+"/"+i['Name']+" "+ i['Title ID'], i['PKG direct link'] ] )

# download_pkg("psv", ["PCSE00383"])

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("search", type=str, nargs="?",
                    help="name what you want to download.")
parser.add_argument("-c", "--console", help="the console you wanna use with NPS.",
                    type=str, required = True)
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
if args.update == True:
	if args.console == "psv":
		for i in database_psv_links:
			dl_file(i)
	if args.search is None:
		print("No search term provided, exiting...")
		exit(0)
elif args.update == False and args.search is None:
	print("Please, you need to search for something...")
	exit(1)

what_to_dl = [args.games, args.dlcs, args.themes, args.updates, args.demos]

if what_to_dl == [False, False, False, False, False]:
	what_to_dl = [True, True, True, True, True]

print(what_to_dl, args.search)