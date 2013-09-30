from gi.repository import Gtk, WebKit
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
        self.w = Gtk.Window()
        self.v = WebKit.WebView()
        self.stock_traders = {}
        self.budget = 10000
        self.stock_budget = 0
        self.cur_date = datetime.datetime.strptime('2012-01-01', '%Y-%m-%d')
        self.border = 0.5
        self.last_sum = 1
        self.show_window()
        
    
    def show_window(self):
        self.sw = Gtk.ScrolledWindow()
        self.w.add(self.sw)
        self.sw.add(self.v)
        self.w.set_size_request(1000, 800)
        self.w.connect("destroy", lambda q: Gtk.main_quit())
        
        self.v.connect('title-changed', self.title_changed)
        file = os.path.abspath('index1.htm')
        uri = 'file://' + urllib.pathname2url(file)
        self.v.load_uri(uri)
        self.w.show_all()
        Gtk.main()
    
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
        stock = None
        try:
            stock = Stock(symbol, datetime.datetime.strptime(config.DAYSTART, '%Y-%m-%d'))
        except:
            self.v.execute_script("add_stock(%s)" % json.dumps(""))
            return
            
        stock_trader = StockTrader(stock)
        stock_trader.learn(config.DELTA, self.cur_date - datetime.timedelta(config.DELTA))
        self.stock_traders[symbol] = {'symbol':symbol, 'trader':stock_trader, 'stock_cnt':0}
        
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
        print("=====NEXT=====")
        self.stock_budget = 0
        decision_sum = 0
        result = {'date':int(self.cur_date.strftime('%s')) * 1000}
        series = {}
        sum = 0
        
        # Phase 1: withdraw
        for k in self.stock_traders.keys():
            series[k] = {}
            self.stock_traders[k]['decision'], self.stock_traders[k]['price'] = self.stock_traders[k]['trader'].trade(self.cur_date)
            self.stock_traders[k]['decision'] += 1
            series[k]['price'] = self.stock_traders[k]['price']    
            self.stock_traders[k]['old_stock_cnt'] = self.stock_traders[k]['stock_cnt']
            
            self.budget += self.stock_traders[k]['price'] * self.stock_traders[k]['stock_cnt']
            self.stock_traders[k]['stock_cnt'] = 0
            
            # calc decision_sum
            if self.stock_traders[k]['decision'] > self.border:
                decision_sum += self.stock_traders[k]['decision']
                
            #add value to sum
            sum += self.stock_traders[k]['price']
        
        # phase 2: invest
        for k in self.stock_traders.keys():
            
            print("BUDGET: " + str(self.budget))
            print("STOCK_PRICE: " + str(self.stock_traders[k]['price']))
            print("DECISION: " + str(self.stock_traders[k]['decision']))
            print("DECISION_SUM: " + str(decision_sum))
            
            if self.stock_traders[k]['decision'] > self.border:
                #estimation of count_buy for one or multiple stocks
                count_buy = math.floor((float(self.budget) * (float(self.stock_traders[k]['decision']) / decision_sum) * (float(self.stock_traders[k]['decision'])/2)) / self.stock_traders[k]['price'])
                print("buy_percentage: "+str((float(self.stock_traders[k]['decision']) / decision_sum) * (float(self.stock_traders[k]['decision'])/2)))
                    
                self.budget -= count_buy * self.stock_traders[k]['price']
                self.stock_budget += count_buy * self.stock_traders[k]['price']
                decision_sum -= self.stock_traders[k]['decision']
            else:
                count_buy = 0
            self.stock_traders[k]['stock_cnt'] = count_buy

            # coloring points
            print("count_buy " + str(self.stock_traders[k]['symbol']) + ": " + str(count_buy))
            if count_buy > self.stock_traders[k]['old_stock_cnt']:
                series[k]['color'] = '#0F0'
                series[k]['marker'] = {'radius':4, 'fillColor':'#00bd1f'}
            elif count_buy < self.stock_traders[k]['old_stock_cnt']:
                series[k]['color'] = '#F00'
                series[k]['marker'] = {'radius':4, 'fillColor':'#E33'}
            else:
                series[k]['color'] = '#444'
                series[k]['marker'] = {'radius':4, 'fillColor':'#444'}            
                   
        print("BUDGET: " + str(self.budget))
        print("STOCK_BUDGET: " + str(self.stock_budget))
        
        print("TOTAL_SLOPE: "+str(float(sum)/self.last_sum))
        #store sum in last_sum variable
        #series['0total'] = {"price":sum, 'color':'#555', 'marker': {'radius':4, 'fillColor':'#555'}}
        self.last_sum=sum
        
        series['budget'] = self.budget + self.stock_budget
        result['series'] = series
        self.v.execute_script("next(%s)" % json.dumps(result))
        self.cur_date += datetime.timedelta(days=config.DELTA)
        
    def set_data(self, date, budget):
        self.budget = budget
        self.cur_date = datetime.datetime.strptime(date, '%Y-%m-%d')
