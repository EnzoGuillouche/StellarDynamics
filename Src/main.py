from vpython import *
import simulation
import camera

if __name__ == "__main__":
    # ---------------------- Init ---------------------
    camera.cameraInit(simulation.sun.pos)
    simulation.createPlanets()
    
    for planet in simulation.planets:
        if planet.has_rings:
            simulation.createRings(planet)
            
    scene.width = 1200
    scene.height = 800

    # ---------------------- Simulation Loop ---------------------
    simulation.loop()
        