"""
Modern Tkinter UI with Enhanced Styling
Author: Tushar Sharma
"""

import tkinter as tk
from tkinter import messagebox as mess
import tkinter.simpledialog as tsd
import cv2, os
import csv
import numpy as np
from threading import Thread
from tkinter import *
from tkinter.ttk import *
import pandas as pd
import datetime
import time
from PIL import Image, ImageTk

from Generate_Dataset import Generate_Data
from Model_train import Model_Training
from Recognizer import Recognition

# Custom styling
COLORS = {
    'primary': '#8a2e7f',
    'secondary': '#507d2a',
    'accent': '#00aeff',
    'dark': '#262523',
    'light': '#ffffff',
    'success': '#28a745',
    'danger': '#dc3545'
}

class ModernAttendanceUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Smart Attendance System | Tushar Sharma")
        self.master.configure(bg=COLORS['light'])
        
        # Make fullscreen
        pad = 3
        master.geometry("{0}x{1}+0+0".format(
            master.winfo_screenwidth()-pad, master.winfo_screenheight()-pad))
        master.bind('<Escape>', self.toggle_fullscreen)
        
        self.selection = 1
        self.setup_ui()
    
    def toggle_fullscreen(self, event):
        pass
    
    def setup_ui(self):
        # Header
        self.create_header()
        
        # Main content frame
        main_frame = tk.Frame(self.master, bg=COLORS['light'])
        main_frame.place(relx=0.5, rely=0.55, relwidth=0.95, relheight=0.75, anchor=CENTER)
        
        # Left panel - Attendance
        self.create_attendance_panel(main_frame)
        
        # Right panel - Enrollment
        self.create_enrollment_panel(main_frame)
    
    def create_header(self):
        header_frame = tk.Frame(self.master, bg=COLORS['primary'], height=120)
        header_frame.place(relx=0, rely=0, relwidth=1, relheight=0.15)
        
        title = tk.Label(header_frame, text="🎓 Smart Attendance System",
                        fg=COLORS['light'], bg=COLORS['primary'],
                        font=('Helvetica', 36, 'bold'))
        title.place(relx=0.5, rely=0.35, anchor=CENTER)
        
        subtitle = tk.Label(header_frame, text="Powered by Machine Learning & Face Recognition",
                           fg=COLORS['light'], bg=COLORS['primary'],
                           font=('Helvetica', 14))
        subtitle.place(relx=0.5, rely=0.65, anchor=CENTER)
        
        # Date display
        ts = time.time()
        date = datetime.datetime.fromtimestamp(ts).strftime('%d %B %Y')
        date_label = tk.Label(header_frame, text=date,
                             fg=COLORS['light'], bg=COLORS['dark'],
                             font=('Helvetica', 16, 'bold'), padx=20, pady=5)
        date_label.place(relx=0.5, rely=0.95, anchor=CENTER)

    
    def create_attendance_panel(self, parent):
        frame = tk.Frame(parent, bg=COLORS['light'], relief=RAISED, borderwidth=2)
        frame.place(relx=0.02, rely=0, relwidth=0.47, relheight=1)
        
        header = tk.Label(frame, text="📋 Attendance Management",
                         fg=COLORS['light'], bg=COLORS['primary'],
                         font=('Helvetica', 18, 'bold'), pady=15)
        header.pack(fill=X)
        
        # Subject selection
        subject_frame = tk.Frame(frame, bg=COLORS['light'], pady=20)
        subject_frame.pack(fill=X)
        
        tk.Label(subject_frame, text="Select Subject:",
                bg=COLORS['light'], font=('Helvetica', 13, 'bold')).pack()
        
        self.v = tk.IntVar(value=1)
        radio_frame = tk.Frame(subject_frame, bg=COLORS['light'])
        radio_frame.pack(pady=10)
        
        tk.Radiobutton(radio_frame, text="📚 Hindi", variable=self.v, value=1,
                      bg=COLORS['light'], font=('Helvetica', 12, 'bold'),
                      activebackground=COLORS['light']).pack(side=LEFT, padx=20)
        tk.Radiobutton(radio_frame, text="📖 English", variable=self.v, value=2,
                      bg=COLORS['light'], font=('Helvetica', 12, 'bold'),
                      activebackground=COLORS['light']).pack(side=LEFT, padx=20)
        
        # Buttons
        btn_frame = tk.Frame(frame, bg=COLORS['light'], pady=10)
        btn_frame.pack(fill=X, padx=20)
        
        tk.Button(btn_frame, text="📸 Take Attendance", command=self.take_attendance,
                 fg=COLORS['light'], bg=COLORS['secondary'],
                 font=('Helvetica', 13, 'bold'), pady=10).pack(fill=X, pady=5)
        
        tk.Button(btn_frame, text="👁️ Show Attendance", command=self.show_attendance,
                 fg=COLORS['light'], bg=COLORS['accent'],
                 font=('Helvetica', 13, 'bold'), pady=10).pack(fill=X, pady=5)
        
        tk.Button(btn_frame, text="🗑️ Clear Display", command=self.clear_tree,
                 fg=COLORS['light'], bg=COLORS['danger'],
                 font=('Helvetica', 13, 'bold'), pady=10).pack(fill=X, pady=5)
        
        # Table
        self.create_attendance_table(frame)
        
        # Quit button
        tk.Button(frame, text="❌ Quit", command=self.master.destroy,
                 fg=COLORS['light'], bg=COLORS['danger'],
                 font=('Helvetica', 14, 'bold'), pady=12).pack(side=BOTTOM, fill=X, padx=20, pady=20)
    
    def create_enrollment_panel(self, parent):
        frame = tk.Frame(parent, bg=COLORS['light'], relief=RAISED, borderwidth=2)
        frame.place(relx=0.51, rely=0, relwidth=0.47, relheight=1)
        
        header = tk.Label(frame, text="➕ New Student Enrollment",
                         fg=COLORS['light'], bg=COLORS['primary'],
                         font=('Helvetica', 18, 'bold'), pady=15)
        header.pack(fill=X)
        
        # Input fields
        input_frame = tk.Frame(frame, bg=COLORS['light'], pady=20)
        input_frame.pack(fill=X, padx=20)
        
        tk.Label(input_frame, text="Roll Number:",
                bg=COLORS['light'], font=('Helvetica', 12, 'bold')).pack(anchor=W)
        self.roll_entry = tk.Entry(input_frame, font=('Helvetica', 12), bd=2, relief=SOLID)
        self.roll_entry.pack(fill=X, pady=5)
        
        tk.Label(input_frame, text="Student Name:",
                bg=COLORS['light'], font=('Helvetica', 12, 'bold')).pack(anchor=W, pady=(10, 0))
        self.name_entry = tk.Entry(input_frame, font=('Helvetica', 12), bd=2, relief=SOLID)
        self.name_entry.pack(fill=X, pady=5)
        
        # Buttons
        tk.Button(input_frame, text="📷 Take Images", command=self.capture_images,
                 fg=COLORS['light'], bg=COLORS['primary'],
                 font=('Helvetica', 13, 'bold'), pady=10).pack(fill=X, pady=(20, 5))
        
        # Training section
        train_frame = tk.Frame(frame, bg=COLORS['light'], pady=20)
        train_frame.pack(fill=X, padx=20)
        
        tk.Button(train_frame, text="🧠 Train The Model", command=self.train_with_progress,
                 fg=COLORS['light'], bg=COLORS['success'],
                 font=('Helvetica', 14, 'bold'), pady=12).pack(fill=X)
        
        self.progress = Progressbar(train_frame, length=200, mode='determinate')
        self.progress.pack(fill=X, pady=10)
    
    def create_attendance_table(self, parent):
        table_frame = tk.Frame(parent, bg=COLORS['light'])
        table_frame.pack(fill=BOTH, expand=True, padx=20, pady=10)
        
        self.tv = Treeview(table_frame, columns=('roll_no', 'name', 'attendance'),
                          selectmode='browse', show=["headings"], height=15)
        self.tv.column('roll_no', width=100, anchor=tk.CENTER)
        self.tv.column('name', width=150, anchor=tk.CENTER)
        self.tv.column('attendance', width=100, anchor=tk.CENTER)
        
        self.tv.heading('roll_no', text='Roll Number')
        self.tv.heading('name', text='Name')
        self.tv.heading('attendance', text='Attendance')
        
        self.tv.pack(side=LEFT, fill=BOTH, expand=True)
        
        scroll = Scrollbar(table_frame, orient='vertical', command=self.tv.yview)
        scroll.pack(side=RIGHT, fill=Y)
        self.tv.configure(yscrollcommand=scroll.set)
    
    def capture_images(self):
        name = self.name_entry.get()
        roll = self.roll_entry.get()
        
        if not name or not roll:
            mess.showerror("Error", "Please enter both name and roll number")
            return
        
        Generate_Data(name, roll)
        mess.showinfo("Success", f"Images captured for {name}")
        self.name_entry.delete(0, END)
        self.roll_entry.delete(0, END)
    
    def train_with_progress(self):
        Thread(target=Model_Training).start()
        Thread(target=self.progress_measure).start()
    
    def progress_measure(self):
        import time
        steps = [20, 40, 50, 60, 100]
        delays = [2, 6, 6, 6, 5]
        
        for step, delay in zip(steps, delays):
            time.sleep(delay)
            self.progress['value'] = step
            self.master.update_idletasks()
    
    def take_attendance(self):
        self.selection = self.v.get()
        Recognition(str(self.selection))
    
    def show_attendance(self):
        self.selection = self.v.get()
        subject = "Hindi_attendance/Hindi_Attendance.csv" if self.selection == 1 else "English_attendance/English_Attendance.csv"
        
        try:
            with open(subject, newline="") as f:
                reader = csv.DictReader(f, delimiter=',')
                for row in reader:
                    self.tv.insert("", 0, values=(row['Roll Number'], row['Name'], row['Attendance']))
        except Exception as e:
            mess.showerror("Error", f"Failed to load attendance: {str(e)}")
    
    def clear_tree(self):
        for child in self.tv.get_children():
            self.tv.delete(child)

if __name__ == '__main__':
    window = tk.Tk()
    app = ModernAttendanceUI(window)
    window.mainloop()
