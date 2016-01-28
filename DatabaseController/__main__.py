import os
import sys
import getpass
import sqlite3
import Constants
from datetime import datetime
from UpdateDatabase import UpdateDatabase
import base64
from urllib import request, error

"""
	__main__.py

	Create a connection to a local database, if it does not exist then it will
	automatically be created. Create the databases tables if they do not exist
	and then update the database tables by calling the UpdateDatabase class
"""

def generateBookingRequest(start_time, end_time, name, status, date, month, year):
	#return {
	#	"StartTime" : start_time,
	#	"EndTime" : end_time,
	#	"FullName" : name,
	#	"Status" : status,
	#	"StartDate" : date,
	#	"StartMonth" : month,
	#	"StartYear" : year
	#}
	return str.encode("StartTime={0}&EndTime={1}&Fullname={2}&Status={3}&StartDate={4}&StartMonth={5}&StartYear={6}".format((int(start_time) + 1), (int(end_time) + 1), name, status, date, month, year))


def generateAuthorizationCode(username, password):
	auth_code = str.encode(username + ":" + password)
	encoded_bytes = base64.b64encode(auth_code)
	return ("Basic " + bytes.decode(encoded_bytes))


def getTodayString():
	today = datetime.today()
	return today.strftime("%d %b %Y (%A):")


if __name__ == "__main__":
	
	if len(sys.argv) is not 1:
		fetch_request = request.Request(Constants.URL_HEADER + str(sys.argv[1]) + Constants.URL_BOOKING + Constants.URL_ENDER, 
			data = generateBookingRequest(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7], sys.argv[8]))
		added_header = fetch_request.add_header("Authorization", generateAuthorizationCode(sys.argv[9], sys.argv[10]))
		contents = request.urlopen(fetch_request)
	else:
		credentials_confirmed = False

		while credentials_confirmed is False:

			# get user credentials
			username = input("Enter your username: ")
			password = getpass.getpass("Enter your password: ")

			try:
				fetch_request = request.Request(Constants.URL_HEADER + str(1) + Constants.URL_ENDER )
				added_header = fetch_request.add_header("Authorization", generateAuthorizationCode(username, password))
				contents = request.urlopen(fetch_request)
				credentials_confirmed = True
			except error.HTTPError:
				print("User credentials were incorrect")

		# establish connection to database
		sql_location = Constants.DATABASE_NAME
		conn = sqlite3.connect(sql_location)
		c = conn.cursor()

		UpdateDatabase(c, Constants.TABLE_NAME, username, password)
		# Committing changes and closing the connection to the database file
		conn.commit()
		conn.close()

		today = datetime.now()
		take = True
		while take is True:
			# get user input
			command = (input("Enter a command (type 'help' for command options):")).lower()

			if command == "update":
				conn = sqlite3.connect(sql_location)
				c = conn.cursor()
				UpdateDatabase(c, Constants.TABLE_NAME, username, password)
				# Committing changes and closing the connection to the database file
				conn.commit()
				conn.close()
				print("Updated database")

			elif command == "help":
				print(command)
	
			elif command == "today":
				room = (input("What Room?")).lower()
				conn = sqlite3.connect(sql_location)
				c = conn.cursor()
				if room == "all":
					c.execute("SELECT Room, StartTime, EndTime, Message FROM {table_name} WHERE Date = {today}".format(table_name = Constants.TABLE_NAME, today = today.day))
				else:
					c.execute("SELECT Room, StartTime, EndTime, Message FROM {table_name} WHERE Date = {today} AND Room = {room_number}".format(table_name = Constants.TABLE_NAME, today = today.day, room_number = room))	
				for booking in c.fetchall():
					print("| Room: " + booking[0] + " | From: " + booking[1] + " | To " + booking[2] + " | - booked")
				# Committing changes and closing the connection to the database file
				conn.commit()
				conn.close()

			elif command == "book":
				room = (input("What Room?")).lower()
				start_time = input("From:")
				end_time = input("To:")
				name = input("What is your first name?")
				status = "ba3"
				date = input("Day:")
				month = input("Month:")
				year = "1"
				fetch_request = request.Request(Constants.URL_HEADER + str(room) + Constants.URL_BOOKING + Constants.URL_ENDER, data = generateBookingRequest(start_time, end_time, name, status, date, month, year))
				added_header = fetch_request.add_header("Authorization", generateAuthorizationCode(username, password))
				contents = request.urlopen(fetch_request)
	
			elif command == "quit":
				take = False
			else:
				print("No such command '" + command + "' found")

