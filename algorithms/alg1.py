from yapsy.IPlugin import IPlugin

class Algorithm1(IPlugin):
    def print_name(self):
        print("This is the first algorithm")
        
    def calc(self, data):
        return 'bla', 123