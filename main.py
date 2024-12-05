from tkinter import *
from web_scrape import app_search, get_reviews
from image_render import show_image_from_url
import pandas as pd
from sentiment_analysis import analyze, good_bad_interst_split, summarize
from classes import *

class AppResult:
    def __init__(self, canvas, app_id, y_pos = 0, frame = None, current_selected = None):
        self.ypos = y_pos
        self.canvas = canvas
        self.height = 100
        self.yanchor = 150
        self.id = app_id
        self.current_selected = current_result
        self.frame = frame
        self.body = self.canvas.create_rectangle(0,0,self.canvas.winfo_width(), self.height)
        self.app_name = "Blank"

        placeholder_name = '==  '+""+'  '+ '='*75

        self.name = AnLabel(self.canvas, placeholder_name, 400, ((self.yanchor + 20) + (self.height*y_pos)), frame=self.frame)

        self.image = None

        self.canvas.move(self.body, 0, (self.yanchor + (self.height*y_pos)))

        self.select_button = MyButton(self.canvas, 'white', self.select_result, "Select", 400, ((self.yanchor + 50) + (self.height*y_pos)))
    
    def set_name(self, name):
        self.app_name = name
        formatted_name = '==  '+name+'  '+ '='*( 75 - len(name))
        self.name.label.config(self.name.label.config(text = formatted_name))
    
    def set_image(self, image):
        app_image = show_image_from_url(image, (100, 90))
        self.image = anImage(self.canvas, app_image, 50, (50 +((self.yanchor + 2) + (self.height*self.ypos))), self.frame)
        self.image.label.image = self.image.image
        

    def select_result(self):
        
        show_frame(loading_frame)

        self.current_selected.change(self)

        analysis_lbl.label.config(text = self.app_name, font=("Helvetica", 20))

        reviews_df = get_reviews(self.app_name, self.id)
        
        scored_reviews = analyze(reviews_df)

        self.good_r, self.bad_r, self.interesting_r = good_bad_interst_split(scored_reviews)

        self.summary = AnLabel(analysis_canvas, 'white', 350, 150)

        summary_text = AnLabel(analysis_canvas, "b", 80, 150)

        summary_text.label.config(text="Summary:")

        self.res_flag = "pos"
        self.review_list = []

        pos_result = MyButton(analysis_canvas, 'white', self.show_good, "Positive Results", 80, 100)
        neg_result = MyButton(analysis_canvas, 'white', self.show_bad, "Negative Results", 300, 100)
        int_result = MyButton(analysis_canvas, 'white', self.show_interesting, "Interesting Results", 500, 100)

        self.good_rev = summarize(self.good_r)
        self.bad_rev = summarize(self.bad_r)
        self.int_rev = summarize(self.interesting_r)

        self.body = analysis_canvas.create_rectangle(0,0,self.canvas.winfo_width(), 200)

        self.y_offset = 55

        label_y = 225

        review_num_label_1 = AnLabel(analysis_canvas, "", 80, label_y)
        review_num_label_1.label.config(text="1) ")
        review_num_label_2 = AnLabel(analysis_canvas, "", 80, label_y+(self.y_offset))
        review_num_label_2.label.config(text="2) ")
        review_num_label_3 = AnLabel(analysis_canvas, "", 80, label_y+(2*self.y_offset))
        review_num_label_3.label.config(text="3) ")
        review_num_label_4 = AnLabel(analysis_canvas, "", 80, label_y+(3*self.y_offset))
        review_num_label_4.label.config(text="4) ")
        review_num_label_5 = AnLabel(analysis_canvas, "", 80, label_y+(4*self.y_offset))
        review_num_label_5.label.config(text="5) ")


        self.show_good(init_flag=True)

        show_frame(analysis_frame)


    def show_good(self, init_flag = False):

        if self.res_flag != "pos" or init_flag:

            if not(init_flag):
                self.summary.label.destroy()
                self.summary = AnLabel(analysis_canvas, 'white', 350, 150)
            

                for review in self.review_list:
                        review.label.destroy()
                        analysis_canvas.delete(review)

            
            self.res_flag = "pos"
            self.summary.label.config(text = self.good_rev, wraplength=400) 

            self.review_list.clear()
            
            analysis_canvas.update()

            index = 0

            for _, review in self.good_r.head().iterrows():
                current_review = AnLabel(analysis_canvas, "", 350, 225+(index*self.y_offset))
                current_review.label.config(text=review["content"], wraplength=375)
                self.review_list.append(current_review)
                index = index + 1

        else:
            pass 

    def show_bad(self):
        if self.res_flag != "neg":
            
            self.summary.label.destroy()
            self.summary = AnLabel(analysis_canvas, 'white', 350, 150)

            self.res_flag = "neg"
            self.summary.label.config(text = self.bad_rev, wraplength=375) 

           

            for review in self.review_list:
                    review.label.destroy()
                    analysis_canvas.delete(review)

            
            

            self.review_list.clear()
            
            analysis_canvas.update()

            index = 0

            for _, review in self.bad_r.head().iterrows():
                current_review = AnLabel(analysis_canvas, "", 350, 225+(index*self.y_offset))
                current_review.label.config(text=review["content"], wraplength=375)
                self.review_list.append(current_review)
                index = index + 1

        else:
            pass 

    def show_interesting(self):
        if self.res_flag != "int":

            self.summary.label.destroy()
            self.summary = AnLabel(analysis_canvas, 'white', 350, 150)

            self.res_flag = "int"
            self.summary.label.config(text = self.int_rev, wraplength=375) 

           

            for review in self.review_list:
                    review.label.destroy()
                    analysis_canvas.delete(review)

            
            

            self.review_list.clear()
            
            analysis_canvas.update()

            index = 0

            for _, review in self.interesting_r.head().iterrows():
                current_review = AnLabel(analysis_canvas, "", 350, 225+(index*self.y_offset))
                current_review.label.config(text=review["content"], wraplength=375)
                self.review_list.append(current_review)
                index = index + 1

        else:
            pass 

def show_frame(frame):
    frame.tkraise()

# Add mousewheel scrolling support
def on_mouse_wheel(event):
        search_canvas.yview_scroll(-1 * int(event.delta / 120), "units")

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
            apps.append(AppResult(search_canvas, results[i]['appId'], i, current_selected=current_result))
            apps[i].set_name(results[i]['title'])
            apps[i].set_image(results[i]['icon'])
        
        search_frame.update()

        
    else:
        home_lbl.label.config(text = "You must input an app name!") 


def back_home():
    show_frame(home_frame)


def back_to_results():
    current_result.current.summary.label.destroy()
    analysis_canvas.delete(current_result.current.summary)
    for review in current_result.current.review_list:
        review.label.destroy()
        analysis_canvas.delete(review)
    current_result.current.review_list.clear()
    analysis_canvas.update()
    show_frame(search_frame)

# Animation loop
def animate():
    loading_symbol.animate_load()
    tk.after(10, animate)  # Schedule next update in 10ms

if __name__ == "__main__":
    # Create the main window and canvas
    tk = Tk()
    tk.resizable(False, False)  # Prevent window resizing
    tk.title("Review Insights")

    current_result = Selected()

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

    search_canvas.bind_all("<MouseWheel>", on_mouse_wheel)

    search_text = Textbox(home_canvas, 'white')

    home_lbl = AnLabel(home_canvas, 'white')
    search_lbl = AnLabel(search_canvas, 'white', None, 20)
    load_lbl = AnLabel(loading_canvas, 'white')
    analysis_lbl = AnLabel(analysis_canvas, 'white', analysis_canvas.winfo_width()/2, 60)
    load_lbl.label.config(text = "Loading...") 

    # Create a frame inside the canvas for content
    search_content_frame = Frame(search_canvas)
    search_canvas.create_window((0, 0), window=search_content_frame, anchor="nw")

    search_button = MyButton(home_canvas, 'white', print_textbox_content, "Search App")

    back_button = MyButton(search_canvas, 'b', back_home, "Back to search", 50, 20)
    cancel_button = MyButton(loading_canvas, 'b', back_home, "Cancel", 50, 20)
    results_button = MyButton(analysis_canvas, 'b', back_to_results, "Back to Results", 50, 20)

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

    show_frame(home_frame)
    animate()

    tk.mainloop()