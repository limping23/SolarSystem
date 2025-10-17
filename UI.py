import tkinter as tk
import data
import main
from random import randint
import tkinter.font as tkFont
import pygame
import webbrowser
import threading
import math


running = True
show_trails = True
show_stars = True
show_moons = True
pause_times = 0
time_past = 0
show_text = True
visible = True
joker = False


pygame.mixer.init()
pygame.mixer.music.load('Hans_Zimmer_-_S.T.A.Y._Interstellar_Main_Theme_(SkySound.cc).mp3')
pygame.mixer.music.play(-1)


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

        self.canvas = tk.Canvas(self.root, width=self.root.winfo_screenwidth(), highlightthickness=0,height=self.root.winfo_screenheight(), bg="#000000")

        data.Credits.font = tkFont.Font(family='Helvetica', size=12, weight='bold')
        self.root_elements["credits"] = tk.Label(self.root, text=data.Credits.text, font=data.Credits.font, bg=data.Credits.bg_color, fg=data.Credits.text_color)
        self.root_elements["credits"].place(x=self.root.winfo_screenwidth()-180, y=self.root.winfo_screenheight()-100)

        data.Controls.font = tkFont.Font(family='Helvetica', size=12, weight='bold')
        self.root_elements["controls"] = tk.Label(self.root, text=data.Controls.text, font=data.Controls.font, bg=data.Controls.bg_color, fg=data.Controls.text_color)
        self.root_elements["controls"].place(x=-15, y=self.root.winfo_screenheight() - 140)

        data.Time_text.font = tkFont.Font(family='Magneto', size=48, weight='bold')
        data.Time_text.text = f"{main.format_ymwd(time_past)}"
        self.root_elements["time_text"] = tk.Label(self.root, text=data.Time_text.text, font=data.Time_text.font, bg=data.Time_text.bg_color, fg=data.Time_text.text_color)
        self.root_elements["time_text"].place(x=(self.root.winfo_screenwidth() - data.Time_text.font.measure(data.Time_text.text)) / 2, y=self.root.winfo_screenheight()-170)

        for i in range(60):
            x = randint(0, self.root.winfo_screenwidth())
            y = randint(0, self.root.winfo_screenheight())
            self.stars.append([x, y])
        self.paint_stars()
        self.canvas.pack()

        self.root_elements["trails_button"] = tk.Button(self.root, text="Toggle Trails", command=self.toggle_trails)
        self.root_elements["trails_button"].place(x=self.root.winfo_screenwidth() - 117, y=0)

        self.root_elements["stars_button"] = tk.Button(self.root, text="Hide Stars", command=self.hide_stars)
        self.root_elements["stars_button"].place(x=self.root.winfo_screenwidth() - 103, y=30)

        self.root_elements["moons_button"] = tk.Button(self.root, text="Hide Moons", command=self.hide_moons)
        self.root_elements["moons_button"].place(x=self.root.winfo_screenwidth() - 115, y=60)

        self.root_elements["text_button"] = tk.Button(self.root, text="Hide Text", command=self.hide_text)
        self.root_elements["text_button"].place(x=self.root.winfo_screenwidth() - 100, y=90)

        self.root.bind("<Escape>", self.quit_program)
        self.root.bind("<space>", self.pause)
        self.root.bind("<Right>", self.scale_add)
        self.root.bind("<Left>", self.scale_red)
        self.root.bind("<Up>", self.add_speed)
        self.root.bind("<Down>", self.red_speed)
        self.root.bind("<E>", self.hide_ui)
        self.root.bind("<e>", self.hide_ui)

        self.root.focus_force()

        self.updating = True
        self.root.after(data.constants["update_speed"], self.update)

    def create_pre_root(self):
        if not self.root:
            self.root = tk.Tk()
            self.root.title("Scale choice")
            self.root.attributes("-fullscreen", True)

            font = tkFont.Font(family='Helvetica', size=30, weight='bold')
            text = tk.Label(self.root, text="Выберите масштаб", font=font)
            text.place(x=(self.root.winfo_screenwidth() - font.measure("Выберите масштаб")) / 2, y=400)
            btn1 = tk.Button(self.root, text="   Упрощенный   ", command=self.user_scale_t, bg="#eae6ca")
            btn2 = tk.Button(self.root, text="Действительный", command=self.user_scale_f, bg="#eae6ca")
            btn1.place(x=(self.root.winfo_screenwidth() - 278) // 2.2, y=500)
            btn2.place(x=(self.root.winfo_screenwidth() - 278) // 1.5, y=500)

    def update(self) -> None:
        global time_past
        if not self.updating or not self.root or not self.root.winfo_exists():
            return
        if "time_text" in self.root_elements and visible:
            self.root_elements["time_text"].config(text=f"{main.format_ymwd(time_past)}")
        if running:
            time_past += data.constants["time_step"] * data.constants["dt"]
            for i in range(data.constants["time_step"]):
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

        if data.constants["user_scale"]:
            for body in data.bodies:
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

                if (body.name == "Moon" or body.name in data.jupiter_moons) and not show_moons:
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

                self.bind_planet_tooltip(planet_id, body.name, body.mass, body.radius, math.hypot(body.Orbital_speed.x, body.Orbital_speed.y), body.screen_x, body.screen_y)
                if show_text:
                    self.canvas.create_text(body.screen_x,
                                            body.screen_y - body.screen_radius * data.constants["scale_m"] - 10,
                                            text=body.name,
                                            fill="white")
        else:
            for body in data.bodies:
                body.screen_x = body.position.x * data.constants["real_scale"] * data.constants["scale_m"] + 735
                body.screen_y = body.position.y * data.constants["real_scale"] * data.constants["scale_m"] + 478

                if body.name == "Moon" or body.name in data.jupiter_moons and not show_moons:
                    continue

                planet_id = self.canvas.create_oval(
                    body.screen_x - body.radius * data.constants["real_scale"] * data.constants["scale_m"],
                    body.screen_y - body.radius * data.constants["real_scale"] * data.constants["scale_m"],
                    body.screen_x + body.radius * data.constants["real_scale"] * data.constants["scale_m"],
                    body.screen_y + body.radius * data.constants["real_scale"] * data.constants["scale_m"],
                    fill=body.color,
                    outline=""
                )
                if body.name == "Saturn":
                    self.canvas.create_oval(body.position.x - 146e5 * data.constants["real_scale"] * data.constants["scale_m"],
                                            body.position.y - 146e5 * data.constants["real_scale"] * data.constants["scale_m"],
                                            body.position.x + 146e5 * data.constants["real_scale"] * data.constants["scale_m"],
                                            body.position.y + 146e5 * data.constants["real_scale"] * data.constants["scale_m"],
                                            outline="#ceb8b8", width=533e5 * data.constants["real_scale"] * data.constants["scale_m"])
                self.bind_planet_tooltip(planet_id, body.name, body.mass, body.radius, math.hypot(body.Orbital_speed.x, body.Orbital_speed.y), body.position.x, body.position.y)

        # print(data.Saturn.info)
        main.remove_system_momentum(data.bodies)
        print(data.constants)
        if self.updating and self.root and self.root.winfo_exists():
            self.root.after(data.constants["update_speed"], self.update)

    def quit_program(self, event=None) -> None:
        self.remove_all_tooltips()
        self.root.destroy()

    def run(self):
        self.create_pre_root()
        self.root.mainloop()

    def paint_stars(self):
        if data.constants["user_scale"]:
            for i in self.stars:
                p = self.canvas.create_oval(i[0], i[1], i[0] + 2, i[1] + 2, fill='white', outline='white')
                self.star_ids.append(p)
        else:
            for i in self.stars:
                p = self.canvas.create_oval(i[0], i[1], i[0], i[1], fill='white')
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
        data.constants["user_scale"] = True
        return self.open_main_root()

    def user_scale_f(self):
        global show_trails, show_moons, show_stars
        data.constants["user_scale"] = False
        show_trails = False
        show_moons = False
        show_stars = False
        return self.open_main_root()

    def hide_stars(self):
        global show_stars, pause_times, joker
        show_stars = not show_stars
        if show_stars:
            self.paint_stars()
        if pause_times >= 5 and not joker:
            joker = not joker
            threading.Thread(target=lambda: webbrowser.open("https://youtu.be/dQw4w9WgXcQ?si=EScuTA7EVvjQaglx"), daemon=True).start()


    @staticmethod
    def hide_moons():
        global show_moons
        show_moons = not show_moons

    @staticmethod
    def scale_add(event=None):
        if data.constants["user_scale"]:
            data.constants["scale_m"] += 0.5
            for body in data.bodies:
                body.trail.clear()
        else:
            data.constants["scale_m"] += 0.01
            for body in data.bodies:
                body.trail.clear()

    @staticmethod
    def scale_red(event=None):
        if data.constants["user_scale"]:
            if data.constants["scale_m"] >= 0.6:
                data.constants["scale_m"] -= 0.5
                for body in data.bodies:
                    body.trail.clear()
        else:
            if data.constants["scale_m"] >= 0.2:
                data.constants["scale_m"] -= 0.1
                for body in data.bodies:
                    body.trail.clear()
            elif data.constants["scale_m"] >= 0.02:
                data.constants["scale_m"] -= 0.01
                for body in data.bodies:
                    body.trail.clear()
            elif data.constants["scale_m"] >= 0.002:
                data.constants["scale_m"] -= 0.001
                for body in data.bodies:
                    body.trail.clear()

    @staticmethod
    def hide_text():
        global show_text
        show_text = not show_text

    @staticmethod
    def add_speed(event=None):
        if data.constants["update_speed"] >= 11:
            data.constants["update_speed"] -= 10
        elif data.constants["update_speed"] >= 2:
            data.constants["update_speed"] -= 1
        elif data.constants["dt"] <= 1191:
            data.constants["dt"] += 10
        elif data.constants["time_step"] <= 270:
            data.constants["time_step"] += 5

    @staticmethod
    def red_speed(event=None):
        if data.constants["time_step"] >= 4:
            data.constants["time_step"] -= 3
        elif data.constants["time_step"] >= 2:
            data.constants["time_step"] -= 1
        else:
            if data.constants["dt"] >= 11:
                data.constants["dt"] -= 10
            elif data.constants["dt"] >= 2:
                data.constants["dt"] -= 1
            else:
                if data.constants["update_speed"] <= 90:
                    data.constants["update_speed"] += 10
                elif data.constants["update_speed"] < 100:
                    data.constants["update_speed"] += 9

    def bind_planet_tooltip(self, planet_id, name, mass, radius, speed, x, y):
        def show_tooltip(event):
            if self.tooltip:
                self.tooltip.destroy()
                self.tooltip_text.destroy()
            self.tooltip = tk.Toplevel(self.root)
            self.tooltip.wm_overrideredirect(True)
            self.tooltip.configure(bg="lightyellow")
            self.tooltip_text = tk.Label(self.tooltip, background="black", fg="white", font=("Helvetica", 10))
            self.tooltip_text.pack()
            self.tooltip.withdraw()
            if data.constants["user_scale"]:
                self.tooltip_text.config(
                    text=f"{name}\nMass: {mass} kg\nRadius: {radius} m\nSpeed: {speed} m/s\nX: {round(x, 2)}, Y: {round(y, 2)}")
            self.tooltip_text.config(text=f"{name}\nMass: {mass} kg\nRadius: {radius} m\nSpeed: {speed} m/s\nX: {round(x*data.constants["scale_m"], 2)}e7, Y: {round(y*data.constants["scale_m"], 2)}e7")
            self.tooltip.wm_geometry(f"+{self.root.winfo_screenwidth()-250}+{self.root.winfo_screenheight()-700}")
            self.tooltip.deiconify()

        def hide_tooltip(event):
            self.tooltip.destroy()
            self.tooltip_text.destroy()

        if not running:
            self.canvas.tag_bind(planet_id, "<Button-1>", show_tooltip)
            self.root.bind("<Button-2>", hide_tooltip)

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
            self.root_elements["credits"].place(x=self.root.winfo_screenwidth() - 180, y=self.root.winfo_screenheight() - 100)
            self.root_elements["controls"].place(x=-15, y=self.root.winfo_screenheight() - 120)
            self.root_elements["time_text"].place(x=(self.root.winfo_screenwidth() - data.Time_text.font.measure(data.Time_text.text)) / 2, y=self.root.winfo_screenheight()-170)
            self.root_elements["trails_button"].place(x=self.root.winfo_screenwidth() - 117, y=0)
            self.root_elements["stars_button"].place(x=self.root.winfo_screenwidth() - 103, y=30)
            self.root_elements["moons_button"].place(x=self.root.winfo_screenwidth() - 115, y=60)
            if data.constants["user_scale"]:
                self.root_elements["text_button"].place(x=self.root.winfo_screenwidth() - 100, y=90)
        else:
            for element in self.root_elements.values():
                element.place_forget()


for body in data.bodies:
    if body.name == "Sun":
        continue
    if body.name == "Moon":
        main.set_circular_velocity(body, data.Earth)
    elif body.name in data.jupiter_moons:
        main.set_circular_velocity(body, data.Jupiter)
    else:
        main.set_circular_velocity(body, data.Sun)