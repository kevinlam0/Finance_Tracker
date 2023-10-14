import csv
import personalization
import gspread

class FinanceAutomator:
    __google_sheet_name: str
    __sheet_file: gspread.spreadsheet.Spreadsheet
    
    def __init__(self, google_file):
        self.__google_sheet_name = google_file
    
    def __create_working_rows(self, file: str) -> list:
        transactions = []
        with open(file, 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            
            for row in csv_reader: 
                date = row[0]
                amount = float(row[1])
                desc = row[4]
                category = self.__find_category(desc, personalization.categories, amount)
                transaction: tuple = ((date, amount, desc, category))
                transactions.append(transaction)
                
        return transactions
    
    def __find_category(self, description: str, amount: float) -> str: 
        lower_desc = description.lower()
        for key in personalization.categories.keys():
            if key in lower_desc: return personalization.categories[key]
            
        category = input(f"We could not label the transaction.\nThis is the description: {description}\nThis is the amount: {amount}")
        if category.strip() == "": return "Other"
        return category
    
    def connect_to_google(self):
        sa = gspread.service_account()
        self.__sheet_file = sa.open(self.__google_sheet_name)
        print("Connection to Google is successful!")
        
    def inject_into_sheet(self, sheet):
        pass
    