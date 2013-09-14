from yapsy.IPlugin import IPlugin

class SimpleAVG(IPlugin):
    def __init__(self):
        self.probabilityCounter=0
        self.probability = 0.5
        self.rightDecision = 0
        self.decision = 0
        self.history = []
        self.border = 0
    
    def weighted_average(self, values):
        if len(values) == 0:
            return 0
        sum = 0
        cnt = 0
        cntSum = 0
        for e in values:
            cnt+=1
            cntSum+=cnt
            sum += e*cnt
        average = float(sum)/cntSum 
        return average
    
    def calc(self, data):
        
        values = []
        historical_values= []
        history_object = {}
        
        for x in range(0, len(data)-1):
            values.insert(x+1,data[x]['close']) 
        history_object['average'] = self.weighted_average(values)
        history_object['last_value_old'] = data[len(data)-1]['close']
        
        if len(self.history) != 0:
            last_history_object = self.history[len(self.history)-1]
            if last_history_object['last_value_old'] < data[len(data)-1]['close']:
                last_history_object['right_decision'] = 1
            else:
                last_history_object['right_decision'] = -1
                
            if last_history_object['right_decision'] == last_history_object['decision']:
                self.probabilityCounter+=1
            else:
                self.border=(self.border+last_history_object['average'])/2
                
            self.probability = float(self.probabilityCounter)/len(self.history)      
                
        else:
            self.border = history_object['average']
        
        if history_object['average'] < self.border:
            history_object['decision'] = 1
        else:
            history_object['decision'] = -1
        
        self.history.append(history_object)
        #print("border: "+str(self.border))
        #print("curravg: "+str(history_object['average']))
        print("decision_wavg: "+str(history_object['decision']))
        print("weighted-probability: "+str(self.probability))
        #print("last_val: "+str(history_object['last_value_old']))
        return history_object['decision'], self.probability
