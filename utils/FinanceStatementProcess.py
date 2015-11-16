from bs4 import BeautifulSoup


class ParseFShtml(object):

    def __init__(self):
        #read htmp file
        self.html_data_folder = r'/Users/misc/code/data/SEC/AAPL/'
        self.htmlfile=""
        #self.htmlfile = self.html_data_folder+r'AAPL10K.html'
        self.soup = ""

    def html2txt(self,inputhtmlfile):
        self.htmlfile = self.html_data_folder+inputhtmlfile
        with open(self.htmlfile, 'r') as html_file:
            self.soup = BeautifulSoup(html_file, 'html.parser')
            html_file.close()

        #print(self.soup.get_text())

        jsonchildfile = self.html_data_folder+inputhtmlfile+'_out.txt'
        with open(jsonchildfile, 'w') as outfile:
            outfile.write(self.soup.get_text().encode('utf8'))
            outfile.close()

if __name__ == '__main__':

    choice  = 4

    if choice ==2:

        pp = ParseFShtml()
        # pp.set_stocklist(['BN4','BS6','N4E','U96'])
        # pp.get_com_data_fr_all_stocks()
        # pp.get_trend_data()
        # pp.modify_stock_sym_in_df()
        # print pp.hist_company_data_trends_df