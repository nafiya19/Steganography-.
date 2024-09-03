import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import wave
import tkinter.simpledialog as simpledialog

from steganography import (
    encode_txt_data, decode_txt_data, 
    encode_img_data, decode_img_data, 
    encode_aud_data, decode_aud_data
)

# Create the main window
root = tk.Tk()
root.title("Steganography Tool")

# Initialize global variables
img = None
audio = None
file_path = None


def load_text_in_chunks(file_path, chunk_size=1024 * 1024):  # 1 MB chunks
    with open(file_path, 'r') as file:
        while True:
            chunk = file.read(chunk_size)
            if not chunk:
                break
            text_widget.insert('end', chunk)
            text_widget.yview('end')  # Scroll to the end


def load_file_for_encoding():
    global file_path, img, audio
    file_type = option_var.get()
    
    if file_type == "Image":
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp *.gif"), ("All files", "*.*")]
        )
        if file_path:
            img = Image.open(file_path)
            img_rgb = img.convert("RGB")
            img_display = ImageTk.PhotoImage(img_rgb)
            canvas.create_image(0, 0, anchor=tk.NW, image=img_display)
            canvas.image = img_display
            lbl_status.config(text="Image file loaded for encoding message")
        else:
            messagebox.showerror("Error", "No file selected. Please try again.")
            
    elif file_type == "Audio":
        file_path = filedialog.askopenfilename(
            filetypes=[("Audio files", "*.wav"), ("All files", "*.*")]
        )
        if file_path:
            audio = wave.open(file_path, 'rb')
            audio_icon = Image.open("C:\\sasta copies\\7 excellent\\Sample_cover_files\\icons\\music-icon.png")
            audio_icon_display = ImageTk.PhotoImage(audio_icon)
            canvas.create_image(0, 0, anchor=tk.NW, image=audio_icon_display)
            canvas.image = audio_icon_display
            lbl_status.config(text="Audio file loaded for encoding message")
        else:
            messagebox.showerror("Error", "No file selected. Please try again.")
    
    elif file_type == "Document":
        file_path = filedialog.askopenfilename(
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if file_path:
            document_icon = Image.open("C:\\sasta copies\\7 excellent\\Sample_cover_files\\icons\\document-icon.png")
            document_icon_display = ImageTk.PhotoImage(document_icon)
            canvas.create_image(0, 0, anchor=tk.NW, image=document_icon_display)
            canvas.image = document_icon_display
            lbl_status.config(text="Document file loaded for encoding message")
        else:
            messagebox.showerror("Error", "No file selected. Please try again.")
    
    if file_path:
        btn_encode.config(state=tk.NORMAL)
        btn_decode.config(state=tk.DISABLED)
        messagebox.showinfo("Success", f"{file_type} file loaded successfully")

def load_file_for_decoding():
    global file_path, img, audio
    file_type = option_var.get()
    
    if file_type == "Image":
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp *.gif"), ("All files", "*.*")]
        )
        if file_path:
            img = Image.open(file_path)
            img_rgb = img.convert("RGB")
            img_display = ImageTk.PhotoImage(img_rgb)
            canvas.create_image(0, 0, anchor=tk.NW, image=img_display)
            canvas.image = img_display
            lbl_status.config(text="Image file loaded for decoding message")
        else:
            messagebox.showerror("Error", "No file selected. Please try again.")
    
    elif file_type == "Audio":
        file_path = filedialog.askopenfilename(
            filetypes=[("Audio files", "*.wav"), ("All files", "*.*")]
        )
        if file_path:
            audio = wave.open(file_path, 'rb')
            lbl_status.config(text="Audio file loaded for decoding message")
        else:
            messagebox.showerror("Error", "No file selected. Please try again.")
    
    elif file_type == "Document":
        file_path = filedialog.askopenfilename(
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if file_path:
            document_icon = Image.open("C:\\sasta copies\\7 excellent\\Sample_cover_files\\icons\\document-icon.png")
            document_icon_display = ImageTk.PhotoImage(document_icon)
            canvas.create_image(0, 0, anchor=tk.NW, image=document_icon_display)
            canvas.image = document_icon_display
            lbl_status.config(text="Document file loaded for decoding message")
        else:
            messagebox.showerror("Error", "No file selected. Please try again.")
    
    if file_path:
        btn_encode.config(state=tk.DISABLED)
        btn_decode.config(state=tk.NORMAL)
        lbl_status.config(text=f"{file_type} file loaded successfully for decoding")
        

def encode_message():
    global file_path, img, audio
    message = text_widget.get("1.0", tk.END).strip()
    if not message:
        messagebox.showerror("Error", "Please enter a message to encode")
        return

    key = simpledialog.askstring("Input", "Enter the key:", parent=root)
    if not key:
        messagebox.showerror("Error", "Please enter a key")
        return

    file_type = option_var.get()
    output_path = None
    
    if file_type == "Image":
        output_path = filedialog.asksaveasfilename(
            defaultextension=".png", 
            filetypes=[("PNG files", "*.png"), ("All files", "*.*")]
        )
    elif file_type == "Audio":
        output_path = filedialog.asksaveasfilename(
            defaultextension=".wav", 
            filetypes=[("WAV files", "*.wav"), ("All files", "*.*")]
        )
    elif file_type == "Document":
        output_path = filedialog.asksaveasfilename(
            defaultextension=".txt", 
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )

    if not output_path:
        messagebox.showerror("Error", "No output path selected.")
        return
    
    try:
        if file_type == "Image":
            print(f"Encoding message in image file: {file_path}")
            encode_img_data(file_path, message, key, output_path)
            print(f"Encoded message saved to: {output_path}")
        elif file_type == "Audio":
            print(f"Encoding message in audio file: {file_path}")
            encode_aud_data(file_path, message, key, output_path)
            print(f"Encoded message saved to: {output_path}")
        elif file_type == "Document":
            print(f"Encoding message in document file: {file_path}")
            encode_txt_data(file_path, message, key, output_path)
            print(f"Encoded message saved to: {output_path}")
                
        messagebox.showinfo("Success", f"Message encoded in {file_type} file successfully")
        text_widget.delete("1.0", tk.END)  # Clear the text area after encoding
    except Exception as e:
        messagebox.showerror("Error", f"Failed to encode message: {str(e)}")

def decode_message():
    global file_path, img, audio
    key = simpledialog.askstring("Input", "Enter the key:", parent=root)
    if not key:
        messagebox.showerror("Error", "Please enter a key")
        return

    file_type = option_var.get()
    try:
        if file_type == "Image":
            print(f"Decoding message from image file: {file_path}")
            decoded_message = decode_img_data(file_path, key)
            
        elif file_type == "Audio":
            print(f"Decoding message from audio file: {file_path}")
            decoded_message = decode_aud_data(file_path, key)
            
        elif file_type == "Document":
            print(f"Decoding message from document file: {file_path}")
            decoded_message = decode_txt_data(file_path, key)
        #text_widget.delete("1.0", tk.END)
        #text_widget.insert(tk.END, decoded_message)

        if decoded_message:
            messagebox.showinfo("Decoded Message", f"Decoded message: {decoded_message}")
        else:
            messagebox.showinfo("Decoded Message", "No hidden message found or incorrect key.")
        #text_widget.insert(tk.END, decoded_message)    
        text_widget.delete("1.0", tk.END)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to decode message: {str(e)}")

# GUI components
frame = tk.Frame(root)
frame.pack(pady=10)

label = tk.Label(frame, text="Select file type:")
label.grid(row=0, column=0, padx=5)

option_var = tk.StringVar()
option_var.set("Image")
options = ["Image", "Audio", "Document"]
option_menu = tk.OptionMenu(frame, option_var, *options)
option_menu.grid(row=0, column=1, padx=5)

btn_load_encode = tk.Button(frame, text="Load File for Encoding", command=load_file_for_encoding)
btn_load_encode.grid(row=1, column=0, padx=5, pady=5)

btn_load_decode = tk.Button(frame, text="Load File for Decoding", command=load_file_for_decoding)
btn_load_decode.grid(row=1, column=1, padx=5, pady=5)

lbl_status = tk.Label(root, text="")
lbl_status.pack(pady=5)

canvas = tk.Canvas(root, width=400, height=300, bg="mint cream")
canvas.pack()

lbl_message = tk.Label(root, text="Enter message to encode:")
lbl_message.pack(pady=5)

# # Create a Text widget with scrollbars
# text_frame = tk.Frame(root)
# text_frame.pack()

# scroll_y = tk.Scrollbar(text_frame, orient=tk.VERTICAL)
# scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

# text_message = tk.Text(text_frame, wrap=tk.WORD, yscrollcommand=scroll_y.set, width=50, height=10)
# text_message.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
# scroll_y.config(command=text_message.yview)
# entry_message = tk.Entry(root, width=50)
# entry_message.pack(pady=5)

btn_encode = tk.Button(root, text="Encode Message", state=tk.DISABLED, command=encode_message)
btn_encode.pack(pady=5)

btn_decode = tk.Button(root, text="Decode Message", state=tk.DISABLED, command=decode_message)
btn_decode.pack(pady=5)

text_widget = tk.Text(root, wrap='none')
text_widget.pack(expand=1, fill='both')

# Start the main loop
root.mainloop()
