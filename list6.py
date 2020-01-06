import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib.animation as animation


class boids_sim:
    def __init__(self, number_of_boids, width, height, velocity_limit, sight_range):
        self.number_of_boids = number_of_boids  # For calculating averages
        self.velocity_limit = velocity_limit
        self.sight_range = sight_range
        self.boundaries = [[0, width], [0, height]]
        self.list_of_boids = []
        rand_position = np.random.randint(0, height, size=(number_of_boids, 2))
        rand_velocity = np.random.randint(-1, 1, size=(number_of_boids, 2))
        for i in range(1, number_of_boids):
            self.list_of_boids.append(boid(rand_position[i], rand_velocity[i], velocity_limit, sight_range, self)) # list of boids

    def update_boids_sim(self):
        for boid in self.list_of_boids:
            #three main rules of Reynold's boids
            r1 = boid.separation()  #separation - avoiding collision with other boids
            r2 = boid.alignment()   #alignment - matching velocity with other boids
            r3 = boid.cohesion()    #cohesion - staying close to with other boids
            #fourth rule so boids won't "fall off"           
            r4 = boid.boundaries()
            #apply rules
            boid.velocity = boid.velocity + r1 + r2 + r3 + r4
            #velocity limit
            boid.limit_velocity()
            #update boid position
            boid.position = boid.position + boid.velocity


class boid:
    def __init__(self, position, velocity, velocity_limit, sight_range, boids_sim):
        self.position = position
        self.velocity = velocity
        self.velocity_limit = velocity_limit
        self.sight_range = sight_range
        self.boids_sim = boids_sim

    def separation(self):
        course_correction = np.array([0, 0], dtype=np.float64)
        for boid in self.boids_sim.list_of_boids:
            if boid != self:
                difference_magnitude = np.linalg.norm(boid.position - self.position)
                if difference_magnitude < 10:
                    course_correction = course_correction - (boid.position - self.position)
        return course_correction / 2

    def alignment(self):
        course_correction = np.array([0, 0], dtype=np.float64)
        for boid in self.boids_sim.list_of_boids:
            # if boid isn't myself and sqrt(((x2 - x1)^2) + (y2 - y1)^2)  is shorter than sight range
            if boid != self: #and math.sqrt((boid.position[0] - self.position[0])**2 + (boid.position[1] - self.position[1])**2) < self.sight_range:
                course_correction = course_correction + boid.velocity
        course_correction = course_correction / (self.boids_sim.number_of_boids - 1)
        course_correction = (course_correction - self.velocity) / 10
        return course_correction

    def cohesion(self):
        course_correction = np.array([0, 0], dtype=np.float64)
        for boid in self.boids_sim.list_of_boids:
            if boid != self: #and math.sqrt((boid.position[0] - self.position[0])**2 + (boid.position[1] - self.position[1])**2) < self.sight_range:
                course_correction = course_correction + boid.position
        course_correction = course_correction / (self.boids_sim.number_of_boids - 1)
        course_correction = (course_correction - self.position) / 100
        return course_correction

    def boundaries(self):
        course_correction = np.array([0, 0], dtype=np.float64)
        #horizontal boundaries
        if self.position[0] < self.boids_sim.boundaries[0][0]:      #xmin
#            course_correction[0] = 1
            self.position[0] = self.boids_sim.boundaries[0][1]
        elif self.position[0] > self.boids_sim.boundaries[0][1]:    #xmax
#            course_correction[0] = -1
            self.position[0] = self.boids_sim.boundaries[0][0]
        #vertical boundaries
        if self.position[1] < self.boids_sim.boundaries[1][0]:      #ymin
#            course_correction[1] = 1
            self.position[1] = self.boids_sim.boundaries[1][1]
        elif self.position[1] > self.boids_sim.boundaries[1][1]:    #ymax
#            course_correction[1] = -1
            self.position[1] = self.boids_sim.boundaries[1][0]
        return course_correction

    def limit_velocity(self):
        velocity_magnitude = np.linalg.norm(self.velocity)
        #limit velocity if necessary
        if velocity_magnitude > self.velocity_limit:
            self.velocity = (self.velocity / velocity_magnitude) * self.velocity_limit


def update(i) :
    boids_sim.update_boids_sim()
    boid_pos_x = []
    boid_pos_y = []
    for boid in boids_sim.list_of_boids :
        boid_pos_x.append( boid.position[0] )
        boid_pos_y.append( boid.position[1] )
    graph.set_data(boid_pos_x, boid_pos_y)
    return graph


boids_sim = boids_sim(60, 1000, 1000, 7.0, 40)  #main function. arguments: number of boids, width, height, velocity limit
fig = plt.figure()
axis = plt.axes(xlim=[0, 1000], ylim=[0, 1000])
graph, = axis.plot([], [], '.')
anim = animation.FuncAnimation(fig, update, frames=30, interval=10)

