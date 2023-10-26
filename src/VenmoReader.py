import calendar, os, sys
fpath = os.path.join(os.path.dirname(__file__), "../")
sys.path.append(fpath)
from src.CustomExceptions.IllegalDateError import IllegalDateError
OLDEST_YEAR = 2015
NEWEST_YEAR = 2025
MONTHS = set([calendar.month_name[i].lower() for i in range(1, 13)])

class VenmoReader():
    __data: list
    __year: int
    __month: str
    def __init__(self, file):
        self.__year = _find_year(file)
        self.__month = _find_month(file)
        venmo_file = find_file(self.__month, self.__year)
        self.__data = _read_csv_file(venmo_file)
    def find_venmo_description(self, amount: float, date: str) -> str:
        return "Venmo transaction: " + self.find_venmo_transaction_description(amount, date) 
    def find_venmo_transaction_description(self, amount: float, date: str) -> str:
        """
        Date must be in mm/dd/yyyy format
        """
        # Find the day of this transaction
        day = int(date[3:5])
        if not(1<= day <= 31): raise IllegalDateError(f"The day of this date is not a real day: {date}")
        
        # --- Identifying the correct transaction --- #
        # Buffer for transaction processing lag
        delta = 1
        while delta < 3:
            for i in range(len(self.__data)):
                # Identify amount 
                row: list = self.__data[i].split(",")
                venmo_amount: float = float(row[8][0] + row[8][3:])
                # try:
                #     venmo_amount: float = float(row[8][0] + row[8][3:])
                # except ValueError: raise ValueError(f"{row[8]}")
                if amount != venmo_amount: continue
                
                # Identify the day
                venmo_day: int = int(row[2][8:10])
                if abs(venmo_day - day) <= delta:
                    self.__data.pop(i)
                    return f"\"{row[5]}\" to {row[7]}"
            delta+=1
        raise Exception("This is the transaction: " + str((date, amount)))


def _read_csv_file(file_path: str) -> list:
    file = open(file_path, 'r')
    lines = [line.strip() for line in file]
    lines = lines[4:-27]
    return lines 
def _find_year(file: str) -> int:
    i = file.find("2")
    year = file[i : i+4]
    try: year = int(year)
    except ValueError: raise IllegalDateError(f"This file does not have a valid year: {year}")
    if not (OLDEST_YEAR <= year <= NEWEST_YEAR): raise IllegalDateError(f"This file is outside of the valid years {OLDEST_YEAR} - {NEWEST_YEAR}: {year}")
    return year
def _find_month(file: str) -> str:
    for m in MONTHS:
        if m in file: 
            return m
    raise IllegalDateError(f"This file does not have a valid month: {file}")
def find_file(month: str, year: int) -> str:
    return f"./venmoData/venmo{month}{year}.csv"