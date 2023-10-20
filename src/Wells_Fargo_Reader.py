from Transaction_Reader import Transaction_Reader
import csv
import personalization
import Venmo_Reader

class Wells_Fargo_Reader(Transaction_Reader):
    def __new__(cls, *args, **kwargs):
        instance = super(WellsFargoReader, cls).__new__(cls)
        return instance
    
    def __init__(self):
        pass
    
    def format_rows_from_csv_file(self, file: str) -> list:
        transactions = []
        with open(file, 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            for row in csv_reader: 
                # Need these
                date = row[0]
                amount = float(row[1])
                
                # Find the description of the transaction.
                if "VENMO" in row[4]: 
                    desc = "Venmo transaction: " + Venmo_Reader.find_venmo_transaction_description(amount, date) 
                else: 
                    desc = self.__trim_description(row[4])
                
                # If it is an income
                if amount > 0: 
                    if "Venmo" in desc:
                        category = "Venmo"
                    else: category = super()._find_income_category(desc, amount, date)
                
                else: category = super()._find_category(desc, amount, date)
                
                transaction: tuple = ((date, amount, desc, category))
                transactions.append(transaction)
                
        return transactions

    def __trim_description(self, description: str) -> str:
        desc = description.split()
        if "PURCHASE AUTHORIZED" in description:
            desc = desc[4:]
            
        if "CARD" in desc and personalization.card_ending in desc:
            desc = desc[:-3]
            
        return  " ".join(str(element) for element in desc)

