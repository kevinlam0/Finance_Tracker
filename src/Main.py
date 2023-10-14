import FinanceAutomator
import csv
import calendar
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
    fa = FinanceAutomator.FinanceAutomator(google_sheet)
    fa.connect_to_google()
    fa.inject_one_file(sheet, file_path)
    # fa.inject_all_data(folder)
    file_path = "./venmoData/venmojune2022.csv"
    # with open(file_path, 'r') as csv_reader:
    #     csv_reading = csv.reader(csv_reader)
        
    #     # for i in range(len(csv_reading)):
    #     #     print(csv_reading[i])
    #     loop = 5
    #     for line in csv_reading:
    #         print(line)
    #         if loop <= 0:
    #             break
    #         loop -= 1
            
    # files = open(file_path, 'r')
    # lines = [line.strip() for line in files]
    # for i in range(len(lines)):
    #     print(f"{i} - {lines[i]}")
    
    
        
    
    # fa.venmo_lookup(43.42, "06/07/2022")
    # string = "- $43.42"
    # gsd = -43.42
    # print(float(string[0]+string[3:]) == gsd)