from src.TransactionReader import TransactionReader
import csv

class DiscoverReader(TransactionReader):
    card: str
    
    def __new__(cls, *args, **kwargs):
        instance = super(DiscoverReader, cls).__new__(cls)
        return instance
    
    def __init__(self, type: str):
        c = type.lower()
        if c != "credit" and c != "debit":
            raise Exception("The card type needs to be debit or credit.")
        self.card = c.capitalize()
        
    def format_rows_from_csv_file(self, file: str) -> list:
        pass