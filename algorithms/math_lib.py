def exponential_average(self, values, cnt, alpha):
    if cnt>1:
        return self.exponential_average(values, cnt-1, alpha)+alpha*(values[cnt-1]-self.exponential_average(values, cnt-1, alpha))
    else:
        return alpha*values[cnt-1]