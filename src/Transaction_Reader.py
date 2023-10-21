from abc import ABC, abstractmethod
import os, sys
fpath = os.path.join(os.path.dirname(__file__), '../')
sys.path.append(fpath)
from src.personalization import VALID_CATEGORIES, VALID_INCOME, INPUT_CATEGORIES, INPUT_INCOME, CATEGORIES

class Transaction_Reader(ABC):
    
    def initialize(cls, data: str):
        if data == "Wells Fargo":
            from Wells_Fargo_Reader import Wells_Fargo_Reader
            card = input("What type of card is this Wells Fargo data from, Credit or Debit?: ")
            return Wells_Fargo_Reader(card)
        
    @abstractmethod
    def format_rows_from_csv_file(self, file: str) -> list:
        # [Date, Amount, Description, Category, Type]
        pass
    
    def _find_category(self, description: str, amount: str, date: str) -> str:
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
        lower_desc = description.lower()
        for key in VALID_INCOME:
            if key in lower_desc: 
                return VALID_INCOME.get(key)

        return _get_user_income_category(description, amount, date)

def _get_user_category(message: str):
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

def format_rows_csv_file(file: str):
    from Wells_Fargo_Reader import Wells_Fargo_Reader
    if "WF" in file:
        card = input("What type of card is this Wells Fargo data from, Credit or Debit?: ")
        reader: Wells_Fargo_Reader = Wells_Fargo_Reader(card)
        return reader.format_rows_from_csv_file(file)