import config
from AlgorithmManager import AlgorithmManager
from Stock import Stock


class StockTrader():
    def __init__(self, stock):
        if not isinstance(stock, Stock):
            raise Exception('Wrong argument exception: has to be instance of Stock')
        self._stock = stock
        self._algmanager = AlgorithmManager()
        
    def learn(self):
        for chunk in self._stock.get_day_chunks():
            result = self._algmanager.execute_calc(chunk)
            print(result)
        
        