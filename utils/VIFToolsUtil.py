import urllib
import csv
import MySQLdb
import pandas as pd
import json
#import jsonpickle
import collections
import os,sys
import string
from couchbase.bucket import Bucket

#import pudb;pu.db #for debugging

# Global scope

#MorningStar URL
#original: "http://financials.morningstar.com/ajax/ReportProcess4CSV.html?t=XNAS:"&Ticker&"&region=usa&culture=en-US&productcode=MLE&cur=&reportType=is&period=12&dataType=A&order=asc&columnYear=10&curYearPart=1st5year&rounding=3&view=raw&r=337816&denominatorView=raw&number=3"
#BalanceSheet reportType = bs
#Income Statement: reportType = is
#Cash Flow statement: reportType = cf

MSURL1="http://financials.morningstar.com/ajax/ReportProcess4CSV.html?t=XNAS:"
MSURL2="&region=usa&culture=en-US&productcode=MLE&cur=&reportType="
MSURL3="&period=12&dataType=A&order=asc&columnYear=10&curYearPart=1st5year&rounding=3&view=raw&r=337816&denominatorView=raw&number=3"



def csvMS(ticker, reportType,outCSVFile):
    # local scope
    urlCSV = MSURL1+ticker+MSURL2+reportType+MSURL3
    #outCSVFile = ticker+reportType+".csv"
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

def csv2mysql(sUnpivotCSVFileName,sTicker,sReportType,sReportFreq):
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
	row.append(sReportFreq)
	#TODO add ReportFreq = Annual or Quarter
	cursor.execute("insert into testcsv(FieldName, year, data_value,StockSymbol,ReportType, ReportFreq) values(%s, %s, %s, %s, %s, %s)", row)
	#cursor.execute("insert into testcsv(FieldName, year, data_value) values(%s, %s, %s)", row)
	#close the connection to the database.

    mydb.commit()
    cursor.close()
    print "Done - import to mysql"

# Import KAy Ratio csv files to mysql db
def csvfiles2mysql():

    # Open database connection
    db = MySQLdb.connect (host="88.88.88.10",port=3306,user="root",\
                          passwd="root",db="testdb",local_infile=1)

    cursor=db.cursor()


    sql = """LOAD DATA LOCAL INFILE '{}'
    INTO TABLE testdb.AnnualKRData
    FIELDS TERMINATED BY ','
    OPTIONALLY ENCLOSED BY '"'
    LINES TERMINATED BY '\\n'
    IGNORE 1 LINES"""

    csvfilefolder = os.listdir(r'/Users/misc/code/viflab/data/temp')
    for file_name in csvfilefolder:
        print file_name
        if file_name.endswith('_t.csv'):
            try:
                cursor = db.cursor()
                sqlcmd = sql.format(r'/Users/misc/code/data/temp/'+file_name)
                print sqlcmd
                cursor.execute(sqlcmd)
#                cursor.execute(sql.format(file_name))
                db.commit()
#            except Exception:
            except Exception, e:
                print ('DB exception: %s' % e)
                # Rollback in case there is any error
                db.rollback()
                print 'Failed to load data from csv file %s to mysql',file_name

    # disconnect from server
    db.close()

def jsonfiles2counchbase(jsonfolder, couchbaseIP, bucketname):

    #cb = Bucket('couchbase://10.141.100.101/vif-finance')
      # check if the uploaded file exists
    if not os.path.exists(jsonfolder):
        sys.stderr.write("Invalid path: %s\n" % jsonfolder)
        print "Invalid path: %s\n" % jsonfolder
        return

    cb = Bucket('couchbase://{0}/{1}'.format(couchbaseIP,bucketname))


    #read files from json file folders
    for dir_entry in os.listdir(jsonfolder):
        dir_entry_path = os.path.join(jsonfolder, dir_entry)
        if os.path.isfile(dir_entry_path) and dir_entry_path.endswith('.json'):
            with open(dir_entry_path, 'r') as jsonfile:
                jsondata = json.load(jsonfile)
                #data[dir_entry] = jsonfile.read()
                #set the key.
                #key = "NAS_AAPL-Balance_Sheet"
                key = "{0}-{1}-{2}".format(
                jsondata['SYMBOL'].lower(),
                jsondata['ReportType'].replace(' ', '_').lower(),
                jsondata['Date'].replace('-','_').lower())
                # key is "nas_aapl-balance_sheet-2007_09"

                #Add json to counch base bucket, cb.upsert()
                result = cb.upsert(key, jsondata)
                jsonfile.close()


    #print one record to validate it
    result = cb.get('nas_aapl-balance_sheet-2006_09')
    print result


    # with open('data.json', 'r') as f:
    #     data = json.load(f)



    #result = cb.get('new_holland_brewing_company-sundog')

    #print result


    # new_beer = {
    #    "name": "Old Yankee Ale Jeren",
    #    "abv": 5.00,
    #    "ibu": 0,
    #    "srm": 0,
    #    "upc": 0,
    #    "type": "beer",
    #    "brewery_id": "cottrell_brewing_co",
    #    "updated": "2012-08-30 20:00:20",
    #    "description": ".A medium-bodied Amber Ale Jeren",
    #    "style": "American-Style Amber Jeren",
    #    "category": "North American Ale"
    # }


    #result = cb.upsert(key, new_beer)


def Sql2Json(sStockSym, sReportType, jsonFile):
    mydb = MySQLdb.connect(host='localhost',
    user='root',
    passwd='',
    db='testdb')
    cursor = mydb.cursor()

    sSQLCmd = "select FieldName,year,data_value,StockSymbol,ReportType,ReportFreq from testcsv \
              where StockSymbol = '%s' and ReportType = '%s'" % (sStockSym,sReportType)
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

        j = json.dumps(objects_list,f)
        #j = json.dumps(objects_list)
        #f = open(jsonFile,'w')
        #print >> f, j
	f.close()
    except:
        print "Error: Unable to fetch data"

    mydb.close()

    print "Done - output to jason from db"

class AnnualReport(object):
    #def __init__(self, hello):
    #    self.hello = 'hello world'

    def __init__(self, sStockSym,sReportType):
        self.ticker = sStockSym
	self.report_type=sReportType
	self.report_freq = 'Annual'
        arr={}
	Year = 0
        #append value to arr
        #arr.update({'key3':'value3'})
        #arr.update({'key4':'value4'})

	mydb = MySQLdb.connect(host='localhost',
	user='root',
        passwd='',
        db='testdb')
        cursor = mydb.cursor()

        sSQLCmd = "select FieldName,year,data_value,StockSymbol,ReportType,ReportFreq from testcsv \
                  where StockSymbol = '%s' and ReportType = '%s'" % (sStockSym,sReportType)
	try:
            cursor.execute(sSQLCmd)
            rows = cursor.fetchall()

        # Convert query to objects of key-value pairs

            #objects_list = []
            for row in rows:
                #d = collections.OrderedDict()
                #d['FieldName'] = row[0]

		arr.update({'Year':row[1]})
		arr.update({row[0]:row[2]})

		#Year = row[1]
                #d['year'] = row[1]
                #d['data_value'] = row[2]
                #d['StockSymbol'] = row[3]
                #d['ReportType'] = row[4]
                #d['ReportFreq'] = row[5]
		#self.ReportFreq = row[5]
                #objects_list.append(d)


        #j = json.dumps(objects_list,f)
        #j = json.dumps(objects_list)
        #f = open(jsonFile,'w')
        #print >> f, j
	#f.close()
	except:
	    print "Error: Unable to update json data"
        self.Yearly_Data = arr


        mydb.close()

        print "Done - Create AnnualReport Object"

#TODO: bugs in the following function
def Sql2AnnualJson(sStockSym, sReportType):
    try:
	obj = AnnualReport(sStockSym, sReportType)
        obj_str = jsonpickle.encode(obj, unpicklable=False, max_depth=2)
	f = open("test2.js", 'w')
	f.write(obj_str)

        #print >> f, j

    except:
        print "Error: Unable to fetch data"

    #mydb.close()
    f.close()
    print "Done - output to annual jason from db"
