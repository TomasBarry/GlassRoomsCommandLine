#!/bin/bash

# This is the code segment that is run inside __main__.py

#if len(sys.argv) is not 1:
#    fetch_request = request.Request(Constants.URL_HEADER + str(sys.argv[1]) + Constants.URL_BOOKING + Constants.URL_ENDER,
#    data = generateBookingRequest(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7], sys.argv[8]))
#    added_header = fetch_request.add_header("Authorization", generateAuthorizationCode(sys.argv[9], sys.argv[10]))
#    contents = request.urlopen(fetch_request)

HOUR=$(date +%-H)
DAY=$(date +%-u)
MONTH=$(date +%-m)
YEAR=1


# where the User, user name and password are stored
source ~/GlassRoomsCommandLine/user_and_password.config

STATUS='ba3'

book_room () {
	# for each room with preference
	for i in 3 5 6 7 8 2 1 9 4
	do
		# python package_name room start_time end_time full_name status start_date start_month start_year(always 1) user_name password
		python3 ~/GlassRoomsCommandLine/DatabaseController/ $i $1 $2 $NAME $STATUS $3 $4 $YEAR $USER $PASS
		echo ~/GlassRoomsCommandLine/DatabaseController/ $i $1 $2 $NAME $STATUS $3 $4 $YEAR $USER $PASS
	done
}

case $DAY in
	# if Monday, book for Tuesday at 14-16, or 14-15 or 15-16
	1)
		if [ $HOUR = 17 ]
			then
			book_room 14 16 $(date +%-d -d "+1 days") $(date +%-m -d "+1 days");
			book_room 14 15 $(date +%-d -d "+1 days") $(date +%-m -d "+1 days");
			book_room 15 16 $(date +%-d -d "+1 days") $(date +%-m -d "+1 days");
		fi
		exit 1
		;;
	# if Tuesday, book for Wednesday at 14-15
	2)
		if [ $HOUR = 16 ]
			then
			book_room 14 16 $(date +%-d -d "+1 days") $(date +%-m -d "+1 days");
		fi
		exit 1
		;;
	# if Wednesday, book for Thursday at 12-14, 12-13 or 13-14
	3)
		if [$HOUR = 16 ]
			then
			book_room 12 14 $(date +%-d -d "+1 days") $(date +%-m -d "+1 days");
			book_room 12 13 $(date +%-d -d "+1 days") $(date +%-m -d "+1 days");
			book_room 13 14 $(date +%-d -d "+1 days") $(date +%-m -d "+1 days");
		fi
		exit 1
		;;
	# if Thursday, book for Friday at 12-14, 12-13 or 13-14
	4)
		if [ $HOUR = 14 ]
			then
			book_room 12 14 $(date +%-d -d "+1 days") $(date +%-m -d "+1 days");
			book_room 12 13 $(date +%-d -d "+1 days") $(date +%-m -d "+1 days");
			book_room 13 14 $(date +%-d -d "+1 days") $(date +%-m -d "+1 days");
		fi
		exit 1
		;;
	# if Friday, book for Monday at 15-17, 15-16 or 116-17
	5)
		if [ $HOUR = 14 ]
			then
			book_room 12 14 $(date +%-d -d "+3 days") $(date +%-m -d "+3 days");
			book_room 12 13 $(date +%-d -d "+3 days") $(date +%-m -d "+3 days");
			book_room 13 14 $(date +%-d -d "+3 days") $(date +%-m -d "+3 days");
		fi
		exit 1
		;;
	# it's the weekend, book Monday
	6)
		book_room 12 14 $(date +%-d -d "+2 days") $(date +%-m -d "+2 days");
		book_room 12 13 $(date +%-d -d "+2 days") $(date +%-m -d "+2 days");
		book_room 13 14 $(date +%-d -d "+2 days") $(date +%-m -d "+2 days");
		exit 1
		;;
	# it's the weekend, book Monday
	7)
		book_room 12 14 $(date +%-d -d "+1 days") $(date +%-m -d "+1 days");
		book_room 12 13 $(date +%-d -d "+1 days") $(date +%-m -d "+1 days");
		book_room 13 14 $(date +%-d -d "+1 days") $(date +%-m -d "+1 days");
		exit 1
		;;
esac