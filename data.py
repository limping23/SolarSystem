from dataclasses import dataclass
from typing import Self


constants = {
    "user_scale": True,
    'G': 6.674e-11,
    'scale': 5e-10,
    "real_scale": 1e-7,
    'time_step': 10,
    "sun_mass": 1.989e30,
    "dt": 1200,
    "scale_m": 1,
    "update_speed": 1
}


class Point:
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    def __add__(self, other) -> Self:
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other) -> Self:
        return Point(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar) -> Self:
        return Point(self.x * scalar, self.y * scalar)

    def __rmul__(self, scalar) -> Self:
        return Point(self.x * scalar, self.y * scalar)

    def __truediv__(self, scalar) -> Self:
        return Point(self.x / scalar, self.y / scalar)


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
        return Vector(self.x1 + scalar * (self.x2 - self.x1), self.y1 +
                      scalar * (self.y2 - self.y1), Point(self.x1, self.y1))

    def __rmul__(self, scalar: float) -> Self:
        return Vector.__mul__(self, scalar)

    def __truediv__(self, scalar: float) -> Self:
        return Vector(self.x1 + (self.x2 - self.x1) / scalar, self.y1 +
                      (self.y2 - self.y1) / scalar, Point(self.x1, self.y1))


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
    trail: list[tuple]
    max_trail_length: float
    scaler: float
    update_counter: int
    trail_update_interval: int
    min_trail_length: float
    screen_x: float
    screen_y: float
    next_pos: Point

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
            "trail": self.trail,
            "max_trail_length": self.max_trail_length,
            "min_trail_length": self.min_trail_length,
            "update_counter": self.update_counter,
            "trail_update_interval": self.trail_update_interval,
            "screen_x": self.screen_x,
            "screen_y": self.screen_y
        }

@dataclass
class Text:
    def __init__(self, text: str, font, bg_color: str, text_color: str):
        self.text = text
        self.font = font
        self.bg_color = bg_color
        self.text_color = text_color


Sun = CelestialBody(
    name='Sun',
    mass=constants['sun_mass'],
    radius=6.9634e8,
    position=Point(0, 0),
    Orbital_speed=OrbitalSpeed(0, 0),
    color="#FFF5C3",
    screen_radius=20,
    scaler=1,
    trail=[],
    max_trail_length=0,
    update_counter=0,
    trail_update_interval=1,
    min_trail_length=0,
    screen_x = 0,
    screen_y = 0,
    next_pos=Point(0, 0)
)

Mercury = CelestialBody(
    name='Mercury',
    mass=3.301e23,
    radius=2.44e6,
    position=Point(5.79e10, 0.0),
    Orbital_speed=OrbitalSpeed(0, 0),
    color="#908D84",
    screen_radius=5,
    scaler=1.2,
    trail=[],
    max_trail_length=500,
    update_counter=0,
    trail_update_interval=3,
    min_trail_length=2.0,
    screen_x = 0,
    screen_y = 0,
    next_pos=Point(0, 0)
)

Venus = CelestialBody(
    name='Venus',
    mass=4.867e24,
    radius=6.052e6,
    position=Point(1.082e11, 0.0),
    Orbital_speed=OrbitalSpeed(0, 0),
    color="#D6C690",
    screen_radius=6,
    scaler=1.18,
    trail=[],
    max_trail_length=400,
    update_counter=0,
    trail_update_interval=3,
    min_trail_length=2.0,
    screen_x = 0,
    screen_y = 0,
    next_pos=Point(0, 0)
)

Earth = CelestialBody(
    name='Earth',
    mass=5.972e24,
    radius=6.371e6,
    position=Point(1.496e11, 0.0),
    Orbital_speed=OrbitalSpeed(0, 0),
    color="#1F75FE",
    screen_radius=6,
    scaler=1.2,
    trail=[],
    max_trail_length=350,
    update_counter=0,
    trail_update_interval=4,
    min_trail_length=2.5,
    screen_x = 0,
    screen_y = 0,
    next_pos=Point(0, 0)
)

Moon = CelestialBody(
    name='Moon',
    mass=7.348e22,
    radius=1.7371e6,
    position=Point(Earth.position.x, Earth.position.y + 3.844e8),
    Orbital_speed=OrbitalSpeed(0,0),
    color="#C2B280",
    screen_radius=3,
    scaler=Earth.scaler,
    trail=[],
    max_trail_length=0,
    update_counter=Earth.update_counter,
    trail_update_interval=Earth.trail_update_interval,
    min_trail_length=Earth.min_trail_length,
    screen_x = 0,
    screen_y = 0,
    next_pos=Point(0, 0)
)

Mars = CelestialBody(
    name='Mars',
    mass=6.417e23,
    radius=3.39e6,
    position=Point(2.279e11, 0.0),
    Orbital_speed=OrbitalSpeed(0, 00),
    color="#C1440E",
    screen_radius=5,
    scaler=1.1,
    trail=[],
    max_trail_length=350,
    update_counter=0,
    trail_update_interval=5,
    min_trail_length=3.0,
    screen_x = 0,
    screen_y = 0,
    next_pos=Point(0, 0)
)

Jupiter = CelestialBody(
    name='Jupiter',
    mass=1.898e27,
    radius=6.9911e7,
    position=Point(7.783e11, 0.0),
    Orbital_speed=OrbitalSpeed(0, 0),
    color="#D2B48C",
    screen_radius=10,
    scaler=0.5,
    trail=[],
    max_trail_length=330,
    update_counter=0,
    trail_update_interval=7,
    min_trail_length=4.0,
    screen_x = 0,
    screen_y = 0,
    next_pos=Point(0, 0)
)

Io = CelestialBody(
    name='Io',
    mass=8.9319e22,
    radius=1.8213e6,
    position=Point(Jupiter.position.x, Jupiter.position.y + 4.217e8),
    Orbital_speed=OrbitalSpeed(0, 0),
    color="#E5B73B",
    screen_radius=2,
    scaler=Jupiter.scaler,
    trail=[],
    max_trail_length=0,
    update_counter=Jupiter.update_counter,
    trail_update_interval=Jupiter.trail_update_interval,
    min_trail_length=Jupiter.min_trail_length,
    screen_x = 0,
    screen_y = 0,
    next_pos=Point(0, 0)
)

Europa = CelestialBody(
    name='Europa',
    mass=4.8e22,
    radius=1.561e6,
    position=Point(Jupiter.position.x, Jupiter.position.y + 6.711e8),
    Orbital_speed=OrbitalSpeed(0, 0),
    color="#D9C7A9",
    screen_radius=2,
    scaler=Jupiter.scaler,
    trail=[],
    max_trail_length=0,
    update_counter=Jupiter.update_counter,
    trail_update_interval=Jupiter.trail_update_interval,
    min_trail_length=Jupiter.min_trail_length,
    screen_x = 0,
    screen_y = 0,
    next_pos=Point(0, 0)
)

Ganymede = CelestialBody(
    name='Ganymede',
    mass=1.48e23,
    radius=2.634e6,
    position=Point(Jupiter.position.x, Jupiter.position.y + 1.070e9),
    Orbital_speed=OrbitalSpeed(0, 0),
    color="#92877D",
    screen_radius=2,
    scaler=Jupiter.scaler,
    trail=[],
    max_trail_length=0,
    update_counter=Jupiter.update_counter,
    trail_update_interval=Jupiter.trail_update_interval,
    min_trail_length=Jupiter.min_trail_length,
    screen_x = 0,
    screen_y = 0,
    next_pos=Point(0, 0)
)

Callisto = CelestialBody(
    name='Callisto',
    mass=1.08e23,
    radius=2.41e6,
    position=Point(Jupiter.position.x, Jupiter.position.y + 1.883e9),
    Orbital_speed=OrbitalSpeed(0, 0),
    color="#5E4B3C",
    screen_radius=2,
    scaler=Jupiter.scaler,
    trail=[],
    max_trail_length=0,
    update_counter=Jupiter.update_counter,
    trail_update_interval=Jupiter.trail_update_interval,
    min_trail_length=Jupiter.min_trail_length,
    screen_x = 0,
    screen_y = 0,
    next_pos=Point(0, 0)
)

Saturn = CelestialBody(
    name='Saturn',
    mass=5.683e26,
    radius=5.8232e7,
    position=Point(1.429e12, 0.0),
    Orbital_speed=OrbitalSpeed(0, 0),
    color="#F5DEB3",
    screen_radius=10,
    scaler=0.39,
    trail=[],
    max_trail_length=500,
    update_counter=0,
    trail_update_interval=9,
    min_trail_length=5.0,
    screen_x = 0,
    screen_y = 0,
    next_pos=Point(0, 0)
)

Uranus = CelestialBody(
    name='Uranus',
    mass=8.681e25,
    radius=2.5362e7,
    position=Point(2.871e12, 0.0),
    Orbital_speed=OrbitalSpeed(0, 0),
    color="#A6E7E3",
    screen_radius=9,
    scaler=0.25,
    trail=[],
    max_trail_length=500,
    update_counter=0,
    trail_update_interval=10,
    min_trail_length=5.0,
    screen_x = 0,
    screen_y = 0,
    next_pos=Point(0, 0)
)

Neptune = CelestialBody(
    name='Neptune',
    mass=1.024e26,
    radius=2.4622e7,
    position=Point(4.504e12, 0.0),
    Orbital_speed=OrbitalSpeed(0, 0),
    color="#2E3DD3",
    screen_radius=9,
    scaler=0.19,
    trail=[],
    max_trail_length=600,
    update_counter=0,
    trail_update_interval=10,
    min_trail_length=5.0,
    screen_x = 0,
    screen_y = 0,
    next_pos=Point(0, 0)
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


Credits = Text(
    text="Made by\n\tArtem Tsygankov\n\tMatvey Nemudrov",
    font=...,
    bg_color="black",
    text_color="white",
)

Controls = Text(
    text="<esc> - quit\t\n<space> - pause\t\n<left-arr> - zoom in\t\n"
         "<right-arr> - zoom out\n<up-arr> - speed up"
         "\t\n      <down-arr> - slow down"
         "\n<E> - hide ui\t",
    font=...,
    bg_color="black",
    text_color="white"
)

Time_text = Text(
    text='',
    font=...,
    bg_color="black",
    text_color="white",
)