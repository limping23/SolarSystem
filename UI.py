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


class App:

    def __init__(self):
        self.root = None
        self.canvas = None
        self.canvas1 = None
        self.button = None
        self.updating = False
        self.stars = []
        self.star_ids = []

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

        for i in range(60):
            x = randint(0, self.root.winfo_screenwidth())
            y = randint(0, self.root.winfo_screenheight())
            self.stars.append([x, y])
        self.paint_stars()
        self.canvas.pack()

        self.canvas1 = tk.Canvas(self.root, bg='#000022', width=400, height=self.root.winfo_screenheight() - 750, highlightthickness=0)
        self.canvas1.place(x=self.root.winfo_screenwidth() - 430, y=30)

        self.button = tk.Button(self.root, highlightcolor="yellow", text="Toggle Trails", command=self.toggle_trails)
        self.button.place(x=self.root.winfo_screenwidth() - 115, y=40)

        self.button = tk.Button(self.root, highlightcolor="yellow", text="Hide Stars", command=self.hide_stars)
        self.button.place(x=self.root.winfo_screenwidth() - 103, y=70)

        self.button = tk.Button(self.root, highlightcolor="yellow", text="Hide Moons", command=self.hide_moons)
        self.button.place(x=self.root.winfo_screenwidth() - 115, y=100)

        self.button = tk.Button(self.root, highlightcolor="yellow", text="Reset", command=self.reset)
        self.button.place(x=self.root.winfo_screenwidth() - 78, y=130)

        self.root.bind("<Escape>", self.quit_program)
        self.root.bind("<space>", self.pause)

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
        if not self.updating or not self.root or not self.root.winfo_exists():
            return

        if running:
            # Update all bodies positions
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

            # Draw planets
            for body in data.bodies:
                add_coord = data.Point(0, 0)
                body.screen_x = body.position.x * body.scaler * data.constants["scale"] + 735
                body.screen_y = body.position.y * body.scaler * data.constants["scale"] + 478
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

                self.canvas.create_oval(
                    body.screen_x - body.screen_radius,
                    body.screen_y - body.screen_radius,
                    body.screen_x + body.screen_radius,
                    body.screen_y + body.screen_radius,
                    fill=body.color,
                    outline=""
                )
                # Signing planets
                self.canvas.create_text(body.screen_x, body.screen_y - body.screen_radius - 10, text=body.name,
                                        fill="white")
            # Barycenter
            main.remove_system_momentum(data.bodies)

        if self.updating and self.root and self.root.winfo_exists():
            self.root.after(1, self.update)

    def quit_program(self, event=None) -> None:
        self.root.destroy()

    def run(self):
        self.create_pre_root()
        self.root.mainloop()

    def paint_stars(self):
        for i in self.stars:
            p = self.canvas.create_oval(i[0], i[1], i[0] + 2, i[1] + 2, fill='white', outline='white')
            self.star_ids.append(p)

    @staticmethod
    def pause(event=None):
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