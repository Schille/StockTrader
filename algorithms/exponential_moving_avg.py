from yapsy.IPlugin import IPlugin

class ExponentialMovingAVG(IPlugin):
    def __init__(self):
        self.probabilityCounter=0
        self.probability = 0.5
        self.decision = 0
        self.history = []
        self.border = 0
    
    def exponential_average(self, values, cnt, alpha):
        if cnt>1:
            return self.exponential_average(values, cnt-1, alpha)+alpha*(values[cnt-1]-self.exponential_average(values, cnt-1, alpha))
        else:
            return alpha*values[cnt-1]
    
    def calc(self, data):
        
        values = []
        history_object = {}
        
        for x in range(0, len(data)-1):
            values.append(data[x]['close']) 
        history_object['average'] = self.exponential_average(values, len(values), float(2)/(len(values)+1))
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
        print("ExpMovingAVG_decision: "+str(history_object['decision']))
        print("ExpMovingAVG_probability: "+str(self.probability))
        #print("last_val: "+str(history_object['last_value_old']))
        return history_object['decision'], self.probability
