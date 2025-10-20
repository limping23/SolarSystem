import tkinter as tk
from tkinter import ttk
import data
import main
from random import randint
import tkinter.font as tkFont
import pygame
import webbrowser
import threading
import math


center_is_jupiter = False
kepler_check = False
running = True
show_trails = True
show_stars = True
show_moons = True
pause_times = 0
time_past = 0
show_text = True
visible = True
joker = False
blackhole = False
BHHighlight = True
start_bh = True

pygame.mixer.init()
pygame.mixer.music.load(main.resource_path('files/Hans_Zimmer_-_S.T.A.Y._Interstellar_Main_Theme_(SkySound.cc).mp3'))
pygame.mixer.music.play(-1)


class App:

    def __init__(self) -> None:
        self.value_label = None
        self.planet_combobox = None
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
        self.planet_multipliers = {}
        self.current_planet = None

    def open_main_root(self) -> None:
        if self.root:
            self.root.destroy()
        self.create_main_root()

    def create_main_root(self) -> None:
        global start_bh
        self.root = tk.Tk()
        data.constants["root_info"] = (self.root.winfo_screenwidth(), self.root.winfo_screenheight())
        self.root.title("Solar System")
        self.root.attributes("-fullscreen", 1)
        self.root.configure(bg="#000000")

        self.canvas = tk.Canvas(self.root, width=self.root.winfo_screenwidth(), highlightthickness=0,height=self.root.winfo_screenheight(), bg="#000000")

        data.Credits.font = tkFont.Font(family='Helvetica', size=12, weight='bold')
        self.root_elements["credits"] = tk.Label(self.root, text=data.Credits.text, font=data.Credits.font, bg=data.Credits.bg_color, fg=data.Credits.text_color)


        data.Controls.font = tkFont.Font(family='Helvetica', size=12, weight='bold')
        self.root_elements["controls"] = tk.Label(self.root, text=data.Controls.text, font=data.Controls.font, bg=data.Controls.bg_color, fg=data.Controls.text_color)


        data.Time_text.font = tkFont.Font(family='Magneto', size=48, weight='bold')
        data.Time_text.text = f"{main.format_ymwd(time_past)}"
        self.root_elements["time_text"] = tk.Label(self.root, text=data.Time_text.text, font=data.Time_text.font, bg=data.Time_text.bg_color, fg=data.Time_text.text_color)

        for i in range(60):
            x = randint(0, self.root.winfo_screenwidth())
            y = randint(0, self.root.winfo_screenheight())
            self.stars.append([x, y])
        self.paint_stars()
        self.canvas.pack()

        self.root_elements["trails_button"] = tk.Button(self.root, text="Hide Trails", command=self.toggle_trails)
        self.root_elements["stars_button"] = tk.Button(self.root, text="Hide Stars", command=self.hide_stars)
        self.root_elements["moons_button"] = tk.Button(self.root, text="Hide Moons", command=self.hide_moons)
        self.root_elements["IsBH"] = tk.Button(self.root, text="Spawn Black Hole", command=self.spawn)
        self.root_elements["BHHighlight"] = tk.Button(self.root, text="Highlight Black Hole", command=self.BHHighlight)
        self.root_elements["text_button"] = tk.Button(self.root, text="Hide Text", command=self.hide_text)
        if not blackhole and not kepler_check:
                start_bh = False
                for body in data.bodies:
                    self.planet_multipliers[body.name] = 1.0
                self.multiplier_var = tk.DoubleVar()
                self.planet_var = tk.StringVar()
                planet_names = [body.name for body in data.bodies if body.name != "BlackHole"]
                self.root_elements["planet_combobox"] = ttk.Combobox(self.root, textvariable=self.planet_var, values=planet_names, state="readonly")
                self.root_elements["planet_combobox"].set("Change planet mass")
                self.root_elements["planet_combobox"].bind('<<ComboboxSelected>>', self.on_planet_select)

        self.multiplier_var = tk.DoubleVar(value=1.0)
        self.root_elements["planet_scale"] = tk.Scale(self.root,
                                                      from_=0.1,
                                                      to=10.0,
                                                      resolution=0.1,
                                                      orient=tk.HORIZONTAL,
                                                      variable=self.multiplier_var,
                                                      command=self.on_multiplier_change,
                                                      length=200,
                                                      showvalue=True,
                                                      )
        self.root_elements["planet_scale_text"] = tk.Label(self.root, text="Mass Multiplier: 1.0", fg="white",
                                                           bg="#000000")

        self.root.update_idletasks()

        self.root_elements["credits"].place(
            x=self.root.winfo_screenwidth() - self.root_elements["credits"].winfo_reqwidth(),
            y=self.root.winfo_screenheight() - self.root_elements["credits"].winfo_reqheight() * 2)
        self.root_elements["controls"].place(
            x=0,
            y=self.root.winfo_screenheight() - self.root_elements["controls"].winfo_reqheight() * 1.5)
        self.root_elements["time_text"].place(
            x=(self.root.winfo_screenwidth() - data.Time_text.font.measure(data.Time_text.text)) / 2,
            y=self.root.winfo_screenheight() - 170)
        self.root_elements["trails_button"].place(x=self.root.winfo_screenwidth() - self.root_elements["trails_button"].winfo_reqwidth(), y=0)
        self.root_elements["stars_button"].place(x=self.root.winfo_screenwidth() - self.root_elements["stars_button"].winfo_reqwidth(), y=30)
        if not kepler_check and len(data.bodies) > 5:
            self.root_elements["moons_button"].place(x=self.root.winfo_screenwidth() - self.root_elements["moons_button"].winfo_reqwidth(), y=60)
        if data.constants["user_scale"]:
            if center_is_jupiter or len(data.bodies) == 3:
                self.root_elements["text_button"].place(
                    x=self.root.winfo_screenwidth() - self.root_elements["text_button"].winfo_reqwidth(), y=60)
            else:
                self.root_elements["text_button"].place(x=self.root.winfo_screenwidth() - self.root_elements["text_button"].winfo_reqwidth(), y=90)
        if not data.constants["user_scale"] and not kepler_check and not center_is_jupiter:
            if blackhole:
                self.root_elements["IsBH"].place(x=self.root.winfo_screenwidth() - self.root_elements["IsBH"].winfo_reqwidth(), y=90)
            else:
                if len(data.bodies) > 5:
                    self.root_elements["IsBH"].place(
                        x=self.root.winfo_screenwidth() - self.root_elements["IsBH"].winfo_reqwidth(), y=120)
        if blackhole:
            self.root_elements["BHHighlight"].place(x=self.root.winfo_screenwidth() - self.root_elements["BHHighlight"].winfo_reqwidth(), y=120)
        if not kepler_check and not blackhole:
            if data.constants["user_scale"]:
                if center_is_jupiter or len(data.bodies) == 3:
                    self.root_elements["planet_combobox"].place(
                        x=self.root.winfo_screenwidth() - self.root_elements["planet_combobox"].winfo_reqwidth(), y=90)
                else:
                    self.root_elements["planet_combobox"].place(x=self.root.winfo_screenwidth() - self.root_elements["planet_combobox"].winfo_reqwidth(), y=120)
            else:
                if center_is_jupiter or len(data.bodies) == 3:
                    self.root_elements["planet_combobox"].place(
                        x=self.root.winfo_screenwidth() - self.root_elements["planet_combobox"].winfo_reqwidth(), y=60)
                else:
                    self.root_elements["planet_combobox"].place(x=self.root.winfo_screenwidth() - self.root_elements["planet_combobox"].winfo_reqwidth(), y=90)


        self.root.bind("<Escape>", self.quit_program)
        self.root.bind("<space>", self.pause)
        self.root.bind("<Right>", self.scale_add)
        self.root.bind("<Left>", self.scale_red)
        self.root.bind("<Up>", self.add_speed)
        self.root.bind("<Down>", self.red_speed)
        self.root.bind("<E>", self.hide_ui)
        self.root.bind("<e>", self.hide_ui)
        self.root.bind("<A>", self.add_move)
        self.root.bind("<a>", self.add_move)
        self.root.bind("<d>", self.red_move)
        self.root.bind("<D>", self.red_move)
        self.root.bind("<W>", self.add_move_y)
        self.root.bind("<w>", self.add_move_y)
        self.root.bind("<s>", self.red_move_y)
        self.root.bind("<S>", self.red_move_y)

        self.root.focus_force()

        self.updating = True
        self.root.after(data.constants["update_speed"], self.update)

    def create_pre_root(self) -> None:
        if not self.root:
            self.root = tk.Tk()
            self.root.title("Scale choice")
            self.root.attributes("-fullscreen", True)

            font = tkFont.Font(family='Helvetica', size=30, weight='bold')
            text1 = tk.Label(self.root, text="Choose mode", font=font)
            text2 = tk.Label(self.root, text="Sun Earth Moon", font=font)
            text3 = tk.Label(self.root, text="Jupiter and moons", font=font)
            btn1 = tk.Button(self.root, text="         Simplified         ", font=font, command=self.user_scale_t, bg="#eae6ca")
            btn2 = tk.Button(self.root, text="             Real             ",  font=font, command=self.user_scale_f, bg="#eae6ca")
            btn3 = tk.Button(self.root, text="          Kepler-11          ", font=font, command=self.kepler, bg="#eae6ca")
            btn4 = tk.Button(self.root, text="Solar System with Black Hole", font=font, command=self.black_hole, bg="#eae6ca")
            btn5 = tk.Button(self.root, text="Simplified", font=font, command=self.sem_s, bg="#eae6ca")
            btn6 = tk.Button(self.root, text="   Real   ", font=font, command=self.sem, bg="#eae6ca")
            btn7 = tk.Button(self.root, text="Simplified", font=font, command=self.jm_s, bg="#eae6ca")
            btn8 = tk.Button(self.root, text="   Real   ", font=font, command=self.jm, bg="#eae6ca")
            self.root.update_idletasks()

            text1.place(x=(self.root.winfo_screenwidth() - font.measure("Choose mode")) / 2, y=100)
            text2.place(x=(self.root.winfo_screenwidth() - font.measure("Sun Earth Moon")) / 2 - 265, y=650)
            text3.place(x=(self.root.winfo_screenwidth() - font.measure("Jupiter and moons")) / 2 + 300, y=650)
            btn1.place(x=(self.root.winfo_screenwidth() / 2 - btn1.winfo_reqwidth() - 100), y=300)
            btn2.place(x=(self.root.winfo_screenwidth() / 2 + 100), y=300)
            btn3.place(x=(self.root.winfo_screenwidth() / 2 - btn3.winfo_reqwidth() - 200), y=500)
            btn4.place(x=(self.root.winfo_screenwidth() / 2 + 200), y=500)
            btn5.place(x=(self.root.winfo_screenwidth() - font.measure("Sun Earth Moon")) / 2 - 185 - btn5.winfo_reqwidth(), y=750)
            btn6.place(x=(self.root.winfo_screenwidth() - font.measure("Sun Earth Moon")) / 2 - 265 + btn6.winfo_reqwidth(), y=750)
            btn7.place(
                x=(self.root.winfo_screenwidth() - font.measure("Jupiter and moons")) / 2 + 300 + btn7.winfo_reqwidth(),
                y=750)
            btn8.place(
                x=(self.root.winfo_screenwidth() - font.measure("Jupiter and moons")) / 2 + 380 - btn8.winfo_reqwidth(),
                y=750)
            self.root.bind("<Escape>", self.quit_program)

    def update(self) -> None:
        global time_past, blackhole, BHHighlight
        if not kepler_check:
            if not self.updating or not self.root or not self.root.winfo_exists():
                return
            if "time_text" in self.root_elements and visible:
                self.root_elements["time_text"].config(text=f"{main.format_ymwd(time_past)}")
            if running:
                time_past += data.constants["time_step"] * data.constants["dt"]
                for i in range(data.constants["time_step"]):
                    for body in data.bodies:
                        if body.name == "Sun" and not blackhole or body.name == "BlackHole" or center_is_jupiter and body.name == "Jupiter":
                            continue
                        main.update_position(body, blackhole)
                    for body in data.bodies:
                        if body.name == "BlackHole":
                            continue
                        body.position = body.next_pos
            self.apply_all_multipliers()
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
                    if body.name == "BlackHole":
                        continue
                    body.screen_x = body.position.x * body.scaler * data.constants["scale_m"] * data.constants["scale"] + self.root.winfo_screenwidth() / 2
                    body.screen_y = body.position.y * body.scaler * data.constants["scale_m"] * data.constants["scale"] + self.root.winfo_screenheight() / 2
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
                        body.screen_x + data.constants["move_mx"] - body.screen_radius * data.constants["scale_m"],
                        body.screen_y + data.constants["move_my"] - body.screen_radius * data.constants["scale_m"],
                        body.screen_x + data.constants["move_mx"] + body.screen_radius * data.constants["scale_m"],
                        body.screen_y + data.constants["move_my"] + body.screen_radius * data.constants["scale_m"],
                        fill=body.color,
                        outline=""
                    )
                    if body.name == "Saturn":
                        self.canvas.create_oval(body.screen_x + data.constants["move_mx"] - (body.screen_radius + 10) * data.constants["scale_m"],
                                                body.screen_y + data.constants["move_my"] - (body.screen_radius + 10) * data.constants["scale_m"],
                                                body.screen_x + data.constants["move_mx"] + (body.screen_radius + 10) * data.constants["scale_m"],
                                                body.screen_y + data.constants["move_my"] + (body.screen_radius + 10) * data.constants["scale_m"],
                                                outline="#ceb8b8", width=6 * data.constants["scale_m"])

                    self.bind_planet_tooltip(planet_id, body.name, body.mass, body.radius, math.hypot(body.Orbital_speed.x, body.Orbital_speed.y), body.screen_x, body.screen_y)
                    if show_text:
                        self.canvas.create_text(body.screen_x + data.constants["move_mx"],
                                                body.screen_y + data.constants["move_my"] - body.screen_radius * data.constants["scale_m"] - 10,
                                                text=body.name,
                                                fill="white")
            else:
                for body in data.bodies:
                    if body.name == "BlackHole" and not blackhole:
                        continue
                    body.screen_x = body.position.x * data.constants["real_scale"] * data.constants["scale_m"] + 735
                    body.screen_y = body.position.y * data.constants["real_scale"] * data.constants["scale_m"] + 478

                    if body.name == "Moon" or body.name in data.jupiter_moons and not show_moons:
                        continue

                    if body.name == "BlackHole" and BHHighlight:
                        cl = "white"
                    else:
                        cl = ""
                    planet_id = self.canvas.create_oval(
                        body.screen_x + data.constants["move_mx"] - body.radius * data.constants["real_scale"] * data.constants["scale_m"],
                        body.screen_y + data.constants["move_my"] - body.radius * data.constants["real_scale"] * data.constants["scale_m"],
                        body.screen_x + data.constants["move_mx"] + body.radius * data.constants["real_scale"] * data.constants["scale_m"],
                        body.screen_y + data.constants["move_my"] + body.radius * data.constants["real_scale"] * data.constants["scale_m"],
                        fill=body.color,
                        outline=cl
                    )
                    if body.name == "Saturn":
                        self.canvas.create_oval(body.position.x + data.constants["move_mx"] - 146e5 * data.constants["real_scale"] * data.constants["scale_m"],
                                                body.position.y + data.constants["move_my"] - 146e5 * data.constants["real_scale"] * data.constants["scale_m"],
                                                body.position.x + data.constants["move_mx"] + 146e5 * data.constants["real_scale"] * data.constants["scale_m"],
                                                body.position.y + data.constants["move_my"] + 146e5 * data.constants["real_scale"] * data.constants["scale_m"],
                                                outline="#ceb8b8", width=533e5 * data.constants["real_scale"] * data.constants["scale_m"])
                    self.bind_planet_tooltip(planet_id, body.name, body.mass, body.radius, math.hypot(body.Orbital_speed.x, body.Orbital_speed.y), body.position.x, body.position.y)
            if not blackhole:
                main.remove_system_momentum(data.bodies)

        else:
            if not self.updating or not self.root or not self.root.winfo_exists():
                return
            if "time_text" in self.root_elements and visible:
                self.root_elements["time_text"].config(text=f"{main.format_ymwd(time_past)}")
            if running:
                time_past += data.constants["time_step"] * data.constants["dt"]
                for i in range(data.constants["time_step"]):
                    for body in data.kepler_bodies:
                        if body.name == "Kepler-11":
                            continue
                        main.update_position(body, False)
                    for body in data.kepler_bodies:
                        body.position = body.next_pos

            if show_stars:
                for item in self.canvas.find_all():
                    if item not in self.star_ids:
                        self.canvas.delete(item)
            else:
                self.canvas.delete("all")

            for body in data.kepler_bodies:
                if show_trails and len(body.trail) > 1:
                    self.canvas.create_line(body.trail, fill=body.color, width=1, smooth=True)

            for body in data.kepler_bodies:
                body.screen_x = body.position.x * data.constants["real_scale"] * data.constants["scale_m"] + 735
                body.screen_y = body.position.y * data.constants["real_scale"] * data.constants["scale_m"] + 478

                planet_id = self.canvas.create_oval(
                    body.screen_x + data.constants["move_mx"] - body.radius * data.constants["real_scale"] * data.constants["scale_m"],
                    body.screen_y + data.constants["move_my"] - body.radius * data.constants["real_scale"] * data.constants["scale_m"],
                    body.screen_x + data.constants["move_mx"] + body.radius * data.constants["real_scale"] * data.constants["scale_m"],
                    body.screen_y + data.constants["move_my"] + body.radius * data.constants["real_scale"] * data.constants["scale_m"],
                    fill=body.color,
                    outline=""
                )

                self.bind_planet_tooltip(planet_id, body.name, body.mass, body.radius,
                                         math.hypot(body.Orbital_speed.x, body.Orbital_speed.y), body.position.x,
                                         body.position.y)

            main.remove_system_momentum(data.kepler_bodies)
        if self.updating and self.root and self.root.winfo_exists():
            self.root.after(data.constants["update_speed"], self.update)

    def quit_program(self, event=None) -> None:
        self.remove_all_tooltips()
        self.root.destroy()

    def run(self) -> None:
        self.create_pre_root()
        self.root.mainloop()

    def paint_stars(self) -> None:
        if data.constants["user_scale"]:
            for i in self.stars:
                p = self.canvas.create_oval(i[0], i[1], i[0] + 2, i[1] + 2, fill='white', outline='white')
                self.star_ids.append(p)
        else:
            for i in self.stars:
                p = self.canvas.create_oval(i[0], i[1], i[0], i[1], fill='white')
                self.star_ids.append(p)

    def pause(self, event=None) -> None:
        global running
        global pause_times
        running = not running
        pause_times += 1
        self.remove_all_tooltips()

    def spawn(self) -> None:
        global blackhole
        blackhole = not blackhole
        if blackhole:
            data.constants["time_step"] = 1
            data.constants["dt"] = 1
            data.constants["update_speed"] = 1
            data.constants["real_scale"] = 5e-11
        self.root_elements["BHHighlight"].place_forget()
        if not start_bh:
            self.root_elements["planet_combobox"].place_forget()
        self.root_elements["IsBH"].place_forget()
        self.root.update_idletasks()
        if not blackhole:
            if not start_bh:
                self.root_elements["planet_combobox"].place(
                    x=self.root.winfo_screenwidth() - self.root_elements["planet_combobox"].winfo_reqwidth(), y=90)
                self.root_elements["IsBH"].place(
                    x=self.root.winfo_screenwidth() - self.root_elements["IsBH"].winfo_reqwidth(), y=120)
            else:
                self.root_elements["IsBH"].place(
                    x=self.root.winfo_screenwidth() - self.root_elements["IsBH"].winfo_reqwidth(), y=90)
        if blackhole:
            self.root_elements["IsBH"].place(
                x=self.root.winfo_screenwidth() - self.root_elements["IsBH"].winfo_reqwidth(), y=90)
            self.root_elements["BHHighlight"].place(x=self.root.winfo_screenwidth() - self.root_elements["BHHighlight"].winfo_reqwidth(), y=120)

    @staticmethod
    def toggle_trails() -> None:
        global show_trails
        show_trails = not show_trails

    def user_scale_t(self) -> None:
        global blackhole
        data.constants["user_scale"] = True
        blackhole = False
        return self.open_main_root()

    def user_scale_f(self) -> None:
        global show_trails, show_moons, show_stars
        data.constants["user_scale"] = False
        data.constants["real_scale"] = 9e-9
        show_trails = False
        show_moons = False
        show_stars = False
        return self.open_main_root()

    def kepler(self) -> None:
        global show_trails, show_moons, show_stars, kepler_check
        kepler_check = True
        data.constants["user_scale"] = False
        show_trails = False
        show_moons = False
        show_stars = False
        data.constants["time_step"] = 1
        data.constants["dt"] = 1
        data.constants["real_scale"] = 5e-8
        return self.open_main_root()

    def black_hole(self) -> None:
        global show_trails, show_moons, show_stars, blackhole
        blackhole = True
        data.constants["user_scale"] = False
        show_trails = False
        show_moons = False
        show_stars = False
        data.constants["time_step"] = 1
        data.constants["dt"] = 1
        data.constants["update_speed"] = 1
        data.constants["real_scale"] = 5e-11
        return self.open_main_root()

    def sem(self, t=False) -> None:
        data.constants["scale"] = 9e-10 if t else data.constants["scale"]
        data.constants["real_scale"] = 3e-9 if not t else data.constants["real_scale"]
        data.constants["user_scale"] = t
        data.bodies = [
            data.Sun,
            data.Earth,
            data.Moon
        ]
        return self.open_main_root()

    def sem_s(self) -> None:
        self.sem(t=True)

    def jm(self, t=False) -> None:
        global center_is_jupiter
        center_is_jupiter = True
        data.constants["dt"] = 1
        data.constants["time_step"] = 1
        data.constants["update_speed"] = 16
        data.constants["scale"] = 8e-9 if t else data.constants["scale"]
        data.constants["user_scale"] = t
        data.constants["real_scale"] = 2e-7 if not t else data.constants["real_scale"]
        data.bodies = [
            data.Jupiter,
            data.Io,
            data.Europa,
            data.Ganymede,
            data.Callisto
        ]
        for body in data.bodies:
            match body.name:
                case "Jupiter":
                    body.position = data.Point(0, 0)
                    body.Orbital_speed = data.Point(0,0)
                    body.screen_radius = 25 if t else body.screen_radius
                case "Io":
                    body.position = data.Point(data.Jupiter.position.x, data.Jupiter.position.y  + 4.217e8)
                    main.set_circular_velocity(body, data.Jupiter)
                    body.screen_radius = 6 if t else body.screen_radius
                    body.max_trail_length = 300
                    body.min_trail_length = 0 if t else body.min_trail_length
                case "Europa":
                    body.position = data.Point(data.Jupiter.position.x, data.Jupiter.position.y  + 6.711e8)
                    main.set_circular_velocity(body, data.Jupiter)
                    body.screen_radius = 6 if t else body.screen_radius
                    body.max_trail_length = 300
                    body.min_trail_length = 0 if t else body.min_trail_length
                case "Ganymede":
                    body.position = data.Point(data.Jupiter.position.x, data.Jupiter.position.y  + 1.070e9)
                    main.set_circular_velocity(body, data.Jupiter)
                    body.screen_radius = 6 if t else body.screen_radius
                    body.max_trail_length = 320
                    body.min_trail_length = 0 if t else body.min_trail_length
                case "Callisto":
                    body.position = data.Point(data.Jupiter.position.x, data.Jupiter.position.y  + 1.883e9)
                    main.set_circular_velocity(body, data.Jupiter)
                    body.screen_radius = 6 if t else body.screen_radius
                    body.max_trail_length = 450
                    body.min_trail_length = 0 if t else body.min_trail_length
        return self.open_main_root()

    def jm_s(self) -> None:
        self.jm(t=True)

    def hide_stars(self) -> None:
        global show_stars, pause_times, joker
        show_stars = not show_stars
        if show_stars:
            self.paint_stars()
        if pause_times >= 5 and not joker:
            joker = not joker
            threading.Thread(target=lambda: webbrowser.open("https://youtu.be/dQw4w9WgXcQ?si=EScuTA7EVvjQaglx"), daemon=True).start()


    @staticmethod
    def BHHighlight() -> None:
        global BHHighlight
        BHHighlight = not BHHighlight

    @staticmethod
    def hide_moons() -> None:
        global show_moons
        show_moons = not show_moons

    @staticmethod
    def scale_add(event=None) -> None:
        if data.constants["user_scale"]:
            data.constants["scale_m"] += 0.5
            for body in data.bodies:
                body.trail.clear()
            for body in data.kepler_bodies:
                body.trail.clear()
        else:
            if blackhole:
                data.constants["scale_m"] += 0.5
            else:
                data.constants["scale_m"] += 0.02
            for body in data.bodies:
                body.trail.clear()
            for body in data.kepler_bodies:
                body.trail.clear()

    @staticmethod
    def scale_red(event=None) -> None:
        if data.constants["user_scale"]:
            if data.constants["scale_m"] >= 0.6:
                data.constants["scale_m"] -= 0.5
                for body in data.bodies:
                    body.trail.clear()
                for body in data.kepler_bodies:
                    body.trail.clear()
        else:
            if data.constants["scale_m"] >= 0.2:
                data.constants["scale_m"] -= 0.1
                for body in data.bodies:
                    body.trail.clear()
                for body in data.kepler_bodies:
                    body.trail.clear()
            elif data.constants["scale_m"] >= 0.02:
                data.constants["scale_m"] -= 0.01
                for body in data.bodies:
                    body.trail.clear()
                for body in data.kepler_bodies:
                    body.trail.clear()
            elif data.constants["scale_m"] >= 0.002:
                data.constants["scale_m"] -= 0.001
                for body in data.bodies:
                    body.trail.clear()
                for body in data.kepler_bodies:
                    body.trail.clear()

    @staticmethod
    def hide_text() -> None:
        global show_text
        show_text = not show_text

    @staticmethod
    def add_speed(event=None) -> None:
        if data.constants["update_speed"] >= 11:
            data.constants["update_speed"] -= 10
        elif data.constants["update_speed"] >= 2:
            data.constants["update_speed"] -= 1
        elif data.constants["dt"] <= 1191:
            data.constants["dt"] += 10
        elif data.constants["time_step"] <= 270:
            data.constants["time_step"] += 5

    @staticmethod
    def red_speed(event=None) -> None:
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

    def bind_planet_tooltip(self, planet_id, name: str, mass: float, radius: float, speed: float, x: float, y: float) -> None:
        def show_tooltip(event) -> None:
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

        def hide_tooltip(event) -> None:
            self.tooltip.destroy()
            self.tooltip_text.destroy()

        if not running:
            self.canvas.tag_bind(planet_id, "<Button-1>", show_tooltip)
            self.root.bind("<Button-2>", hide_tooltip)

        self.tooltips[planet_id] = self.tooltip

    def remove_all_tooltips(self) -> None:
        for planet_id, tooltip in self.tooltips.items():
            if tooltip and tooltip.winfo_exists():
                tooltip.destroy()
        self.tooltips = {}

    def hide_ui(self, event=None) -> None:
        global visible
        visible = not visible

        if visible:
            self.root.update_idletasks()

            self.root_elements["credits"].place(
                x=self.root.winfo_screenwidth() - self.root_elements["credits"].winfo_reqwidth(),
                y=self.root.winfo_screenheight() - self.root_elements["credits"].winfo_reqheight() * 2)
            self.root_elements["controls"].place(
                x=0,
                y=self.root.winfo_screenheight() - self.root_elements["controls"].winfo_reqheight() * 1.5)
            self.root_elements["time_text"].place(
                x=(self.root.winfo_screenwidth() - data.Time_text.font.measure(data.Time_text.text)) / 2,
                y=self.root.winfo_screenheight() - 170)
            self.root_elements["trails_button"].place(
                x=self.root.winfo_screenwidth() - self.root_elements["trails_button"].winfo_reqwidth(), y=0)
            self.root_elements["stars_button"].place(
                x=self.root.winfo_screenwidth() - self.root_elements["stars_button"].winfo_reqwidth(), y=30)
            if not kepler_check and len(data.bodies) > 5:
                self.root_elements["moons_button"].place(
                    x=self.root.winfo_screenwidth() - self.root_elements["moons_button"].winfo_reqwidth(), y=60)
            if data.constants["user_scale"]:
                if center_is_jupiter or len(data.bodies) == 3:
                    self.root_elements["text_button"].place(
                        x=self.root.winfo_screenwidth() - self.root_elements["text_button"].winfo_reqwidth(), y=60)
                else:
                    self.root_elements["text_button"].place(
                        x=self.root.winfo_screenwidth() - self.root_elements["text_button"].winfo_reqwidth(), y=90)
            if not data.constants["user_scale"] and not kepler_check and not center_is_jupiter:
                if blackhole:
                    self.root_elements["IsBH"].place(
                        x=self.root.winfo_screenwidth() - self.root_elements["IsBH"].winfo_reqwidth(), y=90)
                else:
                    if len(data.bodies) > 5:
                        self.root_elements["IsBH"].place(
                            x=self.root.winfo_screenwidth() - self.root_elements["IsBH"].winfo_reqwidth(), y=120)
            if blackhole:
                self.root_elements["BHHighlight"].place(
                    x=self.root.winfo_screenwidth() - self.root_elements["BHHighlight"].winfo_reqwidth(), y=120)
            if not kepler_check and not blackhole:
                if data.constants["user_scale"]:
                    if center_is_jupiter or len(data.bodies) == 3:
                        self.root_elements["planet_combobox"].place(
                            x=self.root.winfo_screenwidth() - self.root_elements["planet_combobox"].winfo_reqwidth(),
                            y=90)
                    else:
                        self.root_elements["planet_combobox"].place(
                            x=self.root.winfo_screenwidth() - self.root_elements["planet_combobox"].winfo_reqwidth(),
                            y=120)
                else:
                    if center_is_jupiter or len(data.bodies) == 3:
                        self.root_elements["planet_combobox"].place(
                            x=self.root.winfo_screenwidth() - self.root_elements["planet_combobox"].winfo_reqwidth(),
                            y=60)
                    else:
                        self.root_elements["planet_combobox"].place(
                            x=self.root.winfo_screenwidth() - self.root_elements["planet_combobox"].winfo_reqwidth(),
                            y=90)
        else:
            for element in self.root_elements.values():
                element.place_forget()
            self.remove_all_tooltips()

    @staticmethod
    def add_move(event=None) -> None:
        for body in data.bodies:
            body.trail.clear()
        for body in data.kepler_bodies:
            body.trail.clear()
        data.constants["move_mx"] += 10

    @staticmethod
    def red_move(event=None) -> None:
        for body in data.bodies:
            body.trail.clear()
        for body in data.kepler_bodies:
            body.trail.clear()
        data.constants["move_mx"] -= 10

    @staticmethod
    def add_move_y(event=None) -> None:
        for body in data.bodies:
            body.trail.clear()
        for body in data.kepler_bodies:
            body.trail.clear()
        data.constants["move_my"] += 10

    @staticmethod
    def red_move_y(event=None) -> None:
        for body in data.bodies:
            body.trail.clear()
        for body in data.kepler_bodies:
            body.trail.clear()
        data.constants["move_my"] -= 10

    def on_planet_select(self, event) -> None:
        self.current_planet = self.planet_var.get()
        current_multiplier = self.planet_multipliers.get(self.current_planet, 1.0)
        self.multiplier_var.set(current_multiplier)
        self.root_elements["planet_scale_text"].config(text=f"{self.current_planet} mass multiplier: {current_multiplier:.1f}")
        self.root_elements["planet_scale"].place(x=self.root.winfo_screenwidth() - self.root_elements["planet_scale"].winfo_reqwidth(), y=200)
        self.root_elements["planet_scale_text"].place(x=self.root.winfo_screenwidth() - self.root_elements["planet_scale_text"].winfo_reqwidth(), y=170)

    def apply_mass_multiplier(self) -> None:
        if self.current_planet:
            for body in data.bodies:
                if body.name == self.current_planet:
                    body.mass *= self.planet_multipliers[self.current_planet]
                    break

    def on_multiplier_change(self, value) -> None:
        if self.current_planet:
            multiplier_value = float(value)
            self.planet_multipliers[self.current_planet] = multiplier_value
            self.root_elements["planet_scale_text"].config(text=f"{self.current_planet} mass multiplier: {multiplier_value:.1f}")
            self.apply_mass_multiplier()

    def update_value(self, val) -> None:
        self.root_elements["planet_scale_text"].config(text=f"Значение: {float(val):.1f}")

    def apply_all_multipliers(self) -> None:
        for body in data.bodies:
            if body.name in self.planet_multipliers:
                if not hasattr(body, 'original_mass'):
                    body.original_mass = body.mass
                body.mass = body.original_mass * self.planet_multipliers[body.name]


for body in data.bodies:
    if body.name == "Sun" or body.name == "BlackHole":
        continue
    if body.name == "Moon":
        main.set_circular_velocity(body, data.Earth)
    elif body.name in data.jupiter_moons:
        main.set_circular_velocity(body, data.Jupiter)
    else:
        main.set_circular_velocity(body, data.Sun)

for body in data.kepler_bodies:
    if body.name == "Kepler-11":
        continue
    main.set_circular_velocity(body, data.Kepler11)

