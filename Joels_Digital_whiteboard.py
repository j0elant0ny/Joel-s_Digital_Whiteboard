import tkinter as tk
from tkinter import colorchooser, filedialog, messagebox
from PIL import Image, ImageDraw

class DigitalWhiteboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Joel's Digital Whiteboard")
        self.root.geometry("1000x700")

        self._create_toolbar()
        self._create_canvas()
        self._init_drawing_state()

    def _create_toolbar(self):
        self.toolbar_frame = tk.Frame(self.root, bg="lightgray")
        self.toolbar_frame.pack(side=tk.TOP, fill=tk.X)  # Ensures toolbar stays on top

        tools = [
            ("Pencil", "pencil"),
            ("Eraser", "eraser"),
            ("Line", "line"),
            ("Rectangle", "rectangle"),
            ("Circle", "circle"),
        ]
        for name, tool in tools:
            btn = tk.Button(self.toolbar_frame, text=name, command=lambda t=tool: self._select_tool(t))
            btn.pack(side=tk.LEFT, padx=5, pady=5)

        tk.Button(self.toolbar_frame, text="Color", command=self._choose_color).pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(self.toolbar_frame, text="Clear", command=self._clear_canvas).pack(side=tk.LEFT, padx=5, pady=5)

        self.brush_size = tk.IntVar(value=2)
        tk.Scale(self.toolbar_frame, from_=1, to=20, orient=tk.HORIZONTAL, variable=self.brush_size).pack(side=tk.LEFT, padx=5, pady=5)

        tk.Button(self.toolbar_frame, text="Save", command=self._save_drawing).pack(side=tk.LEFT, padx=5)

    def _create_canvas(self):
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(self.main_frame, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.bind("<Button-1>", self._start_draw)
        self.canvas.bind("<B1-Motion>", self._draw)
        self.canvas.bind("<ButtonRelease-1>", self._stop_draw)

    def _init_drawing_state(self):
        self.current_tool = "pencil"
        self.color = "black"
        self.drawing = False
        self.start_x = None
        self.start_y = None
        self.image = Image.new("RGB", (1000, 700), "white")
        self.draw = ImageDraw.Draw(self.image)
        self.current_shape = None

    def _select_tool(self, tool):
        self.current_tool = tool

    def _choose_color(self):
        color = colorchooser.askcolor(title="Choose Color")[1]
        if color:
            self.color = color

    def _start_draw(self, event):
        self.drawing = True
        self.start_x, self.start_y = event.x, event.y
        self.current_shape = None

    def _draw(self, event):
        if not self.drawing:
            return
        size = self.brush_size.get()
        if self.current_tool == "pencil":
            self.canvas.create_line(self.start_x, self.start_y, event.x, event.y, fill=self.color, width=size)
            self.draw.line([self.start_x, self.start_y, event.x, event.y], fill=self.color, width=size)
            self.start_x, self.start_y = event.x, event.y
        elif self.current_tool == "eraser":
            self.canvas.create_rectangle(event.x - size, event.y - size, event.x + size, event.y + size, fill="white", outline="white")
            self.draw.rectangle([event.x - size, event.y - size, event.x + size, event.y + size], fill="white")
        elif self.current_tool in {"line", "rectangle", "circle"}:
            if self.current_shape:
                self.canvas.delete(self.current_shape)
            if self.current_tool == "line":
                self.current_shape = self.canvas.create_line(self.start_x, self.start_y, event.x, event.y, fill=self.color, width=size)
            elif self.current_tool == "rectangle":
                self.current_shape = self.canvas.create_rectangle(self.start_x, self.start_y, event.x, event.y, outline=self.color, width=size)
            elif self.current_tool == "circle":
                self.current_shape = self.canvas.create_oval(self.start_x, self.start_y, event.x, event.y, outline=self.color, width=size)

    def _stop_draw(self, event):
        self.drawing = False
        if self.current_shape and self.current_tool in {"line", "rectangle", "circle"}:
            size = self.brush_size.get()
            if self.current_tool == "line":
                self.draw.line([self.start_x, self.start_y, event.x, event.y], fill=self.color, width=size)
            elif self.current_tool == "rectangle":
                self.draw.rectangle([self.start_x, self.start_y, event.x, event.y], outline=self.color, width=size)
            elif self.current_tool == "circle":
                self.draw.ellipse([self.start_x, self.start_y, event.x, event.y], outline=self.color, width=size)

    def _save_drawing(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
        if file_path:
            self.image.save(file_path, "PNG")
            messagebox.showinfo("Save", "Drawing saved successfully!")

    def _clear_canvas(self):
        self.canvas.delete("all")
        self.image = Image.new("RGB", (1000, 700), "white")
        self.draw = ImageDraw.Draw(self.image)

if __name__ == "__main__":
    root = tk.Tk()
    app = DigitalWhiteboard(root)
    root.mainloop()
