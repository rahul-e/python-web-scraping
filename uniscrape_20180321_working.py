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
outfile = datapath + 'uniscrape_results_20181109.csv' 

# Define the variable names
varnames = ['Average Professor Rating', 'Overall Quality Rating', 'REPUTATION',	'LOCATION',	'INTERNET',	'FOOD',	'OPPORTUNITY', 'FACILITIES', 'CLUBS', 'SOCIAL',	'HAPPINESS', 'SAFETY', 'University']

# Open the output file and write the varnames
with open(outfile, 'a', newline='') as f:
	writer = csv.writer(f)
	writer.writerow(varnames)

for orgid in range(1, 100):
	try:
		org_url = rate_url + str(orgid)

		r = requests.get(org_url, allow_redirects=True) # Request the webpage
		print(r.status_code) # Confirm if the request was successful (200 = success, anything else = not successful)

		soup = BeautifulSoup(r.text, 'html.parser') # Convert the webpage's text into an object called 'soup'
		#print(soup)

		results = soup.find_all('span', attrs={'class': 'score'}) # Find all web elements called 'span' whose 'class' attribute has the value 'score'
		#print(results)


		scores = [] # Create a list for storing the ratings of each university
		for el in results:
			print(el)
			scores.append(el.text)
		#print(len(scores))

		if len(scores)==11:
			scores.append('.')
			name = soup.find_all('div', attrs={'class': 'result-text'})
			for el in name:
				print(el.text)
				desc = el.text
				desc = desc.replace('\r', '')
				desc = desc.replace('\n', '')
				scores.append(desc)

			with open(outfile, 'a', newline='') as f:
				writer = csv.writer(f)
				writer.writerow(scores)
		else:
			name = soup.find_all('div', attrs={'class': 'result-text'})
			for el in name:
				print(el.text)
				desc = el.text
				desc = desc.replace('\r', '') # Get rid of blank spaces, newlines, carraige returns etc
				desc = desc.replace('\n', '')
				scores.append(desc) # Append the name to the list of scores

			with open(outfile, 'a', newline='') as f: # Open the output file and write the scores as rows
				writer = csv.writer(f)
				writer.writerow(scores)

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