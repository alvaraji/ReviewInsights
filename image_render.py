import tkinter as tk
from PIL import Image, ImageTk
import requests
from io import BytesIO

def show_image_from_url(url, dims):
    # Fetch the image from the URL
    response = requests.get(url)
    response.raise_for_status()  # Ensure the request was successful
    
    # Convert the image to a format compatible with Tkinter
    image_data = BytesIO(response.content)
    pil_image = Image.open(image_data)

    resized_image = pil_image.resize(dims)

    tk_image = ImageTk.PhotoImage(resized_image)
    
    return tk_image