import gspread
import random
import copy
import time
from google.oauth2.service_account import Credentials
from datetime import datetime
from datetime import timedelta
from datetime import date
from pprint import pprint

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
update_calendar = SHEET.worksheet('calendar')
gs_size_guide = SHEET.worksheet('size_guide').get_all_values()

booked_bikes = []
not_booked_bikes = []
bikes_dictionary = []
num_req_bikes = ""
unavailable_bikes = []
hire_dates_requested = []


def stop_running():
    print("STOP!!")
    raise SystemExit()


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

    # max bikes hired = 5, but remove empty values from list
    types_list = list(filter(None, types_list_orig))
    heights_list = list(filter(None, heights_list_orig))

    # create dictionaries to store info about each bike requested
    for j in range(len(types_list)):
        d = {
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

    num_req_bikes = len(bikes_dictionary)
    print(f"Num req bikes = {num_req_bikes}")

    # num_dates_check_start = sort_data[1][1]
    # print(num_dates_check_start)

    match_size(bikes_dictionary)


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
   
    if len(booked_bikes) == 5:
        stop_running()

    print(f"Unavailable bikes: {unavailable_bikes}")
    print(booked_bikes)
    #print(f"Num iterations: {num_iterations}")
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
    start_date = datetime.strptime(users_start_date, "%Y-%m-%d")

    # calculate end date based on the hire duration
    delta = timedelta(days=int(responses_list[-1][6]) - 1)
    delta_day = timedelta(days=int(1))
    end_date = start_date + delta

    # list all dates in between and append to
    # hire_dates_requested
    # only do this ONCE
    if len(hire_dates_requested) == 0:
        while start_date <= end_date:
            hire_dates_requested.append(start_date.strftime("%Y-%m-%d"))
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

    print("Find unavailable bikes sleep")
    print(f"Unavailable bikes: {unavailable_bikes}")
    print(f"Hire dates req: {hire_dates_requested}")
    time.sleep(10)

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
                # print(f"Bike index {choose_bike_index} booked!")
                bikes_dictionary[j]['booked_bike'] = choose_bike_index
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
                # print(f"Bike index {choose_bike_index} booked!")
                bikes_dictionary[j]['booked_bike'] = choose_bike_index
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

    # for all bikes dictionaries
    for j in range(len(bikes_dictionary)):

        # if the status does not equal Booked, they are
        # NOT booked, so append them to not_booked_bikes list
        if bikes_dictionary[j]['status'] != "Booked":
            not_booked_bikes.append(bikes_dictionary[j])

    if len(booked_bikes) == num_req_bikes:
        return

    # if not all bikes have been booked
    # re-assign the bike dictionary to not_booked_bikes
    # to perform the iteration again for only these bikes
    else:
        bikes_dictionary = copy.copy(not_booked_bikes)
        find_alternatives(bikes_dictionary)

    return


get_latest_response()

# pprint(bikes_dictionary)

# print(f"Unavailable bikes: {unavailable_bikes}")

# print(f"Number of bikes booked: {len(booked_bikes)}")

# num_dates_check_end = sort_data[1][1]
