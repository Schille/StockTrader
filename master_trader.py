from gi.repository import Gtk, WebKit
import json
import os
import urllib
from Trader import StockTrader
from Stock import Stock
import config
import datetime

def show_window():
    w = Gtk.Window()
    v = WebKit.WebView()
    sw = Gtk.ScrolledWindow()
    w.add(sw)
    sw.add(v)
    w.set_size_request(1000, 800)
    w.connect("destroy", lambda q: Gtk.main_quit())
    
    v.connect("notify::title", window_title_change)
    file = os.path.abspath('index1.htm')
    uri = 'file://' + urllib.pathname2url(file)
    v.load_uri(uri)
    w.show_all()
    Gtk.main()

# list of StockTraders
stock_traders = {}
budget = 10000
stock_budget = 0
cur_date = datetime.datetime.strptime('2012-01-01', '%Y-%m-%d')

def window_title_change(v, param):
    if not v.get_title():
        return
    if v.get_title():
        func = v.get_title().split("::", 1)[0]
        param = v.get_title().split("::", 1)[1]
    
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
    
def add_stock(symbol):
    try:
        stock = Stock(symbol)
    except undefined_symbol:
        v.execute_script("add_stock(%s)" % "")
        
    stock_trader = StockTrader(stock)
    stock_trader.learn(config.DELTA, self.cur_date - datetime.timedelta(config.DELTA))
    self.stock_traders[symbol] = {'symbol':symbol,'trader':stock_trader, 'stock_cnt':0}
    
    # Now, send a message back to JavaScript
    v.execute_script("add_stock(%s)" % symbol)
    
def rm_stock(symbol):
    if self.stock_traders.has_key(symbol):
        del self.stock_traders[symbol]
        v.execute_script("rm_stock(%s)" % symbol)
    else:
        v.execute_script("rm_stock(%s)" % "")
    
def next():
    self.stock_budget=0
    buy_stocks = []
    decision_sum = 0
    result = {'date':int(self.cur_date.strftime('%s')) * 1000}
    # setting decisions and prices
    series = {}
    for k in self.stock_traders.keys():
        series[k] = {}
        self.stock_traders[k]['decision'], self.stock_traders[k]['price'] = self.stock_traders[k]['trader'].trade(self.cur_date)
        series[k]['price'] = self.stock_traders[k]['price']
        if self.stock_traders[k]['decision'] > 0:
            series[k]['color']='#0F0'
            self.budget += self.stock_traders[k]['price'] * self.stock_traders[k]['stock_cnt']
            self.stock_traders[k]['stock_cnt'] = 0
            buy_stocks.append(self.stock_traders[k])
            decision_sum += self.stock_traders[k]['decision']
        else:
            series[k]['color']='#F00'
            count_sell = math.floor(self.stock_traders[k]['stock_cnt'] * math.fabs(decision))
            if count_sell == 0:
                series[k]['marker']={'radius':3, 'fillColor':'#D99'}
            else:
                series[k]['marker']={'radius':4, 'fillColor':'#E33'}
            self.budget += self.stock_traders[k]['price'] * count_sell
            self.stock_traders[k]['stock_cnt'] -= count_sell
            self.stock_budget+=self.stock_traders[k]['stock_cnt']*self.stock_traders[k]['price']
        
    for stock in buy_stocks:
        count_buy = math.floor((self.budget * (stock['decision'] / decision_sum)) / stock['price'])
        if count_buy == 0:
            series[stock['symbol']]['marker']={'radius':3, 'fillColor':'#9D9'}
        else:
            series[stock['symbol']]['marker']={'radius':4, 'fillColor':'#00bd1f'}
        self.budget -= count_buy * stock['price']
        stock['stock_cnt'] = count_buy
        self.stock_budget+=stock['stock_cnt']*stock['price']
    
    series['budget'] = self.budget+self.stock_budget
    result['series'] = series
    v.execute_script("next(%s)" % json.dumps(result))
    self.date += datetime.timedelta(config.DELTA)
    
def set_data(date, budget):
    self.budget = budget
    self.cur_date = datetime.datetime.strptime(date, '%Y-%m-%d')
