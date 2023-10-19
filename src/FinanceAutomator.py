import csv
import personalization
import gspread
import time
import os
import calendar
import TransactionReader

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
        
    def inject_one_file(self, sheet: str, file: str):
        wks = self.__sheet_file.worksheet(sheet)
        rows = TransactionReader.format_rows_csv_file(file)
        
        for row in rows:
            insertion_row = [row[0], row[1], row[2], row[3]]
            print(insertion_row)
            # wks.insert_row(insertion_row, 2)
            # time.sleep(2)
            
    def inject_all_data(self, folder: str):
        directory = './' + folder
        files = os.listdir(directory)
        for file in files:
            # If not a csv file skip
            if not file.endswith('csv'): continue
            
            # Find index of the year
            i = file.find("2")
            month = file[:i].capitalize()
            year = file[i:i+4]
            
            sheet = f"{month} {year}"
            data_file = f"{directory}/{file}"
            self.inject_one_file(sheet, data_file)

    # ---- Private Helper Methods ---- #
    # def __create_working_rows(self, file: str) -> list:
    #     transactions = []
    #     with open(file, 'r') as csv_file:
    #         csv_reader = csv.reader(csv_file)
    #         for row in csv_reader: 
    #             # Need these
    #             date = row[0]
    #             amount = float(row[1])
                
    #             # Find the description of the transaction.
    #             # Could be a spending or an income 
    #             if "VENMO" in row[4]: desc = "Venmo transaction: " + self.venmo_desc(amount, date) 
    #             else: desc = self.__trim_description(row[4])
                
    #             if amount > 0: category = "Venmo" if "Venmo" in desc else "Work income"
    #             category = self.__find_category(desc, amount, date)
    #             transaction: tuple = ((date, amount, desc, category))
    #             transactions.append(transaction)
                
    #     return transactions
    
    # def __find_category(self, description: str, amount: float, date: str) -> str: 
    #     lower_desc = description.lower()
        
    #     # Already a listed category
    #     for key in personalization.categories.keys():
    #         if key in lower_desc: return personalization.categories[key]
        
    #     venmo = "This is the description: " if "Venmo" not in description else ""
    #     message = f"\nWe could not label the transaction.\n{venmo}{description}\nThis is the amount: {amount}\nThis is the date: {date}"
    #     return self.__get_users_cat(message, personalization.VALID_CATEGORIES)
    
    # def __trim_description(self, description: str) -> str:
    #     desc = description.split()
    #     if "PURCHASE AUTHORIZED" in description:
    #         desc = desc[4:]
            
    #     if "CARD" in desc and personalization.card_ending in desc:
    #         desc = desc[:-3]
            
    #     return  " ".join(str(element) for element in desc)
    
    # def venmo_desc(self, amount: float, date: str):
    #     # Get the file path of the correct venmo month data
    #     month = calendar.month_name[int(date[:2])].lower()
    #     day = int(date[3:5])
    #     year = date[-4:]
    #     file_path = f"./venmoData/venmo{month}{year}.csv"
        
    #     # Reading the file
    #     file = open(file_path, 'r')
    #     # Transform into list 
    #     lines = [line.strip() for line in file]
    #     # Dropping the unnecessary information
    #     lines = lines[4:-27]
        
    #     # Find the correct transaction
    #     for i in range(len(lines)):
    #         row = lines[i].split(",")
    #         venmo_amount = float(row[8][0] + row[8][3:])
    #         venmo_day = int(row[2][8:10])
    #         if venmo_amount == amount and abs(day - venmo_day) < 3: return f"\"{row[5]}\" to {row[7]}" 
            
    #     raise Exception
            
            
        """[2] Date '2022-05-03T19:35:58'
            [5] Description
            [7] to who
            [8] amount"""
        
        
               
        