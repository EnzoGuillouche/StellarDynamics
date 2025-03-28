from vpython import *
import random
import camera

# --------------------- Simulation Constants ---------------------
GRAVITY_CONSTANT = 1000
SUN_MASS = 1000
PLANET_MASS = 1
MIN_ORBIT_RADIUS = 2.0
SOFTENING_FACTOR = 0.03  # Prevents division by zero in gravity calculation
NUM_PLANETS = 8
NUM_RINGS = 50
DELTA_TIME = 0.01

# ---------------------- Create Central Star ---------------------
sun = sphere(pos=vector(0, 0, 0), radius=250, color=color.yellow, shininess=True)

# ---------------------- Planet colors ---------------------
planet_colors = {
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
    1: 0.000055,
    2: 0.000815,
    3: 0.000003,
    4: 0.000107,
    5: 0.000954,
    6: 0.000285,
    7: 0.000047,
    8: 0.000055
}

# ---------------------- Create Orbiting Planets ---------------------
planets = []
def createPlanets():
    for i in range(NUM_PLANETS):
        # Random orbital radius and angle
        orbit_radius = sun.radius + sun.radius * planet_orbital_radius[i+1]
        angle = random.uniform(0, 2 * pi)

        # Initial position in the XY plane
        initial_position = vector(orbit_radius * cos(angle), 0, orbit_radius * sin(angle))

        # Calculate velocity for a circular orbit
        orbital_speed = sqrt(GRAVITY_CONSTANT * SUN_MASS / orbit_radius)
        initial_velocity = vector(-sin(angle), 0, cos(angle)) * orbital_speed

        # Create planet
        planet = sphere(
            pos=initial_position, 
            radius=sun.radius * (planet_radius[i+1]/2), 
            color=planet_colors[i+1],
        )
        planet.mass = SUN_MASS * planet_mass[i+1]
        planet.velocity = initial_velocity
        planet.has_rings = i+1 == 6

        planets.append(planet)
        
# ---------------------- Create Orbiting Rings ---------------------
rings = []
rings_color = [ # Predefined rings color options
    vector(205/255, 133/255, 63/255),
    vector(218/255, 165/255, 32/255),
    vector(238/255, 232/255, 170/255)
]

def createRings(planet):
    for i in range(NUM_RINGS):
        # Random orbital radius and angle
        orbit_radius = planet.radius + planet.radius * random.uniform(1, 2)
        angle = random.uniform(0, 2 * pi)

        # Initial position in the XY plane
        initial_position = vector(orbit_radius * cos(angle), 0, orbit_radius * sin(angle))

        # Calculate velocity for a circular orbit
        orbital_speed = sqrt(GRAVITY_CONSTANT * planet.mass / orbit_radius)
        initial_velocity = vector(-sin(angle), 0, cos(angle)) * orbital_speed

        ring_color = random.choice(rings_color)

        # Create ring
        ring = sphere(
            pos=planet.pos + initial_position, 
            radius=planet.radius * 0.005, 
            color=ring_color,
            make_trail=True,
            retain=200
        )
        ring.mass = planet.mass * 0.001
        ring.velocity = initial_velocity
        ring.orbit_radius = orbit_radius
        ring.angle = angle

        rings.append(ring)

# ---------------------- Simulation Loop ---------------------
def loop():
    while True:
        rate(100)  # simulation speed

        move_direction = camera.cameraMovement()

        # Apply acceleration and smooth stop
        camera_velocity = camera.updateCameraVelocity(move_direction)
        scene.camera.pos += camera_velocity

        # Update planetary motion
        for planet in planets:
            displacement = sun.pos - planet.pos
            distance = mag(displacement)
            force_magnitude = (GRAVITY_CONSTANT * SUN_MASS * planet.mass) / (distance**2 + SOFTENING_FACTOR**2)
            gravitational_force = force_magnitude * norm(displacement)
            
            # Update velocity and position
            planet.velocity += (gravitational_force / planet.mass) * DELTA_TIME
            planet.pos += planet.velocity * DELTA_TIME
            
            if planet.has_rings:
                # Update ring motion (circular movement around the planet)
                for ring in rings:
                    ring.angle += DELTA_TIME
                    
                    ring.pos = planet.pos + vector(
                        ring.orbit_radius * cos(ring.angle),
                        0,
                        ring.orbit_radius * sin(ring.angle)
                    )
                    
