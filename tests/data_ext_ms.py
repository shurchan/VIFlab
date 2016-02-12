#!/usr/bin/env python

import sys
sys.path.insert(0, r'/Users/jeren/code/viflab/utils')

from morningstar_stats_extractor import MS_StatsExtract
#from utils.VIFToolsUtil import VIFToolsUtil

import VIFToolsUtil

#data_ext = YFinanceDataExtr()
data_ext = MS_StatsExtract()

#cvsfilefolder = r'/Users/misc/code/viflab/data/temp'

## Specify the stocks to be retrieved. Each url constuct max up to 50 stocks.


#data_ext.stock_list = 'AAPL' #special character need to be converted
#data_ext.com_data_stock_portion_url = 'AAPL'
#data_ext.set_target_stock_url('NAS:TROW')
#data_ext.stock_list = ['NAS:AAPL','NAS:GOOG','NAS:MU','NYS:BRK.A','NAS:yhoo','NYS:BAC.WS.B','NAS:msft','NYS:gm','NYS:unp','NAS:LBTYA','NYS:WFC','NYS:SAN','NAS:ARMH','NAS:ZINC','NYS:BP','NYS:CHK','NYS:NOV','NYS:CL','NYS:MMM']
#data_ext.stock_list = ['NAS:AAPL','NYS:BRK.A','NYS:BAC.WS.B','NYS:WFC']
#data_ext.stock_list = ['NYS:KING', 'NYS:PAH','NYS:BAM','NAS:GLUU','NYS:MKL','NAS:COST']

#data_ext.stock_list = ['NAS:AAPL','NAS:ARMH','NYS:SAN','NAS:ZINC','NYS:BP','NYS:CHK','NYS:NOV','NYS:CL','NYS:MMM']
#data_ext.stock_list = ['NAS:AAPL']
data_ext.stock_list = ['NAS:TROW']
#data_ext.stock_list = ['NYS:BAC.WS.A','NAS:AAPL']
#data_ext.stock_list =['NAS:AAPL','NYS:CL','NYS:BRK.A','NYS:BRK.B']

## Get the url str
#data_ext.form_url_str()
#print data_ext.com_data_full_url

## Go to url and download the csv.
## Stored the data as pandas.Dataframe.

data_ext.get_com_data_fr_all_stocks()


# Dump all csv data to mysql
#VIFToolsUtil.csvfiles2mysql()


VIFToolsUtil.jsonfiles2counchbase('/Users/jeren/code/data/temp/jsonchild/','10.112.110.101','vif-finance')

#data_ext.target_stock_data_df.info()
#data_ext.get_trend_data()

#data_ext.modify_stock_sym_in_df()

#print data_ext.hist_company_data_trends_df

#print data_ext.com_data_allstock_df


## >>>   NAME  SYMBOL  LATEST_PRICE  OPEN  CLOSE      VOL  YEAR_HIGH  YEAR_LOW
## >>> 0  SATS  S58.SI          2.99  3.00   3.00  1815000       3.53      2.93
## >>> 1   SGX  S68.SI          7.18  7.19   7.18  1397000       7.63      6.66
