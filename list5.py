import sys
import random
import math
#import matplotlib.pyplot as plt
#import numpy as np
#from matplotlib import animation
#from copy import copy, deepcopy
#from operator import itemgetter

#if len(sys.argv) != 5:
#    print("Wrong arguments number")
#    quit()

L = sys.argv[1] # iteracje
speed_limit = sys.argv[2] # limit prędkosci
p = sys.argv[3] # szansa na hamowanie
q = sys.argv[4] # gestosc
size = 30 # rozmiar autostrady

class Car:
    
    def __init__(self, current_speed, max_speed, brake_chance):
        self.current_speed = current_speed
        self.max_speed = max_speed
        self.brake_chance = brake_chance

    def change_speed(self, new_speed):
        self.current_speed = new_speed
        
    def random_brake(self):
        brake = [True, False]
        if self.current_speed > 1 & random.choice(brake) == True:
            self.change_speed(self.current_speed - 1) 
    
    def get_current_speed(self):
        return self.current_speed
    
    def get_max_speed(self):
        return self.max_speed
    
    def to_string(self):
        return ('cs:\t' + str(self.current_speed) + '\tsl:\t' + str(self.max_speed) + '\tp:\t' + str(self.brake_chance))

class Freeway:
    
    freeway = []
    
    def __init__(self, size):
        self.size = size
        self.freeway = [None] * self.size # pusta autostrada o rozmiarze size
    
    def move_car(self, old_position, new_position, car_id):
        self.freeway[old_position] = None
        self.freeway[new_position] = car_id
        
    def get_freeway(self):
        return self.freeway
        
    def to_string(self):
        return ('size:\t' + str(self.size) + '\tlist:\t' + str(self.freeway))

class Simulation:
    
    simulation_matrix = []
    
    def __init__(self, iterations, cars_density):
        self.iterations = iterations
        self.cars_density = cars_density

    def start_simulation(self):
        cars = []
        f1 = Freeway(size)
        cars_number = math.floor(float(size) * float(q))
        for i in range(cars_number):
            cars.append(Car(0, speed_limit, p))
            f1.move_car(i, i, i)
#            print('car[' + str(i) + ']:\t' + cars[i].to_string())
#        print('freeway: ' + f1.to_string())

        for i in range(int(self.iterations)):
            speed_sum = 0.0
            for j in range(cars_number):
                speed_sum += cars[j].get_current_speed()
            speed_avg = speed_sum / float(cars_number)
            self.simulation_matrix.append([i] + f1.freeway + [speed_avg])
#            print(self.simulation_matrix)
            for field in f1.freeway:
                if field != None:
                    next_field_pointer = 1
                    while ((next_field_pointer + 1 <= int(cars[field].get_max_speed())) & (f1.freeway[field + next_field_pointer] == None)):
                        next_field_pointer += 1
                    cars[field].change_speed(next_field_pointer)
            pass
                    
        

            
s1 = Simulation(L, q)
s1.start_simulation()

## initialize algorithm parameter
#M = 100
#p = 0.3
#init_v = 0
#N = 10
#t_max = 100
#v_max = 5
#
## initialize cars
#random.seed(4)
#roads = np.array( [ [[0,M+0.5], [3,3]], [[0,M+0.5], [7,7]] ] )
#cars = np.array([[random.randint(1,M), 5] for i in range(1,N+1)])
#cars = np.array(sorted(cars, key=itemgetter(0)))
#
## main program
#v = init_v
#all_car_movement = []
#cars_order = [i for i in range(N)]
#new_cars_order = []
#print(cars_order)
#for t in range(t_max):
#    x_row = []
#    for i in cars_order:
#        car = cars[i]
#        next_car = cars[i+1 if i+1 < N else 0]
#        
#        # v pertama
#        v = np.min([v+1, v_max])
#        
#        # v kedua
#        if (next_car[0] < car[0]):
#            d = M - next_car[0]
#        else: 
#            d = (next_car[0]-car[0])
#        v = np.min([v, d-1])
#
#        # v ketiga
#        prob = random.rand()
#        if (prob < p):
#            v = np.max([0, v-1])
#        
#        # update nilai x
#        x = copy(car[0])
#        x = x + v
#        if (x >= M):
#            temp = []
#            for i in range(N):
#                order = cars_order[i] + N-1
#                if (order + N-1 > N):
#                    order = order - N
#                temp.append(order)
#            cars_order = deepcopy(temp)
#            x = x - M
#        x_row.append(copy([x,car[1]]))
#
#    cars = deepcopy(x_row)
#    all_car_movement.append(deepcopy(x_row))
#
## animating
#fig = plt.figure()
#ax = plt.axes(ylim=(0,10), xlim=(0,M+0.5))
#for road in roads:
#    plt.plot(road[0], road[1], c="black")
#car_marker = ax.scatter([], [], s=75, marker="s")
#
#def animate(i):
#    cars_position = all_car_movement[i]
#    car_marker.set_offsets(cars_position)
#    return car_marker
#
#anim = animation.FuncAnimation(fig, animate, frames=len(all_car_movement), interval=50)
#plt.show()
