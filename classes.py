from tkinter import *
from web_scrape import app_search, get_reviews
from image_render import show_image_from_url
import pandas as pd
from sentiment_analysis import analyze, good_bad_interst_split, summarize

class Ball:
    def __init__(self, canvas, wall, width, color, speed):
        self.wall = wall
        self.width = width
        self.speed = speed
        self.xspeed = self.speed
        self.yspeed = 0

        self.id = canvas.create_oval(0,0,self.width,self.width, fill=color)

class LoadBar:
    def __init__(self, canvas, color, width = 15, speed = 2, padding = 100):
        self.canvas = canvas
        self.canvas_width = self.canvas.winfo_width()
        self.canvas_height = self.canvas.winfo_height()
        #set width and if the ball has hit the bottom
        self.width = width
        # Set the initial speed of the ball
        self.padding = padding
        #create an oval of 15x15 px
        self.balls = []
        for i in ('t', 'l', 'r', 'r'):
            self.balls.append(Ball(canvas, i, self.width, color, 2))
        #move it to the middle of the canvas, 10% from the top
        
        self.canvas.move(self.balls[0].id, padding, padding)
        self.canvas.move(self.balls[1].id, (self.canvas_width - padding), padding)
        self.canvas.move(self.balls[2].id, (self.canvas_width - padding), (self.canvas_height - padding))
        self.canvas.move(self.balls[3].id, padding, (self.canvas_height - padding))


    def animate_load(self):
        for ball in self.balls:
            self.draw(ball)

    def draw(self, ball):
        # Move the ball by its speed values
        self.canvas.move(ball.id, ball.xspeed, ball.yspeed)
        pos = self.canvas.coords(ball.id)
        
        # Wall collision detection
        if pos[1] <= self.padding and (ball.wall != 't' and ball.wall != 'r'):    # Top wall
            ball.xspeed = abs(ball.speed)
            ball.yspeed = 0
            ball.wall = 't'
        if pos[3] >= (self.canvas_height - self.padding) and ball.wall !='b': # Bottom wall
            ball.yspeed = 0
            ball.xspeed = -1*abs(ball.speed)  
            ball.wall = 'b'
        if pos[2] >= (self.canvas_width - self.padding) and (ball.wall != 'r' and ball.wall != 'b'):  # Right wall
            ball.yspeed = abs(ball.speed)
            ball.xspeed = 0
            ball.wall = 'r'
        if pos[0] <= self.padding and (ball.wall != 'l' and ball.wall != 't'):    # Left wall
            ball.yspeed = -1*abs(ball.speed)
            ball.xspeed = 0
            ball.wall = 'l'
       


class Textbox:
    def __init__(self, canvas, color, w=25, posx = None, posy = None):
        self.canvas = canvas
        self.color = color
        self.width = w
        self.textbox = Entry(canvas, width=w)

        if type(posx) == type(None):
            self.posx = canvas.winfo_width()/2
        else:
            self.posx = posx
        
        if type(posy) == type(None):
            self.posy = (canvas.winfo_height()/2)
        else:
            self.posy = posy

        self.id = self.canvas.create_window(canvas.winfo_width()/2, canvas.winfo_height()/2,window=self.textbox)


class anImage:
    def __init__(self,canvas,image, posx = None, posy = None, frame = None):
        self.canvas = canvas
        self.image = image
        self.frame = frame

        if type(posx) == type(None):
            self.posx = canvas.winfo_width()/2
        else:
            self.posx = posx
        
        if type(posy) == type(None):
            self.posy = (canvas.winfo_height()/2) + 75
        else:
            self.posy = posy

        if type(self.frame) == type(None):
            self.label = Label(self.canvas, image = self.image, background=self.canvas.cget("background"))
        else:
            self.label = Label(self.frame, image = self.image, background=self.canvas.cget("background"))
        self.id = self.canvas.create_window(self.posx, self.posy, window=self.label)

class MyButton:
    def __init__(self, canvas, color, command, text, posx = None, posy = None):
        self.canvas = canvas
        self.color = color
        self.command = command

        if type(posx) == type(None):
            self.posx = 400
        else:
            self.posx = posx
        
        if type(posy) == type(None):
            self.posy = (canvas.winfo_height()/2)
        else:
            self.posy = posy

        self.button = Button(self.canvas, text=text, command=self.command)
        self.id = self.canvas.create_window(self.posx, self.posy, window=self.button)

class AnLabel:
    def __init__(self,canvas,color, posx = None, posy = None, text_var = None, frame = None):
        self.canvas = canvas
        self.color = color
        self.frame = frame

        if type(posx) == type(None):
            self.posx = canvas.winfo_width()/2
        else:
            self.posx = posx
        
        if type(posy) == type(None):
            self.posy = (canvas.winfo_height()/2) + 75
        else:
            self.posy = posy

        if (type(text_var) == type(None)) and (type(frame) == type(None)):
            self.label = Label(self.canvas, text = "", background=self.canvas.cget("background"))
        elif (type(text_var) == type(None)):
            self.label = Label(self.frame, text = "", background=self.canvas.cget("background"))
        elif type(frame) == type(None):
            self.label = Label(self.canvas, background=self.canvas.cget("background"), textvariable = text_var)
        else:
            self.label = Label(self.frame, background=self.canvas.cget("background"), textvariable = text_var)
        self.id = self.canvas.create_window(self.posx, self.posy, window=self.label)

class Selected:
    def __init__(self):
        self.current = None
    
    def change(self, newCurrent):
        self.current = newCurrent

