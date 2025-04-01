from vpython import *

import camera
import Elements.planet
import Elements.ring

# --------------------- Simulation Constants ---------------------
GRAVITY_CONSTANT = 1000
MIN_ORBIT_RADIUS = 2.0
SOFTENING_FACTOR = 0.03  # Prevents division by zero in gravity calculation
DELTA_TIME = 0.01

# ---------------------- Update motion ---------------------
def updateMotion(parent, child):
    displacement = parent.sphere.pos - child.sphere.pos
    distance = mag(displacement)
    force_magnitude = (GRAVITY_CONSTANT * parent.mass * child.mass) / (distance**2 + SOFTENING_FACTOR**2)
    gravitational_force = force_magnitude * norm(displacement)
    
    # Update velocity and position
    child.velocity += (gravitational_force / child.mass) * DELTA_TIME
    child.sphere.pos += child.velocity * DELTA_TIME

# ---------------------- Simulation Loop ---------------------
def loop():
    while True:
        rate(100)  # simulation speed

        move_direction = camera.cameraMovement()

        # Apply acceleration and smooth stop
        camera_velocity = camera.updateCameraVelocity(move_direction)
        
        if camera.camera_has_moved == False:
            camera.focusCamera(camera.planet_focused)
        else:
            scene.camera.pos += camera_velocity

        # Update planetary motion
        for planet in Elements.planet.planets:
            updateMotion(Elements.planet.planets[0], planet)
            
            if planet.has_rings:
                # Update ring motion (circular movement around the planet)
                for ring in Elements.ring.rings:
                    updateMotion(planet, ring)
                    ring.sphere.pos += planet.velocity * DELTA_TIME
                    
                    
