import tkinter as tk
import data, main

root = tk.Tk()
root.title("Solar System")
root.attributes("-fullscreen", 1)
root.configure(bg="#000000")
canvas = tk.Canvas(root, width=root.winfo_screenwidth(), highlightthickness=0, height=root.winfo_screenheight(), bg="#000000")
canvas.pack()
canvas1 = tk.Canvas(root, bg='#F2DDC6', width=350, height=root.winfo_screenheight()-750)
canvas1.place(x=root.winfo_screenwidth()-350, y=0)
# canvas1.create_line(0, canvas1.winfo_screenheight()/2, 500, canvas1.winfo_screenheight()/2, width=1, fill="white")

running = True


def update():
    main.remove_system_momentum(data.bodies)
    for body in data.bodies:
        if body.name == "Moon":
            main.set_circular_velocity(body, data.Earth)
        elif body.name in data.jupiter_moons:
            main.set_circular_velocity(body, data.Jupiter)
        # else:
        #     main.set_circular_velocity(body, data.Sun)
    if not running:
        return

    # Обновление позиций всех тел
    for i in range(data.constants["time_step"]):
        for body in data.bodies:
            if body.name == "Sun":
                continue
            main.update_position(body)


    # Отрисовка
    canvas.delete("all")

    # Рисуем планеты
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
        # Подписи планет
        canvas.create_text(x, y - body.screen_radius - 10, text=body.name, fill="white")

        if len(body.trail) > 1:
            canvas.create_line(body.trail, fill=body.color, width=1)


    root.after(10, update)  # ~60 FPS


root.after(0, update)
root.mainloop()
