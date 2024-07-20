import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from PIL import Image, ImageTk
import cv2
import numpy as np


class ImageApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Viewer with Zoom and Report")

        # UI Elements
        self.create_widgets()

        # Variables
        self.image_path = ""
        self.cv_img = None
        self.original_img = None
        self.filtered_img = None
        self.tk_img_original = None
        self.tk_img_filtered = None
        self.current_zoom = 1.0
        self.zoomed_original = None
        self.zoomed_filtered = None

        # Variables for mouse interaction
        self.last_x = None
        self.last_y = None
        self.canvas_original.bind("<ButtonPress-1>", self.on_start_drag)
        self.canvas_original.bind("<B1-Motion>", self.on_dragging)
        self.canvas_filtered.bind("<ButtonPress-1>", self.on_start_drag)
        self.canvas_filtered.bind("<B1-Motion>", self.on_dragging)

        self.canvas_original.bind("<MouseWheel>", self.on_mousewheel)
        self.canvas_filtered.bind("<MouseWheel>", self.on_mousewheel)

    def create_widgets(self):
        # Load Image Button
        self.load_btn = ttk.Button(self.root, text="Upload Your Image", command=self.load_image)
        self.load_btn.grid(row=0, column=0, pady=10, padx=10)

        # Canvas for Original Image
        self.canvas_original = tk.Canvas(self.root, width=400, height=600, bg="light blue")
        self.canvas_original.grid(row=1, column=0, padx=10)

        # Canvas for Filtered Image
        self.canvas_filtered = tk.Canvas(self.root, width=400, height=600, bg="light gray")
        self.canvas_filtered.grid(row=1, column=1, padx=10)

        # Zoom Scale
        self.zoom_scale = ttk.Scale(self.root, from_=0.5, to=3.0, orient="horizontal", command=self.zoom_image)
        self.zoom_scale.grid(row=2, column=0, columnspan=2, pady=10, padx=10)
        self.zoom_scale.set(1.0)  # Set initial zoom scale

        # Report Button
        self.report_btn = ttk.Button(self.root, text="Generate Report", command=self.generate_report)
        self.report_btn.grid(row=3, column=0, columnspan=2, pady=10, padx=10)

    def load_image(self):
        self.image_path = filedialog.askopenfilename()
        if self.image_path:
            self.cv_img = cv2.imread(self.image_path)
            self.process_images()

    def process_images(self):
        if self.cv_img is not None:
            # Resize original image to fit canvas
            self.original_img = cv2.cvtColor(self.cv_img, cv2.COLOR_BGR2RGB)
            self.display_original_image()

            # Apply filter to create filtered image (e.g., edge detection)
            gray = cv2.cvtColor(self.cv_img, cv2.COLOR_BGR2GRAY)
            edges = cv2.Canny(gray, 50, 150)  # Adjust parameters as needed
            self.filtered_img = cv2.cvtColor(edges, cv2.COLOR_GRAY2RGB)
            self.display_filtered_image()

    def display_original_image(self):
        if self.original_img is not None:
            # Use original image size
            self.zoomed_original = self.original_img.copy()

            # Convert to PIL format and then to ImageTk format
            img_pil = Image.fromarray(self.zoomed_original)
            self.tk_img_original = ImageTk.PhotoImage(img_pil)

            # Clear canvas before displaying the new image
            self.canvas_original.delete("all")

            # Update Canvas with the original size image
            self.canvas_original.create_image(0, 0, anchor="nw", image=self.tk_img_original)
            self.canvas_original.config(scrollregion=self.canvas_original.bbox(tk.ALL))

    def display_filtered_image(self):
        if self.filtered_img is not None:
            # Use filtered image size
            self.zoomed_filtered = self.filtered_img.copy()

            # Convert to PIL format and then to ImageTk format
            img_pil = Image.fromarray(self.zoomed_filtered)
            self.tk_img_filtered = ImageTk.PhotoImage(img_pil)

            # Clear canvas before displaying the new image
            self.canvas_filtered.delete("all")

            # Update Canvas with the original size image
            self.canvas_filtered.create_image(0, 0, anchor="nw", image=self.tk_img_filtered)
            self.canvas_filtered.config(scrollregion=self.canvas_filtered.bbox(tk.ALL))

    def zoom_image(self, scale):
        if self.original_img is not None and self.filtered_img is not None:
            scale = float(scale)
            self.current_zoom = scale

            # Resize original image based on current zoom scale
            height, width, _ = self.original_img.shape
            new_size = (int(width * scale), int(height * scale))
            self.zoomed_original = cv2.resize(self.original_img, new_size, interpolation=cv2.INTER_LINEAR)

            # Resize filtered image based on current zoom scale
            height, width, _ = self.filtered_img.shape
            new_size = (int(width * scale), int(height * scale))
            self.zoomed_filtered = cv2.resize(self.filtered_img, new_size, interpolation=cv2.INTER_LINEAR)

            # Convert to PIL format and then to ImageTk format
            img_pil_original = Image.fromarray(self.zoomed_original)
            self.tk_img_original = ImageTk.PhotoImage(img_pil_original)

            img_pil_filtered = Image.fromarray(self.zoomed_filtered)
            self.tk_img_filtered = ImageTk.PhotoImage(img_pil_filtered)

            # Clear canvas before displaying the new image
            self.canvas_original.delete("all")
            self.canvas_filtered.delete("all")

            # Update Canvas with the resized original image
            self.canvas_original.create_image(0, 0, anchor="nw", image=self.tk_img_original)
            self.canvas_original.config(scrollregion=self.canvas_original.bbox(tk.ALL))

            # Update Canvas with the resized filtered image
            self.canvas_filtered.create_image(0, 0, anchor="nw", image=self.tk_img_filtered)
            self.canvas_filtered.config(scrollregion=self.canvas_filtered.bbox(tk.ALL))

    # Ensure you remove duplicate method definitions for `on_mousewheel`
    def on_mousewheel(self, event):
        # Determine zoom direction
        if event.delta > 0:
            zoom_factor = 1.1
        else:
            zoom_factor = 0.9

        # Update zoom scale
        new_scale = self.zoom_scale.get() * zoom_factor
        new_scale = min(max(new_scale, 0.5), 3.0)  # Restrict the scale within the range
        self.zoom_scale.set(new_scale)
        self.zoom_image(new_scale)

        # Update zoom scale
        new_scale = self.zoom_scale.get() * zoom_factor
        new_scale = min(max(new_scale, 0.5), 3.0)  # Restrict the scale within the range
        self.zoom_scale.set(new_scale)
        self.zoom_image(new_scale)

    def on_start_drag(self, event):
        self.last_x = event.x
        self.last_y = event.y

    def on_dragging(self, event):
        if self.last_x is not None and self.last_y is not None:
            dx = event.x - self.last_x
            dy = event.y - self.last_y
            self.last_x = event.x
            self.last_y = event.y

            # Move original canvas image
            self.canvas_original.move(tk.ALL, dx, dy)

            # Move filtered canvas image
            self.canvas_filtered.move(tk.ALL, dx, dy)

    def on_mousewheel(self, event):
        scale = 1.1 if event.delta > 0 else 0.9
        self.zoom_scale.set(self.zoom_scale.get() * scale)
        self.zoom_image(self.zoom_scale.get())

    def generate_report(self):
        if self.cv_img is None:
            messagebox.showerror("Error", "No image loaded")
            return

        # Example report generation (can be modified as needed)
        gray = cv2.cvtColor(self.cv_img, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY_INV)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        report = []
        for contour in contours:
            area = cv2.contourArea(contour)
            x, y, w, h = cv2.boundingRect(contour)
            report.append(f"Defect at ({x}, {y}), Width: {w}, Height: {h}, Area: {area}")

        if report:
            report_text = "\n".join(report)
            messagebox.showinfo("Defect Report", report_text)
        else:
            messagebox.showinfo("Defect Report", "No defects detected")


if __name__ == "__main__":
    root = tk.Tk()
    app = ImageApp(root)
    root.mainloop()