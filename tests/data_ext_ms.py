#!/usr/bin/env python

import sys
sys.path.insert(0, r'/Users/misc/code/viflab/utils')

from utils.morningstar_stats_extractor import MS_StatsExtract
#from utils.VIFToolsUtil import VIFToolsUtil

import VIFToolsUtil

#data_ext = YFinanceDataExtr()
data_ext = MS_StatsExtract()

cvsfilefolder = r'/Users/misc/code/viflab/data/temp'

## Specify the stocks to be retrieved. Each url constuct max up to 50 stocks.
#data_ext.target_stocks = ['AAPL','GOOG'] #special character need to be converted

#data_ext.stock_list = 'AAPL' #special character need to be converted
#data_ext.com_data_stock_portion_url = 'AAPL'
#data_ext.set_target_stock_url('AAPL')
data_ext.stock_list = ['NAS:AAPL','NAS:GOOG','NAS:yhoo','NAS:msft','NYS:gm','NYS:unp','NAS:LBTYA','NYS:WFC','NYS:SAN','NYS:ARMH','NYS:ZINC','NYS:BP','NYS:CHK','NYS:NOV','NYS:CL','NYS:MMM']

## Get the url str
#data_ext.form_url_str()
#print data_ext.com_data_full_url

## Go to url and download the csv.
## Stored the data as pandas.Dataframe.

data_ext.get_com_data_fr_all_stocks()


# Dump all csv data to mysql
#VIFToolsUtil.csvfiles2mysql()


#data_ext.target_stock_data_df.info()
#data_ext.get_trend_data()

#data_ext.modify_stock_sym_in_df()

#print data_ext.hist_company_data_trends_df

#print data_ext.com_data_allstock_df


## >>>   NAME  SYMBOL  LATEST_PRICE  OPEN  CLOSE      VOL  YEAR_HIGH  YEAR_LOW
## >>> 0  SATS  S58.SI          2.99  3.00   3.00  1815000       3.53      2.93
## >>> 1   SGX  S68.SI          7.18  7.19   7.18  1397000       7.63      6.66
