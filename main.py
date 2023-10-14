import math
import random
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.style as style
from matplotlib.animation import FuncAnimation


class Agent:
    def __init__(self, base_x, base_y, target_x, target_y, swarm_intelligence):
        """
        An independent agent within the swarm using an established set of rules to optimize its path through the env.

           :param base_x : X coordinate of the main hub where resources are collected.
           :param base_y : Y coordinate of the main hub where resources are collected.
           :param target_x : X coordinate of the destination target where resources are delivered.
           :param target_y : X coordinate of the destination target where resources are delivered.
        """

        self.location = np.array([base_x, base_y])
        self.target = np.array([target_x, target_y])
        self.base = np.array([base_x, base_y])
        self.vector = np.array([random.uniform(-3.0, 3.0), random.uniform(-3.0, 3.0)])
        self.launched = False
        self.communication_range = 40
        self.max_comm_links = 50
        self.velocity = 0
        self.max_velocity = 0
        self.resource = 100

        if swarm_intelligence:
            self.weights = {"Random": .1,
                        "Destination": .6,
                        "Alignment": .1,
                        "Attraction": .5,
                        }
        else:
            self.weights = {"Random": .1,
                            "Destination": .6,
                            "Alignment": .0,
                            "Attraction": .0,
                            }

    def exec_swarm_algorithm(self, swarm, threats):
        """
        An independent agent within the swarm using an established set of rules to optimize its path through the env.
           :param swarm_instance : Pass list with other agents in the swarm so communication can be simulated.
           :param threat_instance : Pass threats in teh swarm so detection can be simulated.
        """
        # Initializing vectors to be used later.
        vector_destination = np.array([0, 0])
        vector_attraction = np.array([0, 0])
        vector_alignment = np.array([0, 0])
        vector_random = np.array([random.randrange(-100, 100), random.randrange(-100, 100)])

        # If agent has resources goes to target.
        if self.resource == 100:
            vector_destination = self.target - self.location

        # If agent dropped off complete returns to base for more resources.
        if self.resource == 0:
            vector_destination = self.base - self.location

        # If within range of a threat sets velocity to minimum.
        self.velocity = self.max_velocity
        for threat in threats:
            if abs(self.location[0] - threat.location[0]) < threat.range and abs(
                    self.location[1] - threat.location[1]) < threat.range:
                self.velocity = min(self.max_velocity, 1)

        if abs(self.base[0] - self.location[0]) < 5 and abs(
                self.base[0] - self.location[0]) < 5 and self.resource == 0:
            self.resource = 100

        # For each agent in range determines if it is close enough to communicate.
        agents_in_range = 0

        for agent in swarm:
            if agents_in_range < self.max_comm_links:

                # If it is close enough to communicate.
                if abs(agent.location[0] - self.location[0]) < self.communication_range and \
                        abs(agent.location[1] - self.location[1]) < self.communication_range:
                    agents_in_range = agents_in_range + 1

                    if agent.velocity < agent.max_velocity and agent.launched:
                        vector_attraction = vector_attraction + self.location - agent.location
                        vector_alignment = vector_alignment + agent.vector

        magnitude = math.sqrt(pow(vector_attraction[0], 2) + pow(vector_attraction[1], 2))
        if magnitude > 0:
            vector_attraction = vector_attraction / magnitude

        magnitude = math.sqrt(pow(vector_destination[0], 2) + pow(vector_destination[1], 2))
        if magnitude > 0:
            vector_destination = vector_destination / magnitude

        magnitude = math.sqrt(pow(vector_alignment[0], 2) + pow(vector_alignment[1], 2))
        if magnitude > 0:
            vector_alignment = vector_alignment / magnitude

        magnitude = math.sqrt(pow(vector_random[0], 2) + pow(vector_random[1], 2))
        if magnitude > 0:
            vector_random = vector_random / magnitude

        self.vector[0] = vector_destination[0] * self.weights["Destination"] + \
                         vector_attraction[0] * self.weights["Attraction"] + \
                         vector_alignment[0] * self.weights["Alignment"] + \
                         vector_random[0] * self.weights["Random"]

        self.vector[1] = vector_destination[1] * self.weights["Destination"] + \
                         vector_attraction[1] * self.weights["Attraction"] + \
                         vector_alignment[1] * self.weights["Alignment"] + \
                         vector_random[1] * self.weights["Random"]

        magnitude = math.sqrt(pow(self.vector[0], 2) + pow(self.vector[1], 2))
        self.vector = self.vector / magnitude

    def update(self):
        self.location = self.location + self.vector * self.velocity


class Threat:
    def __init__(self, x, y):
        self.location = np.array([x, y])
        self.vector = np.array([random.uniform(-1.0, 1.0), random.uniform(-1.0, 1.0)])
        self.range = 20

    def update(self):
        self.location = self.location + self.vector


class Target:
    def __init__(self, x, y, target_label):
        self.location = np.array([x, y])
        self.label = target_label
        self.deliveries = 0

    def delivery(self):
        self.deliveries = self.deliveries + 1

# Stores data and representation for agents in the swarm.
num_agents = 500
swarm = []
swarm_points = []

# Stores data and representation for threats in the environment.
num_threats = 200
threats = []
threat_points = []

# Stores data and representation for targets in the environment.
num_targets = 20
targets = []
target_points = []
target_label = []

swarm_intelligent_deliveries = [0]
non_swarm_intelligent_deliveries = [0]

launch_sequence = 0
fig = plt.figure(figsize=(11, 10), facecolor='white')
ax = plt.subplot(frameon=False)

# Add the logistics hub to the graph.
point, = ax.plot(0, 0, marker='o', color='blue', markersize=20, alpha=.2)
label = ax.annotate("Logistics Hub", (30, 20), size=8)

# Cycles through creating threats and adding to the graph.
for i in range(0, num_threats):
    threats.append(Threat(random.randrange(-970, 970), random.randrange(-970, 970)))
    point, = ax.plot(threats[i].location[0],
                     threats[i].location[1],
                     marker='o', color='red',
                     markersize=threats[i].range, alpha=.2)
    threat_points.append(point)

# Cycles through and adds the non-swarm intelligent targets to the graph.
for i in range(0, int(num_targets / 2)):
    targets.append(
        Target(random.randrange(-970, -800), random.randrange(-970, 970), f"Site: {i}\nDeliveries: 0"))
    point, = ax.plot(targets[i].location[0], targets[i].location[1], marker='o', color='blue', markersize=20, alpha=.2)
    target_points.append(point)
    label = ax.annotate(targets[i].label, (targets[i].location[0] + 30, targets[i].location[1] - 20), size=8)
    target_label.append(label)

# Cycles through and adds the swarm intelligent targets to the graph.
for i in range(int(num_targets / 2), num_targets):
    targets.append(Target(random.randrange(800, 970), random.randrange(-970, 970), f"Site: {i}\nDeliveries: 0"))
    point, = ax.plot(targets[i].location[0], targets[i].location[1], marker='o', color='blue', markersize=20, alpha=.2)
    target_points.append(point)
    label = ax.annotate(targets[i].label, (targets[i].location[0] + 30, targets[i].location[1] - 20), size=8)
    target_label.append(label)

non_intelligent_label = ax.annotate("Non-Swarm Intelligent Deliveries: 0", (-800, 1000), size=16)
intelligent_label = ax.annotate("Swarm Intelligent Deliveries: 0", (200, 1000), size=16)

# Cycles through and adds the targets to the graph.
for i in range(0, num_agents):
    target = random.choice(targets)
    if target.location[0] < 0:
        swarm.append(Agent(0, 0, target.location[0], target.location[1], False))
    else:
        swarm.append(Agent(0, 0, target.location[0], target.location[1], True))
    point, = ax.plot(swarm[i].location[0], swarm[i].location[1], marker='+', color='blue', markersize=2)
    swarm_points.append(point)


def animate(frame):
    global launch_sequence
    launch_sequence = launch_sequence + 1

    for i in range(0, num_targets):
        target_label[i].set_text(f"Site: {i}\nDeliveries: {targets[i].deliveries}")

    if launch_sequence < num_agents:
        swarm[launch_sequence].max_velocity = 4
        swarm[launch_sequence].launched = True

    for i in range(0, num_agents):

        # If reached target it drops of resources.
        for target in targets:
            if abs(target.location[0] - swarm[i].location[0]) < 5 and abs(target.location[1] - swarm[i].location[1]) < 5 and swarm[i].resource == 100:
                swarm[i].resource = 0
                target.deliveries = target.deliveries + 1

        swarm[i].exec_swarm_algorithm(swarm, threats)
        swarm[i].update()
        swarm_points[i].set_data(swarm[i].location[0], swarm[i].location[1])
        if swarm[i].velocity == 1:
            swarm_points[i].set_color('red')
        else:
            swarm_points[i].set_color('green')

    ans = launch_sequence % 100
    for i in range(0, num_threats):
        if ans == 0:
            threats[i].vector = -threats[i].vector
        threats[i].update()
        threat_points[i].set_data(threats[i].location[0], threats[i].location[1])

    sum_intelligent_deliveries = 0
    sum_non_intelligent_deliveries = 0
    for i in range(0, num_targets):
        if i < num_targets / 2:
            sum_non_intelligent_deliveries = sum_non_intelligent_deliveries + targets[i].deliveries
        else:
            print()
            sum_intelligent_deliveries = sum_intelligent_deliveries + targets[i].deliveries
    swarm_intelligent_deliveries.append(sum_intelligent_deliveries)
    non_swarm_intelligent_deliveries.append(sum_non_intelligent_deliveries)
    non_intelligent_label.set_text(f"Non-Swarm Intelligent Deliveries: {sum_non_intelligent_deliveries}")
    intelligent_label.set_text(f"Swarm Intelligent Deliveries: {sum_intelligent_deliveries}")
    return swarm_points


# Create the animation
ani = FuncAnimation(fig, animate, interval=1)
plt.show()

style.use('dark_background')

fig, (ax1) = plt.subplots(1, 1, figsize=(20, 9))
ax1.set_title("Swarm vs. Non Swarm Algorithm Comparison", fontsize=20)


plt.plot(swarm_intelligent_deliveries, label = "Swarm Intelligence")
plt.plot(non_swarm_intelligent_deliveries, label = "Brute Force")
ax1.legend()
plt.show()


# Set plot limits
#ax.set_axis_off()

# Display the plot
plt.show()
