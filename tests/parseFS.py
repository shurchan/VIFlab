import sys
sys.path.insert(0, r'/Users/misc/code/viflab/utils')

from utils.FinanceStatementProcess import ParseFShtml

text_ext = ParseFShtml()

text_ext.html2txt("AAPL10K.html")

