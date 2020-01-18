import matplotlib.pyplot as pyplot

def productDiffusion2(inSize, imSize, p, q, f, years, dt):
    InList = []
    ImList = []
    totalList= []
    timeList = []
    
    influenced_adopters_Before= 0
    imitated_adopters_Before = 0
    total_adopters_Before = 0
    t = 0
    InList.append(influenced_adopters_Before)
    ImList.append(imitated_adopters_Before)
    totalList.append(total_adopters_Before)
    timeList.append(t)
    InList1 = [0]
    ImList1 = [0]
    totalList1 = [0]
    
    for i in range(0, int(years/dt)+1):
        newly_influenced = InList[-1] + p * (1 - InList[-1])  *dt + q * InList[-1] * (1 - InList[-1]) * dt   #differential equation for newly influenced agents
        InList.append(newly_influenced)
        newly_imitated = ImList[-1] + p * (1 - ImList[-1]) * dt + f * q * InList[-1] * (1 - ImList[-1])*dt + (1 - f) * q * ImList[-1] * (1 - ImList[-1]) * dt    #differential equation for new imitators
        ImList.append(newly_imitated)
        
        t = t + dt
        timeList.append(t)
        
        total_new_influenced = (newly_influenced - influenced_adopters_Before) / dt
        InList1.append(total_new_influenced)
        
        total_new_imitated = (newly_imitated - imitated_adopters_Before) / dt
        ImList1.append(total_new_imitated)
        
        total_new_adoptions = ((newly_influenced) + (newly_imitated))
        totalList.append(total_new_adoptions)
        total_adoptions = (total_new_adoptions - total_adopters_Before) / dt
        totalList1.append(total_adoptions)

        influenced_adopters_Before = newly_influenced
        imitated_adopters_Before = newly_imitated
        total_adopters_Before = total_new_adoptions
        
    for i in range(len(InList)): # second loop to change fraction into percentage
        InList[i] = InList[i] * inSize
        InList1[i] = InList1[i] * inSize
        ImList[i] = ImList[i] * imSize
        ImList1[i] = ImList1[i] * imSize
        totalList1[i] = InList1[i] + ImList1[i]
        totalList[i] = InList[i] + ImList[i]
    return InList, ImList, InList1, ImList1, timeList, totalList, totalList1
def main():
    
#    Parameters:
#        p - the chance of the product adoption
#        q - interaction between adopters and non-adopters
#        years - number of years
#        dt - the quant of time
#        inSize - population size of innovators
#        imSize - population size of imitators
#        f - the strength with which non-adopters impress adopters
#    Return Values:
#        timeList - time for X axis
#        aList - list of adopters
#        totalList - list of all agents
#        Inlist1 - list of rates of changes for the innovators
#        ImList1 - list of rates of changes for the imitators
    
    inSize = 600
    imSize = 400
    p = 0.03
    q = 0.38
    f = 0.6
    years = 30
    dt = 0.01
    InList, ImList, InList1, ImList1, timeList, totalList, totalList1 = productDiffusion2(inSize, imSize, p, q, f, years, dt)
    pyplot.figure(1)
    pyplot.plot(timeList, InList, label = 'Innovators')
    pyplot.plot(timeList, ImList, label = 'Imitators')
    pyplot.plot(timeList, totalList, label = 'Total')
    pyplot.legend()
    
    pyplot.figure(2)
    pyplot.plot(timeList, InList1, label = 'Innovators')
    pyplot.plot(timeList, ImList1, label = 'Imitators')
    pyplot.plot(timeList, totalList1, label = 'Total')
    pyplot.legend()
    pyplot.show()
    
main()