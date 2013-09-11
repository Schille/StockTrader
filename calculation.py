#
#    Calculation happen here!
#
#
#


def average(values):
    sum = 0
    for e in values:
        sum+=e
    average = sum/float(len(values))
    return average

def littleGauss(value):
    return (value**2 + value)/2

def linearGrowth(values):
    sumX = littleGauss(len(values))
    sumY = 0
    sumXY = 0
    sumXsquare = 0
    counter = 1
    for y in values:
        sumY += y
        sumXY += counter*y
        sumXsquare += counter**2
        counter+=1
    return (len(values)*sumXY-sumX*sumY)/(len(values)*sumXsquare-sumX**2)
