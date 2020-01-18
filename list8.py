import matplotlib.pyplot as pyplot

def produce_diffusion(innovators_population, imitators_population, p, q, f, years, dt):
    time_list = []
    innovators_list = []
    imitators_list = []
    all_agents_list= []
    innovators_list2 = [0]
    imitators_list2 = [0]
    all_agents_list2 = [0]
    
    t = 0
    influenced_adopters_before = 0
    imitating_adopters_before = 0
    all_adopters_before = 0

    innovators_list.append(influenced_adopters_before)
    imitators_list.append(imitating_adopters_before)
    all_agents_list.append(all_adopters_before)
    time_list.append(t)
    
    for i in range(0, int(years / dt) + 1):
        newly_influenced = innovators_list[-1] + p * (1 - innovators_list[-1])  * dt + q * innovators_list[-1] * (1 - innovators_list[-1]) * dt   # differential equation for newly influenced agents
        innovators_list.append(newly_influenced)
        newly_imitated = imitators_list[-1] + p * (1 - imitators_list[-1]) * dt + f * q * innovators_list[-1] * (1 - imitators_list[-1]) * dt + (1 - f) * q * imitators_list[-1] * (1 - imitators_list[-1]) * dt    #differential equation for new imitators
        imitators_list.append(newly_imitated)
        
        t = t + dt
        time_list.append(t)
        
        total_new_influenced = (newly_influenced - influenced_adopters_before) / dt
        innovators_list2.append(total_new_influenced) #innovators_list for figure 2 is probably counted wrong :c
        
        total_new_imitated = (newly_imitated - imitating_adopters_before) / dt
        imitators_list2.append(total_new_imitated)
        
        total_new_adoptions = ((newly_influenced) + (newly_imitated))
        all_agents_list.append(total_new_adoptions)
        total_adoptions = (total_new_adoptions - all_adopters_before) / dt
        all_agents_list2.append(total_adoptions)

        influenced_adopters_before = newly_influenced
        imitating_adopters_before = newly_imitated
        all_adopters_before = total_new_adoptions
        
    for i in range(len(innovators_list)): # second loop to change fraction into percentage
        innovators_list[i] = innovators_list[i] * innovators_population
        innovators_list2[i] = innovators_list2[i] * innovators_population
        imitators_list[i] = imitators_list[i] * imitators_population
        imitators_list2[i] = imitators_list2[i] * imitators_population
        all_agents_list2[i] = innovators_list2[i] + imitators_list2[i]
        all_agents_list[i] = innovators_list[i] + imitators_list[i]
#        time_list - time for X axis
#        all_agents_list - list of all agents
#        innovators_list - list of rates of changes for the innovators
#        imitators_list - list of rates of changes for the imitators
#        lists with 2 are for figure 2
    return innovators_list, imitators_list, innovators_list2, imitators_list2, time_list, all_agents_list, all_agents_list2

def bass_diffusion_model(innovators_population, imitators_population, p, q, f, years, dt):
    
    innovators_list, imitators_list, innovators_list2, imitators_list2, time_list, all_agents_list, all_agents_list2 = produce_diffusion(innovators_population, imitators_population, p, q, f, years, dt)
    pyplot.figure(1)
    pyplot.plot(time_list, innovators_list, label = 'Innovators')
    pyplot.plot(time_list, imitators_list, label = 'Imitators')
    pyplot.plot(time_list, all_agents_list, label = 'Total')
    pyplot.legend()
    
    pyplot.figure(2)
    pyplot.plot(time_list, innovators_list2, label = 'Innovators')
    pyplot.plot(time_list, imitators_list2, label = 'Imitators')
    pyplot.plot(time_list, all_agents_list2, label = 'Total')
    pyplot.legend()
    pyplot.show()


if __name__ == "__main__":

#    Parameters:
#    innovators_population - population size of innovators
#    imitators_population - population size of imitators
#    p - the chance of the product adoption
#    q - interaction between adopters and non-adopters
#    f - the strength with which non-adopters impress adopters
#    years - number of years
#    dt - the quant of time
    bass_diffusion_model(600, 400, 0.03, 0.38, 0.6, 30, 0.01)
    
    