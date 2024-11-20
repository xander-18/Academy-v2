import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import cv2
import numpy as np
import os


class FacialLoginSystem:
    def __init__(self):
        self.users_file = "users.json"
        self.load_users()

        # Main Login Window
        self.root = tk.Tk()
        self.root.title("Facial Recognition System")
        self.root.geometry("300x300")

        # Username Entry
        tk.Label(self.root, text="Username").pack(pady=10)
        self.username_entry = tk.Entry(self.root, width=20)
        self.username_entry.pack()

        # Login Buttons
        tk.Button(
            self.root, text="Iniciar sesion con contrasena", command=self.password_login
        ).pack(pady=5)
        tk.Button(
            self.root, text="Iniciar sesión con rostro", command=self.facial_login
        ).pack(pady=5)

        # New Registration Button
        tk.Button(
            self.root, text="Registrar nuevo usuario", command=self.register_user
        ).pack(pady=5)

        self.root.mainloop()

    def load_users(self):
        if os.path.exists(self.users_file):
            with open(self.users_file, "r") as f:
                self.users = json.load(f)
        else:
            self.users = {}

    def save_users(self):
        with open(self.users_file, "w") as f:
            json.dump(self.users, f)

    def register_user(self):
        username = self.username_entry.get()
        if not username:
            messagebox.showerror("Error", "Por favor, ingresa tu username")
            return

        if username in self.users:
            messagebox.showerror("Error", "El nombre de usuario ya existe")
            return

        # Open camera for face capture
        cap = cv2.VideoCapture(0)
        cv2.namedWindow("Face Registration")

        while True:
            ret, frame = cap.read()
            cv2.imshow("Face Registration", frame)

            key = cv2.waitKey(1)
            if key % 256 == 32:  # Space key
                # Capture face
                _, buffer = cv2.imencode(".jpg", frame)
                face_data = buffer.tobytes().hex()  # Convert to hex string for JSON

                # Prompt for password
                password = simpledialog.askstring(
                    "Password", "Enter password:", show="*"
                )

                if password:
                    # Store user data
                    self.users[username] = {
                        "password": password,
                        "face_data": face_data,
                    }
                    self.save_users()
                    messagebox.showinfo(
                        "Success", f"El usuario {username} se registro existosamente!"
                    )
                    break

            elif key % 256 == 27:  # ESC key
                break

        cap.release()
        cv2.destroyAllWindows()

    def password_login(self):
        username = self.username_entry.get()
        user = self.users.get(username)

        if user:
            password_window = tk.Toplevel(self.root)
            password_window.title("Password Login")
            password_window.geometry("250x150")

            tk.Label(password_window, text="Enter Password").pack(pady=10)
            password_entry = tk.Entry(password_window, show="*")
            password_entry.pack(pady=10)

            def verify_password():
                if password_entry.get() == user["password"]:
                    messagebox.showinfo(
                        "Iniciar sesión exitosamente", f"Welcome, {username}!"
                    )
                    password_window.destroy()
                    self.root.destroy()
                    Dashboard(username)  # Launch Dashboard
                else:
                    messagebox.showerror(
                        "Error de inicio de sesion", "Incorrect Password"
                    )

            tk.Button(password_window, text="Login", command=verify_password).pack(
                pady=10
            )
        else:
            messagebox.showerror("Error al iniciar sesión", "Usuario no encontrado")

    def facial_login(self):
        username = self.username_entry.get()
        user = self.users.get(username)

        if not user:
            messagebox.showerror("Error", "Usuario no encontrado")
            return

        # Open camera for facial recognition
        cap = cv2.VideoCapture(0)
        cv2.namedWindow("Facial Login")

        while True:
            ret, frame = cap.read()
            cv2.imshow("Facial Login", frame)

            key = cv2.waitKey(1)
            if key % 256 == 32:  # Space key
                # Capture current face
                _, buffer = cv2.imencode(".jpg", frame)
                current_face = buffer.tobytes().hex()

                # Compare faces
                if self.compare_faces(current_face, user["face_data"]):
                    messagebox.showinfo("Login Success", f"Bienvenido, {username}!")
                    cap.release()
                    cv2.destroyAllWindows()
                    self.root.destroy()
                    Dashboard(username)  # Launch Dashboard
                    return
                else:
                    messagebox.showerror(
                        "Error al iniciar sesión", "La cara no coincide"
                    )

                break

            elif key % 256 == 27:  # ESC key
                break

        cap.release()
        cv2.destroyAllWindows()

    def compare_faces(self, face1, face2, threshold=0.8):
        # Simple comparison of face data length
        return len(face1) > 0 and len(face2) > 0


class Dashboard:
    # (Previous Dashboard implementation remains the same)
    def __init__(self, username):
        self.dashboard = tk.Tk()
        self.dashboard.title(f"Welcome, {username}")
        self.dashboard.geometry("400x300")

        # Welcome Label
        welcome_label = tk.Label(
            self.dashboard, text=f"Bienvenido, {username}!", font=("Arial", 16)
        )
        welcome_label.pack(pady=20)

        # Dashboard Buttons
        buttons = [
            ("Perfil", self.show_profile),
            ("Configuraciones", self.show_settings),
            ("Cerrar Sesión", self.logout),
        ]

        for text, command in buttons:
            btn = tk.Button(self.dashboard, text=text, width=20, command=command)
            btn.pack(pady=10)

        self.dashboard.mainloop()

    def show_profile(self):
        messagebox.showinfo("Perfil", "Funcionalidad de perfil en desarrollo")

    def show_settings(self):
        messagebox.showinfo(
            "Configuraciones", "Funcionalidad de configuraciones en desarrollo"
        )

    def logout(self):
        self.dashboard.destroy()


if __name__ == "__main__":
    FacialLoginSystem()
