import config
from AlgorithmManager import AlgorithmManager
from Stock import Stock
import math
import json


class StockTrader():
    def __init__(self, stock):
        if not isinstance(stock, Stock):
            raise Exception('Wrong argument exception: has to be instance of Stock')
        self._stock = stock
        self._algmanager = AlgorithmManager()
        self._cur_date = self.exit_stock.get_start_date()
        
    def learn(self, chunk_size, end_date):
        self._cur_date = end_date
        for chunk in self._stock.get_day_chunks(chunk_size, self._stock.get_start_date(), end_date):
            self._algmanager.execute_calc(chunk)
            
    def trade(self, end_date):
        period = self._stock.get_day_prices(self._cur_date, end_date)
        result = self._algmanager.execute_calc(period)
        self._cur_date = end_date
        return self.__acc_alg_results(result),period[-1]['close']
        
        
    def __acc_alg_results(self, result_set):
        decision = 0
        probability = 0
        v = 0
        for score in result_set:
                decision += score[score.keys()[0]][0] * score[score.keys()[0]][1]
                v += score[score.keys()[0]][1]
        decision = decision / v
        probability = decision / len(result_set)
        return decision * probability
   
