import os, sys
fpath = os.path.join(os.path.dirname(__file__), '../')
sys.path.append(fpath)
from src.TransactionReader import TransactionReader
import csv
import src.VenmoReader as VenmoReader
import src.personalization as personalization

class WellsFargoReader(TransactionReader):
    __card: str
    __Venmo_Reader: VenmoReader.VenmoReader
    
    def __new__(cls, *args, **kwargs):
        instance = super(WellsFargoReader, cls).__new__(cls)
        return instance
    
    def __init__(self, type: str, file: str):
        c = type.lower()
        if c != "credit" and c != "debit": raise Exception("The card type needs to be debit or credit.")
        self.__card = c.capitalize()
        self.__Venmo_Reader = super().find_venmo_data(file, self.__card, "Wells Fargo")
        
    def format_rows_from_csv_file(self, file: str) -> list:
        transactions = []
        with open(file, 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            for row in csv_reader: 
                # Need these
                date = row[0]
                amount = float(row[1])
                
                # -- Find the description and payment method -- #
                # This is payment to another card 
                if _is_another_cards_transaction(row[4]): continue
                
                # Cashout from venmo
                if amount > 0 and ("VENMO CASHOUT" in row[4] or "RTP from VENMO" in row[4]):
                    desc = "Venmo cashout"
                    payment_type = "Venmo"
                    
                # Venmo but not cashout
                elif "VENMO" in row[4]: 
                    desc = self.__Venmo_Reader.find_venmo_description(amount, date)
                    payment_type = "Venmo"
                
                # Anything else 
                else: 
                    desc = self.__trim_description(row[4])
                    payment_type = self.__card
                
                # If it is an income and not from venmo
                if amount > 0:
                    if "Venmo" in desc: category = "Venmo income"
                    else: category = super()._find_income_category(desc, amount, date) 
                
                else: category = super()._find_category(desc, amount, date)
                
                transaction: tuple = ((date, amount, desc, category, payment_type))
                transactions.append(transaction)
                
        return transactions

    def __trim_description(self, description: str) -> str:
        desc = description.split()
        if "PURCHASE AUTHORIZED" in description:
            desc = desc[4:]
            
        if "CARD" in desc and personalization.card_ending in desc:
            desc = desc[:-3]
            
        return  " ".join(str(element) for element in desc)

    def get_card(self) -> str:
        return self.__card

    def get_venmo_reader(self) -> VenmoReader.VenmoReader:
        return self.__Venmo_Reader

def _is_another_cards_transaction(description: str) -> bool:
    for card in personalization.OTHER_CARDS:
        if card in description:
            return True
    return False