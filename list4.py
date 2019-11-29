import numpy as np
import random
from itertools import product
import matplotlib.pylab as plt
from matplotlib.colors import ListedColormap
import imageio as io
import os


#segregation model function with given parameters
#neighbourhood_depth means how many neighbours we have
# 1 --> first layer --> 8 neighbours
# 2 --> second + first layer --> 24 neighbours, etc.

# N --> number of red agents and blue agents separately

# L --> size of lattice

def segregation_model(N = 30, L = 10, neighbourhood_depth = 1, ratio=0.5):    
    
    max_iter = 1000 #10000
    
    #creating our initial state
    state = np.array([0]*(L**2-2*N)+[1]*(N)+[2]*(N))
    np.random.shuffle(state)
    state = state.reshape((L, L))
    
    #creating list of neighbours for our cell
    cells_around = list(product(
            range(-neighbourhood_depth, neighbourhood_depth + 1),
            range(-neighbourhood_depth, neighbourhood_depth + 1)
    ))
    cells_around.remove((0, 0))
    
    #coordinates for all cells
    all_places = [(x, y) for x in range(L) for y in range(L)]
    
    all_states = [np.copy(state)]
    
    for step_counter in range(max_iter):
        
        #receiving coordinates for agents and empty places
        fulls = [position for position in all_places if state[position] != 0]
        emptys = [position for position in all_places if state[position] == 0]
        while fulls:
            
        # randomly selecting an agent
            agent = random.choice(fulls)
            x_agent, y_agent = agent
            neighbours = []
            for x_change, y_change in cells_around:
                
                #bounadry conditions: closed torrus
                neighbours.append( ((x_agent + x_change) % L, (y_agent + y_change) % L) )
                
                #checking if a neighbor is like us or another  
            similar = 0
            other = 0
            for neighbour in neighbours:
                if state[neighbour] == state[agent]:
                    similar += 1
                elif state[neighbour] != 0:
                    other += 1
                    
                # if neighbour is happy (counting ratio):
            if similar+other == 0 or similar / (similar + other) >= ratio:
                pass
                # if neighbour is unhappy:
            else:
                # take empty cell
                place_to_go = random.choice(emptys)
                
                # remove that cell from the emptys list
                emptys.remove(place_to_go)
                agent_type = state[agent]
                state[agent] = 0
                emptys.append(agent)
                state[place_to_go] = agent_type
            
            # remove agent from the fulls list
            fulls.remove(agent)
            
        # to stop the model
        all_states.append(np.copy(state))
        all_happy = True
        for position in all_places:
            if state[position] == 0:
                continue
            else:
                x_agent, y_agent = position
                neighbours = []
                for x_change, y_change in cells_around:
                    neighbours.append( ((x_agent + x_change) % L, (y_agent + y_change) % L) )
                    
                similar = 0
                other = 0
                for neighbour in neighbours:
                    if state[neighbour] == state[position]:
                        similar += 1
                    elif state[neighbour] != 0:
                        other += 1
                if similar+other == 0 or similar / (similar + other) >= ratio:
                    continue
                else:
                    all_happy = False
                    break
        if all_happy:
            break
       
    print('Number of iterations:')
    print(len(all_states))
    return all_states

# function for counting the segregation index
def calculate_sni(state, neighbourhood_depth = 1):
    
    L = state.shape[0]
    
    cells_around = list(product(
            range(-neighbourhood_depth, neighbourhood_depth + 1),
            range(-neighbourhood_depth, neighbourhood_depth + 1)
    ))
    cells_around.remove((0, 0))
    
    all_places = [(x, y) for x in range(L) for y in range(L)]
    agents = [position for position in all_places if state[position] != 0]
    
    neighbours_similarities = []
    
    for agent in agents:
        x_agent, y_agent = agent
        neighbours = []
        for x_change, y_change in cells_around:
            neighbours.append( ((x_agent + x_change) % L, (y_agent + y_change) % L) )
        similar = 0
        other = 0
        
        for neighbour in neighbours:
            if state[neighbour] == state[agent]:
                similar += 1
            elif state[neighbour] != 0:
                other += 1
        if similar + other != 0:
            sni = similar/(similar+other)
            neighbours_similarities.append(sni)
        else:
            pass
    
    return sum(neighbours_similarities) / len(neighbours_similarities)

# animation function
def animate(states, directory='Images'):
    segregation_colours = ListedColormap(['k', 'b', 'r'])
    i = 0
    fig, ax = plt.subplots()
    ax.axis('off')
#    ax.set_xticks([])
#    ax.set_yticks([])
    files = []
    for state in states:
        ax.clear()
        ax.set_xticks([])
        ax.set_yticks([])
        ax.matshow(state, cmap=segregation_colours)
        file_name = os.path.join(directory, str(i) + '.png')
        files.append(file_name)
        fig.savefig(file_name, dpi=100)
        i += 1
    with io.get_writer('animation.gif', mode='I', duration=0.3) as w:
        for file in files:
            w.append_data(io.imread(file))

#-------------------------------------------------------------------------------------------------------#
# Exercise 1
            
#Baseline model with N_blue = 2500 and N_red = 2500, neighbourhood_depth = 1 (it means 8 neigbours) 
#L = 100 and ratio = 0.5 
#run1 = segregation_model(2500, 100, 1, 0.5)
#run2 = segregation_model(3500, 100, 1, 0.5)
#run3 = segregation_model(4500, 100, 1, 0.5)            

#animate(run1)

#-------------------------------------------------------------------------------------------------------#
            
# Exercise 2
            
#segregation_colours = ListedColormap(['k', 'b', 'r'])
#initial = run1[0]
#final = run1[-1]
#plt.figure()
#plt.matshow(initial,cmap=segregation_colours)
#plt.title('Plot of initial distribution for N = 9000', fontsize=10)

#plt.figure()
#plt.matshow(final,cmap=segregation_colours)
#plt.title('Plot of final distribution for N = 9000', fontsize=10)

#-------------------------------------------------------------------------------------------------------#
            
# Exercise 3
            
#sizes = np.arange(250, 4000, 50)
#runs = []
#for s in sizes:
#    print(s)
#    runs.append(len(segregation_model(s, 100, 1, 0.5)))
#plt.plot(sizes, runs)
#plt.title('Number of iterations for population size', fontsize=12)
#plt.xlabel('population size', fontsize=10)
#plt.ylabel('number of iterations', fontsize=10)
#plt.show()

#-------------------------------------------------------------------------------------------------------#
            
# Exercise 4
            
#ratios = np.arange(0.1, 1, 0.1)
#new_snis=[]
#for r in ratios:
#    print(r)
#    run = segregation_model(2500, 100, 1, r)
#    new_snis.append(calculate_sni(run[-1], 1))
#plt.plot(ratios, new_snis)
#plt.title('Segregation index for the ratio', fontsize=12)
#plt.xlabel('ratio', fontsize=10)
#plt.ylabel('segregation index', fontsize=10)
#plt.show()

#-------------------------------------------------------------------------------------------------------#
            
# Exercise 5
            
#depths = range(1,6)
#my_depths=[]
#for d in depths:
#    run2 = segregation_model(4800, 100, d, 0.5)
#    my_depths.append(calculate_sni(run2[-1], d))
#plt.scatter(depths, my_depths)
#plt.title('Segregation index for the number of layers', fontsize=12)
#plt.xlabel('number of layers', fontsize=10)
#plt.ylabel('segregation index', fontsize=10)
#plt.show()

#-------------------------------------------------------------------------------------------------------#

# Exercise 6

#ratio1 = segregation_model(2500, 100, 1, 6/8)
#ratio2 = segregation_model(3500, 100, 1, 6/8)
#ratio3 = segregation_model(4500, 100, 1, 6/8)

#ratio4 = segregation_model(2500, 100, 1, 3/8)
#ratio5 = segregation_model(3500, 100, 1, 3/8)
#ratio6 = segregation_model(4500, 100, 1, 3/8)

#animate(ratio6)

#segregation_colours = ListedColormap(['k', 'b', 'r'])
#initial = ratio6[0]
#final = ratio6[-1]
#plt.figure()
#plt.matshow(initial,cmap=segregation_colours)
#plt.title('Plot of initial distribution for N = 9000', fontsize=10)

#plt.figure()
#plt.matshow(final,cmap=segregation_colours)
#plt.title('Plot of final distribution for N = 9000', fontsize=10)


