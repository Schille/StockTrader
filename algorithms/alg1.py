from yapsy.IPlugin import IPlugin

class Algorithm1(IPlugin):
    def __init__(self):
        self.probability = 0.5
        self.rightDecision = 0
        self.decision = 0
        self.history = []
        self.upper_border = 0
        self.lower_border = 0
    
    def average(self, values):
        if len(values) == 0:
            return 0
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
        
        if len(self.history) != 0:
            last_history_object = self.history[len(self.history)-1]
            if last_history_object['last_value_new'] < data[len(data)-1]['close']:
                last_history_object['right_decision'] = 1
            elif last_history_object['last_value_new'] > data[len(data)-1]['close']:
                last_history_object['right_decision'] = -1
            else:
                last_history_object['right_decision'] = 0
                
        pos_growth_list = []
        neg_growth_list = []
        for x in range (0, len(self.history)-1):
            if last_history_object['right_decision'] == last_history_object['decision']:
                if last_history_object['right_decision'] == 1:
                    pos_growth_list.append(last_history_object['growth'])
                elif last_history_object['right_decision'] == -1:
                    neg_growth_list.append(last_history_object['growth'])
        
        self.upper_border = self.average(pos_growth_list)
        self.lower_border = self.average(neg_growth_list)
        
        values = []
        history_object = {}
        
        
        
        for x in range(0, len(data)-1):
            values.insert(x+1,data[x]['close']) 
        history_object['last_value_old'] = data[len(data)-1]['close']
        m = self.linearGrowth(values)
        history_object['growth'] = m
        
        if m > self.upper_border:
            history_object['decision'] = 1
        elif m < self.lower_border:
            history_object['decision'] = -1
        else: 
            history_object['decision'] = 0
        
        self.history.append(history_object)
        
        return history_object['decision']