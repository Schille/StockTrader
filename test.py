import master_trader

m=master_trader.MasterTrader()

m.add_stock('GOOG')

print (str(m.stock_traders))

m.rm_stock('GOOG')

print (str(m.stock_traders))