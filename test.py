from Trader import StockTrader
from Stock import Stock

a=Stock('RWE.DE')
b=StockTrader(a)
b.learn()
b.trade(10000)