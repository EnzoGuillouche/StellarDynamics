from vpython import *
import random
import json

# ---------------------- Planet data from JSON ---------------------
with open('data.json', 'r') as file:
    planets_data = json.load(file)

NUM_PLANETS = len(planets_data)

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

planets = []

class Planet:
  def __init__(self, index, pos, GRAVITY_CONSTANT):
    self.index = index
    self.name = list(planets_data.keys())[self.index]
    self.mass = planets_data[self.name]["mass"]
    self.has_rings = self.index == 6
    self.sphere = sphere()
    self.velocity = vector(0, 0, 0)
    
    if self.name == "Sun":
        # Create star
        self.sphere = sphere(
            pos=pos, 
            radius=planet_radius[self.index], 
            color=vector(planets_data[self.name]["color"][0] / 255, planets_data[self.name]["color"][1] / 255, planets_data[self.name]["color"][2] / 255),
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
            color=vector(planets_data[self.name]["color"][0] / 255, planets_data[self.name]["color"][1] / 255, planets_data[self.name]["color"][2] / 255),
        )
        self.mass = planets_data["Sun"]["mass"] * planets_data[self.name]["mass"]
        self.velocity = initial_velocity

    planets.append(self)

# ---------------------- Create Orbiting Planets ---------------------
def createPlanets(GRAVITY_CONSTANT):
    for i in range(NUM_PLANETS): # Including the Sun creation
        e = Planet(i, vector(0, 0, 0), GRAVITY_CONSTANT)
        print("Created", e.name)
        