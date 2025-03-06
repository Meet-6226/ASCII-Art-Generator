import tkinter as tk
from tkinter import filedialog, ttk, scrolledtext, messagebox
from pyfiglet import figlet_format
from termcolor import colored
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import numpy as np

# Constants
ASCII_CHARS = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "
FIXED_WIDTH = 120

# Theme Colors
DARK_THEME = {
    'bg': "#1E1E1E",
    'fg': "#0F0",
    'button_bg': "#2D2D2D",
    'active_bg': "#3D3D3D",
    'pressed_bg': "#2D2D2D"
}

WHITE_THEME = {
    'bg': "#FFFFFF",
    'fg': "#666666",
    'button_bg': "#F0F0F0",
    'active_bg': "#E0E0E0",
    'pressed_bg': "#D0D0D0"
}

# Font and UI Settings
FONT_STYLES = ['slant', 'banner', 'block', 'bubble', 'digital', 'ivrit', 'mini', 
               'script', 'shadow', 'smscript', 'smshadow', 'smslant']
TEXT_COLORS = ["green", "red", "yellow", "blue", "magenta", "cyan", "white"]
DEFAULT_FONT = ('Arial', 12)
DEFAULT_PADDING = (10, 5)

class ASCIIArtGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("ASCII Art Generator")
        self.root.geometry("1200x800")
        
        self.style = ttk.Style()
        self.setup_styles()
        self.create_widgets()
        self.setup_layout()
        
    def setup_styles(self):
        # Dark Theme Styles
        self.style.configure('TLabel', 
            padding=DEFAULT_PADDING, 
            font=DEFAULT_FONT,
            background=DARK_THEME['bg'],
            foreground=DARK_THEME['fg']
        )
        
        for widget in ['TCombobox', 'TEntry']:
            self.style.configure(widget, 
                padding=DEFAULT_PADDING,
                font=DEFAULT_FONT,
                fieldbackground=DARK_THEME['button_bg'],
                foreground=DARK_THEME['fg'],
                background=DARK_THEME['bg']
            )
            
        for frame in ['Controls.TFrame', 'Button.TFrame']:
            self.style.configure(frame, background=DARK_THEME['bg'])
            
        self.style.configure('Action.TButton',
            background=DARK_THEME['button_bg'],
            foreground=DARK_THEME['fg'],
            padding=DEFAULT_PADDING,
            font=DEFAULT_FONT
        )
        
        # White Theme Styles
        self.style.configure('White.TLabel',
            padding=DEFAULT_PADDING,
            font=DEFAULT_FONT,
            background=WHITE_THEME['bg'],
            foreground=WHITE_THEME['fg']
        )
        
        for widget in ['TCombobox', 'TEntry']:
            self.style.configure(f'White.{widget}',
                padding=DEFAULT_PADDING,
                font=DEFAULT_FONT,
                fieldbackground=WHITE_THEME['button_bg'],
                foreground=WHITE_THEME['fg'],
                background=WHITE_THEME['bg']
            )
            
        for frame in ['Controls.TFrame', 'Button.TFrame']:
            self.style.configure(f'White.{frame}', background=WHITE_THEME['bg'])
            
        self.style.configure('White.Action.TButton',
            background=WHITE_THEME['button_bg'],
            foreground=WHITE_THEME['fg'],
            padding=DEFAULT_PADDING,
            font=DEFAULT_FONT
        )
        
        # Button States
        self.style.map('Action.TButton',
            background=[('active', DARK_THEME['active_bg']), ('pressed', DARK_THEME['pressed_bg'])],
            foreground=[('active', DARK_THEME['fg']), ('pressed', DARK_THEME['fg'])]
        )
        
        self.style.map('White.Action.TButton',
            background=[('active', WHITE_THEME['active_bg']), ('pressed', WHITE_THEME['pressed_bg'])],
            foreground=[('active', WHITE_THEME['fg']), ('pressed', WHITE_THEME['fg'])]
        )
        
        # Combobox States
        for theme, colors in [('', DARK_THEME), ('White.', WHITE_THEME)]:
            self.style.map(f'{theme}TCombobox',
                fieldbackground=[('readonly', colors['button_bg']), ('active', colors['button_bg'])],
                selectbackground=[('readonly', colors['button_bg'])],
                selectforeground=[('readonly', colors['fg'])],
                background=[('readonly', colors['bg']), ('active', colors['bg'])]
            )
    
    def create_widgets(self):
        # Create Frames
        self.controls_frame = ttk.Frame(self.root, style='Controls.TFrame')
        self.button_frame = ttk.Frame(self.root, style='Button.TFrame')
        
        # Create Input Widgets
        self.create_input_widgets()
        
        # Create Buttons
        self.create_buttons()
        
        # Create Output Text
        self.output_text = scrolledtext.ScrolledText(
            self.root, 
            width=120, 
            height=30, 
            font=('Courier', 10),
            borderwidth=2,
            relief="solid"
        )
        
    def create_input_widgets(self):
        # Message Entry
        self.msg_label = ttk.Label(self.controls_frame, text="Message:")
        self.msg_entry = ttk.Entry(self.controls_frame, width=50, font=DEFAULT_FONT)
        self.msg_entry.bind("<KeyRelease>", self.update_preview)
        
        # Font Selection
        self.font_label = ttk.Label(self.controls_frame, text="Font:")
        self.font_var = ttk.Combobox(self.controls_frame, values=FONT_STYLES, width=30, state='readonly')
        self.font_var.set("banner")
        self.font_var.bind("<<ComboboxSelected>>", self.update_preview)
        
        # Theme Selection
        self.theme_label = ttk.Label(self.controls_frame, text="Theme:")
        self.theme_var = ttk.Combobox(self.controls_frame, values=["dark", "white"], width=30, state='readonly')
        self.theme_var.set("dark")
        self.theme_var.bind("<<ComboboxSelected>>", self.update_theme)
        
        # Color Selection
        self.color_label = ttk.Label(self.controls_frame, text="Text Color:")
        self.color_var = ttk.Combobox(self.controls_frame, values=TEXT_COLORS, width=30, state='readonly')
        self.color_var.set("green")
        self.color_var.bind("<<ComboboxSelected>>", self.update_preview)
        
    def create_buttons(self):
        button_configs = [
            ("Generate ASCII", self.generate_ascii),
            ("Upload Image", self.upload_image),
            ("Save as TXT", self.save_as_txt),
            ("Save as PNG", self.save_as_png)
        ]
        
        self.buttons = []
        for i, (text, command) in enumerate(button_configs, start=1):
            btn = ttk.Button(self.button_frame, text=text, command=command, width=15)
            btn.grid(row=0, column=i, padx=10, pady=10)
            self.buttons.append(btn)
            
    def setup_layout(self):
        # Configure Grid Weights
        self.root.grid_rowconfigure(2, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        # Configure Controls Frame
        self.controls_frame.grid(row=0, column=0, columnspan=4, padx=20, pady=(20,10), sticky="nsew")
        self.controls_frame.grid_columnconfigure(1, weight=1)
        self.controls_frame.grid_columnconfigure(2, minsize=20)
        self.controls_frame.grid_columnconfigure(3, weight=1)
        
        # Layout Input Widgets
        widgets = [
            (self.msg_label, self.msg_entry),
            (self.font_label, self.font_var),
            (self.theme_label, self.theme_var),
            (self.color_label, self.color_var)
        ]
        
        for i, (label, widget) in enumerate(widgets):
            label.grid(row=i, column=0, sticky="w", padx=(10,5), pady=15)
            widget.grid(row=i, column=1, sticky="ew" if isinstance(widget, ttk.Entry) else "w", 
                       columnspan=3 if isinstance(widget, ttk.Entry) else 1,
                       padx=5, pady=15)
        
        # Layout Button Frame
        self.button_frame.grid(row=1, column=0, columnspan=4, padx=20, pady=(10,20), sticky="nsew")
        self.button_frame.grid_columnconfigure(0, weight=1)
        self.button_frame.grid_columnconfigure(5, weight=1)
        
        # Layout Output Text
        self.output_text.grid(row=2, column=0, columnspan=4, padx=20, pady=(0,20), sticky="nsew")
        
    def image_to_ascii(self, image_path):
        try:
            img = Image.open(image_path)
            img = ImageEnhance.Contrast(img).enhance(1.5)
            img = ImageEnhance.Brightness(img).enhance(1.2)
            
            aspect_ratio = img.height / img.width
            height = int(FIXED_WIDTH * aspect_ratio * 0.5)
            img = img.resize((FIXED_WIDTH, height), Image.Resampling.LANCZOS)
            
            img = img.convert('L')
            pixels = np.array(img)
            
            return '\n'.join(''.join(ASCII_CHARS[int((pixel / 255) * (len(ASCII_CHARS) - 1))]
                                   for pixel in row) for row in pixels)
        except Exception as e:
            return f"Error converting image: {str(e)}"
            
    def update_preview(self, *args):
        try:
            ascii_art = figlet_format(self.msg_entry.get(), font=self.font_var.get())
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, ascii_art)
            self.output_text.configure(fg=self.color_var.get())
        except Exception as e:
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, f"Error: {e}")
            
    def update_theme(self, *args):
        theme = self.theme_var.get()
        colors = WHITE_THEME if theme == "white" else DARK_THEME
        
        self.root.configure(bg=colors['bg'])
        
        # Update Frames
        self.controls_frame.configure(style=f"{'White.' if theme == 'white' else ''}Controls.TFrame")
        self.button_frame.configure(style=f"{'White.' if theme == 'white' else ''}Button.TFrame")
        
        # Update Labels
        for label in [self.msg_label, self.font_label, self.theme_label, self.color_label]:
            label.configure(style=f"{'White.' if theme == 'white' else ''}TLabel")
            
        # Update Comboboxes
        for combo in [self.font_var, self.theme_var, self.color_var]:
            combo.configure(style=f"{'White.' if theme == 'white' else ''}TCombobox")
            
        # Update Buttons
        button_style = f"{'White.' if theme == 'white' else ''}Action.TButton"
        for button in self.buttons:
            button.configure(style=button_style)
            
        # Keep Output Window Consistent
        self.output_text.configure(bg="black", fg="green", insertbackground="green")
        
    def generate_ascii(self):
        self.update_preview()
        
    def save_as_txt(self):
        ascii_art = self.output_text.get(1.0, tk.END)
        file_path = filedialog.asksaveasfilename(defaultextension=".txt")
        if file_path:
            with open(file_path, "w") as f:
                f.write(ascii_art)
            messagebox.showinfo("Saved", f"ASCII art saved as {file_path}")
            
    def save_as_png(self):
        ascii_art = self.output_text.get(1.0, tk.END)
        file_path = filedialog.asksaveasfilename(defaultextension=".png")
        if file_path:
            lines = ascii_art.split("\n")
            font = ImageFont.load_default()
            line_height = 15
            img_width = max(len(line) for line in lines) * 10
            img_height = len(lines) * line_height + 20
            
            img = Image.new("RGB", (img_width, img_height), "black")
            draw = ImageDraw.Draw(img)
            
            y_offset = 10
            for line in lines:
                draw.text((10, y_offset), line, fill=self.color_var.get(), font=font)
                y_offset += line_height
                
            img.save(file_path)
            messagebox.showinfo("Saved", f"ASCII art saved as {file_path}")
            
    def upload_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp")]
        )
        if file_path:
            try:
                ascii_art = self.image_to_ascii(file_path)
                self.output_text.delete(1.0, tk.END)
                self.output_text.insert(tk.END, ascii_art)
                messagebox.showinfo("Success", "Image converted to ASCII art successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to convert image: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ASCIIArtGenerator(root)
    root.mainloop()
