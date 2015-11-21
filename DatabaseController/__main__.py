import os
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


def generateAuthorizationCode(username, password):
	auth_code = str.encode(username + ":" + password)
	encoded_bytes = base64.b64encode(auth_code)
	return ("Basic " + bytes.decode(encoded_bytes))


def getTodayString():
	today = datetime.today()
	return today.strftime("%d %b %Y (%A):")


if __name__ == "__main__":

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

		elif command == "quit":
			take = False
		else:
			print("No such command '" + command + "' found")