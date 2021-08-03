import turtle
import tkinter as tk
import datetime as dt
import math
import time
import random
import threading 

class Firework():
    def __init__(self, colour, lines, steps, **kwargs):
        self.colour = colour
        self.lines = lines
        self.steps = steps
        
        if 'launch_pos_x' in kwargs:
            self.create_path(
                kwargs['launch_pos_x'], 
                kwargs['launch_pos_y'], 
                kwargs['launch_angle'],
                self.steps,300)
        else:
            self.create_path(*self.find_launch_pos(
                kwargs['screen_width'], 
                kwargs['screen_height']),
                self.steps, kwargs['screen_height'])
        
        self.explosion_point = self.path_positions[-1]

        self.create_explosion()

    def create_explosion(self):
        gravity = -5
        speed = 20
        time = .5

        self.explosion_positions = [ [] for _ in range(self.lines)]
        for i in range(self.lines):
            t_heading = 360 / self.lines * i
            x_speed = speed * math.cos(math.radians(t_heading))
            y_speed = speed * math.sin(math.radians(t_heading))
            self.explosion_positions[i].append((
                self.path_positions[-1][0],
                self.path_positions[-1][1]
            ))
            self.explosion_positions[i].append((
                x_speed * time + self.path_positions[-1][0], 
                y_speed * time + self.path_positions[-1][1]))
            for j in range(self.steps - 1):
                y_speed += gravity * time
                x_speed *= 0.95
                self.explosion_positions[i].append((
                    x_speed * time + self.explosion_positions[i][-1][0], 
                    y_speed * time + self.explosion_positions[i][-1][1]))

    def find_launch_pos(self, screen_width, screen_height):
        launch_pos_x = random.randint(0, screen_width) - screen_width / 2
        launch_pos_y = - screen_height / 2

        if launch_pos_x == 0:
            launch_angle = 90
        elif launch_pos_x > 0:
            launch_angle = random.randint(10, 40) + 90
        else:
            launch_angle = random.randint(30, 80)
        
        return launch_pos_x, launch_pos_y, launch_angle

    def create_path(self, launch_pos_x, launch_pos_y, launch_angle, steps, height):
        gravity = -5
        time = .5
        speed = height / (steps * .4) * (random.randint(7,9) / 10)
        x_speed = speed * math.cos(math.radians(launch_angle))
        y_speed = speed * math.sin(math.radians(launch_angle))

        self.path_positions = [(launch_pos_x, launch_pos_y)]

        for _ in range(steps):
            self.path_positions.append((
                self.path_positions[-1][0] + x_speed * time,
                self.path_positions[-1][1] + y_speed * time
            ))
            x_speed *= 0.95
            y_speed += gravity * time

    def run_launch(self, screen):
        
        screen.tracer(0)
        self.launch_turtle = turtle.RawTurtle(screen)

        self.launch_turtle.color(self.colour)
        self.launch_turtle.speed(0)
        self.launch_turtle.up()
        self.launch_turtle.goto(self.path_positions[0])
        self.launch_turtle.down()

        for position in self.path_positions:
            self.launch_turtle.goto(position)
            screen.update()

        self.launch_turtle.reset()

        self.explosion_turtles = [turtle.RawTurtle(screen) for _ in range(self.lines)]

        for turt in self.explosion_turtles:
            turt.color(self.colour)
            turt.speed(0)
            turt.shape('circle')
            turt.shapesize(.1,.1,.1)
            turt.up()
            turt.goto(self.explosion_positions[0][0])
            turt.down()
            

        for i in range(self.steps):
            for j, turt in enumerate(self.explosion_turtles):
                turt.goto(self.explosion_positions[j][i])
                turt.pensize(turt.pensize() + 0.3)
            screen.update()

    def reset(self):
        for turt in self.explosion_turtles:
            turt.reset()
            turt.hideturtle()

class Timer():
    def __init__(self):
        self.page = tk.Tk()
        self.frame = tk.Frame(self.page)
        self.frame.pack(side='top')

        tk.Label(self.frame, text = 'Enter shift end point').pack(side='top')
        self.hour_var = tk.StringVar()
        self.min_var = tk.StringVar()
        self.text_var = tk.StringVar()
        self.hour_var.set("17")
        self.min_var.set('00')
        self.text_var.set("Home Time")
        self.update()

        self.spin_frame = tk.Frame(self.frame)
        self.spin_frame.pack(side='top')

        self.hr_sb = tk.Spinbox(self.spin_frame, from_=0, to_= 23, wrap=True, textvariable=self.hour_var,
                                state = 'readonly', width = 2, justify='center')
        self.min_sb = tk.Spinbox(self.spin_frame, from_=0, to_= 59, wrap=True, textvariable=self.min_var,
                                state = 'readonly', width = 2, justify='center')
        
        self.hr_sb.pack(side='left')
        self.min_sb.pack(side='left')

        self.textbox = tk.Entry(self.frame, textvariable=self.text_var)
        self.textbox.pack(side='top')

        self.update_button = tk.Button(self.frame, text = 'Update', command=self.update)
        self.update_button.pack(side='top')
        self.Threading()

        self.page.mainloop()

    def alarm(self):
        while True:
            if dt.datetime.now().time() >= self.time:
                Fireworks_Screen(self.end_text, 10)
                return

    def update(self):
        self.time = dt.time(hour = int(self.hour_var.get()), minute = int(self.min_var.get()))
        self.end_text = self.text_var.get()

    def Threading(self):
        t1 = threading.Thread(target=self.alarm)
        t1.start()

class Fireworks_Screen():
    def __init__(self, label_text="", number=1):
        self.page = tk.Tk()

        self.page.attributes("-fullscreen", True)
        self.page.attributes('-alpha',0.3)
        self.page.update_idletasks()
        self.width = self.page.winfo_width()
        self.height = self.page.winfo_height()
        print(self.width,self.height)
        label = tk.Label(self.page, text = label_text)
        label.config(font=('Comic Sans', 96))
        label.pack(side='top')
        self.canvas = tk.Canvas(self.page, width=self.width, height=self.height)
        self.canvas.pack(side='top')

        self.screen = turtle.TurtleScreen(self.canvas)

        self.run_fireworks(number)


    def run_fireworks(self, number):
        colours = ['blue', 'red', 'green', 'yellow', 'pink', 'orange']
        fireworks = []
        for i in range(number + 2):
            if i < number:
                fireworks.append(Firework(
                    colours[random.randint(0,len(colours) - 1)], 
                    random.randint(10,20),
                    random.randint(15,25),
                    screen_width = self.width,
                    screen_height = self.height
                ))
                fireworks[-1].run_launch(self.screen)
            if i - 2 >= 0:
                fireworks[i - 2].reset()


def explosion(x, y, lines, colour, steps):
    gravity = -5
    speed = 20
    time = .5
    turtle.tracer(0,0)

    turtles = [turtle.Turtle() for _ in range(lines)]
    for index, turt in enumerate(turtles):
        turt.color(colour)
        turt.speed(0)
        turt.shape('circle')
        turt.shapesize(.1,.1,.1)
        turt.up()
        turt.setheading(index * 360/len(turtles))
        turt.goto(x,y)
        turt.down()

    positions = [ [] for _ in range(len(turtles))]

    for index, turt in enumerate(turtles):
        t_heading = turt.heading()
        x_speed = speed * math.cos(math.radians(t_heading))
        y_speed = speed * math.sin(math.radians(t_heading))
        positions[index].append((x_speed * time + x, y_speed * time + y))
        for i in range(steps-1):
            y_speed += gravity * time
            x_speed *= 0.95
            positions[index].append((
                x_speed * time + positions[index][-1][0], 
                y_speed * time + positions[index][-1][1]))
    
    for i in range(steps):
        for index, turt in enumerate(turtles):
            turt.goto(positions[index][i])
            turt.pensize(turt.pensize() + .3)
        turtle.update()

def rocket_path(screen_width, screen_height, steps, colour):
    speed = random.randint(50, 60)
    gravity = -1
    time = 0.5
    turtle.tracer(0,0)

    launch_pos_x = random.randint(0, screen_width) - screen_width / 2
    launch_pos_y = - screen_height / 2

    if launch_pos_x == 0:
        launch_angle = 90
    elif launch_pos_x > 0:
        launch_angle = random.randint(10, 40) + 90
    else:
        launch_angle = random.randint(30, 80)

    x_speed = speed * math.cos(math.radians(launch_angle))
    y_speed = speed * math.sin(math.radians(launch_angle))

    positions = [(launch_pos_x, launch_pos_y)]

    for _ in range(steps):
        positions.append((
            positions[-1][0] + x_speed * time,
            positions[-1][1] + y_speed * time
        ))
        x_speed *= 0.95
        y_speed += gravity * time
    
    turt = turtle.Turtle()
    turt.color(colour)
    turt.speed(0)
    turt.up()
    turt.goto(launch_pos_x, launch_pos_y)
    turt.down()

    for pos in positions:
        turt.goto(pos[0], pos[1])
        turtle.update()
    
    turt.reset()

    return positions[-1]

if __name__ =='__main__':
    Timer()
    input()