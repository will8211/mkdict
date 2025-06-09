#!/usr/bin/env python3
#
# Exports MK dictionary from mysql to an xls file for sharing

from datetime import datetime

import MySQLdb
import xlwt

# Connect to database in SQL

conn = MySQLdb.connect(host="localhost", user='root', passwd='iamafish', 
                       db='mkdictionary', charset='utf8')
cursor = conn.cursor()
SQL = cursor.execute

# xlwt variables

book = xlwt.Workbook()
sheet1 = book.add_sheet("Sheet1")

# Column headings

cols = ["Type",
    "Chinese",
    "English",
    "POJ",
    "TRS",
    "DT",
    "POJ_numbers",
    "TRS_numbers",
    "DT_numbers",
    "Tai_char"]

row = sheet1.row(0)
for index, col in enumerate(cols):
    row.write(index, col)

# Copy db to xls

SQL("SELECT COUNT(*) FROM Dict")
data = cursor.fetchone()
length = data[0]

for num in range(1, length):
    db_num = num+1

    if not db_num % 1000:
        print(db_num, 'of', length)

    row = sheet1.row(num)
    for index, col in enumerate(cols):
        SQL("SELECT %s FROM Dict WHERE Id=%s" % (col, db_num))
        data = cursor.fetchone()
        row.write(index, data[0])

# Close connection

cursor.close()
conn.close()

# Save to file

d = datetime.now()
filename = "MkDict_%d_%d_%d.xls" % (d.year, d.month, d.day)
book.save(filename)
