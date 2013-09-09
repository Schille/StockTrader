import ystockquote as ysq
import config
from datetime import date

class Stock:
    def __init__(self, symbol):
        self._symbol = symbol
        self._data = self.get_data(symbol)
    
    
    def get_data(self,symbol):
        return ysq.get_historical_prices(symbol, config.DAYSTART, date.today().isoformat())
    
    
     
    