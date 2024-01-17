import os
import re
import time

SAVE_LOCATION="./Attendance/"
EXTENSION=".csv"
COLUMNS="Timestamp,ID\n"

file_name = input(f"Enter the name of the file to save or modify: {SAVE_LOCATION}")
full_path = SAVE_LOCATION + file_name + EXTENSION

if not os.path.isfile(full_path):
	print("! No existing file found, creating a new one.")
	f = open(full_path, "w")
	f.write(COLUMNS)
else:
	print("! Existing file found, appending to it.")
	f = open(full_path, "a")

print("===================")

while True:
	# ;09160198161404100000000000000000000?
	inp = input("> ")
	if match := re.search(';(\\d\\d)(\\d\\d\\d\\d\\d\\d\\d\\d)(\\d*)\\?', inp):
		extracted_zone = match.group(1)
		if extracted_zone == "09":
			extracted_id = "A" + match.group(2)
		else:
			extracted_id = match.group(1) + match.group(2) + match.group(3)
		
		f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())},{extracted_id}\n")
		f.flush()
		print(f"Checked in {extracted_id}")
	elif match := re.search('@(.*)', inp):
		extracted = match.group(1)
		f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())},{extracted}\n")
		f.flush()
		print(f"Manual entry checked in {extracted}")
	else:
		print("Input doesn't match ID, ending check-in.")
		break


f.close()