#!/usr/bin/env python
import MySQLdb
import json
import collections

def Sql2Json():
    mydb = MySQLdb.connect(host='localhost',
    user='root',
    passwd='',
    db='testdb')
    cursor = mydb.cursor()
    
    sSQLCmd = "select FieldName,year,data_value,StockSymbol,ReportType,ReportFreq from testcsv \
              where StockSymbol = '%s' and ReportType = '%s'" % ('mu','is')
    try:
        cursor.execute(sSQLCmd)
        rows = cursor.fetchall()
  
    # Convert query to objects of key-value pairs
 
        objects_list = []
        for row in rows:
            d = collections.OrderedDict()
            d['FieldName'] = row[0]
            d['year'] = row[1]
            d['data_value'] = row[2]
            d['StockSymbol'] = row[3]
            d['ReportType'] = row[4]
            d['ReportFreq'] = row[5]
            objects_list.append(d)
 
        j = json.dumps(objects_list)
        objects_file = 'Finance_Info.js'
        f = open(objects_file,'w')
        print >> f, j
    except:
        print "Error: Unable to fetch data"
        
    mydb.close()

    print "Done - output to jason from db"

