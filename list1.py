import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from matplotlib import colors
from itertools import product
from scipy.ndimage.measurements import label
import collections

#color which are needed to use --> black as an empty ground, green - trees, red - burning tree, 
#grey - burnt tree
forest_colors = ['black','green','orangered', 'dimgrey']

#cells which are neigbors of our tree (cell) --> 8 other cells
cells_around = list(product([-1,0,1],[-1,0,1]))

#in fucntion burn(): if 1 - tree,if 2 - burning_tree, if 3 - burnt_tree, if 0 - empty ground
tree = 1
burning_tree = 2
burnt_tree = 3

#size of lattice
L = 20 #30, 50, 100

#loop size
M=10

#list of probabilities
probabilities = np.linspace(0.05, 0.95, num=50)

#main function for burning forest
def burn(X):
    
    #creating matrix of zeros with a specific edge length
    forest = np.zeros((L, L))

    #starting two ranges
    for i in range(L):
        for j in range(L):

            #if we have trees on first line of forest change them to the burning trees (FIRE)
            if X[1,i] == tree:
                forest[1,i] = burning_tree
                
            #change a fire into a burned tree
            if X[j,i] == burning_tree:
                forest[j,i] = burnt_tree
                
            #if our cell=burnt tree, we just leave burnt tree there    
            if X[j,i] == burnt_tree:
                forest[j,i] = burnt_tree
                
            #if our cell=tree, we just leave green tree there
            if X[j,i] == tree:
                forest[j,i] = tree
                
                #if a neighbor of our tree burns, our tree also begins to burn
                for step1,step2 in cells_around:
                    if X[j+step2, i+step1] == burning_tree:
                        forest[j,i] = burning_tree
                        break


    return forest

    
#function to print matrices of forest
def print_matrix(X):
    global_list = []
    global_list.append(burn(X))
    counter = 0
    while True:
        counter += 1
        new = burn(global_list[-1])
        last = global_list[-1]
        if np.array_equal(new, last):
            break
        else:
            global_list.append(new)
    #print("iterations: " + str(counter))
    return global_list


#function to find cluster
def find(Y):
    
    Y[Y != burnt_tree] = 0 #zeros if some trees have not been burnt
    labeled, clusters = label(Y)
    my_cluster = dict(collections.Counter(labeled.flatten()))
    del my_cluster[0] #delete cluster of zeros (empty cells)
    try:
        return max(my_cluster.values()) #return the biggest cluster
    except ValueError: #fixing problem when probability was to small to start the fire
        return 0

    

avg_probabilities = [] #empty list for average of probabilities
avg_biggest_cluster = [] #empty list for average of the biggest clusters
for p in probabilities:
    prob_list=[] #list for collecting 0 or 1 to calculate probability that fire hits opposite edge
    big_cluster=[] #list for clusters
    
    for _ in range(M):
        #initial afforestation
        #rand numbers in the matrix of zeros and if they are smaller than the given afforestation, 
        #then true (1) or false (0) -> our trees
        X  = np.zeros((L, L))
        X[1:L-1, 1:L-1] = np.random.random(size = (L-2, L-2)) < p
        data = print_matrix(X)
        row_end = data[-1][-2] #penultimate line from last printed matrix
        row_start = X[-2] #penultimate line from the initial forest matrix
        if np.array_equal(row_end, row_start): #check if they are the same
            prob_list.append(0)
        else:
            prob_list.append(1)
        #if the are the same it means that fire ended before last edge
        #if not it means that fire burnt some trees on the last edge
        big_cluster.append(find(data[-1]))   
            
    calc_prob = sum(prob_list)/M #calculate probability that fire hits opposite edge
    avg_probabilities.append(calc_prob)
    
    calc_cluster = sum(big_cluster)/M #calculate average of clusters
    avg_biggest_cluster.append(calc_cluster)

#plots
print(avg_probabilities)
plt.plot(probabilities, avg_probabilities)
plt.title('Probability that the fire hits the opposite edge with respect to p; L = 100', fontsize=12)
plt.xlabel('probabilities', fontsize=10)
plt.ylabel('average of probabilities', fontsize=10)

plt.figure()
print(avg_biggest_cluster)
plt.plot(probabilities,avg_biggest_cluster)
plt.title('Size of the biggest burnt cluster with respect to p; L = 100', fontsize=12)
plt.xlabel('probabilities', fontsize=10)
plt.ylabel('average of the biggest cluster', fontsize=10)

#part for making one animation 
X  = np.zeros((L, L))
X[1:L-1, 1:L-1] = np.random.random(size = (L-2, L-2)) < 0.5
data = print_matrix(X)
fig = plt.figure()
fig.add_subplot(111).set_axis_off()
im = plt.imshow(X, cmap=colors.ListedColormap(forest_colors), 
               norm=colors.BoundaryNorm(list(range(0, 5)), 
                colors.ListedColormap(forest_colors).N))

#making one fire animation
def animate(i):
    im.set_data(animate.X)
    animate.X = burn(animate.X)

animate.X = X
interval = 100
anim = animation.FuncAnimation(fig, animate, interval=interval)
plt.show()

anim.save('my_gif.gif', writer=animation.ImageMagickFileWriter(fps=2))
    
