import unittest
import sys
sys.path.append("/Finance_Tracker/")
import src.Transaction_Reader as tr
tr.Transaction_Reader

class Transaction_Reader_Tests(unittest.TestCase):
    
    def initialize_test(self):
        result = tr.initialize("Wells Fargo")
        assert isinstance(result, Wells_Fargo_Reader)
        
if __name__ == "__main__":
    unittest.main()