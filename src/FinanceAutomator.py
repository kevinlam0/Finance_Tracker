import csv
class FinanceAutomator:
    def __init__(self):
        pass
    def __create_working_rows(self, file: str) -> list:
        transactions = []
        with open(file, 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            
            for row in csv_reader: 
                date = row[0]
                amount = float(row[1])
                desc = row[4]
                category = self.__find_category(desc, categories, amount)
                
    def __find_category(self, description: str, categories: dict, amount: float) -> str: 
        lower_desc = description.lower()
        for key in categories.keys():
            if key in lower_desc: return categories[key]
            
        category = input(f"We could not label the transaction.\nThis is the description: {description}\nThis is the amount: {amount}")
        if category.strip() == "": return "Other"
        return category