import pandas as pd
 
#read the normalized CSV file
#df = pandas.read_csv('AAPL Income Statement.csv')


df = pd.read_csv('AAPL Income Statement.csv')


 
#melt the normalized file, hold the country name and code variables, rename the melted columns
le = pd.melt(df, id_vars=['FieldName'], var_name="year", value_name="data_value")
 
#sort by country name for convenience
le2 =  le.sort(['FieldName'])
 
#write out the csv without and index
le2.to_csv('CSV-unpivoted.csv', sep=',', index=False)