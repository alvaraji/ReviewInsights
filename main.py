from tkinter import *
from web_scrape import app_search
from image_render import show_image_from_url

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


class AppResult:
    def __init__(self, canvas, app_id, y_pos = 0, frame = None):
        self.ypos = y_pos
        self.canvas = canvas
        self.height = 100
        self.yanchor = 150
        self.id = app_id
        self.frame = frame
        self.body = self.canvas.create_rectangle(0,0,self.canvas.winfo_width(), self.height)

        placeholder_name = '==  '+""+'  '+ '='*75

        self.name = AnLabel(self.canvas, placeholder_name, 400, ((self.yanchor + 20) + (self.height*y_pos)), frame=self.frame)
        #self.name.label.config(text = "test") 
        
        #self.name.label.place(x= 130 - self.name.label.winfo_width(), y =  ((self.yanchor + 10) + (self.height*y_pos)))

        self.image = None
    

        self.canvas.move(self.body, 0, (self.yanchor + (self.height*y_pos)))
    
    def set_name(self, name):
        formatted_name = '==  '+name+'  '+ '='*( 75 - len(name))
        self.name.label.config(self.name.label.config(text = formatted_name))
    
    def set_image(self, image):
        app_image = show_image_from_url(image, (100, 90))
        self.image = anImage(self.canvas, app_image, 50, (50 +((self.yanchor + 2) + (self.height*self.ypos))), self.frame)
        self.image.label.image = self.image.image
        

        #self.image.label.place(x=0, y =  ((self.yanchor + 2) + (self.height*self.ypos)))



# Create the main window and canvas
tk = Tk()
tk.resizable(False, False)  # Prevent window resizing
tk.title("Review Insights")


def show_frame(frame):
    frame.tkraise()

frames = []

home_frame = Frame(tk, width=600, height=500)
search_frame = Frame(tk, width=600, height=500)
loading_frame = Frame(tk, width=600, height=500)
analysis_frame = Frame(tk, width=600, height=500)

frames.append(home_frame)
frames.append(search_frame)
frames.append(loading_frame)
frames.append(analysis_frame)

for frame in frames:
    frame.grid(row=0, column=0, sticky="nsew")

home_canvas = Canvas(home_frame, width=600, height=500, bd=0, bg='#ADD8E6') #change to ivory
home_canvas.pack() # Pack is used to display objects in the window
home_canvas.update() # Needed to get the rendered canvas size 

search_canvas = Canvas(search_frame, width=600, height=500, bd=0, bg='#ADD8E6') #change to ivory
search_canvas.pack(side="left", fill="both", expand=True) # Pack is used to display objects in the window
search_canvas.update() # Needed to get the rendered canvas size 

loading_canvas = Canvas(loading_frame, width=600, height=500, bd=0, bg='#ADD8E6') #change to ivory
loading_canvas.pack() # Pack is used to display objects in the window
loading_canvas.update() # Needed to get the rendered canvas size 

analysis_canvas = Canvas(analysis_frame, width=600, height=500, bd=0, bg='#ADD8E6') #change to ivory
analysis_canvas.pack() # Pack is used to display objects in the window
analysis_canvas.update() # Needed to get the rendered canvas size 

# Add a scrollbar to the canvas
scrollbar = Scrollbar(search_frame, orient="vertical", command=search_canvas.yview)
scrollbar.pack(side="right", fill="y")

# Add mousewheel scrolling support
def on_mouse_wheel(event):
        search_canvas.yview_scroll(-1 * int(event.delta / 120), "units")

search_canvas.bind_all("<MouseWheel>", on_mouse_wheel)

search_text = Textbox(home_canvas, 'white')

home_lbl = AnLabel(home_canvas, 'white')
search_lbl = AnLabel(search_canvas, 'white', None, 20)
load_lbl = AnLabel(loading_canvas, 'white')
load_lbl.label.config(text = "Loading...") 

# Create a frame inside the canvas for content
search_content_frame = Frame(search_canvas)
search_canvas.create_window((0, 0), window=search_content_frame, anchor="nw")

# Function to print the textbox content
def print_textbox_content():
    inp = search_text.textbox.get() 
    if len(inp) > 0:

        show_frame(loading_frame)

        search_lbl.label.config(text = "Searching For: "+inp) 

        results = app_search(inp)

        show_frame(search_frame)
        
        apps = []

        for i in range(0 , len(results)):
            apps.append(AppResult(search_canvas, results[i]['appId'], i))
            apps[i].set_name(results[i]['title'])
            apps[i].set_image(results[i]['icon'])
        
        search_frame.update()

        
    else:
        home_lbl.label.config(text = "You must input an app name!") 


def back_home():
    show_frame(home_frame)

search_button = MyButton(home_canvas, 'white', print_textbox_content, "Search App")

back_button = MyButton(search_canvas, 'b', back_home, "Back to search", 50, 20)
cancel_button = MyButton(loading_canvas, 'b', back_home, "Cancel", 50, 20)

title = home_canvas.create_text(
        home_canvas.winfo_width()/2, 40,
        text="Review Insights",
        font=("Helvetica", 30),
        fill='black'
    )

subtitle = home_canvas.create_text(
        home_canvas.winfo_width()/2, 90,
        text="Search for an App to get Started",
        font=("Helvetica", 12),
        fill='black'
    )


loading_symbol = LoadBar(loading_canvas,"gray")

# Animation loop
def animate():
    loading_symbol.animate_load()
    tk.after(10, animate)  # Schedule next update in 10ms

show_frame(home_frame)
animate()

tk.mainloop()