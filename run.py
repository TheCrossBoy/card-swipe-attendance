import os
import re
import time
import pandas as pd

SAVE_LOCATION="./Attendance/"
EXTENSION=".csv"
COLUMNS="Timestamp,ID\n"
GRADEBOOK_NAME="Gradebook.csv"
DEFAULT_SCORE = 2.0

week_num = input(f"What week would you like to enter attendance for? ")
file_name = "Week" + week_num + "Attendance"
full_path = SAVE_LOCATION + file_name + EXTENSION

if not os.path.isfile(full_path):
	print("! No existing file found, creating a new one.")
	f = open(full_path, "w")
	f.write(COLUMNS)
else:
	print("! Existing file found, appending to it.")
	f = open(full_path, "a")

gradebook = None
if os.path.isfile(GRADEBOOK_NAME):
	gradebook = pd.read_csv(GRADEBOOK_NAME)
	col_raw = f"Week {week_num} Attendance"
	cols = [col for col in gradebook.columns if col_raw in col]
	print(cols)
	if len(cols) == 0:
		print(f"ERROR, {col_raw} NOT FOUND")
		gradebook = None
	else:
		col = cols[0]
		print(f"! Loaded gradebook {GRADEBOOK_NAME} on {col}")
	# print(gradebook)

print("===================")
score = DEFAULT_SCORE
while True:
	# ;09160198161404100000000000000000000?
	inp = input("> ")
	pid = None
	if match := re.search(';(\\d\\d)(\\d\\d\\d\\d\\d\\d\\d\\d)(\\d*)\\?', inp):
		extracted_zone = match.group(1)
		if extracted_zone == "09":
			extracted_id = "A" + match.group(2)
		else:
			extracted_id = match.group(1) + match.group(2) + match.group(3)
		pid = extracted_id
		f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())},{extracted_id}\n")
		f.flush()
		print(f"Checked in {extracted_id}")
	elif match := re.search('(A\\d\\d\\d\\d\\d\\d\\d\\d)', inp):
		pid = match.group(1)
		f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())},{pid}\n")
		f.flush()
		print(f"Checked in manually entered PID {pid}")
	elif match := re.search('@(.*)', inp):
		extracted = match.group(1)
		f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())},{extracted}\n")
		f.flush()

		try:
			pid = gradebook.loc[gradebook['SIS Login ID'] == extracted, 'SIS User ID'].item()
			print(f"Manual entry checked in {extracted} ({pid})")
		except:
			print(f"Manual entry checked in {extracted}, but couldn't find PID.")
			continue
		
		
	elif match := re.search('\\*(\\d*\\.?\\d*)$', inp):
		score = float(match.group(1))
		print(f"Score now {score}")
		continue
	else:
		print("Input doesn't match ID, ending check-in.")
		break
	
	if gradebook is not None and pid is not None:
		try:
			gradebook.loc[gradebook['SIS User ID'] == pid, col] = score
			gradebook.to_csv(GRADEBOOK_NAME, index=False)
			print(f"Added gradebook entry for {gradebook.loc[gradebook['SIS User ID'] == pid, 'Student'].item()}")
		except:
			print(f"Couldn't find row for {pid}!")


f.close()