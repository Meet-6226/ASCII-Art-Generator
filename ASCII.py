import tkinter as tk
from tkinter import filedialog, ttk, scrolledtext, messagebox
from pyfiglet import figlet_format
from termcolor import colored
from PIL import Image, ImageDraw, ImageFont

def update_preview(*args):
    msg = msg_entry.get()
    font_name = font_var.get()
    text_color = color_var.get()

    try:
        ascii_art = figlet_format(msg, font=font_name)
        colored_text = colored(ascii_art, text_color)
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, ascii_art) 
        output_text.configure(fg=text_color) 
    except Exception as e:
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, f"Error: {e}")

def update_theme(*args):
    theme = theme_var.get()
    bg_color, fg_color = ("#333", "#EEE") if theme == "dark" else ("#EEE", "#333")

    root.configure(bg=bg_color)
    msg_label.configure(background=bg_color, foreground=fg_color)
    font_label.configure(background=bg_color, foreground=fg_color)
    theme_label.configure(background=bg_color, foreground=fg_color)
    color_label.configure(background=bg_color, foreground=fg_color)

    output_text.configure(bg="black")  

def generate_ascii():
    msg = msg_entry.get()
    font_name = font_var.get()

    try:
        ascii_art = figlet_format(msg, font=font_name)
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, ascii_art)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def save_as_txt():
    ascii_art = output_text.get(1.0, tk.END)
    file_path = filedialog.asksaveasfilename(defaultextension=".txt")
    if file_path:
        with open(file_path, "w") as f:
            f.write(ascii_art)
        messagebox.showinfo("Saved", f"ASCII art saved as {file_path}")

def save_as_png():
    ascii_art = output_text.get(1.0, tk.END)
    file_path = filedialog.asksaveasfilename(defaultextension=".png")
    if file_path:
        lines = ascii_art.split("\n")
        font = ImageFont.load_default()
        line_height = 15
        img_width = max([len(line) for line in lines]) * 10
        img_height = len(lines) * line_height + 20
        
        bg_color = "black"
        text_color = color_var.get()

        img = Image.new("RGB", (img_width, img_height), bg_color)
        draw = ImageDraw.Draw(img)

        y_offset = 10
        for line in lines:
            draw.text((10, y_offset), line, fill=text_color, font=font)
            y_offset += line_height

        img.save(file_path)
        messagebox.showinfo("Saved", f"ASCII art saved as {file_path}")

root = tk.Tk()
root.title("ASCII Art Generator")
root.geometry("800x600")

style = ttk.Style()
style.configure('TLabel', padding=(10, 5), font=('Arial', 12))
style.configure('TCombobox', padding=(10, 5), font=('Arial', 12))
style.configure('TButton', padding=(10, 5), font=('Arial', 12))

msg_label = ttk.Label(root, text="Message:")
msg_label.grid(row=0, column=0, sticky="w", padx=10, pady=10)
msg_entry = ttk.Entry(root, width=40, font=('Arial', 12))
msg_entry.grid(row=0, column=1, columnspan=3, padx=10, pady=10)
msg_entry.bind("<KeyRelease>", update_preview)

font_label = ttk.Label(root, text="Font:")
font_label.grid(row=1, column=0, sticky="w", padx=10, pady=10)
font_list = ['slant', 'banner', 'block', 'bubble', 'digital', 'ivrit', 'mini', 'script', 'shadow', 'smscript', 'smshadow', 'smslant']
font_var = ttk.Combobox(root, values=font_list, style='TCombobox')
font_var.grid(row=1, column=1, padx=10, pady=10)
font_var.set("banner")
font_var.bind("<<ComboboxSelected>>", update_preview)

theme_label = ttk.Label(root, text="Theme:")
theme_label.grid(row=2, column=0, sticky="w", padx=10, pady=10)
theme_var = ttk.Combobox(root, values=["dark", "light"], style='TCombobox')
theme_var.grid(row=2, column=1, padx=10, pady=10)
theme_var.set("dark")
theme_var.bind("<<ComboboxSelected>>", update_theme)

color_label = ttk.Label(root, text="Text Color:")
color_label.grid(row=3, column=0, sticky="w", padx=10, pady=10)
color_list = ["green", "red", "yellow", "blue", "magenta", "cyan", "white"]
color_var = ttk.Combobox(root, values=color_list, style='TCombobox')
color_var.grid(row=3, column=1, padx=10, pady=10)
color_var.set("green")
color_var.bind("<<ComboboxSelected>>", update_preview)

generate_button = ttk.Button(root, text="Generate ASCII", command=generate_ascii, style='TButton')
generate_button.grid(row=4, column=0, columnspan=2, padx=10, pady=20)

save_txt_button = ttk.Button(root, text="Save as TXT", command=save_as_txt, style='TButton')
save_txt_button.grid(row=5, column=0, padx=10, pady=10)

save_png_button = ttk.Button(root, text="Save as PNG", command=save_as_png, style='TButton')
save_png_button.grid(row=5, column=1, padx=10, pady=10)

output_text = scrolledtext.ScrolledText(root, width=60, height=15, font=('Courier', 12))
output_text.grid(row=6, column=0, columnspan=4, padx=10, pady=10)

output_text.configure(bg="black", fg="green", insertbackground="green")

update_theme() 
root.mainloop()