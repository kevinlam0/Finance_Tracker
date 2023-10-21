import os, sys
fpath = os.path.join(os.path.dirname(__file__), '../')
sys.path.append(fpath)
from src.Transaction_Reader import Transaction_Reader as tr 
from src.Wells_Fargo_Reader import Wells_Fargo_Reader as wfr
import unittest


class Transaction_Reader_Tests(unittest.TestCase):
    
    def test_initialize(self):
        result = tr.initialize("Wells Fargo")
        self.assertIsInstance(result, wfr)
        
if __name__ == "__main__":
    unittest.main()