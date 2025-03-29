from vpython import *
import os

import simulation
import Elements.planet
import camera

if __name__ == "__main__":
    # ---------------------- Init ---------------------
    Elements.planet.createPlanets(simulation.GRAVITY_CONSTANT)
    camera.cameraInit(Elements.planet.planets[0])
    
    for planet in Elements.planet.planets:
        if planet.has_rings:
            Elements.ring.createRings(planet, simulation.GRAVITY_CONSTANT)
            
    scene.width = 1200
    scene.height = 800

    # ---------------------- Simulation Loop ---------------------
    os.system('cls' if os.name == 'nt' else 'clear')
    simulation.loop()
        