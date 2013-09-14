from Trader import StockTrader
from Stock import Stock

a=Stock('O1E.F')
b=StockTrader(a)
b.learn()
b.trade(10000)