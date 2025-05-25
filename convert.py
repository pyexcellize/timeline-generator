from openpyxl import Workbook
import csv

wb = Workbook()
ws = wb.active
with open('./data/appearances.csv', 'r') as f:
    for row in csv.reader(f):
        ws.append(row)
wb.save('./data/appearances.xlsx')
