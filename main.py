import customtkinter as ctk  # pip install customtkinter
import tkinter
import os
import requests
from requests.exceptions import ConnectTimeout
import base64
from PIL import Image, ImageTk
import io

# Global variable to hold the generated image
generated_image = None

def generate():
    global generated_image  # Declare as global to use in save_image function
    api_key = "key-HhzW2rU57zoPp39pIpE7WeH2Q2ua0Gl9pXqjTe1tbTDvOqOjO2nXiJUhjPLMRwbDBT0ug3kvZQO5MyqHShzfe1kxBKBeGlo"
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json',
    }
    
    user_prompt = prompt_entry.get("0.0", tkinter.END).strip()
    if not user_prompt:
        return  # Don't proceed if the prompt is empty
    
    model = "flux-schnell"  # Specify the model
    style = style_dropdown.get()  # Get selected style from dropdown
    complete_prompt = user_prompt + " in style: " + style
    
    # Define the payload for the getimg.ai API
    generation_data = {
        "prompt": complete_prompt,
        "output_format": "jpeg",  # Specify output format
        "width": 512,  # Image width
        "height": 512,  # Image height
        "response_format": "b64",  # We want base64 image response
    }
    
    # Make a POST request to the getimg.ai API
    try:
        response = requests.post(
            'https://api.getimg.ai/v1/flux-schnell/text-to-image',
            headers=headers,
            json=generation_data,
            timeout=30  # Setting a timeout for the request
        )
        response.raise_for_status()  # Check if the request was successful
    except ConnectTimeout:
        print("Connection to the server timed out. Please check your internet connection or try again later.")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
    
    if response.status_code == 200:
        response_data = response.json()
        base64_image = response_data.get('image')  # Get base64 image
        
        # Decode base64 image
        image_data = base64.b64decode(base64_image)
        generated_image = Image.open(io.BytesIO(image_data))  # Save the image in global variable
        
        # Display the image using Tkinter
        photo_image = ImageTk.PhotoImage(generated_image)
        canvas.image = photo_image
        canvas.create_image(0, 0, anchor="nw", image=photo_image)
        
        print("Image generated and displayed successfully.")
    else:
        print(f"Error: {response.status_code}")
        print(response.text)

def save_image():
    if generated_image is not None:
        # Get the current working directory
        current_dir = os.getcwd()

        # Generate a valid filename based on prompt and style
        user_prompt = prompt_entry.get("0.0", tkinter.END).strip()
        style = style_dropdown.get()
        filename = f"{user_prompt[:50].strip().replace(' ', '_')}_in_style_{style}.jpeg"

        # Save the image in the current directory
        image_path = os.path.join(current_dir, filename)
        generated_image.save(image_path, "JPEG")
        print(f"Image saved as {image_path}")
    else:
        print("No image to save.")

# Create the GUI window
root = ctk.CTk()
root.title("AI Image Generator")

ctk.set_appearance_mode("dark")

# Create input frame
input_frame = ctk.CTkFrame(root)
input_frame.pack(side="left", expand=True, padx=20, pady=20)

# Prompt label and text box
prompt_label = ctk.CTkLabel(input_frame, text="Prompt")
prompt_label.grid(row=0, column=0, padx=10, pady=10)
prompt_entry = ctk.CTkTextbox(input_frame, height=10)
prompt_entry.grid(row=0, column=1, padx=10, pady=10)

# Style label and dropdown
style_label = ctk.CTkLabel(input_frame, text="Style")
style_label.grid(row=1, column=0, padx=10, pady=10)
style_dropdown = ctk.CTkComboBox(input_frame, values=["Realistic", "Cartoon", "3D Illustration", "Flat Art"])
style_dropdown.grid(row=1, column=1, padx=10, pady=10)

# Generate button
generate_button = ctk.CTkButton(input_frame, text="Generate", command=generate)
generate_button.grid(row=2, column=0, columnspan=2, sticky="news", padx=10, pady=10)

# Save button
save_button = ctk.CTkButton(input_frame, text="Save Image", command=save_image)
save_button.grid(row=3, column=0, columnspan=2, sticky="news", padx=10, pady=10)

# Create a canvas for image display
canvas = tkinter.Canvas(root, width=512, height=512)
canvas.pack(side="left")

# Start the GUI main loop
root.mainloop()
