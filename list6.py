import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


class Swarm:
    def __init__(self, sizeOfFlock, xAxis, yAxis):
        self.sizeOfFlock = sizeOfFlock  # For calculating averages
        self.bounds = [xAxis, yAxis]
        self.list = []
        temp_pos = np.random.randint(yAxis[0], yAxis[1], size=(sizeOfFlock, 2))
        temp_vel = np.random.randint(-1, 1, size=(sizeOfFlock, 2))

        # By using numpy arrays we can use simple x + y operators,
        # instead of np.add(x,y). Makes code more readable.

        for i in range(1, sizeOfFlock):
            self.list.append(
                Boid(temp_pos[i], temp_vel[i], self))

    def updateSwarm(self):
        for boid in self.list:
            # Three main rules
            v1 = boid.rule1_separation()  # separation, avoiding collision
            v2 = boid.rule2_alignment()  # alignment, matching velocity
            v3 = boid.rule3_cohesion()  # cohesion, staying close to others
            # Extra rules
            v4 = boid.rule4_bounds()  # bounds, boid should stay inside visible boundaries

            boid.velocity = boid.velocity + v1 + v2 + v3 + v4
            # speed limit, no arbitarily fast speeds
            boid.limitVelocity()

            boid.position = boid.position + boid.velocity

        return

    def simplePrintSwarm(self):
        for boid in self.list:
            print(np.round(boid.position, 1), end='')
        print('')
        return


class Boid:
    def __init__(self, pos, vel, swarm):
        self.swarm = swarm
        self.position = pos
        self.velocity = vel

    def rule1_separation(self):
        correction = np.array([0, 0], dtype=np.float64)

        for boid in self.swarm.list:
            if boid != self:
                differenceMagnitude = np.linalg.norm(boid.position - self.position)

                if differenceMagnitude < 10:
                    correction = correction - (boid.position - self.position)

        return correction / 2

    def rule2_alignment(self):
        correction = np.array([0, 0], dtype=np.float64)

        for boid in self.swarm.list:
            if boid != self:
                correction = correction + boid.velocity

        correction = correction / (self.swarm.sizeOfFlock - 1)
        correction = (correction - self.velocity) / 10

        return correction

    def rule3_cohesion(self):
        correction = np.array([0, 0], dtype=np.float64)

        for boid in self.swarm.list:
            if boid != self:
                correction = correction + boid.position

        correction = correction / (self.swarm.sizeOfFlock - 1)
        correction = (correction - self.position) / 100

        return correction

    def rule4_bounds(self):
        correction = np.array([0, 0], dtype=np.float64)

        # Horizontal bounds
        if self.position[0] < self.swarm.bounds[0][0]:  # xmin
            correction[0] = 1
        elif self.position[0] > self.swarm.bounds[0][1]:  # xmax
            correction[0] = -1

        # Vertical bounds
        if self.position[1] < self.swarm.bounds[1][0]:  # ymin
            correction[1] = 1
        elif self.position[1] > self.swarm.bounds[1][1]:  # ymax
            correction[1] = -1

        return correction

    def limitVelocity(self):
        vlim = 5.0

        velMagnitude = np.linalg.norm(self.velocity)

        # Limit speed if necessary
        if velMagnitude > vlim:
            self.velocity = (self.velocity / velMagnitude) * vlim
            
X_LIM = [ 0, 1000 ]
Y_LIM = [ 0, 1000 ]
swarm = Swarm( 50, X_LIM, Y_LIM )

fig = plt.figure()
ax = plt.axes( xlim=X_LIM, ylim=Y_LIM )
graph, = ax.plot([], [], 'o')


def update(i) :
    #swarm.simplePrintSwarm()
    swarm.updateSwarm()

    boid_pos_x = []
    boid_pos_y = []
    
    #data_vel = []

    for boid in swarm.list :
        boid_pos_x.append( boid.position[0] )
        boid_pos_y.append( boid.position[1] )
        #data_vel.append( boid.velocity )
        
    graph.set_data(boid_pos_x, boid_pos_y)
    return graph


ani = animation.FuncAnimation(fig, update, frames=30, interval=10)

plt.show()

