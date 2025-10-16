import os
import tkinter as tk
import data
import main
from random import randint
import sys

running = True
user_scale = False
show_trails = True
show_stars = True
show_moons = True
pause_times = 0
time_past = 0
show_text = True
speed_m = 0
visible = True

class App:

    def __init__(self):
        self.tooltip = None
        self.tooltip_text = None
        self.scale = None
        self.root = None
        self.canvas = None
        self.canvas1 = None
        self.button = None
        self.updating = False
        self.stars = []
        self.star_ids = []
        self.planet_ids = []
        self.tooltips = {}
        self.root_elements = {}

    def open_main_root(self):
        if self.root:
            self.root.destroy()
        self.create_main_root()

    def create_main_root(self):
        self.root = tk.Tk()
        self.root.title("Solar System")
        self.root.attributes("-fullscreen", 1)
        self.root.configure(bg="#000000")

        self.canvas = tk.Canvas(self.root, width=self.root.winfo_screenwidth(), highlightthickness=0,
                                height=self.root.winfo_screenheight(), bg="#000000")
        self.root_elements["credits"] = tk.Label(self.root, text="Made by\n\tArtem Tsygankov\n\tMatvey Nemudrov", font=("Helvetica", 12), bg="black", fg="white")
        self.root_elements["credits"].place(x=self.root.winfo_screenwidth()-210, y=self.root.winfo_screenheight()-60)

        self.root_elements["controls"] = tk.Label(self.root, text="<esc> - quit\t\n<space> - pause\t\n<left-arr> - zoom in\t\n"
                                                                  "<right-arr> - zoom out\n<up-arr> - speed up"
                                                                  "\t\n      <down-arr> - slow down"
                                                                  "\n<E> - hide ui\t", font=("Helvetica", 12),
                                                                  bg="black", fg="white")
        self.root_elements["controls"].place(x=-15, y=self.root.winfo_screenheight() - 140)
        self.root_elements["time_text"] = tk.Label(self.root, text="time past: {format_ymwd(time_past)}",
                                                   font=("Helvetica", 12), bg="black", fg="white")
        self.root_elements["time_text"].place(x=10, y=10)

        for i in range(60):
            x = randint(0, self.root.winfo_screenwidth())
            y = randint(0, self.root.winfo_screenheight())
            self.stars.append([x, y])
        self.paint_stars()
        self.canvas.pack()

        self.canvas1 = tk.Canvas(self.root, bg='#000022', width=400, height=self.root.winfo_screenheight() - 750, highlightthickness=0)
        self.canvas1.place(x=self.root.winfo_screenwidth() - 430, y=30)

        self.root_elements["trails_button"] = tk.Button(self.root, highlightcolor="yellow", text="Toggle Trails", command=self.toggle_trails)
        self.root_elements["trails_button"].place(x=self.root.winfo_screenwidth() - 117, y=40)

        self.root_elements["stars_button"] = tk.Button(self.root, highlightcolor="yellow", text="Hide Stars", command=self.hide_stars)
        self.root_elements["stars_button"].place(x=self.root.winfo_screenwidth() - 103, y=70)

        self.root_elements["moons_button"] = tk.Button(self.root, highlightcolor="yellow", text="Hide Moons", command=self.hide_moons)
        self.root_elements["moons_button"].place(x=self.root.winfo_screenwidth() - 115, y=100)

        self.root_elements["reset_button"] = tk.Button(self.root, highlightcolor="yellow", text="Reset", command=self.reset)
        self.root_elements["reset_button"].place(x=self.root.winfo_screenwidth() - 78, y=130)

        self.root_elements["text_button"] = tk.Button(self.root, highlightcolor="yellow", text="Hide Text", command=self.hide_text)
        self.root_elements["text_button"].place(x=self.root.winfo_screenwidth() - 100, y=160)

        self.root.bind("<Escape>", self.quit_program)
        self.root.bind("<space>", self.pause)
        self.root.bind("<Left>", self.scale_add)
        self.root.bind("<Right>", self.scale_red)
        self.root.bind("<Up>", self.add_speed)
        self.root.bind("<Down>", self.red_speed)
        self.root.bind("<E>", self.hide_ui)
        self.root.bind("<e>", self.hide_ui)

        self.root.focus_force()

        self.updating = True
        self.root.after(1, self.update)

    def create_pre_root(self):
        if not self.root:
            self.root = tk.Tk()
            self.root.title("Scale choice")

            root_width = 400
            root_height = 200
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()
            x = (screen_width - root_width) // 2
            y = (screen_height - root_height) // 2
            self.root.geometry(f"{root_width}x{root_height}+{x}+{y}")

            text = tk.Label(self.root, text="Выберите масштаб:", font=("Helvetica", 16))
            text.place(x=100, y=40)
            btn1 = tk.Button(self.root, text="Упрощенный", command=self.user_scale_t, bg="#eae6ca")
            btn1.place(x=70, y=100)
            btn2 = tk.Button(self.root, text="Действительный", command=self.user_scale_f, bg="#eae6ca")
            btn2.place(x=230, y=100)

    def update(self) -> None:
        global time_past
        if not self.updating or not self.root or not self.root.winfo_exists():
            return
        if "time_text" in self.root_elements and visible:
            self.root_elements["time_text"].config(text=f"time past: {format_ymwd(time_past)}")
        if running:
            time_past += (data.constants["time_step"] + speed_m) * data.constants["dt"]
            for i in range(data.constants["time_step"] + speed_m):
                for body in data.bodies:
                    if body.name == "Sun":
                        continue
                    main.update_position(body)
                for body in data.bodies:
                    body.position = body.next_pos

        if show_stars:
            for item in self.canvas.find_all():
                if item not in self.star_ids:
                    self.canvas.delete(item)
        else:
            self.canvas.delete("all")

        for body in data.bodies:
            if show_trails and len(body.trail) > 1:
                self.canvas.create_line(body.trail, fill=body.color, width=1, smooth=True)

        for body in data.bodies:
            add_coord = data.Point(0, 0)
            body.screen_x = body.position.x * body.scaler * data.constants["scale_m"] * data.constants["scale"] + 735
            body.screen_y = body.position.y * body.scaler * data.constants["scale_m"] * data.constants["scale"] + 478
            if body.name == "Moon":
                add_coord = data.Point(data.Earth.screen_x - body.screen_x, data.Earth.screen_y - body.screen_y)
                body.screen_x = data.Earth.screen_x + add_coord.x * 27
                body.screen_y = data.Earth.screen_y + add_coord.y * 27
            if body.name in data.jupiter_moons:
                add_coord = data.Point(data.Jupiter.screen_x - body.screen_x, data.Jupiter.screen_y - body.screen_y)
                match body.name:
                    case "Io":
                        scale = 18
                    case "Europa":
                        scale = 20
                    case "Ganymede":
                        scale = 22
                    case "Callisto":
                        scale = 23
                body.screen_x = data.Jupiter.screen_x + add_coord.x * scale
                body.screen_y = data.Jupiter.screen_y + add_coord.y * scale

            if body.name == "Moon" and not show_moons:
                continue

            if body.name in data.jupiter_moons and not show_moons:
                continue

            planet_id = self.canvas.create_oval(
                body.screen_x - body.screen_radius * data.constants["scale_m"],
                body.screen_y - body.screen_radius * data.constants["scale_m"],
                body.screen_x + body.screen_radius * data.constants["scale_m"],
                body.screen_y + body.screen_radius * data.constants["scale_m"],
                fill=body.color,
                outline=""
            )
            if body.name == "Saturn":
                self.canvas.create_oval(body.screen_x - (body.screen_radius + 10) * data.constants["scale_m"],
                                        body.screen_y - (body.screen_radius + 10) * data.constants["scale_m"],
                                        body.screen_x + (body.screen_radius + 10) * data.constants["scale_m"],
                                        body.screen_y + (body.screen_radius + 10) * data.constants["scale_m"],
                                        outline="#ceb8b8", width=6 * data.constants["scale_m"])

            self.bind_planet_tooltip(planet_id, body.name, body.mass, body.radius, body.screen_x, body.screen_y)
            if show_text:
                self.canvas.create_text(body.screen_x,
                                        body.screen_y - body.screen_radius * data.constants["scale_m"] - 10,
                                        text=body.name,
                                        fill="white")

        main.remove_system_momentum(data.bodies)

        if self.updating and self.root and self.root.winfo_exists():
            self.root.after(1, self.update)

    def quit_program(self, event=None) -> None:
        self.remove_all_tooltips()
        self.root.destroy()

    def run(self):
        self.create_pre_root()
        self.root.mainloop()

    def paint_stars(self):
        for i in self.stars:
            p = self.canvas.create_oval(i[0], i[1], i[0] + 2, i[1] + 2, fill='white', outline='white')
            self.star_ids.append(p)

    def pause(self, event=None):
        global running
        global pause_times
        running = not running
        pause_times += 1


    @staticmethod
    def toggle_trails() -> None:
        global show_trails
        show_trails = not show_trails

    def user_scale_t(self):
        global user_scale
        user_scale = True
        return self.open_main_root()

    def user_scale_f(self):
        global user_scale
        user_scale = False
        return self.open_main_root()

    def hide_stars(self):
        global show_stars
        show_stars = not show_stars
        if show_stars:
            self.paint_stars()

    @staticmethod
    def hide_moons():
        global show_moons
        show_moons = not show_moons

    def reset(self):
        self.root.destroy()
        os.execv(sys.executable, [sys.executable] + sys.argv)

    @staticmethod
    def scale_add(event=None):
        data.constants["scale_m"] += 0.5
        for body in data.bodies:
            body.trail.clear()

    @staticmethod
    def scale_red(event=None):
        if data.constants["scale_m"] > 1:
            data.constants["scale_m"] -= 0.5
            for body in data.bodies:
                body.trail.clear()

    @staticmethod
    def hide_text():
        global show_text
        show_text = not show_text

    @staticmethod
    def add_speed(event=None):
        global speed_m
        if speed_m <= 290:
            speed_m += 10

    @staticmethod
    def red_speed(event=None):
        global speed_m
        if speed_m >= 20:
            speed_m -= 10

    def bind_planet_tooltip(self, planet_id, name, mass, radius, x, y):
        def show_tooltip(event):
            self.tooltip = tk.Toplevel(self.root)
            self.tooltip.wm_overrideredirect(True)
            self.tooltip.configure(bg="lightyellow")
            self.tooltip_text = tk.Label(self.tooltip, background="black", fg="white", font=("Helvetica", 10))
            self.tooltip_text.pack()
            self.tooltip.withdraw()
            self.tooltip_text.config(text=f"{name}\nMass: {mass} kg\nRadius: {radius//1000} km\nX: {round(x, 2)}, Y: {round(y, 2)}")
            self.tooltip.wm_geometry(f"+{self.root.winfo_screenwidth()-160}+{self.root.winfo_screenheight()-700}")
            self.tooltip.deiconify()

        def hide_tooltip(event):
            self.tooltip.withdraw()

        self.canvas.tag_bind(planet_id, "<Enter>", show_tooltip)
        self.canvas.tag_bind(planet_id, "<Leave>", hide_tooltip)

        self.tooltips[planet_id] = self.tooltip

    def remove_all_tooltips(self):
        for planet_id, tooltip in self.tooltips.items():
            if tooltip and tooltip.winfo_exists():
                tooltip.destroy()
        self.tooltips = {}

    def hide_ui(self, event=None):
        global visible
        visible = not visible

        if visible:
            self.root_elements["credits"].place(x=self.root.winfo_screenwidth() - 210,
                                              y=self.root.winfo_screenheight() - 60)
            self.root_elements["controls"].place(x=-15, y=self.root.winfo_screenheight() - 120)
            self.root_elements["time_text"].place(x=10, y=10)
            self.root_elements["trails_button"].place(x=self.root.winfo_screenwidth() - 117, y=40)
            self.root_elements["stars_button"].place(x=self.root.winfo_screenwidth() - 103, y=70)
            self.root_elements["moons_button"].place(x=self.root.winfo_screenwidth() - 115, y=100)
            self.root_elements["reset_button"].place(x=self.root.winfo_screenwidth() - 78, y=130)
            self.root_elements["text_button"].place(x=self.root.winfo_screenwidth() - 100, y=160)
            self.canvas1.place(x=self.root.winfo_screenwidth() - 430, y=30)
        else:
            for element in self.root_elements.values():
                element.place_forget()
            self.canvas1.place_forget()


def seconds_to_ymwd(seconds: int, year_days: int = 365, month_days: int = 30) -> tuple:
    s = abs(int(seconds))
    seconds_d = 86400
    days = s // seconds_d

    years = days // year_days
    days = days % year_days

    months = days // month_days
    days = days % month_days

    weeks = days // 7
    days = days % 7

    return years, months, weeks, days


def format_ymwd(seconds: int, year_days: int = 365, month_days: int = 30) -> str:
    y, m, w, d = seconds_to_ymwd(seconds, year_days, month_days)
    return f"{y} Y : {m} M : {w} W : {d} D"


for body in data.bodies:
    if body.name == "Sun":
        continue
    if body.name == "Moon":
        main.set_circular_velocity(body, data.Earth)
    elif body.name in data.jupiter_moons:
        main.set_circular_velocity(body, data.Jupiter)
    else:
        main.set_circular_velocity(body, data.Sun)


app = App()
app.run()