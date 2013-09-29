from yapsy.IPlugin import IPlugin
import math

class SimpleSlope(IPlugin):
    def __init__(self):
        self.probability = 0
        self.decision = 0
        self.history = []
        self.summand_init = 0.125
        self.summand = self.summand_init
    
    def calc(self, data):
        history_object = {"slope": 1}
        history_object['last_value'] = data[len(data)-1]['close']
        
        if len(self.history) != 0:
            last_history_object = self.history[len(self.history)-1]
            
            #setting slope
            print("FIRST: "+str(last_history_object['last_value'])) 
            print("LAST: "+str(history_object['last_value'])) 
            history_object['slope']=history_object['last_value']/last_history_object['last_value']-1
            
            if (history_object['slope'] > 0 and last_history_object['slope'] > 0) or (history_object['slope'] <= 0 and last_history_object['slope'] <= 0):
                self.summand *= 2
            else:
                self.summand = self.summand_init
            
        print("SLOPE: "+str(history_object['slope']))
        if history_object['slope'] < 0:
            self.decision = min(self.decision+self.summand, 1)
        else:
            self.decision = max(self.decision-self.summand, -1)
        
        history_object['decision']= 1 if self.decision > 0 else -1
        self.probability=math.fabs(self.decision)
        self.history.append(history_object)
        print("adv_slope_decision: "+str(history_object['decision']))
        print("adv_slope_probability: "+str(self.probability))
        #print("last_val: "+str(history_object['last_value']))
        return history_object['decision'], self.probability