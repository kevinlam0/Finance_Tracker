import FinanceAutomator
import csv
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
file_path = './checkingsData/june2022.csv'
google_sheet = "Finance Tracker 2"
sheet = "May 2022"
folder = "checkingsData"



if __name__ == "__main__":
    # fa = FinanceAutomator.FinanceAutomator(google_sheet)
    # fa.connect_to_google()
    # fa.inject_one_file(sheet, file_path)
    # fa.inject_all_data(folder)
    file_path = "./checkingsData/venmomay2022.csv"
    with open(file_path, 'r') as csv_reader:
        csv_reading = csv.reader(csv_reader)
        
        # for i in range(len(csv_reading)):
        #     print(csv_reading[i])
        loop = 5
        for line in csv_reading:
            print(line)
            if loop <= 0:
                break
            loop -= 1
    