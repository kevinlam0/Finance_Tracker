import os, sys, unittest
fpath = os.path.join(os.path.dirname(__file__), "../")
sys.path.append(fpath)
import src.VenmoReader as VenmoReader
from src.CustomExceptions.IllegalDateError import IllegalDateError as IDE

class VenmoReaderTest(unittest.TestCase):
    
    def test_find_file_exception_outside_valid_years(self):
        file = "rwerewjuly2030.csv"
        self.assertRaises(IDE, lambda: VenmoReader.find_file(file))
        
    def test_find_file_normal_data(self):
        file = "WFoctober2021.csv"
        result = VenmoReader.find_file(file)
        self.assertEqual(result, "./venmoData/venmooctober2021.csv")
    
    def test_find_file_year_before_month(self):
        file = "WE2023december.csv"
        result = VenmoReader.find_file(file)
        self.assertEqual(result, "./venmoData/venmodecember2023.csv")
        
    def test_find_file_month_not_valid(self):
        file = "WEdfjkls2021"
        self.assertRaises(IDE, lambda: VenmoReader.find_file(file))
if __name__ == "__main__":
    unittest.main()