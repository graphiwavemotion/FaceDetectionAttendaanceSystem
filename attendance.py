import cv2
import os
import pandas as pd
from datetime import datetime
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter import PhotoImage

# Setup
dataset_dir = "dataset"
attendance_file = "attendance.xlsx"
os.makedirs(dataset_dir, exist_ok=True)

# Load OpenCV face detector
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# Tkinter window setup
root = tk.Tk()
root.title("Face Attendance System")
root.geometry("500x600")
root.config(bg="#34495e")  # Set background color

# Add a custom icon (optional)
# root.iconbitmap("path_to_icon.ico")

# Styling
style = ttk.Style()
style.configure("TButton", font=("Helvetica", 12, 'bold'), padding=10, relief="flat", background="#1abc9c")
style.configure("TLabel", font=("Helvetica", 12), foreground="white", background="#34495e")
style.configure("TEntry", font=("Helvetica", 12), padding=10)

def register_face():
    name = name_entry.get().strip()
    if not name:
        messagebox.showerror("Error", "Name cannot be empty!")
        return

    person_dir = os.path.join(dataset_dir, name)
    os.makedirs(person_dir, exist_ok=True)

    cap = cv2.VideoCapture(0)
    count = 0

    while count < 5:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            count += 1
            face_img = frame[y:y+h, x:x+w]
            img_path = os.path.join(person_dir, f"{count}.jpg")
            cv2.imwrite(img_path, face_img)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        cv2.imshow("Registering Face", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    messagebox.showinfo("Success", f"Registered {count} face images for {name}")

def mark_attendance():
    name = name_entry.get().strip()
    if not name:
        messagebox.showerror("Error", "Name cannot be empty!")
        return

    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()

    if not ret:
        messagebox.showerror("Error", "Failed to capture image!")
        return

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    if len(faces) == 0:
        messagebox.showerror("Error", "No face detected! Try again.")
        return
    else:
        now = datetime.now()
        time_str = now.strftime("%H:%M:%S")
        date_str = now.strftime("%Y-%m-%d")

        if os.path.exists(attendance_file):
            df = pd.read_excel(attendance_file)
        else:
            df = pd.DataFrame(columns=["Name", "Date", "Time"])

        # Append the new record using pd.concat()
        new_row = pd.DataFrame({"Name": [name], "Date": [date_str], "Time": [time_str]})
        df = pd.concat([df, new_row], ignore_index=True)

        df.to_excel(attendance_file, index=False)

        messagebox.showinfo("Success", f"Attendance marked for {name} at {time_str} on {date_str}")

# GUI layout with custom styling and design
header_label = ttk.Label(root, text="Face Attendance System", font=("Helvetica", 16, 'bold'))
header_label.pack(pady=30)

# Background image (using your provided image path)
bg_image = PhotoImage(file=r"C:\Users\Aditya\Desktop\Kaushik Projects\FaceAttendanceSystem\Face Attendance System Interface.png")  # Your custom image
bg_label = tk.Label(root, image=bg_image)
bg_label.place(relwidth=1, relheight=1)

name_label = ttk.Label(root, text="Enter your name:")
name_label.pack(pady=10)

name_entry = ttk.Entry(root)
name_entry.pack(pady=10, ipadx=10)

# Register Button
register_button = ttk.Button(root, text="Register Face", command=register_face)
register_button.pack(pady=20)

# Mark Attendance Button
attendance_button = ttk.Button(root, text="Mark Attendance", command=mark_attendance)
attendance_button.pack(pady=20)

# Footer with custom styling (optional)
footer_label = ttk.Label(root, text="Powered by Face Attendance System", font=("Helvetica", 8))
footer_label.pack(side="bottom", pady=10)

root.mainloop()
