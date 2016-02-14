import re, os, sys, math, time, datetime, shutil, thread
import pandas
from pattern.web import URL, DOM, plaintext, extension, Element, find_urls
import json

class MS_StatsExtract(object):
    """
        Using morning star ajax call.
        Can only get one stock at a time.
    """
    def __init__(self):
        """ List of url parameters -- for url formation """
## http://financials.morningstar.com/ajax/exportKR2CSV.html?t=XNAS:AAPL&region=usa&culture=en-US&productcode=MLE&cur=&order=desc&r=448121
# http://financials.morningstar.com/ajax/ReportProcess4CSV.html?t=XNAS:GOOG&region=usa&culture=en-US&productcode=MLE&cur=&reportType=is&period=12&dataType=A&order=asc&columnYear=10&curYearPart=1st5year&rounding=3&view=raw&r=904360&denominatorView=raw&number=3
        self.com_kr_data_start_url = r'http://financials.morningstar.com/ajax/exportKR2CSV.html?t=X'
        self.com_data_stock_portion_url = ''
        self.stockexchange_symbol = ''
        self.com_data_stock_portion_additional_url = '' # for adding additonal str to the stock url.
        #self.com_data_end_url = '&region=sgp&culture=en-US&cur=&order=asc'
        #self.com_data_end_url = '&region=usa&culture=en-US&productcode=MLE&cur=&order=desc&r=448121'
        self.com_data_end_url = ''
        self.com_data_full_url = ''
        self.com_is_data_full_url = ''
        self.com_bs_data_full_url = ''
        self.com_cf_data_full_url = ''
        self.stock_list = ''#list of stock to parse.

        #Finance statement
        self.com_data_is_url=r'http://financials.morningstar.com/ajax/ReportProcess4CSV.html?region=usa&culture=en-US&productcode=MLE&cur=&reportType=is&period=12&dataType=A&order=asc&columnYear=10&curYearPart=1st5year&rounding=3&view=raw&r=904360&denominatorView=raw&number=3&t=X'

        #self.com_data_is_url=r'http://financials.morningstar.com/ajax/ReportProcess4CSV.html?reportType=is&t=X'

        #self.com_data_bs_url=r'http://financials.morningstar.com/ajax/ReportProcess4CSV.html?reportType=bs&t=X'

        self.com_data_bs_url=r'http://financials.morningstar.com/ajax/ReportProcess4CSV.html?region=usa&culture=en-US&productcode=MLE&cur=&reportType=bs&period=12&dataType=A&order=asc&columnYear=10&curYearPart=1st5year&rounding=3&view=raw&r=904360&denominatorView=raw&number=3&t=X'

        #self.com_data_cf_url=r'http://financials.morningstar.com/ajax/ReportProcess4CSV.html?reportType=cf&t=X'

        self.com_data_cf_url=r'http://financials.morningstar.com/ajax/ReportProcess4CSV.html?region=usa&culture=en-US&productcode=MLE&cur=&reportType=cf&period=12&dataType=A&order=asc&columnYear=10&curYearPart=1st5year&rounding=3&view=raw&r=904360&denominatorView=raw&number=3&t=X'

        ## printing options
        self.__print_url = 0

        ## temp csv storage path
        #self.ms_stats_extract_temp_csv = r'/Users/jeren/code/data/temp/ms_stats.csv'
        self.com_kr_data_folder = r'/Users/jeren/code/data/temp/kr/'
        self.com_is_data_folder = r'/Users/jeren/code/data/temp/is/'
        self.com_bs_data_folder = r'/Users/jeren/code/data/temp/bs/'
        self.com_cf_data_folder = r'/Users/jeren/code/data/temp/cf/'
        self.com_json_data_folder = r'/Users/jeren/code/data/temp/json/'
        self.com_jsonchild_data_folder= r'/Users/jeren/code/data/temp/jsonchild/'

        #finance statement csv file name
        self.ms_kr_stats_extract_temp_csv = ''
        self.ms_kr_stats_extract_temp_csv_transpose = ''
        self.ms_is_stats_extract_temp_csv = ''
        self.ms_is_stats_extract_temp_csv_transpose = ''
        self.ms_bs_stats_extract_temp_csv = ''
        self.ms_bs_stats_extract_temp_csv_transpose = ''
        self.ms_cf_stats_extract_temp_csv = ''
        self.ms_cf_stats_extract_temp_csv_transpose = ''

        ## Temp Results storage
        self.target_stock_data_df = object()

        ## full result storage
        self.com_data_allstock_df = pandas.DataFrame()
        self.hist_company_data_trends_df = pandas.DataFrame()

    def set_stock_sym_append_str(self, append_str):
        """ Set additional append str to stock symbol when forming stock url.
            Set to sel.cur_quotes_stock_portion_additional_url.
            Mainly to set the '.SI' for singapore stocks.
            Args:
                append_str (str): additional str to append to stock symbol.
        """
        self.com_data_stock_portion_additional_url = append_str

    def set_target_stock_url(self, stock_sym):
        """ Set the target stock. Single stock again.
            Set to self.com_data_stock_portion_url
            Args:
                stock_sym (str): Stock symbol.
        """
        self.com_data_stock_portion_url = stock_sym
        self.stockexchange_symbol = stock_sym.replace(':','_')

    def set_stocklist(self, stocklist):
        """ Set list of stocks to be retrieved.
            Args:
                stocklist (list): list of stocks to be retrieved.
        """
        self.stock_list = stocklist

    def form_url_str(self):
        """ Form the url str necessary to get the .csv file
            May need to segregate into the various types.
            Args:
                type (str): Retrieval type.
        """
        self.com_kr_data_full_url = self.com_kr_data_start_url + self.com_data_stock_portion_url +\
                                   self.com_data_end_url

        self.com_is_data_full_url = self.com_data_is_url + self.com_data_stock_portion_url
        self.com_bs_data_full_url = self.com_data_bs_url + self.com_data_stock_portion_url
        self.com_cf_data_full_url = self.com_data_cf_url + self.com_data_stock_portion_url

    def form_csv_str(self):

        self.ms_kr_stats_extract_temp_csv = self.com_kr_data_folder+self.stockexchange_symbol+'_ms_kr.csv'
        self.ms_kr_stats_extract_temp_csv_transpose = self.com_kr_data_folder+self.stockexchange_symbol+'_ms_kr_t.csv'
        self.ms_bs_stats_extract_temp_csv = self.com_bs_data_folder+self.stockexchange_symbol+'_ms_bs.csv'
        self.ms_bs_stats_extract_temp_csv_transpose = self.com_bs_data_folder+self.stockexchange_symbol+'_ms_bs_t.csv'
        self.ms_is_stats_extract_temp_csv = self.com_is_data_folder+self.stockexchange_symbol+'_ms_is.csv'
        self.ms_is_stats_extract_temp_csv_transpose = self.com_is_data_folder+self.stockexchange_symbol+'_ms_is_t.csv'
        self.ms_cf_stats_extract_temp_csv = self.com_cf_data_folder+self.stockexchange_symbol+'_ms_cf.csv'
        self.ms_cf_stats_extract_temp_csv_transpose = self.com_cf_data_folder+self.stockexchange_symbol+'_ms_cf_t.csv'

    def get_com_data(self):
        """ Combine the cur quotes function.
            Formed the url, download the csv, put in the header. Have a dataframe object.
            Each one is one stock.
        """
        self.form_url_str()
        if self.__print_url: print self.com_data_full_url
        self.form_csv_str()

        ## here will process the data set
        self.downloading_csv('kr')
        self.downloading_csv('is')
        self.downloading_csv('bs')
        self.downloading_csv('cf')

    #doctype = kr (Key Ratio), is (income statement), bs (balance sheet), cf (cash flow)
    def downloading_csv(self,doctype):
        """ Download the csv information for particular stock.
        """
        self.download_fault = 0

        if doctype == 'kr':
            url = URL(self.com_kr_data_full_url)
            print 'Download to: '+self.ms_kr_stats_extract_temp_csv
            f = open(self.ms_kr_stats_extract_temp_csv, 'wb') # save as test.gif
        elif doctype == 'is':
            url = URL(self.com_is_data_full_url)
            print 'Download to: '+self.ms_is_stats_extract_temp_csv
            f = open(self.ms_is_stats_extract_temp_csv, 'wb') # save as test.gif
        elif doctype == 'bs':
            url = URL(self.com_bs_data_full_url)
            print 'Download to: '+self.ms_bs_stats_extract_temp_csv
            f = open(self.ms_bs_stats_extract_temp_csv, 'wb') # save as test.gif
        elif doctype == 'cf':
            url = URL(self.com_cf_data_full_url)
            print 'Download to: '+self.ms_cf_stats_extract_temp_csv
            f = open(self.ms_cf_stats_extract_temp_csv, 'wb') # save as test.gif
        else:
            print 'Error: Do not support doctype =',doctype
            return

        try:
            print ('csv url:', url.string)
            f.write(url.download())#if have problem skip

        except Exception, e:
            print ('Download exception: %s' % e.message)
            print 'Problem when downloading this data: ', url.string
            self.download_fault =1

        f.close()

    #replace non-ascii chars in column name in data frame
    def procee_rename_df_column_chars(self):

        #replace column char space with "_"
        cols = self.target_stock_data_df.columns
        cols = cols.map(lambda x: x.replace(' ', '_') if isinstance(x, (str, unicode)) else x)
        self.target_stock_data_df.columns = cols

        #replace column char "%" with "Percent"
        cols = self.target_stock_data_df.columns
        cols = cols.map(lambda x: x.replace('%', 'Percent') if isinstance(x, (str, unicode)) else x)
        self.target_stock_data_df.columns = cols

        #replace column char "(Average)" with "Average"
        cols = self.target_stock_data_df.columns
        cols = cols.map(lambda x: x.replace('(Average)', 'Average') if isinstance(x, (str, unicode)) else x)
        self.target_stock_data_df.columns = cols

        #replace column char "/" with "Per"
        cols = self.target_stock_data_df.columns
        cols = cols.map(lambda x: x.replace('/', 'Per') if isinstance(x, (str, unicode)) else x)
        self.target_stock_data_df.columns = cols

        #replace column char "'" with ""
        cols = self.target_stock_data_df.columns
        cols = cols.map(lambda x: x.replace('Stockholders\'', 'Stockholders') if isinstance(x, (str, unicode)) else x)
        self.target_stock_data_df.columns = cols

        #replace column char "&" with "append_str"
        cols = self.target_stock_data_df.columns
        cols = cols.map(lambda x: x.replace('&', 'and') if isinstance(x, (str, unicode)) else x)
        self.target_stock_data_df.columns = cols


    def process_krdataset(self):
        """ Processed the data set by converting the csv to dataframe and attached the information for various stocks.

        """
        if self.download_fault:
            print 'Problem when downloading csv from this url: ', self.com_kr_data_full_url
            return

        ## Rows with additional headers are skipped
        try:
            self.target_stock_data_df =  pandas.read_csv(self.ms_kr_stats_extract_temp_csv, header =2, index_col = 0, skiprows = [19,20,31,41,42,43,48,58,53,64,65,72,73,95,101,102])
#            self.target_stock_data_df.info()
        except:
            print 'Problem reading files via pandas.read_csv() so return without transposing csv'
            return
            #thread.interrupt_main()

        self.target_stock_data_df = self.target_stock_data_df.transpose().reset_index()
        self.target_stock_data_df["SYMBOL"] = self.stockexchange_symbol
        self.target_stock_data_df["ReportType"] = 'Key Ratio'
        #after transpose save back to same file and call again for column duplication problem
        self.target_stock_data_df.to_csv(self.ms_kr_stats_extract_temp_csv_transpose, index =False)
        self.target_stock_data_df =  pandas.read_csv(self.ms_kr_stats_extract_temp_csv_transpose)
        #rename columns
        #TODO: There is a bug here. CSV and DF columns do not match.
        self.target_stock_data_df.rename(columns={'Year over Year':'Revenue yoy','3-Year Average':'Revenue 3yr avg',
                                                '5-Year Average':'Revenue 5yr avg','10-Year Average':'Revenue 10yr avg',

                                                'Year over Year.1':'Operating income yoy','3-Year Average.1':'Operating income 3yr avg',
                                                '5-Year Average.1':'Operating income 5yr avg','10-Year Average.1':'Operating income 10yr avg',

                                                'Year over Year.2':'Net income yoy','3-Year Average.2':'Net income 3yr avg',
                                                '5-Year Average.2':'Net income 5yr avg','10-Year Average.2':'Net income 10yr avg',

                                                'Year over Year.3':'EPS yoy','3-Year Average.3':'EPS 3yr avg',
                                                '5-Year Average.3':'EPS 5yr avg','10-Year Average.3':'EPS 10yr avg','index':'Date',},
                                       inplace =True)
        #replace non-ascii chars in column name in data frame
        self.procee_rename_df_column_chars()

        jsonfile = self.com_json_data_folder+self.stockexchange_symbol+'_kr_t.json'
        self.target_stock_data_df.to_json(jsonfile,orient='index')

        #read json file
        with open(jsonfile, 'r') as data_file:
            data = json.load(data_file)
            data_file.close()

        #Output each list item as single json file
        for key in data:
        #Write each line item in t_csv to json file
            jsonchildfile = "{0}{1}_{2}_{3}.json".format(self.com_jsonchild_data_folder,self.stockexchange_symbol,data[key]['Date'],'kr')
            with open(jsonchildfile, 'w') as outfile:
                json.dump(data[key], outfile)
                outfile.close()

        if len(self.com_data_allstock_df) == 0:
            self.com_data_allstock_df = self.target_stock_data_df
        else:
            self.com_data_allstock_df = pandas.concat([self.com_data_allstock_df,self.target_stock_data_df],ignore_index =True)

    def process_isdataset(self):
        """ Processed the data set by converting the csv to dataframe and attached the information for various stocks.

        """
        if self.download_fault:
            print 'Problem when downloading csv from this url: ', self.com_is_data_full_url
            return

        ## Rows with additional headers are skipped
        try:
            self.target_stock_data_df =  pandas.read_csv(self.ms_is_stats_extract_temp_csv, header =1, index_col = 0)
#            self.target_stock_data_df.info()
#        except:
        except Exception, e:
            print 'IS: Problem reading files via pandas.read_csv() so return without transposing csv'
            print ('pandas.read_csv() exception: %s' % e.message)
            return
            #thread.interrupt_main()

        self.target_stock_data_df = self.target_stock_data_df.transpose().reset_index()
        self.target_stock_data_df["SYMBOL"] = self.stockexchange_symbol
        self.target_stock_data_df["ReportType"] = 'Income Statement'
        #after transpose save back to same file and call again for column duplication problem
        self.target_stock_data_df.to_csv(self.ms_is_stats_extract_temp_csv_transpose, index =False)
        self.target_stock_data_df =  pandas.read_csv(self.ms_is_stats_extract_temp_csv_transpose)
        #rename columns
        #TODO: There is a bug here. CSV and DF columns do not match.
        self.target_stock_data_df.rename(columns={'Basic':'EPS Basic','Diluted':'EPS Diluted',
                                                'Basic.1':'Weighted_avg_shares Basic','Diluted.1':'Weighted_avg_shares Diluted','index':'Date',},
                                      inplace =True)
        #replace non-ascii chars in column name in data frame
        self.procee_rename_df_column_chars()

        jsonfile = self.com_json_data_folder+self.stockexchange_symbol+'_is_t.json'
        self.target_stock_data_df.to_json(jsonfile,orient='index')

        #read json file
        with open(jsonfile, 'r') as data_file:
            data = json.load(data_file)
            data_file.close()

        #Output each list item as single json file
        for key in data:
        #Write each line item in t_csv to json file
            jsonchildfile = "{0}{1}_{2}_{3}.json".format(self.com_jsonchild_data_folder,self.stockexchange_symbol,data[key]['Date'],'is')
            with open(jsonchildfile, 'w') as outfile:
                json.dump(data[key], outfile)
                outfile.close()

        if len(self.com_data_allstock_df) == 0:
            self.com_data_allstock_df = self.target_stock_data_df
            #self.target_stock_data_df = object()
        else:
            self.com_data_allstock_df = pandas.concat([self.com_data_allstock_df,self.target_stock_data_df],ignore_index =True)
            #self.target_stock_data_df = object()
            #self.target_stock_data_df.drop()

    def process_bsdataset(self):
        """ Processed the data set by converting the csv to dataframe and attached the information for various stocks.

        """
        if self.download_fault:
            print 'Problem when downloading csv from this url: ', self.com_bs_data_full_url
            return

        ## Rows with additional headers are skipped
        try:
            self.target_stock_data_df =  pandas.read_csv(self.ms_bs_stats_extract_temp_csv, header =1, index_col = 0)
#            self.target_stock_data_df.info()
#        except:
        except Exception, e:
            print 'BS: Problem reading files via pandas.read_csv() so return without transposing csv'
            print ('pandas.read_csv() exception: %s' % e.message)
            return
            #thread.interrupt_main()

        self.target_stock_data_df = self.target_stock_data_df.transpose().reset_index()
        self.target_stock_data_df["SYMBOL"] = self.stockexchange_symbol
        self.target_stock_data_df["ReportType"] = 'Balance Sheet'
        #after transpose save back to same file and call again for column duplication problem
        self.target_stock_data_df.to_csv(self.ms_bs_stats_extract_temp_csv_transpose, index =False)
        self.target_stock_data_df =  pandas.read_csv(self.ms_bs_stats_extract_temp_csv_transpose)
        #rename columns
        #TODO: There is a bug here. CSV and DF columns do not match.
        self.target_stock_data_df.rename(columns={'index':'Date',},
                                      inplace =True)

        #replace non-ascii chars in column name in data frame
        self.procee_rename_df_column_chars()

        jsonfile = self.com_json_data_folder+self.stockexchange_symbol+'_bs_t.json'
        self.target_stock_data_df.to_json(jsonfile,orient='index')

        #read json file
        with open(jsonfile, 'r') as data_file:
            data = json.load(data_file)
            data_file.close()

        #Output each list item as single json file
        for key in data:
        #Write each line item in t_csv to json file
            jsonchildfile = "{0}{1}_{2}_{3}.json".format(self.com_jsonchild_data_folder,self.stockexchange_symbol,data[key]['Date'],'bs')
            with open(jsonchildfile, 'w') as outfile:
                json.dump(data[key], outfile)
                outfile.close()

        if len(self.com_data_allstock_df) == 0:
            self.com_data_allstock_df = self.target_stock_data_df
            #self.target_stock_data_df = object()
        else:
            self.com_data_allstock_df = pandas.concat([self.com_data_allstock_df,self.target_stock_data_df],ignore_index =True)
            #self.target_stock_data_df = object()
            #self.target_stock_data_df.drop()

    def process_cfdataset(self):
        """ Processed the data set by converting the csv to dataframe and attached the information for various stocks.

        """
        if self.download_fault:
            print 'Problem when downloading csv from this url: ', self.com_cf_data_full_url
            return

        ## Rows with additional headers are skipped
        try:
            self.target_stock_data_df =  pandas.read_csv(self.ms_cf_stats_extract_temp_csv, header =1, index_col = 0)
#            self.target_stock_data_df.info()
#        except:
        except Exception, e:
            print 'CF: Problem reading files via pandas.read_csv() so return without transposing csv'
            print ('pandas.read_csv() exception: %s' % e.message)
            return
            #thread.interrupt_main()

        self.target_stock_data_df = self.target_stock_data_df.transpose().reset_index()
        self.target_stock_data_df["SYMBOL"] = self.stockexchange_symbol
        self.target_stock_data_df["ReportType"] = 'Cash Flow'
        #after transpose save back to same file and call again for column duplication problem
        self.target_stock_data_df.to_csv(self.ms_cf_stats_extract_temp_csv_transpose, index =False)
        self.target_stock_data_df =  pandas.read_csv(self.ms_cf_stats_extract_temp_csv_transpose)
        #rename columns
        #TODO: There is a bug here. CSV and DF columns do not match.
        self.target_stock_data_df.rename(columns={'index':'Date',},
                                      inplace =True)

        #replace non-ascii chars in column name in data frame
        self.procee_rename_df_column_chars()

        jsonfile = self.com_json_data_folder+self.stockexchange_symbol+'_cf_t.json'
        self.target_stock_data_df.to_json(jsonfile,orient='index')

        #read json file
        with open(jsonfile, 'r') as data_file:
            data = json.load(data_file)
            data_file.close()

        #Output each list item as single json file
        for key in data:
        #Write each line item in t_csv to json file
            jsonchildfile = "{0}{1}_{2}_{3}.json".format(self.com_jsonchild_data_folder,self.stockexchange_symbol,data[key]['Date'],'cf')
            with open(jsonchildfile, 'w') as outfile:
                json.dump(data[key], outfile)
                outfile.close()

        if len(self.com_data_allstock_df) == 0:
            self.com_data_allstock_df = self.target_stock_data_df
        else:
            self.com_data_allstock_df = pandas.concat([self.com_data_allstock_df,self.target_stock_data_df],ignore_index =True)

    def get_com_data_fr_all_stocks(self):
        """ Cater for all stocks. Each stock is parse one at a time.
        """
        self.com_data_allstock_df = pandas.DataFrame()

        for stock in self.stock_list:
            print 'Set target stock:', stock
            self.set_target_stock_url(stock)
            print 'Get stock info:', stock
            self.get_com_data()
            #print 'Download stock info to csv:', stock
            #self.downloading_csv()
            print 'Processing stock:', stock
            self.process_krdataset()
            self.process_isdataset()
            self.process_bsdataset()
            self.process_cfdataset()

    ## process the data, group by each symbol and take the last 3-5 years EPS year on year??
    def get_trend_data(self):
        """ Use for getting trends data of the dataset.
            Separate to two separate type. One is looking at gain in yoy gain, which means the gain of EPS eg is higher this year over the last as
            compared to the EPS gain of last year over the previous one.
            The other is positive gain which look for gain of company over year.
            may have accel growth if starting is negative

        """
        grouped_symbol = self.com_data_allstock_df.groupby("SYMBOL")

        self.hist_company_data_trends_df = pandas.DataFrame()
        for label in ['EPS yoy','Revenue yoy','Net income yoy']:
            for n in range(9,5,-1):
                if n == 9:
                    prev_data = grouped_symbol.nth(n)[label]
                    accel_growth_check = (prev_data == prev_data) #for EPS growth increase every year
                    normal_growth_check =  (prev_data >0) #for normal increase
                    continue
                current_data = grouped_symbol.nth(n)[label]
                accel_growth_check = accel_growth_check & (current_data <= prev_data)
                normal_growth_check = normal_growth_check & (current_data >0)
                prev_data = current_data

            accel_growth_check = accel_growth_check.to_frame().rename(columns = {label: label + ' 4yr_accel'}).reset_index()
            normal_growth_check = normal_growth_check.to_frame().rename(columns = {label: label + ' 4yr_grow'}).reset_index()

            both_check_df =  pandas.merge(accel_growth_check, normal_growth_check, on = 'SYMBOL' )

            if len(self.hist_company_data_trends_df) ==0:
                self.hist_company_data_trends_df = both_check_df
            else:
                self.hist_company_data_trends_df = pandas.merge(self.hist_company_data_trends_df, both_check_df, on = 'SYMBOL' )

    def modify_stock_sym_in_df(self):
        """ Modify the stock sym in df especially for the Singapore stock where it require .SI to join in some cases.

        """
        self.hist_company_data_trends_df['SYMBOL']= self.hist_company_data_trends_df['SYMBOL'].astype(str) +'.SI'

    def strip_additional_parm_fr_stocklist(self, stocklist, add_parm = '.SI'):
        """ Strip the addtional paramters from the stock list. True in case where the input is XXX.SI and morning star do not required the additioanl SI.
            Args:
                stocklist (list): list of stock sym.
            Kwargs:
                add_parm (str): string to omit (.SI)

        """
        return [re.search('(.*)%s'%add_parm, n).group(1) for n in stocklist]

if __name__ == '__main__':

    choice  = 4

    if choice ==2:

        pp = MS_StatsExtract()
        pp.set_stocklist(['BN4','BS6','N4E','U96'])
        pp.get_com_data_fr_all_stocks()
        pp.get_trend_data()
        pp.modify_stock_sym_in_df()
        print pp.hist_company_data_trends_df
