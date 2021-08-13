import gspread
import random
import copy
import time
import smtplib

port = 2525
smtp_server = "smtp.mailtrap.io"
login = "a3b48bd04430b7" # your login generated by Mailtrap
password = "0ec73c699a910c" # your password generated by Mailtrap

from google.oauth2.service_account import Credentials
from datetime import datetime
from datetime import timedelta
from datetime import date
from pprint import pprint
from socket import gaierror

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('BIKES')

bikes_list = SHEET.worksheet('bike_list').get_all_values()
bikes_list2 = SHEET.worksheet('bike_list')
responses_list = SHEET.worksheet('form_responses').get_all_values()
sort_data = SHEET.worksheet('sort_data').get_all_values()
calendar = SHEET.worksheet('calendar').get_all_values()
calendar2 = SHEET.worksheet('calendar2').get_all_values()
update_calendar2 = SHEET.worksheet('calendar2')
update_calendar = SHEET.worksheet('calendar')
gs_size_guide = SHEET.worksheet('size_guide').get_all_values()

booked_bikes = []
not_booked_bikes = []
bikes_dictionary = []
#num_req_bikes = ""
unavailable_bikes = []
hire_dates_requested = []
dates_filled_in_previous = sort_data[1][1]
#print(dates_filled_in_previous)
sender = responses_list[-1][3]
receiver = "lucycatherine92@gmail.com"

#print(responses_list[-1])

def get_latest_response():
    """
    Fetch the latest form response from googlesheets and determine
    driving factors for bike selection
    """
    # get type and quantity of bikes selected
    # get heights
    # get date and duration of hire

    global types_list
    global heights_list

    # get the most recent form response from google sheets
    last_response = responses_list[-1]

    types_list_orig = [(last_response[7]), (last_response[9]),
    (last_response[11]), (last_response[13]), (last_response[15])]

    heights_list_orig = [(last_response[8]), (last_response[10]),
    (last_response[12]), (last_response[14]), (last_response[16])]

    global booking_number
    booking_number = last_response[18]

    # max bikes hired = 5, but remove empty values from list
    types_list = list(filter(None, types_list_orig))
    heights_list = list(filter(None, heights_list_orig))

    # create dictionaries to store info about each bike requested
    for j in range(len(types_list)):
        d = {
            'booking_number': booking_number,
            'dates_of_hire': [],
            'bike_type': types_list[j],
            'user_height': heights_list[j],
            'bike_size': "",
            'possible_matches': [],
            'num_bikes_available': "",
            'price_per_day': "",
            'status': "Not booked",
            'comments': "",
            'booked_bike': "",
        }
        bikes_dictionary.append(d)

    global num_req_bikes
    num_req_bikes = len(bikes_dictionary)
    #print(f"Num req bikes = {num_req_bikes}")

    match_size(bikes_dictionary)
    #booking_number_occured(bikes_dictionary)
    

# def booking_number_occured(bikes_dictionary):
#     """
#     This function determines if this booking number
#     has already been run through the booking process
#     If it has, stop
#     """

#     # for all bike indexes in the calendar
#     for i in range(len(calendar2)):

#         # and for all cells in that row
#         for j in range(len(calendar2[i])):

#             # do not count the first column (ie Bike Index)
#             if j > 0:

#                 # look for the booking number
#                 if str(bikes_dictionary[0]['booking_number']) == calendar2[i][j]:
#                     print(bikes_dictionary[0]['booking_number'])
#                     print(i)
#                     print(j)
#                     print("This booking has already been completed")
#                     raise SystemExit

#     match_size(bikes_dictionary)


def match_size(bikes_dictionary):
    """
    Match the heights specified in user form to the correct bike size
    """

    # iterate through list of bikes dictionaries (max 5)
    for i in range(len(bikes_dictionary)):

        # iterate through available bike sizes in size_guide google sheet
        for j in range(3, 9):

            # if the bike size in size_guide is the same as the user height
            # index the relevant bike size
            # and append to the dictionary
            if (gs_size_guide[j][4]) == bikes_dictionary[i]['user_height']:
                bikes_dictionary[i]['bike_size'] = gs_size_guide[j][8]

    match_price(bikes_dictionary)


def match_price(bikes_dictionary):
    """
    Fetch the price per day based on the bike type selected
    and append to dictionary
    """
    print(bikes_dictionary)
    print(booked_bikes)
    print("MATCH PRICE SLEEP")
    time.sleep(10)

    # iterate through list of bikes dictionaries (max 5)
    for i in range(len(bikes_dictionary)):

        # iterate through gs_bikes_list
        for j in range(len(bikes_list)):

            # if the bike type in the gs_bikes_list is same as that of the
            # dictionary, index the relevant price
            # and append to the dictionary
            if (bikes_list[j][4]) == bikes_dictionary[i]['bike_type']:
                bikes_dictionary[i]['price_per_day'] = bikes_list[j][5]

    find_unavailable_bikes()


def find_unavailable_bikes():
    """
    Define a list of unavailable bikes for those dates
    """

    # get users selected date
    users_start_date = responses_list[-1][5]
   
    # put date in readable format
    start_date = datetime.strptime(users_start_date, "%m/%d/%Y")

    # calculate end date based on the hire duration
    delta = timedelta(days=int(responses_list[-1][6]) - 1)
    delta_day = timedelta(days=int(1))
    end_date = start_date + delta

    # list all dates in between and append to
    # hire_dates_requested
    # only do this ONCE
    if len(hire_dates_requested) == 0:
        while start_date <= end_date:
            hire_dates_requested.append(start_date.strftime("%m/%d/%Y"))
            start_date += delta_day

    # for each date in the requested hire period
    for k in range(len(hire_dates_requested)):

        # and for each bike index in the calendar
        for i in range(len(calendar)):

            # if any of the bike indexes in the calendar are found
            # in the requested hire period
            if hire_dates_requested[k] in calendar[i]:

                if calendar[i][0] not in unavailable_bikes:

                    # then create a list of these unavailabe bikes
                    # if not calendar[i][0] in unavailable_bikes:
                    unavailable_bikes.append(calendar[i][0])

    # also look for blanket unavailability in bikes list
    # only do this ONCE
    if len(booked_bikes) == 0:

        # for each bike in bikes list
        for q in range(len(bikes_list)):

            # if Available? is No, append bike index to unavailable_bikes
            if bikes_list[q][6] == "No":
                unavailable_bikes.append(bikes_list[q][0])


    print(unavailable_bikes)

    match_suitable_bikes(bikes_dictionary)


def match_suitable_bikes(bikes_dictionary):
    """
    Use submitted form info to find selection of appropriate bikes
    """

    # loop through bikes requested, and compare to
    # bikes available in hire fleet
    # output the bike index of bikes which
    #  match type of those requested to the bike dictionaries
    for j in range(len(bikes_dictionary)):

        if bikes_dictionary[j]['status'] != "Booked":

            for i in range(len(bikes_list)):
                if bikes_dictionary[j]['bike_type'] == bikes_list[i][4] and bikes_dictionary[j]['bike_size'] == bikes_list[i][3]:
                    bikes_dictionary[j]['possible_matches'].append(bikes_list[i][0])

            bikes_dictionary[j]['num_bikes_available'] = (len(bikes_dictionary[j]['possible_matches']))

    print("MATCHES SLEEP")
    pprint(bikes_dictionary)
    time.sleep(5)
    
    check_availability(bikes_dictionary)
    book_bikes(bikes_dictionary)


def check_availability(bikes_dictionary):
    """
    Cross reference possible matches in bike dictionaries with bike
    indexes in 'unavailable_bikes' list to check availability
    If not available, remove this bike index from the bike dictionary
    """

    # for each bike dictionary
    for j in range(len(bikes_dictionary)):

        # # only considering bikes who aren't already booked
        # if bikes_dictionary[j]["status"] != "Booked":

        # and for bike index in unavailable bikes
        for k in range(len(unavailable_bikes)):

            # if any of the bike indexes in unavailable bikes are found
            # in the bike dictionaries
            if unavailable_bikes[k] in bikes_dictionary[j]['possible_matches']:

                # then remove this bike index from the bike
                # dictionaries as it is not available for hire on
                # that date
                (bikes_dictionary[j]['possible_matches']).remove(unavailable_bikes[k])


def book_bikes_to_calendar(choose_bike_index):
    """
    Write the requested hire dates against the relevant bike index
    in google sheets
    """

    # for all bike indexes in the gs calendar
    for i in range(len(calendar)):

        # if bike index on calendar does NOT equal bike index in
        # dictionary, we are not interested in this index,
        # so increment i
        if calendar[i][0] != choose_bike_index:
            continue

        else:
            # if the bike indexes do match, determine the next empty
            # cell next to that bike index
            last_date_in_row = len((calendar[i]))-(calendar[i].count('') - 1)

            # loop through the hire dates requested
            for k in range(len(hire_dates_requested)):

                # update the google sheet by inputting all hire dates
                # requested against that bike index
                update_calendar.update_cell(i+1, last_date_in_row, hire_dates_requested[k])

                # increment the last empty cell ref, so we are not
                # overwriting the same cell
                last_date_in_row += 1


    # for all bike indexes
    for x in range(len(calendar2)):

        # and for all dates listed in the calendar
        for z in range(len(calendar2[0])):

            # and for all hire dates requested
            for w in range(len(hire_dates_requested)):

                # match up the chosen bike index against the date
                if (calendar2[x][0]) == str(choose_bike_index) and calendar2[2][z] == hire_dates_requested[w]:

                    # and write the booking number into that cell
                    print(x)
                    print(z)
                    update_calendar2.update_cell(x,z,bikes_dictionary[0]['booking_number'])



def book_bikes(bikes_dictionary):
    """
    Determine how many matches in the 'possible matches'
    and call up book_bikes_to_calendar
    """

    global choose_bike_index
    choose_bike_index = ""

    # for each bike dictionary
    for j in range(len(bikes_dictionary)):

        # print(f"Length of booked bikes {len(booked_bikes)}")
        # print(f"j = {j}")

        if bikes_dictionary[j]['status'] != "Booked":

            # if the possible matches list is empty, move onto next j value
            # also add a comment and append this 
            # bike dictionary to not_booked_bikes 
            if len(bikes_dictionary[j]['possible_matches']) == 0:

                bikes_dictionary[j]['comments'] = "No bikes available"
                # not_booked_bikes.append(bikes_dictionary[j])

                continue

            # if the possible matches list = 1, then there is only 1 choice
            # so select that, call up book_bikes_to_calendar,
            # and remove it from other bike dictionaries 'possible matches' list
            elif len(bikes_dictionary[j]['possible_matches']) == 1:

                # assign chosen_bike_index to this solo bike index
                choose_bike_index = bikes_dictionary[j]['possible_matches'][0]

                # call up book_bikes_to_calendar function
                book_bikes_to_calendar(choose_bike_index)

                # change status, update this bike dictionary, add bike
                # index to unavailable_bikes list, add this bike dict to
                # booked_bikes list
                bikes_dictionary[j]['status'] = "Booked"
                bikes_dictionary[j]['comments'] = ""
                bikes_dictionary[j]['booked_bike'] = choose_bike_index
                bikes_dictionary[j]['dates_of_hire'] = hire_dates_requested
                unavailable_bikes.append(choose_bike_index)
                booked_bikes.append(bikes_dictionary[j])

                if bikes_dictionary[j] in not_booked_bikes:
                    not_booked_bikes.remove(bikes_dictionary[j])

                # re-run check_availability to remove this bike index from
                # other bike dicts
                # print(f"Re-checking availability")
                check_availability(bikes_dictionary)

            # if there is more than 1 bike available
            # randomly select a bike index from possible matches
            else:

                # randomly select one of the possible matches
                choose_bike_index = random.choice(bikes_dictionary[j]['possible_matches'])

                # run function with this bike index
                book_bikes_to_calendar(choose_bike_index)

                
                bikes_dictionary[j]['status'] = "Booked"
                bikes_dictionary[j]['comments'] = ""
                bikes_dictionary[j]['booked_bike'] = choose_bike_index
                bikes_dictionary[j]['dates_of_hire'] = hire_dates_requested
                unavailable_bikes.append(choose_bike_index)
                booked_bikes.append(bikes_dictionary[j])

                if bikes_dictionary[j] in not_booked_bikes:
                    not_booked_bikes.remove(bikes_dictionary[j])

                # re-run check_availability to remove this bike index from
                # other bike dicts
                # print(f"Re-checking availability")
                check_availability(bikes_dictionary)

        continue

    booked_or_not(bikes_dictionary)


def find_alternatives(bikes_dictionary):
    """
    If the user is happy with alternatives, change the bike
    type (keep size and hire dates the same) and re-iterate
    with this new bike type
    """

    # only need to look for alternatives if there
    # are still bikes that aren't booked
    if not_booked_bikes != 0:

        global alt_bikes

        # for all bike dictionaries (now reduced in size from booked_or_not)
        for j in range(len(bikes_dictionary)):

            # list of all available bike types
            # keep inside j loop to restart from full list each time
            alt_bikes = ['Full suspension', 'Full suspension carbon',
            'Full suspension carbon e-bike', 'Full suspension e-bike',
            'Hardtail', 'Hardtail e-bike']

            # remove current bike type from alt_bikes so
            # function does not randomly choose the same bike type
            alt_bikes.remove(bikes_dictionary[j]['bike_type'])

            # choose random bike type (same size)
            bikes_dictionary[j]['bike_type'] = random.choice(alt_bikes)
            bikes_dictionary[j]['comments'] = "Finding alternative bike"

        # return to relevant function to perform again
        # only need to re-match the price, not the size as we know
        # the size is the same
        match_price(bikes_dictionary)


def booked_or_not(bikes_dictionary):
    """
    This function checks what the status is of all bike dictionaries
    If there are non-booked bikes and user is happy with alternative
    call up find_alternatives
    """
    print("BOOKED OR NOT SLEEP")
    print(bikes_dictionary)
    time.sleep(5)

    still_looking = ["ITERATION"]

    # for all bikes dictionaries
    for j in range(len(bikes_dictionary)):

        # if the status does not equal Booked, they are
        # NOT booked, so append them to not_booked_bikes list
        if bikes_dictionary[j]['status'] != "Booked":
            bikes_dictionary[j]['comments'] = "Found alternative"
            not_booked_bikes.append(bikes_dictionary[j])

    if len(booked_bikes) == num_req_bikes:
        print("ALL BIKES FOUND")
        check_double_bookings()
      
    # if not all bikes have been booked
    # re-assign the bike dictionary to not_booked_bikes
    # to perform the iteration again for only these bikes
    elif responses_list[-1][17] == "Yes":
        bikes_dictionary = copy.copy(not_booked_bikes)
        still_looking.append("ITERATION")
        #print("STILL LOOKING")
        #print(len(still_looking))
        find_alternatives(bikes_dictionary)
        # only allow max 4 iterations
        # if len(still_looking) > 4:
        #     print("Max interations")
        #     print(booked_bikes)
        #     raise SystemExit
      
    else:
        print(f"Bikes found:  {len(booked_bikes)}")
        print(f"Bikes not found:  {len(not_booked_bikes)}")
        print("User does not want alternatives")


def calculate_cost():
    """
    This functions calculates the total cost of 
    bike hire
    """
    bike_costs = []
    price = ""

    for i in range(len(booked_bikes)):
       

        bike_costs.append(int(booked_bikes[i]['price_per_day']) * len(hire_dates_requested))

    total_cost = sum(bike_costs)  
    print(total_cost)
    print(bike_costs)



def check_double_bookings():
    """
    Perform a couple of calculations to ensure there
    are no double bookings
    """

    ## FIRST CHECK
    # re-collect updated number from spreadsheet
    # (number counts num of cells filled in in calendar)
    sort_data2 = SHEET.worksheet('sort_data').get_all_values()
    dates_filled_in_now = sort_data2[1][1]

    # count how many dates have been filled in for this form
    num_dates_calendar = int(dates_filled_in_now) - int(dates_filled_in_previous)

    # count how many dates should have been filled in
    num_dates_booked = num_req_bikes*len(hire_dates_requested)

    # check that these two numbers match
    if num_dates_booked != num_dates_calendar:
        print("PROBLEM")
    else:
        print("YAY IT MATCHES")

    ## SECOND CHECK
    # check whether there are two dates the same in 
    # dates appended to bike indexes in calendar i.e. 
    # a bike has been double booked
    # for number of bikes in calendar
    for i in range(len(calendar)):

        # iterate through range of dates appended to that bike index
        for j in range(len(calendar[i])):

            # if that date appears more than once in this list of dates
            if calendar[i].count(calendar[i][j]) > 1 and calendar[i][j] != "":

                # raise an error
                print("PROBLEM")

    calculate_cost()




get_latest_response()

# message = f"""\
# Subject: Hi Mailtrap
# To: {receiver}
# From: {sender}

# Hello {last_response[1]}!

# Thank you for booking with us.  Below are your booking details:




# """

# try:
#     #send your message with credentials specified above
#     with smtplib.SMTP(smtp_server, port) as server:
#         server.login(login, password)
#         server.sendmail(sender, receiver, message)

#     # tell the script to report if your message was sent or which errors need to be fixed
#     print('Sent')
# except (gaierror, ConnectionRefusedError):
#     print('Failed to connect to the server. Bad connection settings?')
# except smtplib.SMTPServerDisconnected:
#     print('Failed to connect to the server. Wrong user/password?')
# except smtplib.SMTPException as e:
#     print('SMTP error occurred: ' + str(e))


# #pprint(booked_bikes)

# ### USER EMAIL

# # Hello {name}

# # Thanks for looking to us for hiring bikes. 

# # We've managed to book the following bikes for you:


# # And we found these alternatives for ones we couldn't match up entirely:

# # We could not find any bikes suitable for:


# # These have now been booked into the calendar.  Please let us know if you need this booking amended.

# # The price for this hire is displayed below.  You can call up on XXXXX to pay, or bring cash/card on the first date of hire:

# # For more information on what you may need to bring for hire, please see XXXXX on the website. 

# # See you promptly on {date}

# # Kind regards
# # Progression Bikes team

# ### OWNER EMAIL

# # The following bikes have been booked for dates {dates}

# # > 
# # > 
# # > 
# # > 

