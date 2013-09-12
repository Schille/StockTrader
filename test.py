from Trader import StockTrader
from Stock import Stock

a=Stock('ibm')
b=StockTrader(a)
#b.learn()
b.trade(10000)