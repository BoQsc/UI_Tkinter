import tkinter as tk
from itertools import islice

class OptimizedTaskbar:
    def __init__(self, root):
        self.root = root
        self.root.title("Optimized Taskbar")
        self.root.geometry("800x200")
        self.root.minsize(400, 100)
        
        # Program database with 30+ example names
        self.programs = [{"name": f"Program {i+1}"} for i in range(30)]
        self.current_start = 0
        
        # Main container setup
        self.taskbar = tk.Frame(root, bg='gray')
        self.taskbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Grid configuration with proper weight distribution
        self.taskbar.grid_columnconfigure(0, weight=3, minsize=240)  # Green span (3x width)
        for i in range(1, 21):
            self.taskbar.grid_columnconfigure(i, weight=1, minsize=80)
        self.taskbar.grid_columnconfigure(21, weight=0)  # Navigation buttons
        
        # Initialize all UI elements
        self.create_widgets()
        self.update_display()
        self.root.bind('<Configure>', self.on_resize)

    def create_widgets(self):
        """Create permanent widgets with proper parent-child relationships"""
        # Green span (fixed 3:1 ratio)
        self.green_span = tk.Frame(self.taskbar, bg='green', height=30)
        self.green_span.grid(row=0, column=0, sticky='nsew')
        
        # Blue rectangles with persistent references
        self.blue_frames = []
        for col in range(1, 21):
            frame = tk.Frame(self.taskbar,
                           bg='white',
                           highlightbackground='blue',
                           highlightthickness=1,
                           bd=2,
                           relief='solid')
            label = tk.Label(frame, text="", bg='white')
            label.pack(expand=True, fill='both')
            frame.grid(row=0, column=col, sticky='nsew')
            self.blue_frames.append(frame)
        
        # Navigation buttons with proper packing
        self.btn_frame = tk.Frame(self.taskbar)
        self.btn_up = tk.Button(self.btn_frame, text="▲", command=self.move_up)
        self.btn_down = tk.Button(self.btn_frame, text="▼", command=self.move_down)
        self.btn_up.pack(side=tk.TOP, fill='x')
        self.btn_down.pack(side=tk.TOP, fill='x')

    def update_display(self):
        """Safe update of visible elements with bounds checking"""
        try:
            # Calculate visible columns based on current width
            total_width = self.taskbar.winfo_width()
            green_width = self.green_span.winfo_width()
            available_width = total_width - green_width
            
            # Calculate visible blue rectangles
            max_visible = min(len(self.blue_frames), available_width // 80)
            visible_cols = min(max_visible, len(self.programs) - self.current_start)
            
            # Update program labels
            programs = self.programs[self.current_start:self.current_start + visible_cols]
            for i, frame in enumerate(self.blue_frames):
                if i < visible_cols:
                    frame.grid()
                    frame.winfo_children()[0].config(text=programs[i]['name'])
                else:
                    frame.grid_remove()
            
            # Update navigation buttons
            self.update_navigation(visible_cols)
            
        except (IndexError, tk.TclError) as e:
            print(f"Display update error: {e}")

    def update_navigation(self, visible_cols):
        """Proper navigation visibility logic"""
        total_programs = len(self.programs)
        needed = total_programs > visible_cols
        
        if needed:
            self.btn_frame.grid(row=0, column=21, sticky='ns')
        else:
            self.btn_frame.grid_forget()
            
        # Disable buttons at boundaries
        self.btn_up.config(state='normal' if self.current_start > 0 else 'disabled')
        upper_bound = self.current_start + visible_cols
        self.btn_down.config(state='normal' if upper_bound < len(self.programs) else 'disabled')

    def move_up(self):
        if self.current_start > 0:
            self.current_start -= 1
            self.update_display()

    def move_down(self):
        if self.current_start + 1 < len(self.programs):
            self.current_start += 1
            self.update_display()

    def on_resize(self, event):
        """Debounced resize handler with error suppression"""
        if event.widget != self.root:
            return
        
        if hasattr(self, '_resize_timer'):
            self.root.after_cancel(self._resize_timer)
            
        self._resize_timer = self.root.after(50, self.safe_resize)

    def safe_resize(self):
        """Protected resize operation"""
        try:
            self.update_display()
        except Exception as e:
            print(f"Resize error: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = OptimizedTaskbar(root)
    root.mainloop()