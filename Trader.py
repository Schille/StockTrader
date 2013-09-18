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
        self.noTradeCounter=0
        
    def learn(self):
        for chunk in self._stock.get_day_chunks(0, config.STARTTRADE):
            result = self._algmanager.execute_calc(chunk)

    
    def trade(self, budget):
        stock_count = 0
        run = 0
        nonstock_budget = budget
        data = []
        for chunk in self._stock.get_day_chunks(config.DELTA * config.STARTTRADE + 1):
            run += 1
            decision = 0
            v = 0
            point = {}
            marker = {}
            result = self._algmanager.execute_calc(chunk)
            for score in result:
                decision += score[score.keys()[0]][0] * score[score.keys()[0]][1]
                v += score[score.keys()[0]][1]
            # weighted average
           
            if v == 0:
                print('== Run: ' + str(run) + ' ==' )
                print('Stock Sold: ' + str(0) +  ' Bought: ' + str(0))
                print('Stock count:' + str(stock_count))
                print('Budget:' + str(nonstock_budget + stock_count * cur_stock))
                continue 
            decision = decision / v
            # decision must be between -1 and 1
            decision = 1 if decision > 1 else decision
            decision = -1 if decision < -1 else decision
            # buy share / sell share / hold share
            cur_stock = chunk[-1]['close'] 
            print "------->FINAL DECISION: " + str(decision)
            if decision < 0.08 and decision > -0.08:
                print('== Run: ' + str(run) + ' ==' )
                print('Stock Sold: ' + str(0) +  ' Bought: ' + str(0))
                print('Stock count:' + str(stock_count))
                print('Budget:' + str(nonstock_budget + stock_count * cur_stock))
                print "----- I'M HERE -----"
                self.noTradeCounter+=1
                continue
            count_buy = 0
            count_sell = 0
            if decision > 0:
                # how many shares to be bought
                count_buy = math.floor((nonstock_budget * decision) / cur_stock)
                if count_buy == 0:
                    self.noTradeCounter+=1
                stock_count += count_buy
                # how much cash remaining
                nonstock_budget -= count_buy * cur_stock
                point['decision'] = 'buy'
                point['color'] = '#0F0'
                marker['fillColor'] = '#00bd1f' if count_buy != 0 else '#9D9'
                marker['radius'] = 4 if count_buy != 0 else 3
               
            elif decision < 0:
                # how many shares to be sold
                count_sell = math.floor(((stock_count * cur_stock) * math.fabs(decision)) / cur_stock)
                if count_sell == 0:
                    self.noTradeCounter+=1
                stock_count -= count_sell
                # how much cash remaining
                nonstock_budget += count_sell * cur_stock 
                point['decision'] = 'sell'
                point['color'] = '#F00'
                marker['fillColor'] = '#E33' if count_sell != 0 else '#D99'
                marker['radius'] = 4 if count_sell != 0 else 3
                
            point['probability'] = round(math.fabs(decision)*100, 2)
            point['marker'] = marker    
            print('== Run: ' + str(run) + ' ==' )
            print('Stock Sold: ' + str(count_sell) +  ' Bought: ' + str(count_buy))
            print('Stock count:' + str(stock_count))
            print('Budget:' + str(nonstock_budget + stock_count * cur_stock))
            point['y'] = chunk[-1]['close']
            data.append(point)
        print("No Trade Chunks: "+str(self.noTradeCounter))   
        metadata = {}
        metadata['name'] = self._stock._symbol
        
        with open('data.js', 'w') as outfile:
            outfile.write("var data = ")    
            json.dump(data, outfile)        
            outfile.write(";var metadata = ")    
            json.dump(metadata, outfile)
            
   
