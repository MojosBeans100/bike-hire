
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

bikes_list = SHEET.worksheet('bike_list')
responses_list = SHEET.worksheet('form_responses').get_all_values()
sort_data = SHEET.worksheet('sort_data').get_all_values()


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
    end_date = start_date + timedelta(days=int(responses_list[-1][6]) - 1) 

    print(start_date)
    print(end_date)
   

get_available_bikes()

def get_latest_response():
    """
    Fetch the latest form response from googlesheets and determine 
    driving factors for bike selection
    """
    # get type and quantity of bikes selected
    # get heights
    # get date and duration of hire

    # get the most recent form response from google sheets
    last_response = responses_list[-1]  

    bike_types_list = [(last_response[7]),(last_response[9]),(last_response[11]),(last_response[13]),(last_response[15])]
    bike_heights_list = [(last_response[8]),(last_response[10]),(last_response[12]),(last_response[14]),(last_response[16])]
    
    user_bikes_choice = {
        "bikes_types": bike_types_list,
        "bikes_heights": bike_heights_list,
    }
    
    print(user_bikes_choice)


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
