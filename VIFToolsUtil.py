import urllib
import csv
import MySQLdb
import pandas as pd
#import pudb;pu.db

# Global scope
#MorningStar URL
#original: "http://financials.morningstar.com/ajax/ReportProcess4CSV.html?t=XNAS:"&Ticker&"&region=usa&culture=en-US&productcode=MLE&cur=&reportType=is&period=12&dataType=A&order=asc&columnYear=10&curYearPart=1st5year&rounding=3&view=raw&r=337816&denominatorView=raw&number=3"
#BalanceSheet reportType = bs
#Income Statement: reportType = is
#Cash Flow statement: reportType = cf

MSURL1="http://financials.morningstar.com/ajax/ReportProcess4CSV.html?t=XNAS:"
MSURL2="&region=usa&culture=en-US&productcode=MLE&cur=&reportType="
MSURL3="&period=12&dataType=A&order=asc&columnYear=10&curYearPart=1st5year&rounding=3&view=raw&r=337816&denominatorView=raw&number=3"



def csvMS(ticker, reportType):
    # local scope
    urlCSV = MSURL1+ticker+MSURL2+reportType+MSURL3
    outCSVFile = ticker+reportType+".csv"
    urllib.urlretrieve(urlCSV, outCSVFile)

def normalizeMSCSV(sRawMSCSVFile, sNormalizedCSVFile):
	raw_csvdata = csv.reader(file(sRawMSCSVFile))
	
	#Store the first row as full company name with ticker
	fullCompanyName = raw_csvdata.next()
	print fullCompanyName

	tmprow = raw_csvdata.next()
	tmprow[0] = 'FieldName' # replace the first cell with "FieldName"
	#print tmprow
	with open(sNormalizedCSVFile, 'wb') as csvfile:
		 #outCSV = csv.writer(csvfile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
		 outCSV = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
		 outCSV.writerow(tmprow)
		 for row in raw_csvdata:
		 	outCSV.writerow(row)


def unpivotcsv(sPivotCSVFileName,sOutputUnPivotFileName):
	df = pd.read_csv(sPivotCSVFileName)
	#melt the normalized file, hold the country name and code variables, rename the melted columns
	le = pd.melt(df, id_vars=['FieldName'], var_name="year", value_name="data_value")
 
	#sort by country name for convenience
	le2 =  le.sort(['FieldName'])
 
	#write out the csv without and index
	le2.to_csv(sOutputUnPivotFileName, sep=',', index=False)

def csv2mysql(sUnpivotCSVFileName,sTicker,sReportType):
	mydb = MySQLdb.connect(host='localhost',
    user='root',
    passwd='',
    db='testdb')
	cursor = mydb.cursor()

	csv_data = csv.reader(file(sUnpivotCSVFileName))
	header_line = csv_data.next()
	print header_line
	for row in csv_data:
		row.append(sTicker)
		row.append(sReportType)
		cursor.execute("insert into testcsv(FieldName, year, data_value,StockSymbol,ReportType) values(%s, %s, %s, %s, %s)", row)
		#cursor.execute("insert into testcsv(FieldName, year, data_value) values(%s, %s, %s)", row)
	#close the connection to the database.
	mydb.commit()
	cursor.close()
	print "Done - import to mysql"

#test
#csvMS("msft","is")