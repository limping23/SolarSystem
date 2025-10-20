import math
import data
from math import sqrt, cos, sin
from data import CelestialBody
import datetime
import sys, os


def is_between(p1: data.Point, p2: data.Point, p3: data.Point, eps=1e-9):
    x1 = p1.x
    y1 = p1.y
    x2 = p2.x
    y2 = p2.y
    x3 = p3.x
    y3 = p3.y
    collinear = abs((x3 - x1)*(y2 - y1) - (y3 - y1)*(x2 - x1)) < eps
    if not collinear:
        return False
    within_x = min(x1, x2) - eps <= x3 <= max(x1, x2) + eps
    within_y = min(y1, y2) - eps <= y3 <= max(y1, y2) + eps
    return within_x and within_y

def set_circular_velocity(body: CelestialBody, center: CelestialBody) -> None:
    dx = body.position.x - center.position.x
    dy = body.position.y - center.position.y
    r = math.hypot(dx, dy)
    if r == 0:
        return
    v_mag = math.sqrt(data.constants["G"] * center.mass / r)
    tx = dy / r
    ty = dx / r
    body.Orbital_speed.x = center.Orbital_speed.x + v_mag * tx
    body.Orbital_speed.y = center.Orbital_speed.y + v_mag * ty

# Barycenter
def remove_system_momentum(bodies: list[CelestialBody]) -> None:
    px = sum(body.mass * body.Orbital_speed.x for body in bodies)
    py = sum(body.mass * body.Orbital_speed.y for body in bodies)
    M = sum(body.mass for body in bodies)
    vx_cm = px / M
    vy_cm = py / M
    for body in bodies:
        body.Orbital_speed.x -= vx_cm
        body.Orbital_speed.y -= vy_cm

def distance(p1: data.Point, p2: data.Point) -> float: #Distance between 2 points
    return math.hypot(p1.x - p2.x, p1.y - p2.y)

def law_ug(m1: float, m2: float, R: float, softening: float = 0) -> float: #Law of Universal Gravitation
    return data.constants["G"] * m1 * m2 / (R**2 + softening)

def angle(position: data.Vector) -> float: #Angle of vector relative to x
    delta_x = position.x2 - position.x1
    delta_y = position.y2 - position.y1
    return math.atan2(delta_y, delta_x)

def sum_forces(forces: list[tuple]) -> tuple: #Sum of all forces acting on some object
    force_res_x = 0
    force_res_y = 0
    for items in forces:
        force_res_x += items[0] * cos(items[1])
        force_res_y += items[0] * sin(items[1])
    force_res = sqrt(force_res_x**2 + force_res_y**2)
    return force_res, math.atan2(force_res_y, force_res_x)

def update_position(body: CelestialBody, blackhole: bool, dt: float = data.constants["dt"]) -> None:
    # print(body.info)
    forces = []
    for other_body in data.bodies:
        if other_body == body or body.position == other_body.position or other_body.name == "BlackHole" and not blackhole:
            continue
        if blackhole:
            force = law_ug(body.mass, other_body.mass, distance(body.position, other_body.position), 1e5)
        else:
            force = law_ug(body.mass, other_body.mass, distance(body.position, other_body.position)) # The force with which a particular planet is acted upon by another planet
        force_angle = angle(data.Vector(other_body.position.x, other_body.position.y, body.position)) # Angle of said force relative to x
        forces.append((force, force_angle))
    Sum_forces = sum_forces(forces) # The force with which all planets are acted upon by another planet and its direction
    acceleration_res = Sum_forces[0] / body.mass # Momental acceleration
    acceleration = data.Point(acceleration_res * cos(Sum_forces[1]), acceleration_res * sin(Sum_forces[1])) # True acceleration in the Oxy axis
    movement = body.Orbital_speed * dt + acceleration * dt**2 / 2
    body.next_pos = body.position + movement # Setting new pos for planet
    if blackhole and (distance(body.position, data.BlackHole.position) < data.BlackHole.radius  or is_between(body.position, body.next_pos, data.BlackHole.position)):
        body.color = "black"
        body.position = data.BlackHole.position
    body.Orbital_speed += acceleration * dt # Setting new speed for planet

    # Optimized trail creation
    body.update_counter += 1
    if data.constants["user_scale"]:
        if body.update_counter % body.trail_update_interval == 0:
            screen_x = body.position.x * body.scaler * data.constants["scale_m"] * data.constants["scale"] + data.constants["root_info"][0] / 2 + data.constants["move_mx"]
            screen_y = body.position.y * body.scaler * data.constants["scale_m"] * data.constants["scale"] + data.constants["root_info"][1] / 2 + data.constants["move_my"]
            if len(body.trail) == 0 or distance_to_last(body.trail, screen_x, screen_y) > body.min_trail_length:
                body.trail.append((screen_x, screen_y))
                if len(body.trail) > body.max_trail_length:
                    body.trail.pop(0)
    else:
        screen_x = body.position.x * data.constants["real_scale"] * data.constants["scale_m"] + data.constants["root_info"][0] / 2 + data.constants["move_mx"]
        screen_y = body.position.y * data.constants["real_scale"] * data.constants["scale_m"] + data.constants["root_info"][1] / 2 + data.constants["move_my"]
        if len(body.trail) == 0 or distance_to_last(body.trail, screen_x, screen_y) > body.min_trail_length:
            body.trail.append((screen_x, screen_y))
            if len(body.trail) > body.max_trail_length:
                body.trail.pop(0)


# Distance from last trail point to current
def distance_to_last(trail: list[tuple], x: float, y: float) -> float:
    if not trail:
        return float('inf')
    last_x, last_y = trail[-1]
    return math.hypot(x - last_x, y - last_y)


def format_ymwd(seconds: int) -> str:
    start = datetime.datetime(1, 1, 1)
    date = start + datetime.timedelta(seconds=seconds)
    y, m, d = date.year - 1, date.month - 1, date.day
    y = '0' + str(y) if y < 10 else str(y)
    m = '0' + str(m) if m < 10 else str(m)
    d = '0' + str(d) if d < 10 else str(d)
    return f"{y} Y : {m} M : {d} D"


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)



