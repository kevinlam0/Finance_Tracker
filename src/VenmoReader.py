import calendar, os, sys
fpath = os.path.join(os.path.dirname(__file__), "../")
sys.path.append(fpath)
from src.CustomExceptions.MonthNotFoundError import IllegalDateError
OLDEST_YEAR = 2015
NEWEST_YEAR = 2025
MONTHS = set([calendar.month_name[i].lower() for i in range(1, 13)])

class VenmoReader():
    __data: list
    def __init__(self, file):
        venmo_file = find_file(file)
        self.__data = __read_csv_file(venmo_file)

def find_venmo_description(amount: float, date: str) -> str:
    return "Venmo transaction: " + find_venmo_transaction_description(amount, date)


def find_venmo_transaction_description(amount: float, date: str) -> str:
    """
    Date must be in mm/dd/yyyy format
    """
    # Get the file path of the correct venmo month data
    month = calendar.month_name[int(date[:2])].lower()
    day = int(date[3:5])
    if not (1 <= day and day <= 31): raise Exception
    year = date[-4:]
    if not (OLDEST_YEAR <= int(year) <= NEWEST_YEAR): raise Exception
    
    file_path = f"./venmoData/venmo{month}{year}.csv"

    lines = __read_csv_file(file_path)
    
    # Find the correct transaction
    for i in range(len(lines)):
        row: list = lines[i].split(",")
        venmo_amount: float = float(row[8][0] + row[8][3:])
        venmo_day: int = int(row[2][8:10])
        if venmo_amount == amount and abs(day - venmo_day) < 2: 
            return f"\"{row[5]}\" to {row[7]}" 
        
    raise Exception("This is the transaction: " + str((month, day, year, amount)))

def __read_csv_file(file_path: str) -> list:
    file = open(file_path, 'r')
    lines = [line.strip() for line in file]
    lines = lines[4:-27]
    return lines 

def find_file(file: str) -> str:
    i = file.find("2")
    year = file[i:i+4]
    try: year = int(year)
    except ValueError: raise IllegalDateError(f"This file does not have a valid year: {year}")
    if not (OLDEST_YEAR <= year <= NEWEST_YEAR): raise IllegalDateError(f"This file is outside of the valid years {OLDEST_YEAR} - {NEWEST_YEAR}: {year}")
        
    month = ""
    for m in MONTHS:
        if m in file:
            month = m
            break
    if month == "": raise IllegalDateError(f"This file does not have a valid month: {file}")
    return f"venmo{month}{year}.csv"