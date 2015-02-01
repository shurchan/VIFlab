import VIFToolsUtil
ticker = 'csco'
reportType='is'
#csvFileFolder = '~/viflab/csvfiles/'
csvFileFolder = 'csvfiles/'

#tickerList = ['csco','msft','aapl','googl','nov','bhi','stra','sstk','mu','pni','xom','gm']
tickerList = ['csco','msft','aapl','googl','stra','mu'] #bug: nov,bhi,sstk,pni,xom
reportTypeList = ['is','bs','cf']

for curTicker in tickerList:
	for curReportType in reportTypeList:

		
                currentCompanyReport = curTicker+curReportType
                currentCompanyReportFile = csvFileFolder+currentCompanyReport
                

		print 'retieve data from MS:'+currentCompanyReport
		VIFToolsUtil.csvMS(curTicker,curReportType, currentCompanyReportFile+'.csv')

		print 'mornalize MS report....'
		VIFToolsUtil.normalizeMSCSV(currentCompanyReportFile+'.csv',currentCompanyReportFile+'_n.csv') 

		print 'unpivot MS report....'
		VIFToolsUtil.unpivotcsv(currentCompanyReportFile+'_n.csv',currentCompanyReportFile+'_n_unpivot.csv')

		print 'Port data to mysql....'
		VIFToolsUtil.csv2mysql(currentCompanyReportFile+'_n_unpivot.csv',curTicker,curReportType)






'''
print 'retieve data from MS:'+ticker+reportType
VIFToolsUtil.csvMS(ticker,reportType)

print 'mornalize MS report....'
VIFToolsUtil.normalizeMSCSV(ticker+reportType+'.csv',ticker+reportType+'_n.csv') 

print 'unpivot MS report....'
VIFToolsUtil.unpivotcsv(ticker+reportType+'_n.csv',ticker+reportType+'_n_unpivot.csv')

print 'Port data to mysql....'
VIFToolsUtil.csv2mysql(ticker+reportType+'_n_unpivot.csv',ticker,reportType)
'''