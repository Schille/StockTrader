from yapsy.IPlugin import IPlugin
import math

class ExponentialMovingAVG(IPlugin):
    def __init__(self):
        self.probability = 0.5
        self.history = []
        self.border = 0
        self.value_history = []
        self.border_distance_history = []
        self.history_size = 50
    
    def exponential_average(self, values, cnt, alpha):
        if cnt>1:
            return alpha*values[cnt-1]+(1-alpha)*self.exponential_average(values, cnt-1, alpha)
        else:
            return values[cnt-1]
    
    def calc(self, data):
        history_object = {}
        
        history_object['last_value'] = data[len(data)-1]['close']
        
        if len(self.history) != 0:
            last_history_object = self.history[len(self.history)-1]

            self.update_border_distance_history(last_history_object['border_distance'])
            
            self.border = self.exponential_average(self.value_history, len(self.value_history), float(2)/(len(self.value_history)+1))
            
            if max(self.border_distance_history)-min(self.border_distance_history)>0:
                self.probability = (math.fabs(history_object['last_value']-self.border)-min(self.border_distance_history))/(max(self.border_distance_history)-min(self.border_distance_history))
                self.probability = max(min(self.probability, 1), 0)
            else:
                self.probability = 0.5
        else:
            self.border = history_object['last_value']
        
        history_object['border_distance']=math.fabs(history_object['last_value']-self.border)
        
        if history_object['last_value'] < self.border:
            history_object['decision'] = 1
        else:
            history_object['decision'] = -1
        
        #update histories
        self.history.append(history_object)
        self.update_value_history(history_object['last_value'])
        #print(str(self.border_distance_history))
        #print(str(self.value_history))
        #print("border: "+str(self.border))
        #print("last_value: "+str(history_object['last_value']))
        #print("border_distance: "+str(history_object['border_distance']))
        #if len(self.border_distance_history)>0:
            #print("border_distance_max: "+str(max(self.border_distance_history)))
            #print("border_distance_min: "+str(min(self.border_distance_history)))
        print("ExpMovingAVG_decision: "+str(history_object['decision']))
        print("ExpMovingAVG_probability: "+str(self.probability))
        return history_object['decision'], self.probability
    
    def update_border_distance_history(self, value):
        if len(self.border_distance_history) >= self.history_size/2:
            del self.border_distance_history[0]
        self.border_distance_history.append(value)
        
    def update_value_history(self, value):
        if len(self.value_history) >= self.history_size:
            del self.value_history[0]
        self.value_history.append(value)