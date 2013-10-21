from yapsy.IPlugin import IPlugin
import math

class Curvature(IPlugin):
    def __init__(self):
        self.probability = 0.5
        self.rightDecision = 0
        self.decision = 0
        self.history = []
        self.counter = 0
        self.value_history = []
        self.history_size = 20
    
    def average(self, values):
        if len(values) == 0:
            return 0
        sum = 0
        for e in values:
            sum += e
        average = sum / float(len(values))
        return average
    
    def littleGauss(self, value):
        return (value ** 2 + value) / 2
    
    def linearGrowth(self, values):
        if (len(values) != 1):
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
        else:
            return 0
        
    def calc(self, data):
        self.update_value_history(data[-1]['close'])
        
        history_object = {}
        
        history_object['growth'] = self.linearGrowth(self.value_history)
        
        if history_object['growth'] > 0:
            
            if len(self.history)>0:
                if history_object['growth'] > self.history[-1]['growth']:
                    self.decision = max(self.decision-0.1, -1)
                else:
                    self.decision = max(self.decision-0.2, -1)
        else: 
            
            if len(self.history)>0:
                if history_object['growth'] > self.history[-1]['growth']:
                    self.decision = min(self.decision+0.2, 1)
                else:
                    self.decision = min(self.decision+0.1, 1)
        
        history_object['decision']= 1 if self.decision > 0 else -1
        self.probability=math.fabs(self.decision)
        
        #some prints
        print("curvature_growth: "+str(history_object['growth']))
        if len(self.history)>0:
            print("curvature_last_growth: "+str(self.history[-1]['growth']))
        print "curvature decision: " + str(history_object['decision'])
        print("curvature_probability: "+str(self.probability))
        
        self.history.append(history_object)
        return history_object['decision'], self.probability
    
    def update_value_history(self, value):
        if len(self.value_history) >= self.history_size:
            del self.value_history[0]
        self.value_history.append(value)
