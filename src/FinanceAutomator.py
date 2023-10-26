import gspread
import time
import os
import TransactionReader as TransactionReader
import calendar
from TransactionReaderFactory import TransactionReaderFactory as TRF

MONTHS = set([calendar.month_name[i].lower() for i in range(1, 13)])

class FinanceAutomator:
    __google_sheet_name: str
    __sheet_file: gspread.spreadsheet.Spreadsheet
    
    def __init__(self, google_file: str):
        self.__google_sheet_name = google_file
        
    # ---- Public Methods ---- #
    def connect_to_google(self):
        sa = gspread.service_account()
        self.__sheet_file = sa.open(self.__google_sheet_name)
        print("Connection to Google is successful!\n")
        
    def inject_one_file_to_sheet(self, sheet: str, file: str):
        wks = self.__sheet_file.worksheet(sheet)
        reader = TRF.get_reader(file)
        rows = reader.format_rows_from_csv_file(file)
        
        for row in rows:
            insertion_row = [row[0], row[1], row[2], row[3], row[4]]
            print(insertion_row)
            # wks.insert_row(insertion_row, 2)
            # time.sleep(2)
            
    def inject_all_data(self, folder: str):
        directory = './' + folder
        files = os.listdir(directory)
        for file in files:
            # If not a csv file skip
            if not file.endswith('csv'): continue
            sheet, data_file = _findSheet_findFile(file, directory)
            self.inject_one_file_to_sheet(sheet, data_file)
            
def _find_month(file:str, index_of_year: int) -> str:
    file_without_year = file[:index_of_year]
    while file_without_year not in MONTHS:
        file_without_year = file_without_year[1:]
        
    return file_without_year.capitalize()

def _findSheet_findFile(file: str, directory: str):
    i = file.find("2")
    month = _find_month(file, i)
    year = file[i:i+4]
    sheet = f"{month} {year}"
    data_file = f"{directory}/{file}"
    return sheet, data_file