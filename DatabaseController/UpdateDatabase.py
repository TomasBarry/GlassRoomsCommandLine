# fetch html, parse good html data, add data to dict
import re
from urllib import request
from html.parser import HTMLParser
import base64
import Constants


class UpdateDatabase(HTMLParser):

	def __init__(self, database_connection, url, table_name):
		super(UpdateDatabase, self).__init__(convert_charrefs="True")
		self.database_connection = database_connection
		self.table_name = table_name
		
		# dict that will be used when outputting to the db
		self.output_data = {}
		self.latest_key = ""
		self.bookings = ""

		# define the regexs
		self.header_regex = re.compile(Constants.DATE_HEADER_REGEX)
		self.booking_regex = re.compile(Constants.BOOKING_BODY_REGEX)

		# fetch the raw html and get the data
		self.raw_html = self.fetchRawHTML(url)
		self.feed(self.raw_html)

		print(str(self.output_data))


	def fetchRawHTML(self, url):
		fetch_request = request.Request(url)
		added_header = fetch_request.add_header("Authorization", self.generateAuthorizationCode())
		contents = request.urlopen(fetch_request)
		return str(contents.read())

	def generateAuthorizationCode(self):
		username = input("Enter your username: ")
		password = input("Enter your password: ")
		auth_code = str.encode(username + ":" + password)
		encoded_bytes = base64.b64encode(auth_code)
		return ("Basic " + bytes.decode(encoded_bytes))

	def handle_data(self, data):
		# get the clean data
		if self.header_regex.match(data) is not None:
			self.latest_key = data
			self.output_data[self.latest_key] = ""
		elif self.booking_regex.match(data) is not None:
			value = self.output_data[self.latest_key]
			self.output_data[self.latest_key] = value + "\n" + data


UpdateDatabase("c", "https://www.scss.tcd.ie/cgi-bin/webcal/sgmr/sgmr1.pl", "room_1")