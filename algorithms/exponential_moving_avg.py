from yapsy.IPlugin import IPlugin

class ExponentialMovingAVG(IPlugin):
    def __init__(self):
        self.probability = 0.5
        self.decision = 0
        self.decision_history = []
        self.history = []
        self.border = 0
        self.values = []
        self.value_history = []
        self.valuesSize = 10
    
    def exponential_average(self, values, cnt, alpha):
        if cnt>1:
            return alpha*values[cnt-1]+(1-alpha)*self.exponential_average(values, cnt-1, alpha)
        else:
            return values[cnt-1]
    
    def calc(self, data):
        values = []
        history_object = {}
        
        self.updateValues(data)
        
        history_object['average'] = self.exponential_average(self.values, len(self.values), float(2)/(len(self.values)+1))
        history_object['last_value'] = data[len(data)-1]['close']
        
        if len(self.history) != 0:
            last_history_object = self.history[len(self.history)-1]
            if last_history_object['last_value'] < data[len(data)-1]['close']:
                last_history_object['right_decision'] = 1
            else:
                last_history_object['right_decision'] = -1
                
            if last_history_object['right_decision'] == last_history_object['decision']:
                self.update_decision_history(1)
            else:
                self.update_decision_history(0)
            
            self.border = self.exponential_average(self.value_history, len(self.value_history), float(2)/(len(self.value_history)+1))
            self.probability = self.exponential_average(self.decision_history, len(self.decision_history), float(2)/(len(self.decision_history)+1))
                
        else:
            self.border = history_object['average']
        
        if history_object['average'] < self.border:
            history_object['decision'] = 1
        else:
            history_object['decision'] = -1
        
        #update histories
        self.history.append(history_object)
        self.update_value_history(history_object['average'])
        
        print("border: "+str(self.border))
        print("curravg: "+str(history_object['average']))
        print("ExpMovingAVG_decision: "+str(history_object['decision']))
        print("ExpMovingAVG_probability: "+str(self.probability))
        #print("last_val: "+str(history_object['last_value_old']))
        return history_object['decision'], self.probability
    
    def updateValues(self, data):
        for x in range(0, len(data)-1):
            if len(self.values) >= self.valuesSize:
                del self.values[0]
            self.values.append(data[x]['close'])
    
    def update_decision_history(self, value):
        if len(self.decision_history) >= self.valuesSize:
            del self.decision_history[0]
        self.decision_history.append(value)
        
    def update_value_history(self, value):
        if len(self.value_history) >= self.valuesSize:
            del self.value_history[0]
        self.value_history.append(value)