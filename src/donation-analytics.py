###
###
###@author Devin Hansen
###@version 02/12/18
###
###This is a solution to the Insight Data Engineering Challenge
###This code takes FEC style campaign contribution records as input, as well as a percentile, p
###It outputs a list of repeat donors, the p'th percentile repeat contribution from the donors zip code, and the total contributions from that zip code
###

import math
import sys

errors = 0;

#Make sure we can read all of the input files
try:
	open(sys.argv[1])
	pctl = open(sys.argv[2])
except:
	print("Input file not found")
	errors += 1

#And make sure the percentile is given as an integer
try:
	percentile = int(pctl.read())
except:
	print("2nd argument must direct to a file containing a single number between 0 and 100")
	errors += 1

	
#Open the input file
with open(sys.argv[1]) as infile:

	#Open the output file
	try:	
		outfile = open(sys.argv[3], 'w')
	except:
		print("Cannot create output file")
		errors += 1

	
	#
	#A list of the unique donors discovered so far, their names, zip codes, and dates
	#UniqueDonors[n][0] contains the name of the donor
	#UniqueDonors[n][1] contains the zip code of the donor
	#UniqueDonors[n][2] contains the year the first donation seen so far was made
	UniqueDonors = []
	
	
	
	#
	#A list of each campaign and zip code, all individual repeat donations (sorted by amount), and the total contributed
	#For an input file consisting of a single 
	#RepeatDonors[n][0] contains the combined comittee id and zip code
	#RepeatDonors[n][1] is a sorted list of all contributions for this comittee from the zip code specified in RepeatDonors[n][0]
	#RepeatDonors[n][2] is the sum of the elements in RepeatDonors[n][1], i.e. the total amount recieved from this zip code
	RepeatDonors = []
	

	#Go line by line - since these files can be rather large we want to extract as little data as possible
	for line in infile:
		
		#Initialize boolean flag for catching repeat donors to false
		isRepeat = False
		
		#Initialize a list to hold the data for this line
		temp = []
		k = 0
		
		#Separate out each individual field in this line
		for j in range(0, 21):
			temp.append("")
			i = k
			
			try:
				#Grab data character-by-character until we hit a "|"
				while i < len(line):
				
					if line[i] != '|':
						temp[j] += line[i]
						i += 1
					else:
						k = i + 1
						i = len(line)
			except:
				print("Bad formating")
				errors += 1
		#
		#If the important data on this line looks valid
		#Here we check the following:
		#That the "Other ID" is blank (this must be blank for individual contributions),
		#the zip code is at least 5 characters long,
		#the name is not blank,
		#the amount is not blank,
		#the comittee id is not blank
		#the date is a input in MM/DD/YYYY format
		#
		#If all of this checks out, we press on
		if (temp[15] == "" and len(temp[10]) > 4 and temp[7] != "" and temp[14] != "" and temp[0] != 0 and len(temp[13]) == 8):

			#
			#As long as there are no remaining formating issues...
			try:
				#get a 5 digit zip code
				zip = ""
				for l in range(0, 5):
					zip += temp[10][l]
				
				#get the year off of the full date
				year = ""
				for m in range(4, 8):
					year += temp[13][m]
				
				x = 0
				#Check to see if the donor is a repeat donor
				while (isRepeat == False and x < len(UniqueDonors)):
				
					#If the names and zip codes of a donation matches a previously seen donation, add it to the repeats list and stop searching
					if (temp[7] == UniqueDonors[x][0] and zip == UniqueDonors[x][1]):
						isRepeat = True
						
						#If this is a donation from a previous year, mark it as the first known donation
						if year < UniqueDonors[x][2]:
							UniqueDonors[x][2] == year
							
						else:
						
							#A unique identifier for a given campaign id in a given zip code for each year
							comitteeZipAndYear = temp[0] + zip + year
							
							#Is this the first entry for this campaign in this zip code?
							newZip = True
							
							#initialize a counter and search through the existing campaigns and zip codes.
							n = 0
							while (newZip == True and n < len(RepeatDonors)):
								
								#If there is already an entry for this zip code, append this donation to it, re-sort the list, and add to the total
								if comitteeZipAndYear == RepeatDonors[n][0]:
									
									#Make sure we round to the nearest integer for the individual entries
									RepeatDonors[n][1].append(int(float(temp[14]) + 0.5))
									RepeatDonors[n][1] = sorted(RepeatDonors[n][1])
									
									#We keep the total as a float for now, we'll round to the nearest integer when we output.  This way we dont't compound rounding errors. 
									RepeatDonors[n][2] += float(temp[14])
									
									#flag the zip code as not new
									newZip = False
									
								else:
									n += 1
							
							#If there wasn't an entry for this zip code, make a new one
							if newZip == True:
								
								RepeatDonors.append([comitteeZipAndYear, [int(temp[14])], float(temp[14])])
									
							#Calculate the index of the desired percentile
							pIndex = math.ceil((float(percentile)/100.0)*float(len(RepeatDonors[n][1]))) - 1
							
							#Write the comittee id, zip code, year, percentile, total sum, and # of donations from this zip code
							outfile.write(temp[0] + "|" + zip + "|" + year + "|" + str(RepeatDonors[n][1][pIndex]) + "|" + str(int(RepeatDonors[n][2])) + "|" + str(len(RepeatDonors[n][1])) + "\n")
						
					else:
						x += 1
				
				#if this dosnt look like a repeat donation, log it away for future reference.
				if isRepeat == False:
					UniqueDonors.append([temp[7], zip, year])
			except:
				print("Encountered an error while parsing, skipped a record")
				errors += 1
	
	#Note any errors that occured
	if errors > 0:
		print("Analysis completed with errors")
		
	else:
		print("Analysis completed successfully.  Hooray!")

	
