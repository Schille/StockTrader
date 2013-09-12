import ystockquote as ysq
import config
from datetime import date

class Stock:
    def __init__(self, symbol):
        self._symbol = symbol
        self._quotes = self.__get_quotes()
        self._data = self.__get_data()
      
    '''
    Available features (key):
    fifty_two_week_low
    fifty_day_moving_avg
    price
    price_book_ratio
    volume
    market_cap
    dividend_yield
    ebitda
    change
    dividend_per_share
    stock_exchange
    two_hundred_day_moving_avg
    fifty_two_week_high
    price_sales_ratio
    price_earnings_growth_ratio
    earnings_per_share
    short_ratio
    avg_daily_volume
    price_earnings_ratio
    book_value
    '''
    def get_info(self,key):
        return self._data.get(key)
    
    def get_symbol(self):
        return self._symbol
    
    def get_close_prices(self, recent=None):
        if recent is None:
            return self.__iterate_data('Close')
        else:
            return self.__iterate_data('Close')[-recent:]
    
    def get_adjclose_prices(self, recent=None):
        if recent is None:
            return self.__iterate_data('Adj Close')
        else:
            return self.__iterate_data('Adj Close')[-recent:]
    
    def get_open_prices(self, recent=None):
        if recent is None:
            return self.__iterate_data('Open')
        else:
            return self.__iterate_data('Open')[-recent:]
    
    def get_day_prices(self):
        result = []
        for day in sorted(self._quotes.keys()):
            result.append({'close' : float(self._quotes[day]['Close']),
                           'open' : float(self._quotes[day]['Open']),
                           'high' : float(self._quotes[day]['High']),
                           'low' : float(self._quotes[day]['Low'])})
        return result
    
    def get_day_chunks(self):
        result = self.get_day_prices()
        for i in xrange(0, len(result), config.DELTA):
            yield result[i:i+config.DELTA]
    
    def __iterate_data(self, att):
        result = []
        for day in sorted(self._quotes.keys()):
            result.append(float(self._quotes[day][att]))
        return result
    
    def __get_quotes(self):
        return ysq.get_historical_prices(self._symbol, config.DAYSTART, date.today().isoformat())
    
    def __get_data(self):
        return ysq.get_all(self._symbol)
    
    
    