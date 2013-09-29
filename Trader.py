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
        self._cur_date = self._stock.get_start_date()
        
    def learn(self, chunk_size, end_date):
        self._cur_date = end_date
        for chunk in self._stock.get_day_chunks(chunk_size, self._stock.get_start_date(), end_date):
            self._algmanager.execute_calc(chunk)
            
    def trade(self, end_date):
        period = self._stock.get_day_prices(self._cur_date, end_date)
        result = self._algmanager.execute_calc(period)
        self._cur_date = end_date
        return self.__acc_alg_results(result), period[-1]['close']
        
        
    def __acc_alg_results(self, result_set):
        decision = 0
        probability = 0
        v = 0
        sum_buy = 0
        cnt_buy = 0
        sum_sell = 0
        cnt_sell = 0
        for score in result_set:
            if score[score.keys()[0]][0] == 1:
                sum_buy += score[score.keys()[0]][1]
                cnt_buy += 1
            elif score[score.keys()[0]][0] == -1:
                sum_sell -= score[score.keys()[0]][1]
                cnt_sell += 1
                
        if sum_buy > math.fabs(sum_sell):
            return (sum_buy+sum_sell)/cnt_buy
        elif sum_buy < math.fabs(sum_sell):
            return (sum_sell+sum_buy)/cnt_sell
        else:
            return 0
