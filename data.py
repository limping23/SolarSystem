from dataclasses import dataclass
from typing import Self


constants = {
    'G': 6.674e-11,
    'scale': 5e-10,
    'time_step': 150,
    "sun_mass": 1.989e30,
    "dt": 750
}


class Point:
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    def __add__(self, other) -> Self:
        return Point(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other) -> Self:
        return Point(self.x - other.x, self.y - other.y)


class Vector:
    def __init__(self, x1: float, y1: float, origin: Point) -> None:
        self.x2 = x1
        self.y2 = y1
        self.x1 = origin.x
        self.y1 = origin.y

    def __add__(self, other) -> Self:
        return Vector(self.x2 + other.x2 - other.x1, self.y2 + other.y2 - other.y1, Point(self.x1, self.y1))

    def __sub__(self, other) -> Self:
        return Vector(self.x2 - other.x2 + other.x1, self.y2 - other.y2 + other.y1, Point(self.x1, self.y1))

    def __mul__(self, scalar: float) -> Self:
        return Vector(self.x1 + scalar * (self.x2 - self.x1), self.y1 + scalar * (self.y2 - self.y1), Point(self.x1, self.y1))

    def __rmul__(self, scalar: float) -> Self:
        return Vector.__mul__(self, scalar)

    def __truediv__(self, scalar: float) -> Self:
        return Vector(self.x1 + (self.x2 - self.x1) / scalar, self.y1 + (self.y2 - self.y1) / scalar, Point(self.x1, self.y1))


class OrbitalSpeed:
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    def __add__(self, other) -> Self:
        return OrbitalSpeed(self.x + other.x, self.y + other.y)

    def __sub__(self, other) -> Self:
        return OrbitalSpeed(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar: float) -> Self:
        return OrbitalSpeed(self.x * scalar, self.y * scalar)

    def __rmul__(self, scalar: float) -> Self:
        return self * scalar

    def __truediv__(self, scalar: float) -> Self:
        return OrbitalSpeed(self.x / scalar, self.y / scalar)


class Acceleration:
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    def __add__(self, other) -> Self:
        return Acceleration(self.x + other.x, self.y + other.y)

    def __sub__(self, other) -> Self:
        return Acceleration(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar: float) -> Self:
        return Acceleration(self.x * scalar, self.y * scalar)

    def __rmul__(self, scalar: float) -> Self:
        return self * scalar

    def __truediv__(self, scalar: float) -> Self:
        return Acceleration(self.x / scalar, self.y / scalar)


@dataclass
class CelestialBody:
    name: str
    mass: float
    radius: float
    position: Point
    Orbital_speed: OrbitalSpeed
    color: str
    screen_radius: float
    trail: list
    max_trail_length: float
    scaler: float
    update_counter: int
    trail_update_interval: int
    min_trail_length: float

    @property
    def info(self) -> dict:
        return {
            "name": self.name,
            "mass": self.mass,
            "radius": self.radius,
            "position": (self.position.x, self.position.y),
            "Orbital_speed": (self.Orbital_speed.x, self.Orbital_speed.y),
            "colour": self.color,
            "screen_radius": self.screen_radius,
        }

    
Sun = CelestialBody(
    name = 'Sun',
    mass = constants['sun_mass'],
    radius = 6.9634e8,
    position = Point(0,0),
    Orbital_speed = OrbitalSpeed(0,0),
    color="#FFF5C3",
    screen_radius = 20,
    scaler = 1,
    trail = [],
    max_trail_length = 0,
    update_counter = 0,
    trail_update_interval = 1,
    min_trail_length = 0
)

Mercury = CelestialBody(
    name = 'Mercury',
    mass = 3.301e23,
    radius = 2.44e6,
    position = Point(5.79e10, 0.0),
    Orbital_speed = OrbitalSpeed(0,47870),
    color="#908D84",
    screen_radius = 5,
    scaler = 1.2,
    trail = [],
    max_trail_length = 500,
    update_counter = 0,
    trail_update_interval = 3,
    min_trail_length = 2.0
)

Venus = CelestialBody(
    name = 'Venus',
    mass = 4.867e24,
    radius = 6.052e6,
    position = Point(1.082e11, 0.0),
    Orbital_speed = OrbitalSpeed(0,35020),
    color="#D6C690",
    screen_radius = 6,
    scaler = 1.18,
    trail = [],
    max_trail_length = 400,
    update_counter = 0,
    trail_update_interval = 3,
    min_trail_length = 2.0
)

Earth = CelestialBody(
    name = 'Earth',
    mass = 5.972e24,
    radius = 6.371e6,
    position = Point(1.496e11, 0.0),
    Orbital_speed = OrbitalSpeed(0,29780),
    color="#1F75FE",
    screen_radius = 6,
    scaler = 1.2,
    trail = [],
    max_trail_length = 350,
    update_counter = 0,
    trail_update_interval = 4,
    min_trail_length = 2.5
)

Moon = CelestialBody(
    name = 'Moon',
    mass = 7.342e22,
    radius = 1.737e6,
    position = Point(Earth.position.x, Earth.position.y + 3.844e8),
    Orbital_speed = OrbitalSpeed(Earth.Orbital_speed.x, Earth.Orbital_speed.y + 1023),
    color="#C2B280",
    screen_radius = 3,
    scaler = 1.36,
    trail = [],
    max_trail_length = 0,
    update_counter = Earth.update_counter,
    trail_update_interval = Earth.trail_update_interval,
    min_trail_length = Earth.min_trail_length,
)

Mars = CelestialBody(
    name = 'Mars',
    mass = 6.417e23,
    radius = 3.39e6,
    position = Point(2.279e11, 0.0),
    Orbital_speed = OrbitalSpeed(0,24070),
    color="#C1440E",
    screen_radius = 5,
    scaler = 1.1,
    trail = [],
    max_trail_length = 350,
    update_counter = 0,
    trail_update_interval = 5,
    min_trail_length = 3.0
)

Jupiter = CelestialBody(
    name = 'Jupiter',
    mass = 1.898e27,
    radius = 6.9911e7,
    position = Point(7.783e11, 0.0),
    Orbital_speed = OrbitalSpeed(0,13070),
    color="#D2B48C",
    screen_radius = 10,
    scaler = 0.5,
    trail = [],
    max_trail_length = 330,
    update_counter = 0,
    trail_update_interval = 7,
    min_trail_length = 4.0
)

Io = CelestialBody(
    name = 'Io',
    mass = 8.93e22,
    radius = 1.821e6,
    position = Point(Jupiter.position.x, Jupiter.position.y + 4.217e8),
    Orbital_speed = OrbitalSpeed(Jupiter.Orbital_speed.x, Jupiter.Orbital_speed.y + 17330),
    color="#E5B73B",
    screen_radius = 2,
    scaler = 0.46,
    trail = [],
    max_trail_length = 0,
    update_counter = Jupiter.update_counter,
    trail_update_interval = Jupiter.trail_update_interval,
    min_trail_length = Jupiter.min_trail_length,
)

Europa = CelestialBody(
    name = 'Europa',
    mass = 4.8e22,
    radius = 1.561e6,
    position = Point(Jupiter.position.x, Jupiter.position.y + 6.711e8),
    Orbital_speed = OrbitalSpeed(Jupiter.Orbital_speed.x, Jupiter.Orbital_speed.y + 13740),
    color="#D9C7A9",
    screen_radius = 2,
    scaler = 0.45,
    trail = [],
    max_trail_length = 0,
    update_counter = Jupiter.update_counter,
    trail_update_interval = Jupiter.trail_update_interval,
    min_trail_length = Jupiter.min_trail_length,
)

Ganymede = CelestialBody(
    name = 'Ganymede',
    mass = 1.48e23,
    radius = 2.634e6,
    position = Point(Jupiter.position.x, Jupiter.position.y + 1.070e9),
    Orbital_speed = OrbitalSpeed(Jupiter.Orbital_speed.x, Jupiter.Orbital_speed.y + 10880),
    color="#92877D",
    screen_radius = 2,
    scaler = 0.44,
    trail = [],
    max_trail_length = 0,
    update_counter = Jupiter.update_counter,
    trail_update_interval = Jupiter.trail_update_interval,
    min_trail_length = Jupiter.min_trail_length,
)

Callisto = CelestialBody(
    name = 'Callisto',
    mass = 1.08e23,
    radius = 2.41e6,
    position = Point(Jupiter.position.x, Jupiter.position.y + 1.883e9),
    Orbital_speed = OrbitalSpeed(Jupiter.Orbital_speed.x, Jupiter.Orbital_speed.y + 8200),
    color="#5E4B3C",
    screen_radius = 2,
    scaler = 0.42,
    trail = [],
    max_trail_length = 0,
    update_counter = Jupiter.update_counter,
    trail_update_interval = Jupiter.trail_update_interval,
    min_trail_length = Jupiter.min_trail_length,
)

Saturn = CelestialBody(
    name = 'Saturn',
    mass = 5.683e26,
    radius = 5.8232e7,
    position = Point(1.429e12, 0.0),
    Orbital_speed = OrbitalSpeed(0,9690),
    color="#F5DEB3",
    screen_radius = 10,
    scaler = 0.39,
    trail = [],
    max_trail_length = 500,
    update_counter = 0,
    trail_update_interval = 9,
    min_trail_length = 5.0
)

Uranus = CelestialBody(
    name = 'Uranus',
    mass = 8.681e25,
    radius = 2.5362e7,
    position = Point(2.871e12, 0.0),
    Orbital_speed = OrbitalSpeed(0,6810),
    color="#A6E7E3",
    screen_radius = 9,
    scaler = 0.25,
    trail = [],
    max_trail_length = 500,
    update_counter = 0,
    trail_update_interval = 10,
    min_trail_length = 5.0
)

Neptune = CelestialBody(
    name = 'Neptune',
    mass = 1.024e26,
    radius = 2.4622e7,
    position = Point(4.504e12, 0.0),
    Orbital_speed = OrbitalSpeed(0,5430),
    color="#2E3DD3",
    screen_radius = 9,
    scaler = 0.19,
    trail = [],
    max_trail_length = 600,
    update_counter = 0,
    trail_update_interval = 10,
    min_trail_length = 5.0
)


bodies = [
    Sun,
    Mercury,
    Venus,
    Earth, 
    Moon,
    Mars,
    Jupiter,
    Io,
    Europa,
    Ganymede,
    Callisto,
    Saturn, 
    Uranus, 
    Neptune
]

jupiter_moons = [
    "Io",
    "Europa",
    "Ganymede",
    "Callisto"
]

