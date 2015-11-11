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

def generateUrl(room_number):
	return Constants.URL_HEADER + str(room_number) + Constants.URL_ENDER 


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
			fetch_request = request.Request(generateUrl(1))
			added_header = fetch_request.add_header("Authorization", generateAuthorizationCode(username, password))
			contents = request.urlopen(fetch_request)
			credentials_confirmed = True
		except error.HTTPError:
				print("User credentials were incorrect")

	# establish connection to database
	sql_location = Constants.DATABASE_NAME
	conn = sqlite3.connect(sql_location)
	c = conn.cursor()
	take = True
	while take is True:
		# create and update the tables
		for i in range(Constants.STARTING_ROOM_NUMBER, Constants.ENDING_ROOM_NUMBER + 1):
			table_name = Constants.TABLE_NAME_HEADER + str(i)
			# update the tables
			UpdateDatabase(c, generateUrl(i), table_name, username, password)

		# get user input
		command = input("Enter a command (type 'help' for command options):")
		if command == "help":
			print(command)
		elif command == "today":
			c.execute("SELECT Message FROM {table_name} WHERE Primary_Key is '{today}'".format(table_name = "Room_1", today = getTodayString()))
			today = list((c.fetchone()[0]).split("\n"))
			print("Todays bookings")
			for booking in today:
				print("-------------------------------")
				print(booking)
				print("-------------------------------")
		elif command == "quit":
			take = False
		else:
			print("No such command '" + command + "' found")

	# Committing changes and closing the connection to the database file
	conn.commit()
	conn.close()