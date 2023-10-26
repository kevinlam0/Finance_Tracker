import FinanceAutomator as FinanceAutomator

"""
Run this file in order to input transactional data into your Google Sheet.

If you only want to inject one file 
Args:
    file_path (str): Path of the transactional data in CSV format
    google_sheet (str): Name of your Google Sheet
    sheet (str): Name of the specific worksheet within your Google Sheet
    
If you want to inject all data of a folder 
Args:
    folder (str): Name of folder with CSV data files in there
"""
file_path = './checkingsData/WFseptember2022.csv'
google_sheet = "Finance Tracker 2"
sheet = "September 2022"
folder = "checkingsData"



if __name__ == "__main__":
    fa = FinanceAutomator.FinanceAutomator(google_sheet)
    fa.connect_to_google()
    # fa.inject_one_file_to_sheet(sheet, file_path)
    # fa.inject_all_data(folder)
    # file_path = "./venmoData/venmojune2022.csv"
    