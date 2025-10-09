import math
import data
from math import sqrt, cos, sin

from data import CelestialBody, jupiter_moons


def set_circular_velocity(body, center):
    """
    Устанавливает body.Orbital_speed так, чтобы body был на (примерно) круговой орбите вокруг center.
    Если override_distance задан, используется он (вместо расстояния текущих позиций).
    """
    dx = body.position.x - center.position.x
    dy = body.position.y - center.position.y
    r = math.hypot(dx, dy)
    if r == 0:
        return
    v_mag = math.sqrt(data.constants["G"] * center.mass / r)
    # касательная единичная (CCW): (-dy/r, dx/r)
    tx = -dy / r
    ty = dx / r
    body.Orbital_speed.x = center.Orbital_speed.x + v_mag * tx
    body.Orbital_speed.y = center.Orbital_speed.y + v_mag * ty

# --- убрать суммарный импульс системы (чтобы barycenter был в покое) ---
def remove_system_momentum(bodies):
    px = sum(body.mass * body.Orbital_speed.x for body in bodies)
    py = sum(body.mass * body.Orbital_speed.y for body in bodies)
    M = sum(body.mass for body in bodies)
    vx_cm = px / M
    vy_cm = py / M
    for body in bodies:
        body.Orbital_speed.x -= vx_cm
        body.Orbital_speed.y -= vy_cm

def distance(p1: data.Point, p2: data.Point) -> float: #Distance between 2 points
    return sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)

def law_ug(m1: float, m2: float, R: float, softening = 0) -> float: #Law of Universal Gravitation
    return data.constants["G"] * m1 * m2 / R**2 + softening

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

def update_position(body: CelestialBody, dt: float = 3600) -> None:
    forces = []
    for other_body in data.bodies:
        if other_body == body:
            continue
        force = law_ug(body.mass, other_body.mass, distance(body.position, other_body.position))# The force with which a particular planet is acted upon by another planet
        force_angle = angle(data.Vector(other_body.position.x, other_body.position.y, body.position))  # Angle of said force relative to x
        forces.append((force, force_angle))
    Sum_forces = sum_forces(forces) #The force with which all planets are acted upon by another planet and its direction
    acceleration_res = Sum_forces[0] / body.mass #Momental acceleration
    acceleration = data.Acceleration(acceleration_res * cos(Sum_forces[1]), acceleration_res * sin(Sum_forces[1])) #True acceleration in the Oxy axis
    movement = body.Orbital_speed * dt + acceleration * dt**2 / 2
    body.position += movement #Setting new pos for planet
    body.trail.append(
        (body.position.x * body.scaler * data.constants["scale"] + 735,
        body.position.y * body.scaler * data.constants["scale"] + 478)
    )  # Adding a new part of trail
    if len(body.trail) > body.max_trail_length:
        body.trail.pop(0)
    body.Orbital_speed += acceleration * dt #Setting new speed for planet



