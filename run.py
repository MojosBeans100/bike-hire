
import gspread
from google.oauth2.service_account import Credentials

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

def get_latest_response():
    """
    Fetch the latest form response from googlesheets and determine 
    driving factors for bike selection
    """
    # get type and quantity of bikes selected
    # get heights
    # get date and duration of hire
    last_response = sort_data[-1]
    # print(last_response)

    start_date_day = int(last_response[2][:2])
    start_date_month = int(last_response[2][3:-2])
    start_date_year = int(last_response[2][5:-2])
    

    print(start_date_day)
    print(start_date_month)
    print(start_date_year)
    

get_latest_response()


def bikes_available():
    """
    Determine if these bikes are actually available
    in the hire list.  I.e. does the stores have 3 hardtails
    and 2 full sus carbons in stock (irrespective of hire date)
    If not, need to email user with feedback and other suggestions
    """
    # use indexing to find if there is a bike available
    # which matches all criteria from user form
    # repeat for all bikes from user form
    # output list of bikes that are available


def select_bikes():
    """
    Using bikes listed in bikes_available(),
    lookup these bikes in bike database to determine if they are
    available or already booked out for those dates
    """
    # use list from bikes_available() to check dates
    # and output selected bikes


def confirm_hire():
    """
    If bikes are available, use selected bikes and dates to 'book out' 
    bikes on bike database by adding these dates against the bikes selected
    Notify customer via mail of hire confirmation
    """
    # use user form selected dates and bikes to put 
    # "HIRED" in relevant cell to show the bike is hired and
    # therefore unavailable for those dates


def suggest_alt():
    """
    If bikes selected are not available, suggest
    alternatives based on what is available on those dates
    """
    # either find available dates for those bikes
    # OR
    # find available bikes for those dates
    # OR
    # find closest match ie is a Medium bike available instead of a Large

