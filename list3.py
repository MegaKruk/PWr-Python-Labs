import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation


#main function for Conway's Game of Life
def lets_play(X):
    
    #size of grid (world)
    L = 50
    
    #if 1 - living cell, if 0 - dead cell
    live = 1
    dead = 0
    
    #creating matrix of zeros with a specific edge length
    world = np.zeros((L, L))
    
    #starting two ranges
    for i in range(L):
        for j in range(L):
            
            #bounadry conditions: closed torrus
            total = int((X[i, (j-1)%L] + X[i, (j+1)%L] + 
                         X[(i-1)%L, j] + X[(i+1)%L, j] + 
                         X[(i-1)%L, (j-1)%L] + X[(i-1)%L, (j+1)%L] + 
                         X[(i+1)%L, (j-1)%L] + X[(i+1)%L, (j+1)%L]))
            
            #rules of the game
            if X[i,j] == live:
                if total == 2 or total == 3:
                    world[i,j] = live
           
            if X[i, j] and not 2 <= total <= 3: 
                    world[i,j] = dead 
            elif total == 3: 
                    world[i,j] = live  
                    
    return world 




#getting the file with our grid
file = "oscylator.txt" #"4blinkers.txt", "glider.txt", "beacon.txt"

#I,J - give start corner (for exaple I= 10, J= 12 - it moves "dotted grid" to the middle)
I=0
J=0

#size of grid (world) (the same variable is in the lets_play() function)
L = 50 #70 #100

#interval for animation part
interval = 100

#how many iterations are made, it means with how many frames the gif is created
#but the animation displayed in python is looped
frames = 10

#----------------------------------------------------------------------------------------------------#

#reading a txt file with a character grid like:
#...oo.
#.o.o..
#.....o
#oo..o.

#opening file and changing characters:
#if '.' - change into 0 (dead)
#if 'o' - change into 1 (living)

#and saving a new file with zeros and ones (the file has the same name)
#NOTE: the file will be changed so you should have a copy of "the dotted file" in another folder

fin = open(file, "rt")
data = fin.read()
data = data.replace('.', '0')
data = data.replace('o', '1')
fin.close()
        
fin = open(file, "wt")
fin.write(data)
fin.close()

#transformations necessary to obtain the required matrix (list of lists)        
with open(file) as f:
    grid = []
    lines = [line.strip().split(',') for line in f]
    string_list = sum(lines, [])
    for i in string_list:
        correct_list = [int(digit) for digit in i]
        grid.append(correct_list)
        
                
#creating our initial world
X  = np.zeros((L, L))
rows= len(grid) # - how many rows
cols = len(grid[0]) # - how many columns

#defining the place that our grid should take in the whole world
X[I:I+rows, J:J+cols] = grid


#animation part
fig = plt.figure()
fig.add_subplot(111).set_axis_off()   
im = plt.imshow(X, cmap='binary')

def animate(i):
    im.set_data(animate.X)
    animate.X = lets_play(animate.X)

animate.X = X
anim = animation.FuncAnimation(fig, animate, interval=interval, frames=frames)
plt.show()

#saving gif
anim.save('my_gif.gif', writer=animation.ImageMagickFileWriter(fps=2))

    