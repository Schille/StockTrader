from yapsy.IPlugin import IPlugin

class Algorithm1(IPlugin):
    def _init_(self):
        self.probability = 0.5
        self.rightDecision = 0
        self.decision = 0
        self.history = []
    
    def average(self, values):
        sum = 0
        for e in values:
            sum += e
        average = sum / float(len(values))
        return average
    
    def dataobject(self):
        return [{'close' : 1}, {'close' : 2}, {'close' : 3}, {'close' : 4}, {'close' : 5}, {'close' : 6}, {'close' : 7}
                , {'close' : 8}, {'close' : 9}, {'close' : 10}]
    
    def littleGauss(self, value):
        return (value ** 2 + value) / 2
    
    def linearGrowth(self, values):
        sumX = self.littleGauss(len(values))
        sumY = 0
        sumXY = 0
        sumXsquare = 0
        counter = 1
        for y in values:
            sumY += y
            sumXY += counter * y
            sumXsquare += counter ** 2
            counter += 1
        return (len(values) * sumXY - sumX * sumY) / (len(values) * sumXsquare - sumX ** 2)
    
    def calc(self, data):
        values = []
        for x in range(0, 9):
            values.insert(x,data[x]['close']) 
        m = self.linearGrowth(values)
        if m > 0:
            return 1, 0.5
        elif m < 0:
            return -1, 0.5
        return 0, 0.5
