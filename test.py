from Trader import StockTrader
from Stock import Stock
import demo

a=Stock('O1E.F')
b=StockTrader(a)
b.learn()
b.trade(10000)
demo.show_gui()
