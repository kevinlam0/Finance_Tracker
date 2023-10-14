import csv
import personalization
import gspread
import time
import os

VALID_CATEGORIES = {"eating out", "groceries", "materialistic", "productive", "gas", "rent", "miscellaneous"}

class FinanceAutomator:
    __google_sheet_name: str
    __sheet_file: gspread.spreadsheet.Spreadsheet
    
    def __init__(self, google_file):
        self.__google_sheet_name = google_file
        
    # ---- Public Methods ---- #
    def connect_to_google(self):
        sa = gspread.service_account()
        self.__sheet_file = sa.open(self.__google_sheet_name)
        print("Connection to Google is successful!")
        
    def inject_one_file(self, sheet, csv_file: str):
        wks = self.__sheet_file.worksheet(sheet)
        rows = self.__create_working_rows(csv_file)
        for row in rows:
            insertion_row = [row[0], row[1], row[2], row[3]]
            wks.insert_row(insertion_row, 8)
            time.sleep(2)
            
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
    def __create_working_rows(self, file: str) -> list:
        transactions = []
        with open(file, 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            
            for row in csv_reader: 
                date = row[0]
                amount = float(row[1])
                desc = self.__trim_description(row[4]) if "VENMO" not in row[4] else "Venmo transaction" + self.__venmo_lookup()
                category = self.__find_category(desc, amount, date)
                transaction: tuple = ((date, amount, desc, category))
                transactions.append(transaction)
                
        return transactions
    
    def __find_category(self, description: str, amount: float, date: str) -> str: 
        lower_desc = description.lower()
        
        if "venmo" in lower_desc: return self.__venmo_lookup(amount, date)
        
        # Already a listed category
        for key in personalization.categories.keys():
            if key in lower_desc: return personalization.categories[key]
            
        message = f"\nWe could not label the transaction.\nThis is the description: {description}\nThis is the amount: {amount}\nThis is the date: {date}"
        return self.__get_users_cat(message)
    
    def __trim_description(self, description: str) -> str:
        desc = description.split()
        if "PURCHASE AUTHORIZED" in description:
            desc = desc[4:]
            
        if "CARD" in desc and personalization.card_ending in desc:
            desc = desc[:-3]
            
        return  " ".join(str(element) for element in desc)
    
    def __venmo_lookup(self, amount, date):
        print("\nThis is a venmo transaction")
        """[2] Date '2022-05-03T19:35:58'
            [5] Description
            [7] to who
            [8] amount"""
    
    def __get_users_cat(self, initial_message):
        print(initial_message)
        category = input("Please state what is the category of this transaction: ")
        
        while (category.strip() != "" and category.lower() not in VALID_CATEGORIES): 
            category = input("The category is not valid. Please input one of the following or input nothing to skip:\nEating out, Groceries, Materialistic, Productive, Gas, Rent, Miscellaneous: ")
        
        # If blank then just mark it as other
        if category.strip() == "": return "Other"
        
        return category.capitalize()
    