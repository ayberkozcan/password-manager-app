import os
from tkinter import messagebox
import sqlite3
import customtkinter as ctk
import json
import hashlib
import re

class PasswordManager(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.geometry("500x700")
        self.title("Password Manager")

        settings = self.load_settings()
        self.current_theme = settings.get("theme")
        self.language = settings.get("language")

        ctk.set_appearance_mode(self.current_theme)
        # self.load_language(self.language)

        self.connect_database()

        self.widgets()

    def create_label(self, frame, text, font, row, column, padx, pady, sticky="w"):
        label = ctk.CTkLabel(
            frame, 
            text=text, 
            font=font
        )
        label.grid(row=row, column=column, padx=padx, pady=pady, sticky=sticky)

    def create_button(self, frame, text, command, fg_color, hover_color, height, width, row, column, padx, pady, sticky="w"):
        button = ctk.CTkButton(
            frame,
            text=text,
            command=command,
            fg_color=fg_color,
            hover_color=hover_color,
            height=height,
            width=width
        )
        button.grid(row=row, column=column, padx=padx, pady=pady, sticky=sticky)

    def create_entry(self, frame, placeholder_text, width, show, row, column, padx, pady, sticky="w"):
        entry = ctk.CTkEntry(
            frame,
            placeholder_text=placeholder_text,
            corner_radius=5,
            width=width,
            show=show
        )
        entry.grid(row=row, column=column, padx=padx, pady=pady, sticky=sticky)
        return entry

    def connect_database(self):
        self.conn = sqlite3.connect("data/database/password_management.db")
        self.cursor = self.conn.cursor()

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                email TEXT NOT NULL,
                password TEXT NOT NULL
            )
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS passwords (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                website TEXT NOT NULL,
                website_url TEXT,
                username TEXT,
                email TEXT,
                password TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)

        self.conn.commit()

    def load_settings(self):
        try:
            with open("data/settings.json", "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return {"theme": "dark", "language": "en"}
        
    def widgets(self):
        self.welcome_page()

    def welcome_page(self):
        for widget in self.winfo_children():
            widget.grid_forget()

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.create_label(self, "Securely store and manage\nyour passwords", ("Helvetica", 20), 0, 0, 20, 20, "nsew")

        center_frame = ctk.CTkFrame(self)
        center_frame.grid(row=1, column=0, padx=20, pady=20)

        self.create_button(center_frame, "Login", self.login_page, "green", "#006400", 32, 140, 0, 0, 20, 20)
        self.create_button(center_frame, "Sign up", self.signup_page, "red", "#8B0000", 32, 140, 1, 0, 20, 20)
        self.create_button(center_frame, "Quit", self.quit, "#DAA520", "#B8860B", 32, 140, 2, 0, 20, 20)

    def login_page(self):
        for widget in self.winfo_children():
            widget.grid_forget()

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.create_label(self, "Login", ("Helvetica", 20), 0, 0, 20, 20, sticky="nsew")
        
        center_frame = ctk.CTkFrame(self)
        center_frame.grid(row=1, column=0, padx=20, pady=20)

        self.create_label(center_frame, "Username", ("Helvetica", 15), 0, 0, 20, 5)
        username_entry = self.create_entry(center_frame, "...", 200, "", 1, 0, 20, 0)

        self.create_label(center_frame, "Password", ("Helvetica", 15), 2, 0, 20, 5)
        password_entry = self.create_entry(center_frame, "...", 200, "*", 3, 0, 20, 0)

        self.create_button(center_frame, "Submit", lambda: self.login(username_entry.get(), password_entry.get()), "#DAA520", "#B8860B", 32, 200, 4, 0, 20, (20, 10))
        self.create_button(center_frame, "Go Back", self.welcome_page, "#DAA520", "#B8860B", 32, 200, 5, 0, 20, 0)

    def signup_page(self):
        for widget in self.winfo_children():
            widget.grid_forget()

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.create_label(self, "Sign Up", ("Helvetica", 20), 0, 0, 20, 20, sticky="nsew")
        
        center_frame = ctk.CTkFrame(self)
        center_frame.grid(row=1, column=0, padx=20, pady=20)

        self.create_label(center_frame, "Username", ("Helvetica", 15), 0, 0, 20, 5)
        username_entry = self.create_entry(center_frame, "...", 200, "", 1, 0, 20, 0)

        self.create_label(center_frame, "Email", ("Helvetica", 15), 2, 0, 20, 5)
        email_entry = self.create_entry(center_frame, "...", 200, "", 3, 0, 20, 0)

        self.create_label(center_frame, "Password", ("Helvetica", 15), 4, 0, 20, 5)
        password_entry = self.create_entry(center_frame, "...", 200, "*", 5, 0, 20, 0)
        
        self.create_button(center_frame, "Submit", lambda: self.signup(username_entry.get(), email_entry.get(), password_entry.get()), "#DAA520", "#B8860B", 32, 200, 6, 0, 20, (20, 10))
        self.create_button(center_frame, "Go Back", self.welcome_page, "#DAA520", "#B8860B", 32, 200, 7, 0, 20, 0)

    def homepage(self):
        for widget in self.winfo_children():
            widget.grid_forget()

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.create_label(self, "Welcome!", ("Helvetica", 20), 0, 0, 20, 20, "nsew")

        center_frame = ctk.CTkFrame(self)
        center_frame.grid(row=1, column=0, padx=20, pady=20)

        self.create_button(center_frame, "Add Password", self.add_password_page, "green", "#006400", 32, 140, 0, 0, 20, 20)
        self.create_button(center_frame, "My Passwords", self.my_passwords_page, "blue", "darkblue", 32, 140, 1, 0, 20, 20)
        self.create_button(center_frame, "Settings", self.settings_page, "#DAA520", "#B8860B", 32, 140, 2, 0, 20, 20)
        self.create_button(center_frame, "Logout", self.welcome_page, "red", "#8B0000", 32, 140, 3, 0, 20, 20)

    def add_password_page(self):
        for widget in self.winfo_children():
            widget.grid_forget()

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.create_label(self, "Add Password", ("Helvetica", 20), 0, 0, 20, 20, sticky="nsew")
        
        center_frame = ctk.CTkFrame(self)
        center_frame.grid(row=1, column=0, padx=20, pady=20)

        self.create_label(center_frame, "Website", ("Helvetica", 15), 0, 0, 20, 5)
        website_entry = self.create_entry(center_frame, "...", 200, "", 1, 0, 20, 0)

        self.create_label(center_frame, "Website URL (optional)", ("Helvetica", 15), 2, 0, 20, 5)
        website_url = self.create_entry(center_frame, "...", 200, "", 3, 0, 20, 0)

        self.create_label(center_frame, "Username (optional)", ("Helvetica", 15), 4, 0, 20, 5)
        username_entry = self.create_entry(center_frame, "...", 200, "", 5, 0, 20, 0)

        self.create_label(center_frame, "Email (optional)", ("Helvetica", 15), 6, 0, 20, 5)
        email_entry = self.create_entry(center_frame, "...", 200, "", 7, 0, 20, 0)

        self.create_label(center_frame, "Password", ("Helvetica", 15), 8, 0, 20, 5)
        password_entry = self.create_entry(center_frame, "...", 200, "*", 9, 0, 20, 0)
        
        self.create_button(center_frame, "Submit", lambda: self.add_password(self.user_id, website_entry.get(), website_url.get(), username_entry.get(), email_entry.get(), password_entry.get()), "#DAA520", "#B8860B", 32, 200, 10, 0, 20, (20, 10))
        self.create_button(center_frame, "Go Back", self.homepage, "#DAA520", "#B8860B", 32, 200, 11, 0, 20, 0)
    
    def my_passwords_page(self):
        for widget in self.winfo_children():
            widget.grid_forget()

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.create_label(self, "My Passwords", ("Helvetica", 20), 0, 0, 20, 20, "w")
        
        self.create_button(self, "Go Back", self.homepage, "#DAA520", "#B8860B", 32, 60, 0, 0, 20, 20, "e")

        center_frame = ctk.CTkFrame(self)
        center_frame.grid(row=1, column=0, padx=20, pady=20)

        columns = ["Website", "Website URL", "Username", "Email", "Password"]

        for i, column in enumerate(columns):
            self.create_label(center_frame, column, ("Helvetica", 15), 0, i, 5, 10)

        passwords = self.cursor.execute("""SELECT * FROM passwords WHERE user_id = :user_id""", {"user_id": self.user_id}).fetchall()
        
        if not passwords:
            self.create_label(center_frame, "No Passwords...", ("Helvetica", 20), 0, 0, 5, 10)

    def settings_page(self):
        return

    def signup(self, username, email, password):
        def value_exists(column, value):
            return self.cursor.execute(f"""
                SELECT {column}
                FROM users
                WHERE {column} = :value
            """, {
                "value": value
            }).fetchone()

        if value_exists("username", username):
            messagebox.showerror(
                "Error",
                "This username already exists!"
            )
            return

        if len(username) < 5 or len(username) > 20:
            messagebox.showerror(
                "Error",
                "Username must be 5-20 characters long!"
            )
            return

        if value_exists("email", email):
            messagebox.showerror(
                "Error",
                "This email already exists!"
            )
            return

        email_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"

        if not re.match(email_regex, email):
            messagebox.showerror(
                "Error",
                "Invalid email format!"
            )
            return

        if len(password) < 5 or len(password) > 20:
            messagebox.showerror(
                "Error",
                "Password must be 5-20 characters long!"
            )
            return

        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        self.cursor.execute("""
            INSERT INTO users (username, email, password)
            VALUES (:username, :email, :password)
        """, {
            "username": username,
            "email": email,
            "password": hashed_password
        })
        self.conn.commit()

        messagebox.showinfo(
            "Success",
            "Successfully signed up!"
        )
        self.login_page()

    def login(self, username, password):
        def value_check(column, value):
            return self.cursor.execute(f"""
                SELECT {column}
                FROM users
                WHERE {column} = :value
            """, {
                "value": value
            }).fetchone()

        if not value_check("username", username):
            messagebox.showerror(
                "Error",
                "This username does not exist!"
            )
            return

        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        stored_password = self.cursor.execute("""
            SELECT password
            FROM users
            WHERE username = :username
        """, {
            "username": username
        }).fetchone()

        if stored_password and hashed_password == stored_password[0]:
            messagebox.showinfo(
                "Success",
                "Successfully logged in!"
            )

            self.user_id = self.cursor.execute("""
                SELECT id
                FROM users
                WHERE username = :username
            """, {
                "username": username
            }).fetchone()

            self.user_id = self.user_id[0]

            self.homepage()
        else:
            messagebox.showerror(
                "Error",
                "Incorrect Password!"
            )
            return

    def add_password(self, user_id, website, website_url, username, email, password):
        if not website:
            messagebox.showerror(
                "Error",
                "Website can not be empty!"
            )
            return
        if not password:
            messagebox.showerror(
                "Error",
                "Password can not be empty!"
            )
            return
        
        self.cursor.execute("""
            INSERT INTO passwords (user_id, website, website_url, username, email, password)
            VALUES (:user_id, :website, :website_url, :username, :email, :password)
        """, {
            "user_id": user_id,
            "website": website,
            "website_url": website_url,
            "username": username,
            "email": email,
            "password": password
        })
        self.conn.commit()

        messagebox.showinfo(
            "Success",
            "Successful!"
        )

        self.add_password_page()

    def quit(self):
        self.destroy()

if __name__ == "__main__":
    app = PasswordManager()
    app.mainloop()