from vpython import *
import camera
import Elements.planet
import Elements.ring

# --------------------- Simulation Constants ---------------------
GRAVITY_CONSTANT = 1000
MIN_ORBIT_RADIUS = 2.0
SOFTENING_FACTOR = 0.03  # Prevents division by zero in gravity calculation
DELTA_TIME = 0.01

# ---------------------- Simulation Loop ---------------------
def loop():
    while True:
        rate(100)  # simulation speed

        move_direction = camera.cameraMovement()

        # Apply acceleration and smooth stop
        camera_velocity = camera.updateCameraVelocity(move_direction)
        scene.camera.pos += camera_velocity

        # Update planetary motion
        for planet in Elements.planet.planets:
            displacement = Elements.planet.planets[0].sphere.pos - planet.sphere.pos
            distance = mag(displacement)
            force_magnitude = (GRAVITY_CONSTANT * Elements.planet.planets[0].mass * planet.mass) / (distance**2 + SOFTENING_FACTOR**2)
            gravitational_force = force_magnitude * norm(displacement)
            
            # Update velocity and position
            planet.velocity += (gravitational_force / planet.mass) * DELTA_TIME
            planet.sphere.pos += planet.velocity * DELTA_TIME
            
            if planet.has_rings:
                # Update ring motion (circular movement around the planet)
                for ring in Elements.ring.rings:
                    ring.angle += DELTA_TIME
                    
                    ring.sphere.pos += planet.velocity * DELTA_TIME
                    
