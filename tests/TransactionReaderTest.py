import os, sys
fpath = os.path.join(os.path.dirname(__file__), '../')
sys.path.append(fpath)
from src.WellsFargoReader import WellsFargoReader as wfr
from src.DiscoverReader import DiscoverReader as dcr
from src.TransactionReaderFactory import TransactionReaderFactory
import unittest


class TransactionReaderTests(unittest.TestCase):
    
    def test_initialize(self):
        result = TransactionReaderFactory.get_reader("fjskdWF.csv")
        self.assertIsInstance(result, wfr)
        self.assertEqual("Credit", result.get_card())
        
    def test_initialize_discover(self):
        result = TransactionReaderFactory.get_reader("DCfjkdls.fsd")
        self.assertIsInstance(result, dcr)
        self.assertEqual("Credit", result.get_card())
        
if __name__ == "__main__":
    unittest.main()