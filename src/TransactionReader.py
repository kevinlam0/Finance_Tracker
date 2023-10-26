from abc import ABC, abstractmethod
import os, sys
fpath = os.path.join(os.path.dirname(__file__), '../')
sys.path.append(fpath)
from src.personalization import VALID_CATEGORIES, VALID_INCOME, INPUT_CATEGORIES, INPUT_INCOME, CATEGORIES
from src import VenmoReader

class TransactionReader(ABC):
        
    @abstractmethod
    def format_rows_from_csv_file(self, file: str) -> list:
        """ Format rows into list by [date, amount, description, category, type] to inject into Google Sheet. 
        This is an abstract method. """
        pass
    
    def find_venmo_data(self, file: str, card: str, bank: str):
        """ Links the venmo data to reader if there is one associated. If there is not, then return none. """
        ans = input(f"Is this {bank} {card} card linked to a Venmo account (yes/no)? ").lower()
        while ans != "yes" and ans != "no":
            ans = input("Error the answer needs to be yes or no. Is this card linked to a Venmo account? ").lower()
        if ans == "no": return None
        return VenmoReader.VenmoReader(file)
    
    def _find_category(self, description: str, amount: str, date: str) -> str:
        """ Concrete method to find the category of a transaction. 
        It first searches through the categories already defined by user in personalization. If the transaction is not part of the defined categories, then it prompts
        users to input a category. """
        lower_desc = description.lower()
        
        # Already a listed category
        for key in CATEGORIES.keys():
            if key in lower_desc: 
                return CATEGORIES[key]
        
        if "Venmo" in description:
            description_message = ""
        else: 
            description_message = "This is the description: "
            
        """ 
        -- When Venmo is not in the description --
        We could not label the transaction.
        This is the description: {Description}
        This is the amount: {Amount}
        This is the date: {Date}
    
        -- When Venmo is in the description -- 
        We could not label the transaction.
        Venmo transaction: {Desciption}
        This is the amount: {Amount}
        This is the date: {Date}
        """
        message = f"\nWe could not label the transaction.\n{description_message}{description}\nThis is the amount: {amount}\nThis is the date: {date}"
    
        return _get_user_category(message)

    def _find_income_category(self, description: str, amount: float, date: str) -> str:
        """ Finds the category of an income transaction. Prompts user if it cannot be found in defined incomes from personalization. """
        lower_desc = description.lower()
        for key in VALID_INCOME:
            if key in lower_desc: 
                return VALID_INCOME.get(key)

        return _get_user_income_category(description, amount, date)

def _get_user_category(message: str):
    """ Prompts the user to input a valid category already defined in personalization. If nothing matches, user can enter nothing for "Other" """
    print(message)
    category = input("Please state what is the category of this transaction: ").lower().strip()
    while (category != "" and category not in VALID_CATEGORIES and category not in INPUT_CATEGORIES):
        category = input("The category is not valid. Please input one of the following or input nothing to skip:\nEating out, Groceries, Materialistic, Productive, Gas, Rent, Miscellaneous, Subscription: ").lower().strip()
        
    # If blank then just mark it as other
    if category == "": return "Other"
    if category in INPUT_CATEGORIES:
        return INPUT_CATEGORIES.get(category)
    return category.capitalize()

def _get_user_income_category(description: str, amount: float, date: str) -> str:
    """ Prompts the user to input a category for this income transaction. """
    message = f"\nThis is an income with a source we cannot find:\nThis is the description: {description}\nThis is the amount: {amount}\nThis is the date: {date}"
    """
    This is an income with a source we cannot find.
    This is the description: {Description}
    This is the amount: {Amount}
    This is the date: {Date}
    """
    print(message)
    
    category = input("Please state where this income is from: ").lower().strip()
    while (category != "" and category not in VALID_INCOME and category not in INPUT_INCOME):
        category = input("The category is not valid for this income transaction.\nPlease input from your listed income: ").lower().strip()
        
    if category == "": return "Other"
    if category in INPUT_INCOME:
        return INPUT_INCOME.get(category)
    return category.capitalize()

    

    