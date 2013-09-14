from Trader import StockTrader
from Stock import Stock

a=Stock('GOOG')
b=StockTrader(a)
b.learn()
b.trade(10000)