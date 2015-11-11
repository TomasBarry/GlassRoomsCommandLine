# fetch html, parse good html data, add data to dict
import re
from urllib import request, error
from html.parser import HTMLParser
from datetime import datetime
import base64
import Constants


class UpdateDatabase(HTMLParser):

	def __init__(self, database_connection, url, table_name, username, password):
		super(UpdateDatabase, self).__init__(convert_charrefs="True")
		
		self.database_connection = database_connection
		self.table_name = table_name
		self.username = username
		self.password = password
		
		# dict that will be used when outputting to the db
		self.compiled_data = {}
		self.latest_key = ""
		self.bookings = ""

		# define the regexs
		self.header_regex = re.compile(Constants.DATE_HEADER_REGEX)
		self.booking_regex = re.compile(Constants.BOOKING_BODY_REGEX)

		# fetch the raw html and get the data
		self.raw_html = self.fetchRawHTML(url)
		self.feed(self.raw_html)

		self.updateDatabase()


	def updateDatabase(self):
		today = datetime.now()
		self.database_connection.execute("DROP TABLE IF EXISTS {table_name}".format(table_name = self.table_name))
		self.database_connection.execute("CREATE TABLE IF NOT EXISTS {table_name} (Primary_Key TEXT PRIMARY KEY, Timestamp DATETIME, Message TEXT)".format(table_name = self.table_name))
		for key in self.compiled_data.keys():
			if int(key[0 : key.find(" ")]) >= int(today.day):
				self.database_connection.execute("INSERT INTO {table_name} (Primary_Key, Timestamp, Message) VALUES(?, ?, ?)".format(table_name = self.table_name), (key, today.isoformat(" "), self.compiled_data[key]))
		


	def fetchRawHTML(self, url):
		fetch_request = request.Request(url)
		added_header = fetch_request.add_header("Authorization", self.generateAuthorizationCode())
		contents = request.urlopen(fetch_request)
		return str(contents.read())


	def generateAuthorizationCode(self):
		auth_code = str.encode(self.username + ":" + self.password)
		encoded_bytes = base64.b64encode(auth_code)
		return ("Basic " + bytes.decode(encoded_bytes))


	def handle_data(self, data):
		# get the clean data
		if self.header_regex.match(data) is not None:
			self.latest_key = data
			self.compiled_data[self.latest_key] = ""
		elif self.booking_regex.match(data) is not None:
			value = self.compiled_data[self.latest_key]
			self.compiled_data[self.latest_key] = value + "\n" + data


# UpdateDatabase("c", "https://www.scss.tcd.ie/cgi-bin/webcal/sgmr/sgmr1.pl", "room_1")