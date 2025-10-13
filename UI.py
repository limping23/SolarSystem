import tkinter as tk
import data, main
from data import OrbitalSpeed


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
    # Update all bodies positions
    for i in range(data.constants["time_step"]):
        for body in data.bodies:
            if body.name == "Sun":
                continue
            main.update_position(body)

    # Rendering
    canvas.delete("all")

    for body in data.bodies:
        if show_trails and len(body.trail) > 1:
            canvas.create_line(body.trail, fill=body.color, width=1, smooth = True)

    # Draw planets
    for body in data.bodies:
        x = body.position.x * body.scaler * data.constants["scale"] + 735
        y = body.position.y * body.scaler * data.constants["scale"] + 478
        canvas.create_oval(
            x - body.screen_radius,
            y - body.screen_radius,
            x + body.screen_radius,
            y + body.screen_radius,
            fill=body.color,
            outline=""
        )
        # Signing planets
        canvas.create_text(x, y - body.screen_radius - 10, text=body.name, fill="white")
    # Barycenter
    main.remove_system_momentum(data.bodies)

    root.after(10, update)  # ~60 FPS


root.after(0, update)
root.mainloop()
