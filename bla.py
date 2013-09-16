from gi.repository import Gtk,WebKit
import json
import os
import urllib

w = Gtk.Window()
v = WebKit.WebView()
sw = Gtk.ScrolledWindow()
w.add(sw)
sw.add(v)
w.set_size_request(400,300)
w.connect("destroy", lambda q: Gtk.main_quit())
def window_title_change(v, param):
    if not v.get_title():
        return
    if v.get_title().startswith("msgtopython:::"):
        message = v.get_title().split(":::",1)[1]
        # Now, send a message back to JavaScript
        return_message = "You chose '%s'. How interesting." % message
        v.execute_script("jscallback(%s)" % json.dumps(return_message))
v.connect("notify::title", window_title_change)
file = os.path.abspath('index.htm')
uri = 'file://' + urllib.pathname2url(file)
v.load_uri(uri)
w.show_all()
Gtk.main()
