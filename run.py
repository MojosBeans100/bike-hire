
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
from datetime import timedelta
from datetime import date

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
responses_list = SHEET.worksheet('form_responses').get_all_values()
sort_data = SHEET.worksheet('sort_data').get_all_values()
calendar = SHEET.worksheet('calendar').get_all_values()
size_guide = SHEET.worksheet('size_guide').get_all_values()


def get_available_bikes():
    """
    Fetch list of all bikes available on date(s) requested
    """
    # get start date, end date, dates in between
    # format the date into usable format to determine end date

    # get users selected date
    users_start_date = responses_list[-1][5]

    # put date in readable format
    start_date = datetime.strptime(users_start_date, "%Y-%m-%d")

    # calculate end date based on the hire duration
    delta = timedelta(days=int(responses_list[-1][6]) - 1)
    end_date = start_date + delta

    # list all dates in between
    hire_dates_requested = []
    while start_date <= end_date:
        hire_dates_requested.append(start_date.strftime("%Y-%m-%d"))
        start_date += delta

    # get bikes available on that/those dates
    bikes_unavailable = []

    # loop through dates requested, and list of bikes against dates already
    # booked in g.sheets:- if unavailable on dates requested,
    # append bike index to bikes_unavailable list
    for dates in hire_dates_requested:
        for i in range(len(calendar)):
            if dates in calendar[i]:
                bikes_unavailable.append(calendar[i][0])

    print(hire_dates_requested)
    # print(bikes_unavailable)           

    # calendar_first_row = calendar[2]
    # print(calendar_first_row)


get_available_bikes()


def get_latest_response():
    """
    Fetch the latest form response from googlesheets and determine 
    driving factors for bike selection
    """
    # get type and quantity of bikes selected
    # get heights
    # get date and duration of hire

    global bike_types_list
    global bike_heights_list

    # get the most recent form response from google sheets
    last_response = responses_list[-1]  

    bike_types_list_orig = [(last_response[7]),(last_response[9]),(last_response[11]),(last_response[13]),(last_response[15])]
    bike_heights_list_orig = [(last_response[8]),(last_response[10]),(last_response[12]),(last_response[14]),(last_response[16])]

    # max bikes hired = 5, but remove empty values from list 
    bike_types_list = list(filter(None, bike_types_list_orig))
    bike_heights_list = list(filter(None, bike_heights_list_orig))

    # create dictionaries to store info about each bike requested
    global list_of_bikes
    list_of_bikes = []

    for j in range(len(bike_types_list)):
        d = {
            'bike_type': bike_types_list[j],
            'user_height': bike_heights_list[j],
            'bike_size': "",
            'possible_matches': [],
            'num_bikes_available': "",
            'price_per_day': "",
        }
        list_of_bikes.append(d)

   
get_latest_response()

# print(list_of_bikes)

def match_size():
    """
    Match the heights specified in user form to the correct bike size
    """

    # iterate through list of bikes dictionaries (max 5)
    for i in range(len(list_of_bikes)):

        # iterate through available bike sizes in size_guide google sheet
        for j in range(3, 9):  

            # if the bike size in size_guide is the same as the user height, index the relevant bike size
            # and append to the dictionary   
               
            if (size_guide[j][4]) == list_of_bikes[i]['user_height']:
                list_of_bikes[i]['bike_size'] = size_guide[j][8]

match_size()

print(list_of_bikes)

# def match_suitable_bikes():
#     """
#     Use submitted form info to find selection of appropriate bikes
#     """

#     # loop through bikes requested, and compare to bikes available in hire fleet
#     # output the bike index of bikes which match type of those requested to the bike dictionaries
    
#     for j in range(len(list_of_bikes)):
        
#         for i in range(len(bikes_list)):
#             if list_of_bikes[j]['bike_type'] == bikes_list[i][4]:
#                 list_of_bikes[j]['possible_matches'].append(bikes_list[i][0])
#                 list_of_bikes[j]['num_bikes_available'] = (len(list_of_bikes[j]['possible_matches']))
        
#     print(list_of_bikes) 
 
# match_suitable_bikes()




















# def bikes_available():
#     """
#     Determine if these bikes are actually available
#     in the hire list.  I.e. does the stores have 3 hardtails
#     and 2 full sus carbons in stock (irrespective of hire date)
#     If not, need to email user with feedback and other suggestions
#     """
#     # use indexing to find if there is a bike available
#     # which matches all criteria from user form
#     # repeat for all bikes from user form
#     # output list of bikes that are available


# def select_bikes():
#     """
#     Using bikes listed in bikes_available(),
#     lookup these bikes in bike database to determine if they are
#     available or already booked out for those dates
#     """
#     # use list from bikes_available() to check dates
#     # and output selected bikes




# def confirm_hire():
#     """
#     If bikes are available, use selected bikes and dates to 'book out' 
#     bikes on bike database by adding these dates against the bikes selected
#     Notify customer via mail of hire confirmation
#     """
#     # use user form selected dates and bikes to put 
#     # "HIRED" in relevant cell to show the bike is hired and
#     # therefore unavailable for those dates


# def suggest_alt():
#     """
#     If bikes selected are not available, suggest
#     alternatives based on what is available on those dates
#     """
#     # either find available dates for those bikes
#     # OR
#     # find available bikes for those dates
#     # OR
#     # find closest match ie is a Medium bike available instead of a Large


# UNUSED CODE


#  sdate_day = int(start_date[3:5])
#     sdate_month = int(start_date[:2])
#     sdate_year = int(start_date[6:])

#     start_date2 = date(sdate_year, sdate_month, sdate_day)

#     # days_hired_for = int(responses_list[-1][6])

#     # end_date = start_date + days_hired_for

#     print(start_date2)

#     # print(sdate_day)
#     # print(sdate_month)
#     # print(sdate_year)

    # print(end_date)



    # height_1 = last_response[9]

    # num_of_heights = height_1.count(',')
    # user_heights = []

    # if num_of_heights > 0:

    #     user1_height = height_1[0:13]
    #     user2_height = height_1[15:28]
    #     user3_height = height_1[30-43]
    #     user4_height = height_1[45-58]
    #     user5_height = height_1[60-73]

    #     print(user1_height)
    #     print(user2_height)
    #     print(user3_height)
    #     print(user4_height)
    #     print(user5_height)

    # print(user1_height.find(','))

    # print(user1_height)    


# for bike_type in list_of_bikes:
#         for i in range(len(bikes_list)):
#             if bike_type == bikes_list[i][4]:
#                 suitable_bikes.append(bikes_list[i][0])
#                 # list_of_bikes[bike_type]['possible_matches'] = (bikes_list[i][0])
