# HIT 137 Software Now 

# Assignment 3

# Group: CAS/DAN 21
# Abu Saeed Md Shafiqur Rahman (Shafiq Rahman) - S386795
# Annafi Bin Alam (Rafin Alam) - S387086
# Neville James Doyle (Nev Doyle) - S371207
# Yuvraj Singh (Yuvraj Singh) - S383324

# GitHub Repository: https://github.com/shafiqsaeed/HIT137-G21-Assign3

# Submitted: 7 February 2025

# Program - QuikEdit
# This program allows users to upload, manipulate and save edited images 
# through graphical interface. # It uses Object-Oriented Programming principles, 
# GUI development using Tkinter, and image processing using OpenCV. 

import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

class ImageEditorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("QuikEdit - the fastest image editor")
        self.root.geometry("1200x700")

        # Variables
        self.image = None
        self.cropped_image = None
        self.edited_images = []  # For undo/redo functionality
        self.current_image_index = -1

        # GUI Components
        self.create_widgets()

    def create_widgets(self):
        # Frame for image display
        self.image_frame = tk.Frame(self.root, bg="white")
        self.image_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Canvas for displaying images
        self.canvas = tk.Canvas(self.image_frame, bg="gray")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Frame for controls
        self.control_frame = tk.Frame(self.root, bg="lightgray")
        self.control_frame.pack(fill=tk.X, padx=10, pady=5)

        # Buttons
        self.load_button = tk.Button(self.control_frame, text="Load Image", command=self.load_image)
        self.load_button.pack(side=tk.LEFT, padx=5)

        self.crop_button = tk.Button(self.control_frame, text="Crop Image", command=self.start_crop)
        self.crop_button.pack(side=tk.LEFT, padx=5)

        self.resize_slider = tk.Scale(self.control_frame, from_=10, to=200, orient=tk.HORIZONTAL, label="Resize (%)", command=self.resize_image)
        self.resize_slider.pack(side=tk.LEFT, padx=5)

        self.save_button = tk.Button(self.control_frame, text="Save Image", command=self.save_image)
        self.save_button.pack(side=tk.LEFT, padx=5)

        self.undo_button = tk.Button(self.control_frame, text="Undo", command=self.undo)
        self.undo_button.pack(side=tk.LEFT, padx=5)

        self.redo_button = tk.Button(self.control_frame, text="Redo", command=self.redo)
        self.redo_button.pack(side=tk.LEFT, padx=5)

        # Copyright info
        self.copyright_label = tk.Label(self.root, text="© 2025 QuikEdit. All rights reserved.", bg="lightgray")
        self.copyright_label.pack(side=tk.BOTTOM, fill=tk.X)

        # How-to section
        self.how_to_label = tk.Label(self.root, text="How-to: Load an image, crop, resize, and save!", bg="lightgray")
        self.how_to_label.pack(side=tk.BOTTOM, fill=tk.X)

        # Keyboard shortcuts
        self.root.bind("<Control-z>", lambda event: self.undo())
        self.root.bind("<Control-y>", lambda event: self.redo())

    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;*.bmp")])
        if file_path:
            self.image = cv2.imread(file_path)
            self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)  # Convert to RGB
            self.display_image(self.image)
            self.edited_images = [self.image.copy()]
            self.current_image_index = 0

    def display_image(self, image):
        self.canvas.delete("all")
        image = Image.fromarray(image)
        image.thumbnail((1600, 1000))  # Resize to fit canvas
        self.tk_image = ImageTk.PhotoImage(image)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)

    def start_crop(self):
        if self.image is None:
            messagebox.showwarning("Warning", "Please load an image first!")
            return

        self.canvas.bind("<ButtonPress-1>", self.on_crop_start)
        self.canvas.bind("<B1-Motion>", self.on_crop_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_crop_end)

    def on_crop_start(self, event):
        self.start_x = event.x
        self.start_y = event.y

    def on_crop_drag(self, event):
        self.canvas.delete("crop_rect")
        self.canvas.create_rectangle(self.start_x, self.start_y, event.x, event.y, outline="red", tag="crop_rect")

    def on_crop_end(self, event):
        self.end_x = event.x
        self.end_y = event.y
        self.crop_image()

    def crop_image(self):
        if self.image is None:
            return

        # Get crop coordinates
        x1, y1 = min(self.start_x, self.end_x), min(self.start_y, self.end_y)
        x2, y2 = max(self.start_x, self.end_x), max(self.start_y, self.end_y)

        # Crop image
        self.cropped_image = self.image[y1:y2, x1:x2]
        self.display_image(self.cropped_image)
        self.add_to_history(self.cropped_image)

    def resize_image(self, value):
        if self.cropped_image is None:
            return

        scale = int(value) / 100.0
        resized_image = cv2.resize(self.cropped_image, None, fx=scale, fy=scale)
        self.display_image(resized_image)
        self.add_to_history(resized_image)

    def save_image(self):
        if self.cropped_image is None:
            messagebox.showwarning("Warning", "No image to save!")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Files", "*.png")])
        if file_path:
            cv2.imwrite(file_path, cv2.cvtColor(self.cropped_image, cv2.COLOR_RGB2BGR))
            messagebox.showinfo("Success", "Image saved successfully!")

    def add_to_history(self, image):
        self.edited_images = self.edited_images[:self.current_image_index + 1]
        self.edited_images.append(image.copy())
        self.current_image_index += 1

    def undo(self):
        if self.current_image_index > 0:
            self.current_image_index -= 1
            self.display_image(self.edited_images[self.current_image_index])

    def redo(self):
        if self.current_image_index < len(self.edited_images) - 1:
            self.current_image_index += 1
            self.display_image(self.edited_images[self.current_image_index])

    def apply_filter(self, filter_type):
        if self.cropped_image is None:
            return

        if filter_type == "monochrome":
            filtered_image = cv2.cvtColor(self.cropped_image, cv2.COLOR_RGB2GRAY)
            filtered_image = cv2.cvtColor(filtered_image, cv2.COLOR_GRAY2RGB)
        elif filter_type == "warm":
            filtered_image = self.cropped_image.copy()
            filtered_image[:, :, 0] = np.clip(filtered_image[:, :, 0] * 0.9, 0, 255)  # Reduce blue
            filtered_image[:, :, 2] = np.clip(filtered_image[:, :, 2] * 1.1, 0, 255)  # Increase red
        elif filter_type == "cool":
            filtered_image = self.cropped_image.copy()
            filtered_image[:, :, 2] = np.clip(filtered_image[:, :, 2] * 0.9, 0, 255)  # Reduce red
            filtered_image[:, :, 0] = np.clip(filtered_image[:, :, 0] * 1.1, 0, 255)  # Increase blue
        elif filter_type == "bright":
            filtered_image = cv2.convertScaleAbs(self.cropped_image, alpha=1.2, beta=30)

        self.display_image(filtered_image)
        self.add_to_history(filtered_image)

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageEditorApp(root)
    root.mainloop()