import random
import math

L = 10 # iteracje
speed_limit = 3 # limit prędkosci
p = 0.2 # szansa na hamowanie
q = 0.4 # gestosc
size = 20 # rozmiar autostrady

class Car:
    
    def __init__(self, current_speed, max_speed, brake_chance, position):
        self.current_speed = current_speed
        self.max_speed = max_speed
        self.brake_chance = brake_chance
    
    def increase_speed(self):
        self.current_speed += 1
        
    def decrease_speed(self):
        self.current_speed -= 1
        
    def random_brake(self):
        brake = [True, False]
        if self.current_speed > 1 & random.choice(brake) == True:
            self.decrease_speed() 
    
    def get_current_speed(self):
        return self.current_speed
    
    def get_max_speed(self):
        return self.max_speed
    
    def to_string(self):
        return ('cs:\t' + str(self.current_speed) + '\tsl:\t' + str(self.max_speed) + '\tp:\t' + str(self.brake_chance))

class FreewaySim:
    
    simulation_matrix = []
    freeway = []
    freeway_state = []
    
    def __init__(self, iterations, cars_density, size):
        self.iterations = iterations
        self.cars_density = cars_density
        self.size = size

    def start_simulation(self):
        cars_number = math.floor(float(size) * float(q))
        for i in range(cars_number):
            self.freeway.append(Car(0, speed_limit, p, i))
            self.freeway_state.append(1)

        for i in range(cars_number, size):
            self.freeway.append(0)
            self.freeway_state.append(0)

        for i in range(int(self.iterations)):
            position = 0
            for field in self.freeway:
                if field != 0:
                    next_field_pointer = 1
                    while ((next_field_pointer < self.freeway[position].get_max_speed()) & (self.freeway[(position + next_field_pointer) % size] == 0)):
                        next_field_pointer += 1
                    if (self.freeway[position].get_current_speed() > 0) & (next_field_pointer < self.freeway[position].get_current_speed()):
                        self.freeway[position].decrease_speed()
                    elif (self.freeway[position].get_current_speed() < self.freeway[position].get_max_speed()) & (next_field_pointer > self.freeway[position].get_current_speed()):
                        self.freeway[position].increase_speed()
                    else:
                        pass
                position += 1
                
            speed_sum = 0.0
            for j in range(cars_number):
                if self.freeway[j] != 0:
                    speed_sum += self.freeway[j].get_current_speed()
            speed_avg = round((speed_sum / float(cars_number)), 2)

            temp_freeway = [0] * self.size
            position = 0
            for field in self.freeway:
                if field != 0:
                    self.freeway_state[position] = 1
                    if field.get_current_speed() > 0:
                        temp_freeway[(position + field.get_current_speed()) % self.size] = field
                else:
                    self.freeway_state[position] = 0
                position += 1
            self.freeway = temp_freeway
            self.simulation_matrix.append([i] + self.freeway_state + [speed_avg])
                
        for i in range(len(self.simulation_matrix)):            
            print(self.simulation_matrix[i])        
            
s1 = FreewaySim(L, q, size)
s1.start_simulation()
