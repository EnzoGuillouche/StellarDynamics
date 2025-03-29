from vpython import *

# ---------------------- Camera Controls ---------------------
scene.camera.pos = vector(50, 200, 150)
scene.camera.axis = vector(0, -1, -2)

def cameraInit(sun):
    scene.camera.pos = sun.sphere.pos + vector(0, 0, sun.sphere.radius*3)
    scene.camera.axis = sun.sphere.pos - scene.camera.pos

camera_speed = 50
camera_velocity = vector(0, 0, 0)
acceleration_factor = 0.60
deceleration_factor = 0.9

keys_pressed = {"w": False, "s": False, "a": False, "d": False, "q": False, "e": False}

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


scene.bind('keydown', key_down)
scene.bind('keyup', key_up)

def cameraMovement():
    # Smooth camera movement
    move_direction = vector(0, 0, 0)
    if keys_pressed["w"]: move_direction.z -= camera_speed
    if keys_pressed["s"]: move_direction.z += camera_speed
    if keys_pressed["a"]: move_direction.x -= camera_speed
    if keys_pressed["d"]: move_direction.x += camera_speed
    if keys_pressed["q"]: move_direction.y -= camera_speed
    if keys_pressed["e"]: move_direction.y += camera_speed
    
    return move_direction

def updateCameraVelocity(direction):
    return camera_velocity * deceleration_factor + direction * acceleration_factor