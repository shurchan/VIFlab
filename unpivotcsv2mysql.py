import csv
import MySQLdb

mydb = MySQLdb.connect(host='localhost',
    user='root',
    passwd='',
    db='testdb')
cursor = mydb.cursor()

csv_data = csv.reader(file('CSV-unpivoted.csv'))
header_line = csv_data.next()
print header_line
for row in csv_data:

    '''cursor.execute('INSERT INTO testcsv(FieldName, \
          year, data_value )' \
          'VALUES("%s", "%s", "%s")', 
          row)
	'''
    cursor.execute("insert into testcsv(FieldName, year, data_value) values(%s, %s, %s)", row)
#close the connection to the database.
mydb.commit()
cursor.close()
print "Done"