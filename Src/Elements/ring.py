from vpython import *
import random

NUM_RINGS = 1000

rings_color = [ # Predefined rings color options
    vector(205/255, 133/255, 63/255),
    vector(218/255, 165/255, 32/255),
    vector(238/255, 232/255, 170/255),
    vector(0/255, 191/255, 255/255)
]

rings = []

class Ring:
    def __init__(self, planet, GRAVITY_CONSTANT):
        self.planet = planet
        
        # Random orbital radius and angle
        orbit_radius = planet.sphere.radius + planet.sphere.radius * random.uniform(1, 2)
        angle = random.uniform(0, 2 * pi)

        # Initial position in the XY plane
        initial_position = vector(orbit_radius * cos(angle), 0, orbit_radius * sin(angle))

        # Calculate velocity for a circular orbit
        orbital_speed = sqrt(GRAVITY_CONSTANT * planet.mass / orbit_radius)
        initial_velocity = vector(-sin(angle), 0, cos(angle)) * orbital_speed

        ring_color = random.choice(rings_color)

        # Create ring
        self.sphere = sphere(
            pos=planet.sphere.pos + initial_position, 
            radius=planet.sphere.radius * 0.02, 
            color=ring_color
        )
        self.mass = planet.mass * 0.02
        self.velocity = initial_velocity

        rings.append(self)

# ---------------------- Create Orbiting Rings ---------------------
def createRings(planet, GRAVITY_CONSTANT):
    for i in range(NUM_RINGS):
        e = Ring(planet, GRAVITY_CONSTANT)