import gtk, webkit
import json
import os
import urllib
from Trader import StockTrader
from Stock import Stock
import config
import datetime
import math

class MasterTrader():
    
    def __init__(self):
        self.w = gtk.Window()
        self.v = webkit.WebView()
        self.stock_traders = {}
        self.budget = 10000
        self.stock_budget = 0
        self.cur_date = datetime.datetime.strptime('2012-01-01', '%Y-%m-%d')
        self.show_window()
        
    
    def show_window(self):
        self.sw = gtk.ScrolledWindow()
        self.w.add(self.sw)
        self.sw.add(self.v)
        self.w.set_size_request(1000, 800)
        self.w.connect("destroy", lambda q: gtk.main_quit())
        
        self.v.connect('title-changed', self.title_changed)
        file = os.path.abspath('index1.htm')
        uri = 'file://' + urllib.pathname2url(file)
        self.v.load_uri(uri)
        self.w.show_all()
        gtk.main()
    
    def title_changed(self, widget, frame, title):
        if not title:
            return
        func = title.split("::", 1)[0]
        param = title.split("::", 1)[1]
        
        if func == "add_stock":
            self.add_stock(param)
        elif func == "rm_stock":
            self.rm_stock(param)
        elif func == "next":
            self.next()
        elif func == "set_data":
            date = param.split(",", 1)[0]
            budget = param.split(",", 1)[1]
            self.set_data(date, budget)
        else:
            return

        
    def add_stock(self, symbol):
        stock=None
        try:
            stock = Stock(symbol, datetime.datetime.strptime(config.DAYSTART, '%Y-%m-%d'))
        except:
            self.v.execute_script("add_stock(%s)" % json.dumps(""))
            return
            
        stock_trader = StockTrader(stock)
        stock_trader.learn(config.DELTA, self.cur_date - datetime.timedelta(config.DELTA))
        self.stock_traders[symbol] = {'symbol':symbol,'trader':stock_trader, 'stock_cnt':0}
        
        # Now, send a message back to JavaScript
        self.v.execute_script("add_stock(%s)" % json.dumps(symbol))
        
    def rm_stock(self, symbol):
        if self.stock_traders.has_key(symbol):
            print "debug"
            del self.stock_traders[symbol]
            self.v.execute_script("rm_stock(%s)" % json.dumps(symbol))
        else:
            self.v.execute_script("rm_stock(%s)" % json.dumps(""))
        
    def next(self):
        self.stock_budget=0
        buy_stocks = []
        decision_sum = 0
        result = {'date':int(self.cur_date.strftime('%s')) * 1000}
        series = {}
        for k in self.stock_traders.keys():
            series[k] = {}
            self.stock_traders[k]['decision'], self.stock_traders[k]['price'] = self.stock_traders[k]['trader'].trade(self.cur_date)
            series[k]['price'] = self.stock_traders[k]['price']         
            self.stock_traders[k]['old_stock_cnt']=self.stock_traders[k]['stock_cnt']
            
            if self.stock_traders[k]['decision'] > 0:
                series[k]['color']='#0F0'
                self.budget += self.stock_traders[k]['price'] * self.stock_traders[k]['stock_cnt']
                self.stock_traders[k]['stock_cnt'] = 0
                buy_stocks.append(self.stock_traders[k])
                decision_sum += self.stock_traders[k]['decision']
            else:
                series[k]['color']='#F00'
                count_sell = math.floor(self.stock_traders[k]['stock_cnt'] * math.fabs(self.stock_traders[k]['decision']))
                if count_sell == 0:
                    series[k]['marker']={'radius':3, 'fillColor':'#D99'}
                else:
                    series[k]['marker']={'radius':4, 'fillColor':'#E33'}
                self.budget += self.stock_traders[k]['price'] * count_sell
                self.stock_traders[k]['stock_cnt'] -= count_sell
                self.stock_budget+=self.stock_traders[k]['stock_cnt']*self.stock_traders[k]['price']
        
        for stock in buy_stocks:
            print stock['decision']
            print("BUDGET: "+str(self.budget))
            print("STOCK_PRICE: "+str(stock['price']))
            print("DECISION: "+str(stock['decision']))
            print("DECISION_SUM: "+str(decision_sum))
            count_buy = math.floor((self.budget * (stock['decision'] / decision_sum) * stock['decision']) / stock['price'])
            print("count_buy "+str(stock['symbol'])+": "+str(count_buy))
            if count_buy <= stock['old_stock_cnt']:
                series[stock['symbol']]['marker']={'radius':3, 'fillColor':'#9D9'}
            else:
                series[stock['symbol']]['marker']={'radius':4, 'fillColor':'#00bd1f'}
            self.budget -= count_buy * stock['price']
            stock['stock_cnt'] += count_buy
            self.stock_budget+=stock['stock_cnt']*stock['price']
            decision_sum -= stock['decision']
        
        print("FINAL Decision: "+str(self.stock_traders[k]['decision']))
        print("PRICE: "+str(self.stock_traders[k]['price']))
        print("BUDGET: "+str(self.budget))
        print("STOCK_BUDGET: "+str(self.stock_budget))
        
        series['budget'] = self.budget+self.stock_budget
        result['series'] = series
        self.v.execute_script("next(%s)" % json.dumps(result))
        self.cur_date += datetime.timedelta(days=config.DELTA)
        
    def set_data(self, date, budget):
        self.budget = budget
        self.cur_date = datetime.datetime.strptime(date, '%Y-%m-%d')