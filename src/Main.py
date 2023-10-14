import FinanceAutomator

file = 'june2022.csv'
file_path = './checkingsData/june2022.csv'
print(file_path)

if __name__ == "__main__":
    fa = FinanceAutomator.FinanceAutomator("Finance Tracker 2")
    fa.connect_to_google()
    
    