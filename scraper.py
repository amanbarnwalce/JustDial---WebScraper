from bs4 import BeautifulSoup
import urllib2
import csv

hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

searchUrl = raw_input("Enter the Url with pagination\n")
	   
def get_name(body):
	return body.find('span', {'class':'lng_cont_name'}).string

def get_phone_number(body):
	phone = ''
	for item in body.find_all('span', {'class':'mobilesv'}):
		if item['class'][1] == 'icon-dc':
			phone += '+'
		elif item['class'][1] == 'icon-fe':
			phone += '('
		elif item['class'][1] == 'icon-hg':
			phone += ')'
		elif item['class'][1] == 'icon-ba':
			phone += '-'
		elif item['class'][1] == 'icon-ji':
			phone += '9'
		elif item['class'][1] == 'icon-lk':
			phone += '8'
		elif item['class'][1] == 'icon-nm':
			phone += '7'
		elif item['class'][1] == 'icon-po':
			phone += '6'
		elif item['class'][1] == 'icon-rq':
			phone += '5'
		elif item['class'][1] == 'icon-ts':
			phone += '4'
		elif item['class'][1] == 'icon-vu':
			phone += '3'
		elif item['class'][1] == 'icon-wx':
			phone += '2'
		elif item['class'][1] == 'icon-yz':
			phone += '1'
		elif item['class'][1] == 'icon-acb':
			phone += '0'
	return phone

def get_rating(body):
	rating = 0.0
	text = body.find('span', {'class':'star_m'})
	if text is not None:
		for item in text:
			rating += float(item['class'][0][1:])/10

	return rating

def get_rating_count(body):
	text = body.find('span', {'class':'rt_count'}).string

	# Get only digits
	rating_count =''.join(i for i in text if i.isdigit())
	return rating_count

def get_address(body):
	address = ''
	try:
		address = body.find('span', {'class':'mrehover'}).text.strip()
	except AttributeError, e:
		print 'AttributeError'
	return address
		

def get_location(body):
	text = body.find('a', {'class':'rsmap'})
	text_list = text['onclick'].split(",")
	
	latitutde = text_list[3].strip().replace("'", "")
	longitude = text_list[4].strip().replace("'", "")
	
	return latitutde + ", " + longitude

page_number = 1
service_count = 1


fields = ['Name', 'Phone', 'Rating', 'Rating Count', 'Address']
out_file = open('data.csv','wb')
csvwriter = csv.DictWriter(out_file, delimiter=',', fieldnames=fields)

# Write fields first
csvwriter.writerow(dict((fn,fn) for fn in fields))

while True:
	# Check if reached end of result
	url= searchUrl + "%s" % (page_number)
	req = urllib2.Request(url, headers=hdr)
	try:
		page = urllib2.urlopen(req)
	except urllib2.HTTPError, e:
		print e.fp.read()

	soup = BeautifulSoup(page.read(), "html.parser")
	services = soup.find_all('li', {'class': 'cntanr'})
	if len(services) == 0:
		break


	# Iterate through the 10 results in the page
	for service_html in services:

		# Parse HTML to fetch data
		dict_service = {}
		dict_service['Name'] = get_name(service_html)
		dict_service['Phone'] = get_phone_number(service_html)
		dict_service['Rating'] = get_rating(service_html)
		dict_service['Rating Count'] = get_rating_count(service_html)
		dict_service['Address'] = get_address(service_html)
		#print get_location(service_html)

		# Write row to CSV
		csvwriter.writerow(dict_service)

		print "#" + str(service_count) + " " + dict_service['Name']
		service_count += 1

	page_number += 1

out_file.close()









