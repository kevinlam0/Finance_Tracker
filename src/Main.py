import csv
import gspread
import sys

file = 'june2022.csv'
file_path = './checkingsData/june2022.csv'
print(file_path)


with open(file_path, 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    for row in csv_reader:
        print(row)
        
sa = gspread.service_account()
sh = sa.open("Finance Tracker 2")
wks = sh.worksheet("Sheet1")
rows = None
wks.insert_row([1,3], 10)