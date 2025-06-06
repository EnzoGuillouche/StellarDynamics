from vpython import *
import os

import Elements.planet

camera_speed = 25
camera_velocity = vector(0, 0, 0)
acceleration_factor = 0.60
deceleration_factor = 0.9

def focusCamera(planet):
    global camera_has_moved
    scene.camera.pos = planet.sphere.pos + vector(0, 0, planet.sphere.radius*5)
    scene.camera.axis = planet.sphere.pos - scene.camera.pos
    camera_has_moved = False

# ---------------------- Camera Controls ---------------------
keys_pressed = {"w": False, "s": False, "a": False, "d": False, "q": False, "e": False, }

# Handle key press
def key_down(event):
    key = event.key
    if key in keys_pressed:
        keys_pressed[key] = True

# Handle key release
def key_up(event):
    key = event.key
    if key in keys_pressed:
        keys_pressed[key] = False

# Handle mouse click
def on_mouse_click(event):
    camera_pos = scene.camera.pos
    click_pos = event.pos
    ray_direction = norm(click_pos - camera_pos)
    
    clicked_planet_index = -1  # Default if no planet is clicked (out of range)
    closest_distance = float('inf') # Track the closest planet

    for i, planet in enumerate(Elements.planet.planets):
        planet_center = planet.sphere.pos
        planet_radius = planet.sphere.radius

        camera_to_planet = planet_center - camera_pos
        projection_length = dot(camera_to_planet, ray_direction)  # Project onto ray

        # Find the closest point on the ray to the planet's center
        closest_point = camera_pos + projection_length * ray_direction
        distance_to_planet = mag(closest_point - planet_center)

        # Click is valid if within the planet's radius and is the closest so far
        if distance_to_planet <= planet_radius and projection_length > 0:  
            if projection_length < closest_distance:  # Ensure we pick the nearest planet
                closest_distance = projection_length
                clicked_planet_index = i  # Store the correct index

    global planet_focused
    if clicked_planet_index != -1:
        os.system('cls' if os.name == 'nt' else 'clear')
        planet_clicked = list(Elements.planet.planets_data.keys())[clicked_planet_index]
        print(Elements.planet.planets_data[planet_clicked]["description"])
        
        planet_focused = Elements.planet.planets[clicked_planet_index]
        focusCamera(planet_focused)


def cameraInit(sun):
    focusCamera(sun)
    global planet_focused
    planet_focused = sun
    
    scene.bind('keydown', key_down)
    scene.bind('keyup', key_up)
    scene.bind('click', on_mouse_click)
    
    global camera_has_moved
    camera_has_moved = True

def cameraMovement():
    global camera_has_moved
    # Smooth camera movement
    move_direction = vector(0, 0, 0)
    if keys_pressed["w"]: move_direction.z -= camera_speed
    if keys_pressed["s"]: move_direction.z += camera_speed
    if keys_pressed["a"]: move_direction.x -= camera_speed
    if keys_pressed["d"]: move_direction.x += camera_speed
    if keys_pressed["q"]: move_direction.y -= camera_speed
    if keys_pressed["e"]: move_direction.y += camera_speed
    
    if move_direction != vector(0, 0, 0):
        camera_has_moved = True
    
    return move_direction

def updateCameraVelocity(direction):
    return camera_velocity * deceleration_factor + direction * acceleration_factor