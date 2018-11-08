## Python script to download student ratings from the following websites:
#	- http://www.ratemyprofessors.com/campusRatings.jsp?sid=12839 (Rate My Professor - UoS)
#	- https://www.studentcrowd.com/university-l1006588-s1008458-university_of_stirling-stirling

import csv
import requests
import os
from bs4 import BeautifulSoup

# Define the folder where the downloaded data will be stored
datapath = 'C:/Users/mcdonndz-local/Desktop/data/'
print(datapath)

# Define url where data can be downloaded
rate_url = 'http://www.ratemyprofessors.com/campusRatings.jsp?sid=' # Base url for searching for university ratings

############## DOWNLOAD DATA ##############

print('\r')
print('Starting web scrape')
print('\r')

# Define a file for storing the downloaded data
# SYNTAX NEEDED #

# Define the variable names
varnames = ['Average Professor Rating', 'Overall Quality Rating', 'REPUTATION',	'LOCATION',	'INTERNET',	'FOOD',	'OPPORTUNITY', 'FACILITIES', 'CLUBS', 'SOCIAL',	'HAPPINESS', 'SAFETY', 'University']

# Open the output file and write the varnames
with open(outfile, 'a', newline='') as f:
	writer = csv.writer(f)
	writer.writerow(varnames)

for orgid in range(1, 101): # For a given range of university ids (change these numbers if you want)
	try:
		# Build the search url (call it 'org_url')
		# SYNTAX NEEDED #

		r = requests.get(org_url, allow_redirects=True) # Request the webpage
		print(r.status_code) # Confirm if the request was successful (200 = success, anything else = not successful)

		soup = BeautifulSoup(r.text, 'html.parser') # Convert the webpage's text into an object called 'soup'

		results = soup.find_all('span', attrs={'class': 'score'}) # Find all web elements called 'span' whose 'class' attribute has the value 'score'

		# Create a list for storing the ratings of each university - call it 'scores'
		# SYNTAX NEEDED #

		for el in results: # For each element in the object 'results'
			print(el)
			# Append the text of that element to the 'scores' list
			# SYNTAX NEEDED #

		if len(scores)==11: # If there is no rating for 'SAFETY' i.e. the twelfth column in our output file, then proceed as follows:
			# Append a period ('.') to the scores list
			# SYNTAX NEEDED #
			
			name = soup.find_all('div', attrs={'class': 'result-text'}) # Find the name of the university
			for el in name:
				desc = el.text # Extract the text from the element
				desc = desc.replace('\r', '') # Get rid of carriage returns
				
				# Get rid of new lines i.e. '\n'
				# SYNTAX NEEDED #

				# Append the university name to the 'scores' list
				# SYNTAX NEEDED #

			with open(outfile, 'a', newline='') as f: # Write the list of scores to the output file
				# SYNTAX NEEDED #
				# SYNTAX NEEDED #
				# HINT - See how this was achieved when writing the variable names to the output file

		else: # If we have a score for 'SAFETY' then proceed as follows:
			name = soup.find_all('div', attrs={'class': 'result-text'}) # Find the name of the university
			for el in name:
				# SYNTAX NEEDED #
				# HINT - See initial IF statement
				
			# Open the output file and write the scores as rows
			# SYNTAX NEEDED #

	except:
		print('Cannot find university')

print('\r')
print('Finished searching for universities')		

################# REFLECTIONS ###################

'''
	Consider the following:
		- How can this script be improved? Is it efficient enough i.e. could it be done better, quicker with less code?
		- Are there any ethical considerations?
		- Could you schedule/automate this scrape?
		- Are there other file formats in which the data could be saved?
		- What other information could you scrape from the webpage?
'''