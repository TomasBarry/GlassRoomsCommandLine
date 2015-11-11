DATABASE_NAME = "glass_rooms.sqlite"
STARTING_ROOM_NUMBER = 1
ENDING_ROOM_NUMBER = 9
TABLE_NAME_HEADER = "Room_"
URL_HEADER = "https://www.scss.tcd.ie/cgi-bin/webcal/sgmr/sgmr"
URL_ENDER = ".pl"

# Regex Constants
# DATE_HEADER_REGEX: regex to match '4 Nov 2015 (Wednesday):'
# BOOKING_BODY_REGEX: regex to match '13:00-14:00 Sterling Archer [ba3] NATO phonetic alphabet practice'

DATE_HEADER_REGEX = "[0-9]{1,2} [A-Z][a-z]+ 20[0-9]{2,2} \([A-Z][a-z]+\):"
BOOKING_BODY_REGEX = "[0-9][0-9]:00-[0-9][0-9]:00 "