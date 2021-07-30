# python code goes here
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

def get_latest_response():
    """
    Fetch the latest form response from googlesheets and determine 
    driving factors for bike selection
    """
    # get type and quantity of bikes selected
    # get heights
    # get date and duration of hire
    
def bikes_available():
    """
    Determine if these bikes are actually available
    in the hire list.  I.e. does the stores have 3 hardtails
    and 2 full sus carbons in stock (irrespective of hire date)
    """

