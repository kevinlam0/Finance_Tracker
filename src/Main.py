import FinanceAutomator

"""
Run this file in order to input transactional data into your Google Sheet.

Args:
    file_path (str): Path of the transactional data in CSV format
    google_sheet (str): Name of your Google Sheet
    sheet (str): Name of the specific worksheet within your Google Sheet
"""
file_path = './checkingsData/june2022.csv'
google_sheet = "Finance Tracker 2"
sheet = "Sheet1"

if __name__ == "__main__":
    fa = FinanceAutomator.FinanceAutomator(google_sheet)
    fa.connect_to_google()
    # fa.inject_one_file(sheet, file_path)
    fa.inject_all_data("checkingsData")
    