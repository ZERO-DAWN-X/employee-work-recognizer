import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import cv2

class WebcamApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Employee Work Time Recognizer")
        self.root.geometry("800x600")
        self.root.configure(bg="#f7f7f7")
        self.cap = None
        self.is_running = False

        # Header
        self.header = tk.Label(root, text="Employee Work Time Recognizer", font=("Segoe UI", 22, "bold"), bg="#f7f7f7", fg="#222")
        self.header.pack(pady=(20, 10))

        # Webcam display
        self.video_frame = tk.Label(root, bg="#e0e0e0", width=640, height=360, relief="ridge", bd=2)
        self.video_frame.pack(pady=10)

        # Start/Stop button
        self.button_style = ttk.Style()
        self.button_style.configure("TButton", font=("Segoe UI", 12), padding=8)
        self.toggle_btn = ttk.Button(root, text="Start Webcam", command=self.toggle_webcam)
        self.toggle_btn.pack(pady=10)

        # Placeholder for future features
        self.placeholder = tk.Label(root, text="[Future: Activity logs, reports, etc.]", font=("Segoe UI", 12, "italic"), bg="#f7f7f7", fg="#888")
        self.placeholder.pack(pady=(30, 0))

    def toggle_webcam(self):
        if not self.is_running:
            self.cap = cv2.VideoCapture(0)
            if not self.cap.isOpened():
                self.video_frame.config(text="Error: Could not open webcam.")
                return
            self.is_running = True
            self.toggle_btn.config(text="Stop Webcam")
            self.update_frame()
        else:
            self.is_running = False
            self.toggle_btn.config(text="Start Webcam")
            if self.cap:
                self.cap.release()
            self.video_frame.config(image="", text="")

    def update_frame(self):
        if self.is_running and self.cap:
            ret, frame = self.cap.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame)
                img = img.resize((640, 360))
                imgtk = ImageTk.PhotoImage(image=img)
                self.video_frame.imgtk = imgtk
                self.video_frame.config(image=imgtk)
            self.root.after(15, self.update_frame)
        else:
            if self.cap:
                self.cap.release()
            self.video_frame.config(image="", text="")


def run_gui():
    root = tk.Tk()
    app = WebcamApp(root)
    root.mainloop() 