from abc import ABC, abstractmethod
import personalization

class TransactionReader(ABC):
    
    @abstractmethod
    def format_rows_from_csv_file(self, file: str) -> list:
        # [Date, Amount, Description, Category]
        pass
    
    def _find_category(self, description: str, amount: str, date: str) -> str:
        lower_desc = description.lower()
        
        # Already a listed category
        for key in personalization.categories.keys():
            if key in lower_desc: 
                return personalization.categories[key]
        
        venmo = "This is the description: " if "Venmo" not in description else ""
        message = f"\nWe could not label the transaction.\n{venmo}{description}\nThis is the amount: {amount}\nThis is the date: {date}"
        return self.__get_users_cat(message, personalization.VALID_CATEGORIES)

    def __get_users_cat(self, initial_message, map):
        print(initial_message)
        category = input("Please state what is the category of this transaction: ")
        
        while (category.strip() != "" and category.lower() not in map): 
            category = input("The category is not valid. Please input one of the following or input nothing to skip:\nEating out, Groceries, Materialistic, Productive, Gas, Rent, Miscellaneous: ")
        
        # If blank then just mark it as other
        if category.strip() == "": return "Other"
        
        return category.capitalize()

    
def format_rows_csv_file(file: str):
    from WellsFargoReader import WellsFargoReader
    if "WF" in file:
        reader: WellsFargoReader = WellsFargoReader()
        return reader.format_rows_from_csv_file(file)