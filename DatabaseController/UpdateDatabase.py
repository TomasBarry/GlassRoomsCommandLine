# fetch html, parse good html data, add data to dict
import re
from urllib import request, error
from html.parser import HTMLParser
from datetime import datetime
import base64
import Constants


class UpdateDatabase(HTMLParser):

	def __init__(self, database_connection, table_name, username, password):
		super(UpdateDatabase, self).__init__(convert_charrefs="True")
		
		self.database_connection = database_connection
		self.table_name = table_name
		self.username = username
		self.password = password

		# define the regexs
		self.header_regex = re.compile(Constants.DATE_HEADER_REGEX)
		self.booking_regex = re.compile(Constants.BOOKING_BODY_REGEX)

		self.database_connection.execute("DROP TABLE IF EXISTS {table_name}".format(table_name = self.table_name))
		self.database_connection.execute("CREATE TABLE IF NOT EXISTS {table_name} (Primary_Key TEXT PRIMARY KEY, Room TEXT, Date TEXT, StartTime TEXT, EndTime TEXT, Message TEXT)".format(table_name = self.table_name))

		for i in range(Constants.STARTING_ROOM_NUMBER, Constants.ENDING_ROOM_NUMBER + 1):
			url = Constants.URL_HEADER + str(i) + Constants.URL_ENDER 
			
			# dict that will be used when outputting to the db
			self.compiled_data = {}
			self.latest_key = []

			# fetch the raw html and get the data
			self.raw_html = self.fetchRawHTML(url)
			self.feed(self.raw_html)

			self.updateDatabase(i)


	def updateDatabase(self, room):
		today = datetime.now()
		for key in self.compiled_data.keys():
			# Take the 12 from '12 Nov 2015 (Thursday): '
			key_date = int(key[0 : key.find(" ")])
			# only instert data that concerns the next 7 days as bookings are only allowed withing 7 days
			if key_date >= int(today.day) and key_date <= (int(today.day) + 7):
				# insert each booking '17:00-19:00 Niamh Clarke [msiss3] SMF'
				for booking in self.compiled_data[key]:
					primary_key = "Room_" + str(room) + " " + key + " " + booking
					start_time = booking[0 : 5]
					end_time = booking[6 : 11]
					message = booking[12 : ]
					self.database_connection.execute("INSERT INTO {table_name} VALUES (?, ?, ?, ?, ?, ?)".format(table_name = self.table_name), (primary_key, room, key_date, start_time, end_time, message))


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
			self.compiled_data[self.latest_key] = []
		elif self.booking_regex.match(data) is not None:
			self.compiled_data[self.latest_key].append(data)