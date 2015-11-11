import os
import sqlite3
import Constants
from datetime import datetime


"""
	__main__.py

	Create a connection to a local database, if it does not exist then it will
	automatically be created. Create the databases tables if they do not exist
	and then update the database tables by calling the UpdateDatabase class
"""

def generateUrl(room_number):
	return Constants.URL_HEADER + str(room_number) + Constants.URL_ENDER 


if __name__ == "__main__":

	# establish connection to database
	sql_location = Constants.DATABASE_NAME
	conn = sqlite3.connect(sql_location)
	c = conn.cursor()

	# create and update the tables
	for i in range(Constants.STARTING_ROOM_NUMBER, Constants.ENDING_ROOM_NUMBER):
		table_name = Constants.TABLE_NAME_HEADER + str(i)
		# create the tables
		c.execute("CREATE TABLE IF NOT EXISTS {table_name} \
			(Primary_Key TEXT PRIMARY KEY, Timestamp DATETIME, Message TEXT)".format(table_name = table_name))
		# update the tables
		UpdateDatabase(c, generateUrl(i), table_name)

	# Committing changes and closing the connection to the database file
	conn.commit()
	conn.close()