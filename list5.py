import random
from random import shuffle
import math
import numpy as np
import matplotlib.pylab as plt
import os
import imageio as io
from matplotlib.colors import ListedColormap

#iterations = 100
#speed_limit = 5
#brake_chance = 0.1 (probablity of slowing down)
#density = 0.3 (car density)
#size = 20

#class "Car", which stores the car object and its functionality
class Car:
    
    def __init__(self, current_speed, max_speed, brake_chance):
        self.current_speed = current_speed
        self.max_speed = max_speed
        self.brake_chance = brake_chance
        
    def change_speed(self, new_speed):
        self.current_speed = new_speed
           
    def get_current_speed(self):
        return self.current_speed
    
    def get_max_speed(self):
        return self.max_speed

#clas "FreewaySim", which stores car objects and empty spaces (Nones) 
class FreewaySim:
    
    simulation_matrix = []
    freeway = []
    
    def __init__(self, iterations, cars_density, brake_chance, speed_limit, size):
        self.iterations = iterations
        self.cars_density = cars_density
        self.brake_chance = brake_chance
        self.speed_limit = speed_limit
        self.size = size
        self.freeway = [None] * self.size
        self.cars_number = 0
    
    #initiating the freeway with cars - the number of cars is the density * size of the freeway
    #car[i] is on the freeway[i]
    def init_cars(self):
        self.cars_number = math.floor(self.size * self.cars_density)
        for i in range(self.cars_number):
            self.freeway[i] = Car(0, self.speed_limit, self.brake_chance)
        shuffle(self.freeway)
            
    #we check the distance between one car and the next one (until we reach Vmax).
    def car_motion(self):
        iterator = 0
        for field in self.freeway:
            if field != None:
                next_pointer = 1
                while (self.freeway[(iterator + next_pointer) % self.size] == None) and (next_pointer <= self.freeway[iterator].get_max_speed()):
                    next_pointer += 1
                distance = next_pointer - 1
                
                #if distance = 0 and current speed = 0 then do nothing (case of "traffic jam")
                if distance == 0 and self.freeway[iterator].get_current_speed() == 0:
                    pass
                
                #if distance < current speed and current speed > 0 then slow down the car to speed = distance
                elif distance < self.freeway[iterator].get_current_speed() and self.freeway[iterator].get_current_speed() > 0:
                    self.freeway[iterator].change_speed(distance)
                    
                #if distance > current speed and current speed < Vmax
                elif distance > self.freeway[iterator].get_current_speed() and self.freeway[iterator].get_current_speed() < self.freeway[iterator].get_max_speed():
                    
                    #and if random slowing down was selected
                    if random.random() < self.freeway[iterator].brake_chance:
                        
                        #and if we are still driving
                        if self.freeway[iterator].get_current_speed() > 0:
                            
                            #slow down by 1
                            self.freeway[iterator].change_speed(self.freeway[iterator].current_speed - 1)
                            
                    #or speed up by 1       
                    else:
                        self.freeway[iterator].change_speed(self.freeway[iterator].get_current_speed() + 1) 
                else:
                    pass
            iterator += 1
            
        #creating a temporary freeway (empty -> Nones) and putting each car to a new place 
        #with the index [(old position + current speed) % freeway size]
        temp_freeway = [None] * self.size
        for i in range (self.size):
            if self.freeway[i] != None:
                temp_freeway[(i + self.freeway[i].get_current_speed()) % self.size] = self.freeway[i]
        self.freeway = temp_freeway

    def start_simulation(self):
        sum_of_speed_average = 0.0
        for index in range(self.iterations):
            self.car_motion()
            
            #calculating the average velocity on the freeway
            speed_sum = 0.0
            for i in range(self.size):
                if self.freeway[i] != None:
                    speed_sum += self.freeway[i].get_current_speed()
            speed_avg = round((speed_sum / float(self.cars_number)), 3)
            sum_of_speed_average += speed_avg
            
            #creating the matrix with:
            #- current iteration 
            #- current location of cars on the freeway (None = 0, car = 1) 
            #- average velocity
            freeway_state = []
            for i in range(self.size):
                if self.freeway[i] != None:
                    freeway_state.append(1)
                else:
                    freeway_state.append(0)
            self.simulation_matrix.append([index] + freeway_state + [speed_avg])
        #AVG = sum_of_speed_average / float(self.iterations)
        for i in range(len(self.simulation_matrix)):
            print(self.simulation_matrix[i])
        #return AVG
        return self.simulation_matrix
    
    #ODKOMENTOWAĆ AVG JAK ZROBIE GIFY I WYWALIĆ RETURN SELF...

#-----------------------------------------------------------------------------------            
def animate(states, directory='Images'):
    segregation_colours = ListedColormap(['w', 'k'])
    i = 0
    fig, ax = plt.subplots()
    fig.set_size_inches(40, 15)
    ax.axis('off')
    ax.set_xticks([])
    ax.set_yticks([])
    files = []
    for line in states:
        ax.clear()
        ax.set_xticks([])
        ax.set_yticks([])
        ax.matshow(line, cmap=segregation_colours)
        file_name = os.path.join(directory, str(i) + '.png')
        files.append(file_name)
        fig.savefig(file_name, dpi=100)
        i += 1
    with io.get_writer('animation.gif', mode='I', duration=0.2) as w:
        for file in files:
            w.append_data(io.imread(file))
        

#-------------------------------------------------------------------------------------------------
#iterations, cars_density, brake_chance, speed_limit, size          
sim1 = FreewaySim(200, 0.1, 0.35, 5, 100)
sim1.init_cars()
AVG1 = sim1.start_simulation()
#(AVG1)

for i in AVG1:
    del i[0]
    
for j in AVG1:
    del j[-1]

board=[]    
for k in range(len(AVG1)):
    board.append([])

for n in range(len(AVG1)):
     board[n].append(AVG1[n])  
     
ars=[]
for i in range(len(board)):
    ars.append(np.array(board[i]))

animate(ars)   
#-------------------------------------------------------------------------------------------------

#Exercise 2
        
#CarDensities = np.arange(0.1, 1, 0.05)
#
#Runs2 = []
#for q in CarDensities:
#    Runs2.append(FreewaySim(100, q, 0.2, 5, 100))    
#VelocityAverages2 = []    
#for a in range(len(Runs2)):
#    Runs2[a].init_cars()
#    VelocityAverages2.append(Runs2[a].start_simulation())
#    
#Runs5 = []
#for q in CarDensities:
#    Runs5.append(FreewaySim(100, q, 0.5, 5, 100))
#VelocityAverages5 = []    
#for a in range(len(Runs5)):
#    Runs5[a].init_cars()
#    VelocityAverages5.append(Runs5[a].start_simulation())
#    
#Runs7 = []
#for q in CarDensities:
#    Runs7.append(FreewaySim(100, q, 0.7, 5, 100))    
#VelocityAverages7 = []    
#for a in range(len(Runs7)):
#    Runs7[a].init_cars()
#    VelocityAverages7.append(Runs7[a].start_simulation())
#
#fig, ax = plt.subplots()    
#ax.plot(CarDensities, VelocityAverages2, '-b', label='p = 0.2')
#ax.plot(CarDensities, VelocityAverages5, '-r', label='p = 0.5')
#ax.plot(CarDensities, VelocityAverages7, '-g', label='p = 0.7') 
#ax.legend(loc='upper right', frameon=False)
#
#plt.title('Average velocity for probabilities of slowing down', fontsize=12)
#plt.xlabel('car density', fontsize=10)
#plt.ylabel('average velocity', fontsize=10)  
#fig

