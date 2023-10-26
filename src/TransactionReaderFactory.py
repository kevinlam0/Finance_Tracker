import os, sys
fpath = os.path.join(os.path.dirname(__file__), '../')
sys.path.append(fpath)
from src.Wells_Fargo_Reader import Wells_Fargo_Reader as wfr

class TransactionReaderFactory:
    @staticmethod
    def get_reader(bank: str, type: str):
        bank = bank.lower()
        if bank == "wells fargo":
            return wfr(type)
        
        