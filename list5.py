import random
import math

iterations = 20 # iteracje
speed_limit = 3 # limit prędkosci
brake_chance = 0 # szansa na hamowanie
density = 0.3 # gestosc
size = 20 # rozmiar autostrady

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
#        if (self.current_speed > 0) & (random.random() <  self.brake_chance):
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
    
    def __init__(self, iterations, cars_density, size):
        self.iterations = iterations
        self.cars_density = cars_density
        self.size = size
        self.freeway = [None] * self.size
        self.cars_number = 0
    
    def init_cars(self):
        self.cars_number = math.floor(self.size * self.cars_density)
        for i in range(self.cars_number):
            self.freeway[i] = Car(0, speed_limit, brake_chance)
    
    def car_motion(self):
        iterator = 0
        for field in self.freeway:
            if field != None:
                next_pointer = 1
                while (self.freeway[(iterator + next_pointer) % self.size] == None) & (next_pointer <= self.freeway[iterator].get_max_speed()):
                    next_pointer += 1
                distance = next_pointer - 1
                if distance == 0 & self.freeway[iterator].get_current_speed() == 0:
                    pass
                #Jeżeli odległość < obecna prędkość ORAZ obecna prędkość > 0 to zwolnij do prędkości == odległość
                elif distance < self.freeway[iterator].get_current_speed() & self.freeway[iterator].get_current_speed() > 0:
                    self.freeway[iterator].change_speed(distance)
                #Jeżeli obecna prędkość > 0 i wylosowano losowe hamowanie to zwolnij o 1
#                elif self.freeway[iterator].get_current_speed() > 0 & (random.random() < self.freeway[iterator].brake_chance):
#                    self.freeway[iterator].change_speed(self.freeway[iterator].current_speed - 1)
                #Jeżeli odległość > obecna prędkość ORAZ obecna prędkość < Vmax to przyspiesz o 1
                elif distance > self.freeway[iterator].get_current_speed() & self.freeway[iterator].get_current_speed() < self.freeway[iterator].get_max_speed():
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
        for index in range(self.iterations):
            self.car_motion()
            #5. Obliczyć średnią prędkość na  autostradzie
            speed_sum = 0.0
            for i in range(self.size):
                if self.freeway[i] != None:
                    speed_sum += self.freeway[i].get_current_speed()
            speed_avg = round((speed_sum / float(self.cars_number)), 3)
            #6. Na matrycę wrzuć [obecną iterację + stan autostrady (None będzie zapisywany jako 0, obiekt samochód jako 1 + średnia prędkość) 
            freeway_state = []
            for i in range(self.size):
                if self.freeway[i] != None:
                    freeway_state.append(1)
                else:
                    freeway_state.append(0)
            self.simulation_matrix.append([index] + freeway_state + [speed_avg])
        for i in range(len(self.simulation_matrix)):
            print(self.simulation_matrix[i])
    
sim1 = FreewaySim(iterations, density, size)
sim1.init_cars()
sim1.start_simulation()

#class FreewaySim:
#    
#    simulation_matrix = []
#    freeway = []
#    freeway_state = []
#    
#    def __init__(self, iterations, cars_density, size):
#        self.iterations = iterations
#        self.cars_density = cars_density
#        self.size = size
#
#    def start_simulation(self):
#        cars_number = math.floor(float(size) * float(q))
#        for i in range(cars_number):
#            self.freeway.append(Car(0, speed_limit, p, i))
#            self.freeway_state.append(1)
#
#        for i in range(cars_number, size):
#            self.freeway.append(0)
#            self.freeway_state.append(0)
#
#        for i in range(int(self.iterations)):
#            position = 0
#            for field in self.freeway:
#                if field != 0:
#                    next_field_pointer = 1
#                    while ((next_field_pointer < self.freeway[position].get_max_speed()) & (self.freeway[(position + next_field_pointer) % size] == 0)):
#                        next_field_pointer += 1
#                    if (self.freeway[position].get_current_speed() > 0) & (next_field_pointer < self.freeway[position].get_current_speed()):
#                        self.freeway[position].decrease_speed()
#                    elif (self.freeway[position].get_current_speed() < self.freeway[position].get_max_speed()) & (next_field_pointer > self.freeway[position].get_current_speed()):
#                        self.freeway[position].increase_speed()
#                    else:
#                        pass
#                position += 1
#                
#            speed_sum = 0.0
#            for j in range(cars_number):
#                if self.freeway[j] != 0:
#                    speed_sum += self.freeway[j].get_current_speed()
#            speed_avg = round((speed_sum / float(cars_number)), 2)
#
#            temp_freeway = [0] * self.size
#            position = 0
#            for field in self.freeway:
#                if field != 0:
#                    self.freeway_state[position] = 1
#                    if field.get_current_speed() > 0:
#                        temp_freeway[(position + field.get_current_speed()) % self.size] = field
#                else:
#                    self.freeway_state[position] = 0
#                position += 1
#            self.freeway = temp_freeway
#            self.simulation_matrix.append([i] + self.freeway_state + [speed_avg])
#                
#        for i in range(len(self.simulation_matrix)):            
#            print(self.simulation_matrix[i])        
#            
#s1 = FreewaySim(L, q, size)
#s1.start_simulation()
