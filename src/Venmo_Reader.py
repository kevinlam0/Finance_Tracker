import calendar
OLDEST_YEAR = 2015
NEWEST_YEAR = 2025

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
        if venmo_amount == amount and abs(day - venmo_day) < 3: 
            return f"\"{row[5]}\" to {row[7]}" 
        
    raise Exception

def __read_csv_file(file_path: str) -> list:
    file = open(file_path, 'r')
    lines = [line.strip() for line in file]
    lines = lines[4:-27]
    return lines 