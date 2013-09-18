import gtk, webkit
import json
import os
import urllib
from Trader import StockTrader
from Stock import Stock


w = gtk.Window()
v = webkit.WebView()
sw = gtk.ScrolledWindow()
w.add(sw)
sw.add(v)
w.set_size_request(1000,800)
w.connect("destroy", lambda q: Gtk.main_quit())

def window_title_change(v, param):
    if not v.get_title():
        return
    if v.get_title():
	
        message = v.get_title().split("::",1)[1]
	a=Stock(message)
	b=StockTrader(a)	
	b.learn()
	b.trade(10000)
        # Now, send a message back to JavaScript
        return_message = open('data.js','r').read()
        v.execute_script("jscallback(%s)" % json.dumps(return_message))

v.connect("notify::title", window_title_change)
file = os.path.abspath('index1.htm')
uri = 'file://' + urllib.pathname2url(file)
v.load_uri(uri)
w.show_all()
gtk.main()
