from tkinter import *
from web_scrape import app_search

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
    def __init__(self,canvas,color, posx = None, posy = None):
        self.canvas = canvas
        self.color = color

        if type(posx) == type(None):
            self.posx = canvas.winfo_width()/2
        else:
            self.posx = posx
        
        if type(posy) == type(None):
            self.posy = (canvas.winfo_height()/2) + 75
        else:
            self.posy = posy

        self.label = Label(self.canvas, text = "", background=self.canvas.cget("background"))
        self.id = self.canvas.create_window(self.posx, self.posy, window=self.label)

# Create the main window and canvas
tk = Tk()
tk.resizable(False, False)  # Prevent window resizing
tk.title("Review Insights")

def show_frame(frame):
    frame.tkraise()

frames = []

home_frame = Frame(tk, width=600, height=500)
search_frame = Frame(tk, width=600, height=500)

frames.append(home_frame)
frames.append(search_frame)

for frame in frames:
    frame.grid(row=0, column=0, sticky="nsew")

home_canvas = Canvas(home_frame, width=600, height=500, bd=0, bg='#ADD8E6') #change to ivory
home_canvas.pack() # Pack is used to display objects in the window
home_canvas.update() # Needed to get the rendered canvas size 

search_canvas = Canvas(search_frame, width=600, height=500, bd=0, bg='#ADD8E6') #change to ivory
search_canvas.pack() # Pack is used to display objects in the window
search_canvas.update() # Needed to get the rendered canvas size 

search_text = Textbox(home_canvas, 'white')

home_lbl = AnLabel(home_canvas, 'white')
search_lbl = AnLabel(search_canvas, 'white', None, 20)

# Function to print the textbox content
def print_textbox_content():
    inp = search_text.textbox.get() 
    if len(inp) > 0:
        show_frame(search_frame)

        search_lbl.label.config(text = "Sarching For: "+inp) 

        result_lbl = AnLabel(search_canvas, 'white', None, 75)

        result = app_search(inp)

        result_lbl.label.config(text = result[0]['appId'])

        
    else:
        home_lbl.label.config(text = "You must input an app name!") 


def back_home():
    show_frame(home_frame)

search_button = MyButton(home_canvas, 'white', print_textbox_content, "Search App")

back_button = MyButton(search_canvas, 'b', back_home, "Back to search", 50, 20)

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


show_frame(home_frame)


tk.mainloop()