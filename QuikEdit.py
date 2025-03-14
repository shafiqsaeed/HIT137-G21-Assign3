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
# through graphical interface. It uses Object-Oriented Programming principles, 
# GUI development using Tkinter, and image processing using OpenCV. 


import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageOps

class ImageEditorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Editor")
        self.root.geometry("1200x800")

        # Variables
        self.original_image = None  # Stores the original loaded image
        self.current_image = None   # Stores the currently displayed image (original, cropped, or filtered)
        self.edited_images = []     # For undo/redo functionality
        self.current_image_index = -1
        self.zoom_scale = 1.0       # For zoom functionality

        # GUI Components
        self.create_menu()
        self.create_widgets()
        self.bind_shortcuts()

    def create_menu(self):
        # Create a menu bar
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Load Image (Ctrl+L)", command=self.load_image)
        file_menu.add_command(label="Save Image (Ctrl+S)", command=self.save_image)
        file_menu.add_separator()
        file_menu.add_command(label="Exit (Ctrl+Q)", command=self.root.quit)
        menubar.add_cascade(label="File", menu=file_menu)

        # Edit menu
        edit_menu = tk.Menu(menubar, tearoff=0)
        edit_menu.add_command(label="Crop Image (Ctrl+C)", command=self.start_crop)
        edit_menu.add_command(label="Undo (Ctrl+Z)", command=self.undo)
        edit_menu.add_command(label="Redo (Ctrl+Y)", command=self.redo)
        menubar.add_cascade(label="Edit", menu=edit_menu)

        # Filters menu
        filter_menu = tk.Menu(menubar, tearoff=0)
        filter_menu.add_command(label="Monochrome (Ctrl+M)", command=lambda: self.apply_filter("monochrome"))
        filter_menu.add_command(label="Warm (Ctrl+W)", command=lambda: self.apply_filter("warm"))
        filter_menu.add_command(label="Cool (Ctrl+Shift+C)", command=lambda: self.apply_filter("cool"))
        filter_menu.add_command(label="Bright (Ctrl+B)", command=lambda: self.apply_filter("bright"))
        menubar.add_cascade(label="Filters", menu=filter_menu)

        # View menu
        view_menu = tk.Menu(menubar, tearoff=0)
        view_menu.add_command(label="Zoom In (Ctrl+↑)", command=self.zoom_in)
        view_menu.add_command(label="Zoom Out (Ctrl+↓)", command=self.zoom_out)
        menubar.add_cascade(label="View", menu=view_menu)

        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="How-To Guide (F1)", command=self.show_how_to_guide)
        menubar.add_cascade(label="Help", menu=help_menu)

    def bind_shortcuts(self):
        # File operations
        self.root.bind("<Control-l>", lambda event: self.load_image())
        self.root.bind("<Control-s>", lambda event: self.save_image())
        self.root.bind("<Control-q>", lambda event: self.root.quit())
        
        # Edit operations
        self.root.bind("<Control-c>", lambda event: self.start_crop())
        
        # Filters
        self.root.bind("<Control-m>", lambda event: self.apply_filter("monochrome"))
        self.root.bind("<Control-w>", lambda event: self.apply_filter("warm"))
        self.root.bind("<Control-Shift-C>", lambda event: self.apply_filter("cool"))
        self.root.bind("<Control-b>", lambda event: self.apply_filter("bright"))
        
        # View
        self.root.bind("<Control-Up>", lambda event: self.zoom_in())
        self.root.bind("<Control-Down>", lambda event: self.zoom_out())
        
        # Help
        self.root.bind("<F1>", lambda event: self.show_how_to_guide())

    def create_widgets(self):
        # Frame for image display
        self.image_frame = tk.Frame(self.root, bg="white")
        self.image_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Canvas for displaying images
        self.canvas = tk.Canvas(self.image_frame, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Frame for controls
        self.control_frame = tk.Frame(self.root, bg="lightgray")
        self.control_frame.pack(fill=tk.X, padx=10, pady=5)

        # Button styles for different groups
        file_button_style = {"bg": "#4CAF50", "fg": "white", "activebackground": "#45a049", "font": ("Arial", 10)}
        edit_button_style = {"bg": "#2196F3", "fg": "white", "activebackground": "#1e88e5", "font": ("Arial", 10)}
        filter_button_style = {"bg": "#FF9800", "fg": "white", "activebackground": "#fb8c00", "font": ("Arial", 10)}
        view_button_style = {"bg": "#9C27B0", "fg": "white", "activebackground": "#8e24aa", "font": ("Arial", 10)}
        help_button_style = {"bg": "#607D8B", "fg": "white", "activebackground": "#546e7a", "font": ("Arial", 10)}

        # File operations buttons
        self.load_button = tk.Button(self.control_frame, text="Load Image", command=self.load_image, **file_button_style)
        self.load_button.pack(side=tk.LEFT, padx=5)

        self.save_button = tk.Button(self.control_frame, text="Save Image", command=self.save_image, **file_button_style)
        self.save_button.pack(side=tk.LEFT, padx=5)

        # Editing buttons
        self.crop_button = tk.Button(self.control_frame, text="Crop Image", command=self.start_crop, **edit_button_style)
        self.crop_button.pack(side=tk.LEFT, padx=5)

        self.resize_slider = tk.Scale(self.control_frame, from_=10, to=200, orient=tk.HORIZONTAL, label="Resize (%)", command=self.resize_image)
        self.resize_slider.pack(side=tk.LEFT, padx=5)

        self.undo_button = tk.Button(self.control_frame, text="Undo", command=self.undo, **edit_button_style)
        self.undo_button.pack(side=tk.LEFT, padx=5)

        self.redo_button = tk.Button(self.control_frame, text="Redo", command=self.redo, **edit_button_style)
        self.redo_button.pack(side=tk.LEFT, padx=5)

        # Filter buttons
        self.monochrome_button = tk.Button(self.control_frame, text="Monochrome", command=lambda: self.apply_filter("monochrome"), **filter_button_style)
        self.monochrome_button.pack(side=tk.LEFT, padx=5)

        self.warm_button = tk.Button(self.control_frame, text="Warm", command=lambda: self.apply_filter("warm"), **filter_button_style)
        self.warm_button.pack(side=tk.LEFT, padx=5)

        self.cool_button = tk.Button(self.control_frame, text="Cool", command=lambda: self.apply_filter("cool"), **filter_button_style)
        self.cool_button.pack(side=tk.LEFT, padx=5)

        self.bright_button = tk.Button(self.control_frame, text="Bright", command=lambda: self.apply_filter("bright"), **filter_button_style)
        self.bright_button.pack(side=tk.LEFT, padx=5)

        # View buttons
        self.zoom_in_button = tk.Button(self.control_frame, text="Zoom In", command=self.zoom_in, **view_button_style)
        self.zoom_in_button.pack(side=tk.LEFT, padx=5)

        self.zoom_out_button = tk.Button(self.control_frame, text="Zoom Out", command=self.zoom_out, **view_button_style)
        self.zoom_out_button.pack(side=tk.LEFT, padx=5)

        # Help button
        self.how_to_button = tk.Button(self.control_frame, text="How-To Guide", command=self.show_how_to_guide, **help_button_style)
        self.how_to_button.pack(side=tk.LEFT, padx=5)

        # Copyright info
        self.copyright_label = tk.Label(self.root, text="© 2023 Image Editor. All rights reserved.", bg="lightgray")
        self.copyright_label.pack(side=tk.BOTTOM, fill=tk.X)

    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;*.bmp")])
        if file_path:
            self.original_image = cv2.imread(file_path)
            self.original_image = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2RGB)  # Convert to RGB
            self.current_image = self.original_image.copy()
            self.display_image(self.current_image)
            self.edited_images = [self.current_image.copy()]
            self.current_image_index = 0

    def display_image(self, image):
        self.canvas.delete("all")
        image = Image.fromarray(image)
        # Apply zoom
        width, height = image.size
        new_width, new_height = int(width * self.zoom_scale), int(height * self.zoom_scale)
        image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)  # Updated for Pillow 10+
        self.tk_image = ImageTk.PhotoImage(image)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)

    def start_crop(self):
        if self.current_image is None:
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
        if self.current_image is None:
            return

        # Get crop coordinates
        x1, y1 = min(self.start_x, self.end_x), min(self.start_y, self.end_y)
        x2, y2 = max(self.start_x, self.end_x), max(self.start_y, self.end_y)

        # Crop image
        self.current_image = self.current_image[y1:y2, x1:x2]
        self.display_image(self.current_image)
        self.add_to_history(self.current_image)

    def resize_image(self, value):
        if self.current_image is None:
            return

        scale = int(value) / 100.0
        resized_image = cv2.resize(self.current_image, None, fx=scale, fy=scale)
        self.display_image(resized_image)
        self.add_to_history(resized_image)

    def save_image(self):
        if self.current_image is None:
            messagebox.showwarning("Warning", "No image to save!")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Files", "*.png")])
        if file_path:
            cv2.imwrite(file_path, cv2.cvtColor(self.current_image, cv2.COLOR_RGB2BGR))
            messagebox.showinfo("Success", "Image saved successfully!")

    def add_to_history(self, image):
        self.edited_images = self.edited_images[:self.current_image_index + 1]
        self.edited_images.append(image.copy())
        self.current_image_index += 1

    def undo(self):
        if self.current_image_index > 0:
            self.current_image_index -= 1
            self.current_image = self.edited_images[self.current_image_index]
            self.display_image(self.current_image)

    def redo(self):
        if self.current_image_index < len(self.edited_images) - 1:
            self.current_image_index += 1
            self.current_image = self.edited_images[self.current_image_index]
            self.display_image(self.current_image)

    def apply_filter(self, filter_type):
        if self.current_image is None:
            return

        if filter_type == "monochrome":
            filtered_image = cv2.cvtColor(self.current_image, cv2.COLOR_RGB2GRAY)
            filtered_image = cv2.cvtColor(filtered_image, cv2.COLOR_GRAY2RGB)
        elif filter_type == "warm":
            filtered_image = self.current_image.copy()
            filtered_image[:, :, 0] = np.clip(filtered_image[:, :, 0] * 0.9, 0, 255)  # Reduce blue
            filtered_image[:, :, 2] = np.clip(filtered_image[:, :, 2] * 1.1, 0, 255)  # Increase red
        elif filter_type == "cool":
            filtered_image = self.current_image.copy()
            filtered_image[:, :, 2] = np.clip(filtered_image[:, :, 2] * 0.9, 0, 255)  # Reduce red
            filtered_image[:, :, 0] = np.clip(filtered_image[:, :, 0] * 1.1, 0, 255)  # Increase blue
        elif filter_type == "bright":
            filtered_image = cv2.convertScaleAbs(self.current_image, alpha=1.2, beta=30)

        self.current_image = filtered_image
        self.display_image(self.current_image)
        self.add_to_history(self.current_image)

    def zoom_in(self):
        self.zoom_scale *= 1.2
        self.display_image(self.current_image)

    def zoom_out(self):
        self.zoom_scale /= 1.2
        self.display_image(self.current_image)

    def show_how_to_guide(self):
        instructions = """
        How-To Guide & Keyboard Shortcuts:
        
        File Operations:
        - Load Image: Ctrl+L
        - Save Image: Ctrl+S
        - Exit: Ctrl+Q

        Edit Operations:
        - Crop Image: Ctrl+C
        - Undo: Ctrl+Z
        - Redo: Ctrl+Y

        Filters:
        - Monochrome: Ctrl+M
        - Warm: Ctrl+W
        - Cool: Ctrl+Shift+C
        - Bright: Ctrl+B

        View Controls:
        - Zoom In: Ctrl+↑
        - Zoom Out: Ctrl+↓

        General:
        - How-To Guide: F1

        Workflow:
        1. Load an image using Ctrl+L or File > Load Image
        2. Crop the image (Ctrl+C) by drawing a rectangle
        3. Resize using the slider
        4. Apply filters using keyboard shortcuts or menu
        5. Use Zoom controls (Ctrl+↑/↓) to adjust view
        6. Save your work with Ctrl+S
        7. Use Undo/Redo (Ctrl+Z/Y) to correct mistakes
        """
        messagebox.showinfo("How-To Guide & Shortcuts", instructions)

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageEditorApp(root)
    root.mainloop()
