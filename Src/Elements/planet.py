from vpython import *
import random

NUM_PLANETS = 8

planet_names = {
    0: "Sun",
    1: "Mercury",
    2: "Venus",
    3: "Earth",
    4: "Mars",
    5: "Jupiter",
    6: "Saturn",
    7: "Uranus",
    8: "Neptune",
}

# ---------------------- Planet colors ---------------------
planet_colors = {
    0: vector(255/255, 255/255, 0/255),
    1: vector(205/255, 133/255, 63/255),
    2: vector(218/255, 165/255, 32/255),
    3: vector(127/255, 255/255, 212/255),
    4: vector(255/255, 59/255, 0/255),
    5: vector(238/255, 232/255, 170/255),
    6: vector(245/255, 245/255, 220/255),
    7: vector(0/255, 191/255, 255/255),
    8: vector(65/255, 105/255, 225/255)
}

planet_radius = {
    0: 250,
    1: 0.05,
    2: 0.175,
    3: 0.25,
    4: 0.125,
    5: 0.5,
    6: 0.39,
    7: 0.32,
    8: 0.3
}

planet_orbital_radius = { # in astronomical unit
    0: 0.0,
    1: 0.4,
    2: 0.7,
    3: 1.0,
    4: 1.5,
    5: 5.2,
    6: 9.6,
    7: 19.2,
    8: 30.0
}

planet_mass = {
    0: 1000.0,
    1: 0.000055,
    2: 0.000815,
    3: 0.000003,
    4: 0.000107,
    5: 0.000954,
    6: 0.000285,
    7: 0.000047,
    8: 0.000055
}

planets = []

class Planet:
  def __init__(self, index, pos, GRAVITY_CONSTANT):
    self.index = index
    self.name = planet_names[self.index]
    self.mass = planet_mass[self.index]
    self.has_rings = self.index == 6
    self.sphere = sphere()
    self.velocity = vector(0, 0, 0)
    
    if self.name == "Sun":
        # Create star
        self.sphere = sphere(
            pos=pos, 
            radius=planet_radius[self.index], 
            color=planet_colors[self.index],
            shininess=True
        )
    else:
        # Random orbital radius and angle
        orbit_radius = planets[0].sphere.radius + planets[0].sphere.radius * planet_orbital_radius[self.index]
        angle = random.uniform(0, 2 * pi)

        # Initial position in the XY plane
        initial_position = vector(orbit_radius * cos(angle), 0, orbit_radius * sin(angle))

        # Calculate velocity for a circular orbit
        orbital_speed = sqrt(GRAVITY_CONSTANT * planets[0].mass / orbit_radius)
        initial_velocity = vector(-sin(angle), 0, cos(angle)) * orbital_speed

        # Create planet
        self.sphere = sphere(
            pos=initial_position, 
            radius=planets[0].sphere.radius * (planet_radius[self.index]/2), 
            color=planet_colors[self.index],
        )
        self.mass = planets[0].mass * planet_mass[self.index]
        self.velocity = initial_velocity

    planets.append(self)

# ---------------------- Create Orbiting Planets ---------------------
def createPlanets(GRAVITY_CONSTANT):
    for i in range(NUM_PLANETS + 1): # Including the Sun creation
        e = Planet(i, vector(0, 0, 0), GRAVITY_CONSTANT)
        print("Created", e.name)
        