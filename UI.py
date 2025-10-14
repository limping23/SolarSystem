import tkinter as tk
import data, main
import random

running = True


def pause(event=None) -> None:
    global running
    running = not running

def quit_program(event=None) -> None:
    root.destroy()

def toggle_trails() -> None:
    global show_trails
    show_trails = not show_trails


root = tk.Tk()
root.title("Solar System")
root.attributes("-fullscreen", 1)
root.configure(bg="#000000")
canvas = tk.Canvas(root, width=root.winfo_screenwidth(), highlightthickness=0, height=root.winfo_screenheight(), bg="#000000")
canvas.pack()
canvas1 = tk.Canvas(root, bg='#F2DDC6', width=300, height=root.winfo_screenheight()-750)
canvas1.place(x=root.winfo_screenwidth()-300, y=0)
button = tk.Button(root, highlightcolor="yellow", text="Toggle Trails", command=toggle_trails)
button.place(x=root.winfo_screenwidth()-115, y=0)
root.bind("<Escape>", quit_program)
root.bind("<space>", pause)

show_trails = True

for body in data.bodies:
    if body.name == "Sun":
        continue
    if body.name == "Moon":
        main.set_circular_velocity(body, data.Earth)
    elif body.name in data.jupiter_moons:
        main.set_circular_velocity(body, data.Jupiter)
    else:
        main.set_circular_velocity(body, data.Sun)


def update() -> None:
    if running:
        # Update all bodies positions
        for i in range(data.constants["time_step"]):
            for body in data.bodies:
                if body.name == "Sun":
                    continue
                main.update_position(body)
            for body in data.bodies:
                body.position = body.next_pos

        # Rendering
        canvas.delete("all")

        for body in data.bodies:
            if show_trails and len(body.trail) > 1:
                canvas.create_line(body.trail, fill=body.color, width=1, smooth = True)

        # Draw planets
        for body in data.bodies:
            add_coord = data.Point(0,0)
            body.screen_x = body.position.x * body.scaler * data.constants["scale"] + 735
            body.screen_y = body.position.y * body.scaler * data.constants["scale"] + 478
            if body.name == "Moon":
                add_coord = data.Point(data.Earth.screen_x - body.screen_x,data.Earth.screen_y - body.screen_y)
                body.screen_x = data.Earth.screen_x + add_coord.x * 27
                body.screen_y = data.Earth.screen_y + add_coord.y * 27
            if body.name in data.jupiter_moons:
                add_coord = data.Point(data.Jupiter.screen_x - body.screen_x,data.Jupiter.screen_y - body.screen_y)
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
            canvas.create_oval(
                body.screen_x - body.screen_radius,
                body.screen_y - body.screen_radius,
                body.screen_x + body.screen_radius,
                body.screen_y + body.screen_radius,
                fill=body.color,
                outline=""
            )
            # Signing planets
            canvas.create_text(body.screen_x, body.screen_y - body.screen_radius - 10, text=body.name, fill="white")
        # Barycenter
        main.remove_system_momentum(data.bodies)

    root.after(5, update)  # ~60 FPS


root.after(0, update)
root.mainloop()
