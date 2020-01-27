import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def agent_bass_diff(p, q, M, T):
    adopters = list()
    x = np.zeros((M,), np.float32)
    x_tmp = np.zeros((M,), np.float32)
    for j in range(T):
        for i in range(1,M):
            prob = (p + q * (sum(x) / M)) * (1 - x[i])
            if np.random.uniform(0,1,1) <= prob:
                x_tmp[i] = 1
        x = x_tmp
        adopters.append(sum(x))
    return adopters

if __name__ == "__main__":
    simulation = [agent_bass_diff(0.03, 0.38, 1000, 25) for _ in range(25)]
    df = pd.DataFrame(np.array(simulation))
    df = df.transpose()
    
    df['time'] = range(1,26)
    column_list = df.columns.tolist()
    column_list = column_list[-1:] + column_list[:-1]
    df = df[column_list]
    
    a = df.columns[range(1,26)]
    b = ['sim ' + str(i) for i in range(1, len(a) + 1)]
    d = dict(zip(a, b))
    df = df.rename(columns = d)
    
    for column in df.drop('time', axis=1):
        plt.plot(df['time'], df[column], marker='.', label = column)
    
    plt.title("Agent Based Bass Diffusion Model")
    plt.xlabel("Time")
    plt.ylabel("Adopters")
    

#####################################################################################################################################################################################

#import random as rnd
#import matplotlib.pyplot as plt
#import networkx as nx
#import numpy as np
#
#
#def bass_diff(g0, p, q, f, epsilon):
##    p - the chance of the product adoption
##    q - interaction between adopters and non-adopters
##    f - the strength with which non-adopters impress adopters
#
#    innov  =[]
#    imit = []
#    all_agents = []
#    coninnov = []
#    conimit = []
#    conall = []
#    list_of_average_con_innov = []
#    list_of_average_con_imit = []
#    list_of_all_agents = []
#    time = []
#    number_of_nodes = len(g0.nodes())
#    
#    # dictionary for each node's decision
#    labels = {}
#    
#    for h in range(number_of_nodes):
#        #to start: assigning each node a decision 1 (positive)
#        labels[h] = 1   
#    for j in range(16):
#        for i in range(100): 
#            # spinson drawing
#            spinson = rnd.randint(0, number_of_nodes - 1)
#            # if r1 < p - node is independent
#            r1 = rnd.random()
#            if r1 < p: 
#                # changing of decision to the opposite with probability f
#                # !!!NIE WIEM CZY TO MA ZOSTAC!!!
#                r2 = rnd.random()
#                if r2 < f:
#                    labels[spinson] = (-1) * labels[spinson]
#            else:
#                # czyli zamiast tego bedzie po prostu parametr q brany pod uwage... CHYBA???
#                r3 = rnd.random()
#                if r3 < q:
#                    #if the node has 5 neighbors, take them all, if more - draw 5 neighbors
#                    neighbor = list(g0.neighbors(spinson))
#                    if len(neighbor) < 5:
#                        chosen = neighbor
#                    else:
#                        chosen = np.random.choice(neighbor, 5, replace=False)
#                    list_of_decision = []
#                    for k in range(len(chosen)):
#                        list_of_decision.append(labels[chosen[k]])
#                        
#                    #if the decision is unanimous and different than mine, change nodes decision
#                    if min(list_of_decision) == max(list_of_decision):
#                        labels[spinson] = min(list_of_decision)
#                    else:
#                        # if decision is the same as mine, I can change my mind anyway with prob = epsilon
#                        if rnd.random() < epsilon:
#                            labels[spinson] = (-1) * labels[spinson]
#
#            #list of nodes with a positive decision
#            innov = [k for k,v in labels.items() if v==1]
#            imit = [k for k,v in labels.items() if v==-1]
#            all_agents = [k for k,v in labels.items()]
#            
#            #concentartion
#            coninnov.append(len(innov)/number_of_nodes)
#            conimit.append(len(imit)/number_of_nodes) 
#            conall.append(len(all_agents)/number_of_nodes)
#            
#        time.append(j)    
#        list_of_average_con_innov.append(sum(coninnov))
#        list_of_average_con_imit.append(sum(conimit))
#        list_of_all_agents.append(sum(conall))
#        coninnov.clear()
#        conimit.clear()
#        conall.clear()
#    return time, list_of_all_agents, list_of_average_con_innov, list_of_average_con_imit
#
#
#if __name__ == "__main__":
#    Graph_C = nx.complete_graph(100)
#    #p = np.arange(0,1.05,0.05)
#    runs = []
#    #for prob in p:
#    time_list, all_agents_list, innovators_list, imitators_list = bass_diff(Graph_C, 0.03, 0.38, 0.6, 0)
#    #means=[]    
#    #for i in range(len(runs)):
#    #    means.append(sum(runs[i])/len(runs[i]))
#    plt.figure(1)
#    plt.plot(time_list, innovators_list, label = 'Innovators')
#    plt.plot(time_list, imitators_list, label = 'Imitators')
#    plt.plot(time_list, all_agents_list, label = 'Total')
        
#plt.plot(p, means, '.-', label = "q = 4")
#plt.legend()
#plt.xlabel("p")
#plt.ylabel("concentration")
#plt.title("Concentration graph depending on the parameter p for f = 0.5")


#####################################################################################################################################################################################

#import matplotlib.pyplot as pyplot
#
#def produce_diffusion(innovators_population, imitators_population, p, q, f, years, dt):
#    time_list = []
#    innovators_list = []
#    imitators_list = []
#    all_agents_list= []
#    innovators_list2 = [0]
#    imitators_list2 = [0]
#    all_agents_list2 = [0]
#    
#    t = 0
#    influenced_adopters_before = 0
#    imitating_adopters_before = 0
#    all_adopters_before = 0
#
#    innovators_list.append(influenced_adopters_before)
#    imitators_list.append(imitating_adopters_before)
#    all_agents_list.append(all_adopters_before)
#    time_list.append(t)
#    
#    for i in range(0, int(years / dt) + 1):
#        newly_influenced = innovators_list[-1] + p * (1 - innovators_list[-1])  * dt + q * innovators_list[-1] * (1 - innovators_list[-1]) * dt   # differential equation for newly influenced agents
#        innovators_list.append(newly_influenced)
#        newly_imitated = imitators_list[-1] + p * (1 - imitators_list[-1]) * dt + f * q * innovators_list[-1] * (1 - imitators_list[-1]) * dt + (1 - f) * q * imitators_list[-1] * (1 - imitators_list[-1]) * dt    #differential equation for new imitators
#        imitators_list.append(newly_imitated)
#        
#        t = t + dt
#        time_list.append(t)
#        
#        total_new_influenced = (newly_influenced - influenced_adopters_before) / dt
#        innovators_list2.append(total_new_influenced) #innovators_list for figure 2 is probably counted wrong :c
#        
#        total_new_imitated = (newly_imitated - imitating_adopters_before) / dt
#        imitators_list2.append(total_new_imitated)
#        
#        total_new_adoptions = ((newly_influenced) + (newly_imitated))
#        all_agents_list.append(total_new_adoptions)
#        total_adoptions = (total_new_adoptions - all_adopters_before) / dt
#        all_agents_list2.append(total_adoptions)
#
#        influenced_adopters_before = newly_influenced
#        imitating_adopters_before = newly_imitated
#        all_adopters_before = total_new_adoptions
#        
#    for i in range(len(innovators_list)): # second loop to change fraction into percentage
#        innovators_list[i] = innovators_list[i] * innovators_population
#        innovators_list2[i] = innovators_list2[i] * innovators_population
#        imitators_list[i] = imitators_list[i] * imitators_population
#        imitators_list2[i] = imitators_list2[i] * imitators_population
#        all_agents_list2[i] = innovators_list2[i] + imitators_list2[i]
#        all_agents_list[i] = innovators_list[i] + imitators_list[i]
##        time_list - time for X axis
##        all_agents_list - list of all agents
##        innovators_list - list of rates of changes for the innovators
##        imitators_list - list of rates of changes for the imitators
##        lists with 2 are for figure 2
#    return innovators_list, imitators_list, innovators_list2, imitators_list2, time_list, all_agents_list, all_agents_list2
#
#def bass_diffusion_model(innovators_population, imitators_population, p, q, f, years, dt):
#    
#    innovators_list, imitators_list, innovators_list2, imitators_list2, time_list, all_agents_list, all_agents_list2 = produce_diffusion(innovators_population, imitators_population, p, q, f, years, dt)
#    pyplot.figure(1)
#    pyplot.plot(time_list, innovators_list, label = 'Innovators')
#    pyplot.plot(time_list, imitators_list, label = 'Imitators')
#    pyplot.plot(time_list, all_agents_list, label = 'Total')
#    pyplot.legend()
#    
#    pyplot.figure(2)
#    pyplot.plot(time_list, innovators_list2, label = 'Innovators')
#    pyplot.plot(time_list, imitators_list2, label = 'Imitators')
#    pyplot.plot(time_list, all_agents_list2, label = 'Total')
#    pyplot.legend()
#    pyplot.show()
#
#
#if __name__ == "__main__":
#
##    Parameters:
##    innovators_population - population size of innovators
##    imitators_population - population size of imitators
##    p - the chance of the product adoption
##    q - interaction between adopters and non-adopters
##    f - the strength with which non-adopters impress adopters
##    years - number of years
##    dt - the quant of time
#    bass_diffusion_model(600, 400, 0.03, 0.38, 0.6, 30, 0.01)  