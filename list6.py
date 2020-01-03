import numpy as np

class Boid():
    def __init__(self, x, y, vel, acc, max_acc, max_vel, perception_range, width, height):
        self.position = np.array([x, y])
        self.velocity = np.array([vel])
        self.acceleration = np.array([acc])
        self.max_acc = max_acc
        self.max_vel = max_vel
        self.perception_range = perception_range
        self.width = width
        self.height = height

    def update_self(self):
        self.position += self.velocity
        self.velocity += self.acceleration
        #limit
        if np.linalg.norm(self.velocity) > self.max_vel:
            self.velocity = self.velocity / np.linalg.norm(self.velocity) * self.max_vel
        self.acceleration = np.array([0, 0])

    def apply_rules(self, boids):
        alignment_ratio = self.alignment(boids)
        cohesion_ratio = self.cohesion(boids)
        separation_ratio = self.separation(boids)
        self.acceleration += [alignment_ratio, alignment_ratio]
        self.acceleration += [cohesion_ratio, cohesion_ratio]
        self.acceleration += [separation_ratio, separation_ratio]

    def edges(self):
        if self.position.x > self.width:
            self.position.x = 0
        elif self.position.x < 0:
            self.position.x = self.width

        if self.position.y > self.height:
            self.position.y = 0
        elif self.position.y < 0:
            self.position.y = self.height

    def alignment(self, boids):
        steering_vector = np.array([0, 0])
        average_vector = np.array([0, 0])
        total = 0
        for boid in boids:
            if np.linalg.norm(boid.position - self.position) < self.perception_range:
                average_vector += boid.velocity
                total += 1
        if total > 0:
            average_vector /= total
            average_vector = (average_vector / np.linalg.norm(average_vector)) * self.max_vel
            steering_vector = average_vector - self.velocity

        return steering_vector

    def cohesion(self, boids):
        steering_vector = np.array([0, 0])
        center_of_mass = np.array([0, 0])
        total = 0
        for boid in boids:
            if np.linalg.norm(boid.position - self.position) < self.perception_range:
                center_of_mass += boid.position
                total += 1
        if total > 0:
            center_of_mass /= total
            vec_to_com = center_of_mass - self.position
            if np.linalg.norm(vec_to_com) > 0:
                vec_to_com = (vec_to_com / np.linalg.norm(vec_to_com)) * self.max_vel
            steering_vector = vec_to_com - self.velocity
            if np.linalg.norm(steering_vector)> self.max_acc:
                steering_vector = (steering_vector /np.linalg.norm(steering_vector)) * self.max_acc
        return steering_vector

    def separation(self, boids):
        steering_vector = np.array([0, 0])
        average_vector = np.array([0, 0])
        total = 0
        for boid in boids:
            distance = np.linalg.norm(boid.position - self.position)
            if self.position != boid.position and distance < self.perception_range:
                diff = self.position - boid.position
                diff /= distance
                average_vector += diff
                total += 1
        if total > 0:
            average_vector /= total
            if np.linalg.norm(steering_vector) > 0:
                average_vector = (average_vector / np.linalg.norm(steering_vector)) * self.max_vel
            steering_vector = average_vector - self.velocity
            if np.linalg.norm(steering_vector) > self.max_acc:
                steering_vector = (steering_vector /np.linalg.norm(steering_vector)) * self.max_acc
        return steering_vector
    
    def __repr__(self):
        return str(self.__dict__)
        
# arguments: boids number, initial velocity X, initial velocity Y, initial acceleration X, initial acceleration Y, max acceleration, max velocity, perception range, field width, field height
class Simulation():
    def __init__(self, boids_number, vel, acc, max_acc, max_vel, perception_range, width, height):
        boids_list = []
        for i in range(boids_number):
            boids_list.append(Boid(i, i, vel, acc, max_acc, max_vel, perception_range, width, height))
            print(boids_list[i])

#np.random.seed(None)
sim = Simulation(20, ((np.random.rand(2) - 0.5)*10), ((np.random.rand(2) - 0.5)/2), 0.3, 5, 100, 1, 2)
