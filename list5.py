import random
import math
import os
import imageio as io
import matplotlib.pylab as plt
from matplotlib.colors import ListedColormap

#iterations = 20 # iteracje
#speed_limit = 3 # limit prędkosci
#brake_chance = 0.1 # szansa na hamowanie
#density = 0.3 # gestosc
#size = 20 # rozmiar autostrady

#0. Stworzyć autostradę, która przechowuje samochód [obiekt] lub puste miejsce [None]
#1. Zainicjować autostradę samochodami tak, że ilość samochodów to gęstość * rozmiar autostrady. Samochód[i] będzie na autostrada[i]
#2. Sprawdzamy jaka jest odległość między tym a następnym samochodem (do momentu aż dojdziemy do Vmax). 
#3. Jeżeli odległość == 0 ORAZ obecna prędkość == 0 to nic nie rób
#LUB
#Jeżeli odległość < obecna prędkość ORAZ obecna prędkość > 0 to zwolnij do prędkości == odległość
#LUB
#Jeżeli obecna prędkość > 0 i wylosowano losowe hamowanie to zwolnij o 1
#LUB
#Jeżeli odległość > obecna prędkość ORAZ obecna prędkość < Vmax to przyspiesz o 1
#4. Stworzyć tymczasową autostradę (domyślnie pustą) i wrzucamy każdy samochód na nowe miejsce o indeksie [(stara pozycja + obecna prędkość) % rozmiar autostrady]
#5. Obliczyć średnią prędkość na  autostradzie
#6. Na matrycę wrzuć [obecną iterację + stan autostrady (None będzie zapisywany jako 0, obiekt samochód jako 1 + średnia prędkość) 
#7. Jak skończymy całą matrycę to animujemy


class Car:
    
    def __init__(self, current_speed, max_speed, brake_chance):
        self.current_speed = current_speed
        self.max_speed = max_speed
        self.brake_chance = brake_chance
        
    def change_speed(self, new_speed):
        self.current_speed = new_speed
        
#    def random_brake(self):
#        if (self.current_speed > 0) and (random.random() <  self.brake_chance):
#            self.change_speed(self.current_speed - 1) 
    
    def get_current_speed(self):
        return self.current_speed
    
    def get_max_speed(self):
        return self.max_speed
    
    def to_string(self):
        return ('cs:\t' + str(self.current_speed) + '\tsl:\t' + str(self.max_speed) + '\tp:\t' + str(self.brake_chance))
    
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
    
    def init_cars(self):
        self.cars_number = math.floor(self.size * self.cars_density)
        for i in range(self.cars_number):
            self.freeway[i] = Car(0, self.speed_limit, self.brake_chance)
    
    def car_motion(self):
        iterator = 0
        for field in self.freeway:
            if field != None:
                next_pointer = 1
                while (self.freeway[(iterator + next_pointer) % self.size] == None) and (next_pointer <= self.freeway[iterator].get_max_speed()):
                    next_pointer += 1
                distance = next_pointer - 1
                if distance == 0 and self.freeway[iterator].get_current_speed() == 0:
                    pass
                #Jeżeli odległość < obecna prędkość ORAZ obecna prędkość > 0 to zwolnij do prędkości == odległość
                elif distance < self.freeway[iterator].get_current_speed() and self.freeway[iterator].get_current_speed() > 0:
                    self.freeway[iterator].change_speed(distance)
                #Jeżeli obecna prędkość > 0 i wylosowano losowe hamowanie to zwolnij o 1
#                elif self.freeway[iterator].get_current_speed() > 0 and (random.random() < self.freeway[iterator].brake_chance):
#                    self.freeway[iterator].change_speed(self.freeway[iterator].current_speed - 1)
                #Jeżeli odległość > obecna prędkość ORAZ obecna prędkość < Vmax to przyspiesz o 1
                elif distance > self.freeway[iterator].get_current_speed() and self.freeway[iterator].get_current_speed() < self.freeway[iterator].get_max_speed():
                    if random.random() < self.freeway[iterator].brake_chance:
                        if self.freeway[iterator].get_current_speed() > 0:
                            self.freeway[iterator].change_speed(self.freeway[iterator].current_speed - 1)
                    else:
                        self.freeway[iterator].change_speed(self.freeway[iterator].get_current_speed() + 1) 
                else:
                    pass
#                print(self.freeway[iterator].get_current_speed())
            iterator += 1
        #4. Stworzyć tymczasową autostradę (domyślnie pustą) i wrzucamy każdy samochód na nowe miejsce o indeksie [(stara pozycja + obecna prędkość) % rozmiar autostrady]
        temp_freeway = [None] * self.size
        for i in range (self.size):
            if self.freeway[i] != None:
                temp_freeway[(i + self.freeway[i].get_current_speed()) % self.size] = self.freeway[i]
        self.freeway = temp_freeway

    def start_simulation(self):
        sum_of_speed_average = 0.0
        for index in range(self.iterations):
            self.car_motion()
            #5. Obliczyć średnią prędkość na  autostradzie
            speed_sum = 0.0
            for i in range(self.size):
                if self.freeway[i] != None:
                    speed_sum += self.freeway[i].get_current_speed()
            speed_avg = round((speed_sum / float(self.cars_number)), 3)
            sum_of_speed_average += speed_avg
            #6. Na matrycę wrzuć [obecną iterację + stan autostrady (None będzie zapisywany jako 0, obiekt samochód jako 1 + średnia prędkość) 
            freeway_state = []
            for i in range(self.size):
                if self.freeway[i] != None:
                    freeway_state.append(1)
                else:
                    freeway_state.append(0)
            self.simulation_matrix.append([index] + freeway_state + [speed_avg])
        AVG = sum_of_speed_average / float(self.iterations)
        for i in range(len(self.simulation_matrix)):
            print(self.simulation_matrix[i])
        return AVG
            
    def animate(self, directory='Images'): # co x sekund plotuje i-ty stan symulacji
        i = 0
        fig = plt.subplots()
        files = []
        for line in self.simulation_matrix:
             file_name = os.path.join(directory, str(i) + '.png')
             files.append(file_name)
             fig.savefig(file_name, dpi=100)
             i += 1
        
        with io.get_writer('animation.gif', mode='I', duration=0.3) as w:
            for file in files:
                w.append_data(io.imread(file))
        
            
#    def animate(states, directory='Images'):
#    segregation_colours = ListedColormap(['k', 'b', 'r'])
#    i = 0
#    fig, ax = plt.subplots()
#    ax.axis('off')
##    ax.set_xticks([])
##    ax.set_yticks([])
#    files = []
#    for state in states:
#        ax.clear()
#        ax.set_xticks([])
#        ax.set_yticks([])
#        ax.matshow(state, cmap=segregation_colours)
#        file_name = os.path.join(directory, str(i) + '.png')
#        files.append(file_name)
#        fig.savefig(file_name, dpi=100)
#        i += 1
#    with io.get_writer('animation.gif', mode='I', duration=0.3) as w:
#        for file in files:
#            w.append_data(io.imread(file))
        
sim1 = FreewaySim(50, 0.1, 0.1, 5, 40)  #iterations, cars_density, brake_chance, speed_limit, size  
sim1.init_cars()
AVG1 = sim1.start_simulation()
print(AVG1)
#sim1.animate()
