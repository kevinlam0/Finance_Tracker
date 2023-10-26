import os, sys
fpath = os.path.join(os.path.dirname(__file__), '../')
sys.path.append(fpath)
from src.WellsFargoReader import WellsFargoReader as WFR
from src.DiscoverReader import DiscoverReader as DCR

class TransactionReaderFactory:
    @staticmethod
    def get_reader(file: str):
        if "WF" in file:
            type = input("What type of card is this Wells Fargo data from, Credit or Debit?: ")
            return WFR(type, file)
        if "DC" in file:
            type = input("What type of card is this Discover data from, Credit or Debit?: ")
            return DCR(type, file)
        
        