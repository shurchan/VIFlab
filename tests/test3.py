#!/usr/bin/env python

import VIFToolsUtil

ticker = 'aapl'

jsonFileFolder = 'jsonfiles/'
reportTypeList = ['is','bs','cf']

#VIFToolsUtil.Sql2Json(ticker,reportType,jsonFileFolder+ticker+reportType+'.js')

for curReportType in reportTypeList:
		
    currentCompanyReport = ticker+curReportType
                
    print 'output json:'+currentCompanyReport
    VIFToolsUtil.Sql2Json(ticker,curReportType,jsonFileFolder+currentCompanyReport+'.js')