import math
import random
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation


class Agent:
    def __init__(self, base_x, base_y, target_x, target_y):
        """
        An independent agent within the swarm using an established set of rules to optimize its path through the env.

           :param base_x : X coordinate of the main hub where resources are collected.
           :param base_y : Y coordinate of the main hub where resources are collected.
           :param target_x : X coordinate of the destination target where resources are delivered.
           :param target_y : X coordinate of the destination target where resources are delivered.
        """

        self.location = np
        self.location_x = base_x
        self.location_y = base_y
        self.target_x = target_x
        self.target_y = target_y
        self.base_x = base_x
        self.base_y = base_y
        self.launched = False

        self.vector_x = random.uniform(-3.0, 3.0)
        self.vector_y = random.uniform(-3.0, 3.0)

        self.communication_range = 40
        self.max_comm_links = 30
        self.resource = 100

        self.random_weight = .1
        self.destination_weight = .6
        self.alignment_weight = .5
        self.attraction_weight = .5
        self.velocity = 0
        self.max_velocity = 0

    def exec_swarm_algorithm(self, swarm, threats):

        # Initializing vectors to be used later.
        vector_destination_x = 0
        vector_destination_y = 0
        vector_attraction_x = 0
        vector_attraction_y = 0
        vector_alignment_x = 0
        vector_alignment_y = 0
        vector_random_x = random.randrange(-100, 100)
        vector_random_y = random.randrange(-100, 100)

        # Reached the target and drop off resources.
        vector_target_x = self.target_x - self.location_x
        vector_target_y = self.target_y - self.location_y
        vector_base_x = self.base_x - self.location_x
        vector_base_y = self.base_y - self.location_y

        # If reached target it drops of resources.
        if abs(self.target_x - self.location_x) < 5 and abs(
                self.target_y - self.location_y) < 5 and self.resource == 100:
            self.resource = 0

        # If returned to base it picks up new resources.
        if abs(self.base_x - self.location_x) < 5 and abs(self.base_y - self.location_y) < 5 and self.resource == 0:
            self.resource = 100

        # If has resources goes to target.
        if self.resource == 100:
            vector_destination_x = vector_target_x
            vector_destination_y = vector_target_y

        # If drop off complete returns to base for more resources.
        if self.resource == 0:
            vector_destination_x = vector_base_x
            vector_destination_y = vector_base_y

        # If within range of a threat sets velocity to minimum.
        self.velocity = self.max_velocity
        for threat in threats:
            if abs(self.location_x - threat.location_x) < 20 and abs(self.location_y - threat.location_y) < 20:
                self.velocity = min(self.max_velocity, 1)

        # For each agent in range determines if it is close enough to communicate.
        agents_in_range = 0

        for agent in swarm:
            if agents_in_range < self.max_comm_links:

                # If it is close enough to communicate.
                if abs(agent.location_x - self.location_x) < self.communication_range and abs(
                        agent.location_y - self.location_y) < self.communication_range:
                    agents_in_range = agents_in_range + 1

                    if agent.velocity < agent.max_velocity and agent.launched:
                        vector_attraction_x = vector_attraction_x + self.location_x - agent.location_x
                        vector_attraction_y = vector_attraction_y + self.location_y - agent.location_y
                        vector_alignment_x = vector_alignment_x + agent.vector_x
                        vector_alignment_y = vector_alignment_y + agent.vector_y

        magnitude = math.sqrt(pow(vector_attraction_x, 2) + pow(vector_attraction_y, 2))
        if magnitude > 0:
            vector_attraction_x = vector_attraction_x / magnitude
            vector_attraction_y = vector_attraction_y / magnitude

        magnitude = math.sqrt(pow(vector_destination_x, 2) + pow(vector_destination_y, 2))
        if magnitude > 0:
            vector_destination_x = vector_destination_x / magnitude
            vector_destination_y = vector_destination_y / magnitude

        magnitude = math.sqrt(pow(vector_alignment_x, 2) + pow(vector_alignment_y, 2))
        if magnitude > 0:
             vector_alignment_x = vector_alignment_x / magnitude
             vector_alignment_y = vector_alignment_y / magnitude

        magnitude = math.sqrt(pow(vector_random_x, 2) + pow(vector_random_y, 2))
        if magnitude > 0:
            vector_random_x = vector_random_x / magnitude
            vector_random_y = vector_random_y / magnitude

        self.vector_x = vector_destination_x * self.destination_weight + \
                        vector_attraction_x * self.attraction_weight + \
                        vector_alignment_x * self.alignment_weight + \
                        vector_random_x * self.random_weight

        self.vector_y = vector_destination_y * self.destination_weight + \
                        vector_attraction_y * self.attraction_weight + \
                        vector_alignment_y * self.alignment_weight + \
                        vector_random_y * self.random_weight

        magnitude = math.sqrt(pow(self.vector_x, 2) + pow(self.vector_y, 2))
        self.vector_x = self.vector_x / magnitude
        self.vector_y = self.vector_y / magnitude

    def update(self):
        self.location_x = self.location_x + self.vector_x * self.velocity
        self.location_y = self.location_y + self.vector_y * self.velocity


class Threat:
    def __init__(self, x, y, v_x, v_y):
        self.location_x = x
        self.location_y = y
        self.vector_x = random.uniform(-1.0, 1.0)
        self.vector_y = random.uniform(-1.0, 1.0)
        self.range = 20

    def update(self):
        self.location_x = self.location_x + self.vector_x
        self.location_y = self.location_y + self.vector_y

class Target:
    def __init__(self, x, y, label):
        self.location_x = x
        self.location_y = y
        self.label = label
        self.deliveries = 0

    def delivery(self):
        self.deliveries = self.deliveries + 1

num_agents = 500
num_threats = 400
num_targets = 10
launch_sequence = 0

fig = plt.figure(figsize=(16, 10), facecolor='white')
ax = plt.subplot(frameon=False)

swarm = []
swarm_points = []

threats = []
threat_points = []

targets = []
target_points = []
target_label = []
for i in range(0, num_threats):
    threats.append(Threat(random.randrange(-970.0, 970.0), random.randrange(-970.0, 970.0), 0, 0))
    point, = ax.plot(threats[i].location_x, threats[i].location_y, marker='o', color='red', markersize=10, alpha=.2)
    threat_points.append(point)


point, = ax.plot(0, 0, marker='o', color='blue', markersize=20, alpha=.2)
target_points.append(point)
label = ax.annotate("Logistics Hub", (30, 20), size=8)
target_label.append(label)

for i in range(0, int(num_targets/2)):
    targets.append(Target(random.randrange(-970.0, -500.0), random.randrange(-970.0, 970.0), f"Site: {i}\nDeliveries: 0"))
    point, = ax.plot(targets[i].location_x, targets[i].location_y, marker='o', color='blue', markersize=20, alpha=.2)
    target_points.append(point)
    label = ax.annotate(targets[i].label, (targets[i].location_x+30, targets[i].location_y-20), size=8)
    target_label.append(label)

for i in range(int(num_targets/2), num_targets):
    targets.append(Target(random.randrange(500.0, 970.0), random.randrange(-970.0, 970.0), f"Site: {i}\nDeliveries: 0"))
    point, = ax.plot(targets[i].location_x, targets[i].location_y, marker='o', color='blue', markersize=20, alpha=.2)
    target_points.append(point)
    label = ax.annotate(targets[i].label, (targets[i].location_x+30, targets[i].location_y-20), size=8)
    target_label.append(label)

for i in range(0, num_agents):
    target = random.choice(targets)
    swarm.append(Agent(0, 0, target.location_x, target.location_y))
    point, = ax.plot(swarm[i].location_x, swarm[i].location_y, marker='+', color='blue', markersize=2)
    swarm_points.append(point)


def animate(frame):
    global launch_sequence
    launch_sequence = launch_sequence + 1

    for i in range(1, len(target_label)):
        target_label[i].set_text(f"Site: {i}\nDeliveries: {launch_sequence}")

    if launch_sequence < num_agents:
        swarm[launch_sequence].max_velocity = 4
        swarm[launch_sequence].launched = True

    for i in range(0, num_agents):
        swarm[i].exec_swarm_algorithm(swarm, threats)
        swarm[i].update()
        swarm_points[i].set_data(swarm[i].location_x, swarm[i].location_y)
        if swarm[i].velocity == 1:
            swarm_points[i].set_color('red')
        else:
            swarm_points[i].set_color('green')

    ans = launch_sequence % 100
    for i in range(0, num_threats):
        if ans == 0:
            threats[i].vector_x = -threats[i].vector_x
            threats[i].vector_y = -threats[i].vector_y
        threats[i].update()
        threat_points[i].set_data(threats[i].location_x, threats[i].location_y)

    return swarm_points


# Create the animation
ani = FuncAnimation(fig, animate, interval=1)

# Set plot limits
ax.set_xlim(-1000, 1000)
ax.set_ylim(-1000, 1000)
ax.set_axis_off()

# Display the plot
plt.show()
