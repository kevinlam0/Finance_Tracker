import unittest

class FinanceAutomatorTests(unittest.TestCase):
    def getUserCat_space(self):
        fa = FinanceAutomator.FinanceAutomator("whatever")
        
        self.assertEqual("Other", fa.__get_users_cat("Whatever"))