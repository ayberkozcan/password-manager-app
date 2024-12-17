from functools import partial
import os
from tkinter import PhotoImage, messagebox
import sqlite3
import customtkinter as ctk
import json
import hashlib
import re

class PasswordManager(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.geometry("1000x700")
        self.title("Password Manager")

        settings = self.load_settings()
        self.current_theme = settings.get("theme")
        self.language = settings.get("language")

        ctk.set_appearance_mode(self.current_theme)
        self.load_language(self.language)

        self.widget_texts = {}

        BASE_DIR = os.path.dirname(os.path.abspath(__file__))

        self.edit_icon_path = os.path.join(BASE_DIR, "icons/edit_icon.png")
        self.delete_icon_path = os.path.join(BASE_DIR, "icons/delete_icon.png")
        self.eye_icon_path = os.path.join(BASE_DIR, "icons/eye_icon.png")
        self.eye_blind_icon_path = os.path.join(BASE_DIR, "icons/eye_blind_icon.png")
        self.go_back_icon_path = os.path.join(BASE_DIR, "icons/go_back_icon_icon.png")

        self.english_icon_path = os.path.join(BASE_DIR, "icons/languages/english_icon.png")
        self.turkish_icon_path = os.path.join(BASE_DIR, "icons/languages/turkish_icon.png")
        self.german_icon_path = os.path.join(BASE_DIR, "icons/languages/german_icon.png")

        self.connect_database()
        
        # self.user_id=1
        # self.my_passwords_page()
        self.widgets()

    def create_label(self, frame, text, font, row, column, padx, pady, sticky="w", columnspan=1):
        label = ctk.CTkLabel(
            frame, 
            text=text, 
            font=font
        )
        label.grid(row=row, column=column, padx=padx, pady=pady, sticky=sticky, columnspan=columnspan)

    def create_button(self, frame, text, command, fg_color, hover_color, height, width, row, column, padx, pady, sticky="w", hover="", columnspan=1):
        button = ctk.CTkButton(
            frame,
            text=text,
            command=command,
            fg_color=fg_color,
            hover_color=hover_color,
            height=height,
            width=width,
            hover=hover
        )
        button.grid(row=row, column=column, padx=padx, pady=pady, sticky=sticky, columnspan=columnspan)

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

        self.widget_texts["secure"] = self.create_label(self, self.get_text("secure"), ("Helvetica", 20), 0, 0, 20, 20, "nsew")

        center_frame = ctk.CTkFrame(self)
        center_frame.grid(row=1, column=0, padx=20, pady=20)

        self.widget_texts["login"] = self.create_button(center_frame, self.get_text("login"), self.login_page, "#41a500", "#286400", 32, 200, 0, 0, 20, 20)
        self.widget_texts["signup"] = self.create_button(center_frame, self.get_text("signup"), self.signup_page, "#0055e0", "#002d77", 32, 200, 1, 0, 20, 20)
        self.widget_texts["quit"] = self.create_button(center_frame, self.get_text("quit"), self.quit, "#ae0000", "#780000", 32, 200, 2, 0, 20, 20)

    def login_page(self):
        for widget in self.winfo_children():
            widget.grid_forget()

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.widget_texts["login"] = self.create_label(self, self.get_text("login"), ("Helvetica", 20), 0, 0, 20, 20, sticky="nsew")
        
        center_frame = ctk.CTkFrame(self)
        center_frame.grid(row=1, column=0, padx=20, pady=20)

        self.widget_texts["username"] = self.create_label(center_frame, self.get_text("username"), ("Helvetica", 15), 0, 0, 20, 5)
        username_entry = self.create_entry(center_frame, "...", 200, "", 1, 0, 20, 0)

        self.widget_texts["password"] = self.create_label(center_frame, self.get_text("password"), ("Helvetica", 15), 2, 0, 20, 5)
        password_entry = self.create_entry(center_frame, "...", 200, "*", 3, 0, 20, 0)

        self.widget_texts["submit"] = self.create_button(center_frame, self.get_text("submit"), lambda: self.login(username_entry.get(), password_entry.get()), "#41a500", "#286400", 32, 200, 4, 0, 20, (20, 10))
        self.widget_texts["goback"] = self.create_button(center_frame, self.get_text("goback"), self.welcome_page, "#b48900", "#795c00", 32, 200, 5, 0, 20, 0)

        def focus_password(event):
            password_entry.focus_set()

        def on_enter(event):
            self.login(username_entry.get(), password_entry.get())

        username_entry.bind("<Return>", focus_password)
        password_entry.bind("<Return>", on_enter)

    def signup_page(self):
        for widget in self.winfo_children():
            widget.grid_forget()

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.widget_texts["signup"] = self.create_label(self, self.get_text("signup"), ("Helvetica", 20), 0, 0, 20, 20, sticky="nsew")
        
        center_frame = ctk.CTkFrame(self)
        center_frame.grid(row=1, column=0, padx=20, pady=20)

        self.widget_texts["username"] = self.create_label(center_frame, self.get_text("username"), ("Helvetica", 15), 0, 0, 20, 5)
        username_entry = self.create_entry(center_frame, "...", 200, "", 1, 0, 20, 0)

        self.create_label(center_frame, "Email", ("Helvetica", 15), 2, 0, 20, 5)
        email_entry = self.create_entry(center_frame, "...", 200, "", 3, 0, 20, 0)

        self.widget_texts["password"] = self.create_label(center_frame, self.get_text("password"), ("Helvetica", 15), 4, 0, 20, 5)
        password_entry = self.create_entry(center_frame, "...", 200, "*", 5, 0, 20, 0)
        
        self.widget_texts["submit"] = self.create_button(center_frame, self.get_text("submit"), lambda: self.signup(username_entry.get(), email_entry.get(), password_entry.get()), "#41a500", "#286400", 32, 200, 6, 0, 20, (20, 10))
        self.widget_texts["goback"] = self.create_button(center_frame, self.get_text("goback"), self.welcome_page, "#b48900", "#795c00", 32, 200, 7, 0, 20, 0)
        
        def focus_email(event):
            email_entry.focus_set()

        def focus_password(event):
            password_entry.focus_set()

        def on_enter(event):
            self.signup(username_entry.get(), password_entry.get(), email_entry.get())

        username_entry.bind("<Return>", focus_email)
        email_entry.bind("<Return>", focus_password)
        password_entry.bind("<Return>", on_enter)

    def homepage(self):
        for widget in self.winfo_children():
            widget.grid_forget()

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.widget_texts["welcome"] = self.create_label(self, self.get_text("welcome"), ("Helvetica", 20), 0, 0, 20, 20, "nsew")

        center_frame = ctk.CTkFrame(self)
        center_frame.grid(row=1, column=0, padx=20, pady=20)

        self.widget_texts["addpassword"] = self.create_button(center_frame, self.get_text("addpassword"), self.add_password_page, "#41a500", "#286400", 32, 200, 0, 0, 20, 20)
        self.widget_texts["mypasswords"] = self.create_button(center_frame, self.get_text("mypasswords"), self.my_passwords_page, "#0055e0", "#002d77", 32, 200, 1, 0, 20, 20)
        self.widget_texts["settings"] = self.create_button(center_frame, self.get_text("settings"), self.settings_page, "#b48900", "#795c00", 32, 200, 2, 0, 20, 20)
        self.widget_texts["logout"] = self.create_button(center_frame, self.get_text("logout"), self.welcome_page, "#ae0000", "#780000", 32, 200, 3, 0, 20, 20)

    def add_password_page(self):
        for widget in self.winfo_children():
            widget.grid_forget()

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.widget_texts["addpassword"] = self.create_label(self, self.get_text("addpassword"), ("Helvetica", 20), 0, 0, 20, 20, sticky="nsew")
        
        center_frame = ctk.CTkFrame(self)
        center_frame.grid(row=1, column=0, padx=20, pady=20)

        self.widget_texts["website"] = self.create_label(center_frame, self.get_text("website"), ("Helvetica", 15), 0, 0, 20, 5)
        website_entry = self.create_entry(center_frame, "...", 200, "", 1, 0, 20, 0)

        self.widget_texts["websiteurloptional"] = self.create_label(center_frame, self.get_text("websiteurloptional"), ("Helvetica", 15), 2, 0, 20, 5)
        website_url = self.create_entry(center_frame, "...", 200, "", 3, 0, 20, 0)

        self.widget_texts["usernameoptional"] = self.create_label(center_frame, self.get_text("usernameoptional"), ("Helvetica", 15), 4, 0, 20, 5)
        username_entry = self.create_entry(center_frame, "...", 200, "", 5, 0, 20, 0)

        self.widget_texts["emailoptional"] = self.create_label(center_frame, self.get_text("emailoptional"), ("Helvetica", 15), 6, 0, 20, 5)
        email_entry = self.create_entry(center_frame, "...", 200, "", 7, 0, 20, 0)

        self.widget_texts["password"] = self.create_label(center_frame, self.get_text("password"), ("Helvetica", 15), 8, 0, 20, 5)
        password_entry = self.create_entry(center_frame, "...", 200, "*", 9, 0, 20, 0)
        
        self.widget_texts["submit"] = self.create_button(center_frame, self.get_text("submit"), lambda: self.add_password(self.user_id, website_entry.get(), website_url.get(), username_entry.get(), email_entry.get(), password_entry.get()), "#41a500", "#286400", 32, 200, 10, 0, 20, (20, 10))
        self.widget_texts["goback"] = self.create_button(center_frame, self.get_text("goback"), self.homepage, "#b48900", "#795c00", 32, 200, 11, 0, 20, 0)
    
        def focus_website_url(event):
            website_url.focus_set()

        def focus_username(event):
            username_entry.focus_set()

        def focus_email(event):
            email_entry.focus_set()

        def focus_password(event):
            password_entry.focus_set()

        def on_submit(event):
            self.add_password(
                self.user_id,
                website_entry.get(),
                website_url.get(),
                username_entry.get(),
                email_entry.get(),
                password_entry.get()
            )

        website_entry.bind("<Return>", focus_website_url)
        website_url.bind("<Return>", focus_username)
        username_entry.bind("<Return>", focus_email)
        email_entry.bind("<Return>", focus_password)
        password_entry.bind("<Return>", on_submit)

    def my_passwords_page(self):
        for widget in self.winfo_children():
            widget.grid_forget()

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        center_frame = ctk.CTkScrollableFrame(self)
        center_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        center_frame.grid_rowconfigure(0, weight=1)
        center_frame.grid_rowconfigure(1, weight=1)
        center_frame.grid_rowconfigure(2, weight=1)
        center_frame.grid_rowconfigure(3, weight=1)
        center_frame.grid_rowconfigure(4, weight=1)
        center_frame.grid_columnconfigure(0, weight=1)
        center_frame.grid_columnconfigure(1, weight=1)
        center_frame.grid_columnconfigure(2, weight=1)
        center_frame.grid_columnconfigure(3, weight=1)
        center_frame.grid_columnconfigure(4, weight=1)
        center_frame.grid_columnconfigure(5, weight=1)
        center_frame.grid_columnconfigure(6, weight=1)
        center_frame.grid_columnconfigure(7, weight=1)
        
        edit_icon = PhotoImage(file=self.edit_icon_path)
        edit_icon = edit_icon.subsample(25, 25)

        delete_icon = PhotoImage(file=self.delete_icon_path)
        delete_icon = delete_icon.subsample(25, 25)
        
        eye_icon = PhotoImage(file=self.eye_icon_path)
        eye_icon = eye_icon.subsample(25, 25)
        
        eye_blind_icon = PhotoImage(file=self.eye_blind_icon_path)
        eye_blind_icon = eye_blind_icon.subsample(25, 25)
        
        self.widget_texts["mypasswords"] = self.create_label(center_frame, self.get_text("mypasswords"), ("Arial", 36, "bold"), 0, 0, 20, 20, "nw", 10)
        
        self.widget_texts["goback"] = self.create_button(center_frame, self.get_text("goback"), self.homepage, "#b48900", "#795c00", 32, 100, 0, 7, (0, 10), 20, "ne", 2)

        columns = ["Website", "Website URL", "Username", "Email", "Password", "Show"]
        
        password_logs = self.cursor.execute("""SELECT * FROM passwords WHERE user_id = :user_id""", {"user_id": self.user_id}).fetchall()
        indexes_to_pass = [0, 1]
        
        passwords = self.cursor.execute("""SELECT password FROM passwords WHERE user_id = :user_id""", {"user_id": self.user_id}).fetchall()

        # eye_button = ctk.CTkButton(center_frame, image=eye_icon, width=30, height=30, corner_radius=50, text="", fg_color="transparent", hover="None")
        # eye_blind_button = ctk.CTkButton(center_frame, image=eye_blind_icon, width=30, height=30, corner_radius=50, text="", command=lambda: show_password(password_id), fg_color="green", hover="None")

        current_eye = eye_icon

        if not password_logs:
            self.widget_texts["nopasswords"] = self.create_label(center_frame, self.get_text("nopasswords"), ("Helvetica", 20), 1, 0, 0, 10)

        else:
            for i, column in enumerate(columns):
                self.widget_texts["column"] = self.create_label(center_frame, self.get_text(column), ("Helvetica", 15), 1, i, 5, 10)
                
            for j, attributes in enumerate(password_logs):
                for k, attribute in enumerate(attributes):
                    if k not in indexes_to_pass:
                        if not attribute:
                            self.create_label(center_frame, "-", ("Arial", 12), j+2, k-2, 5, 10)
                        else:
                            if k == 6:
                                password = passwords[j][0]

                                password_label = ctk.CTkLabel(center_frame, text="******", font=("Arial", 12))
                                password_label.grid(row=j+2, column=k-2, padx=5, pady=10, sticky="w")

                                current_eye_state = {"icon": eye_blind_icon}

                                def toggle_password(password_label, password, eye_button, current_eye_state):                                    
                                    if current_eye_state["icon"] == eye_blind_icon:
                                        password_text = password
                                        current_eye_state["icon"] = eye_icon
                                    else:
                                        password_text = "******"
                                        current_eye_state["icon"] = eye_blind_icon
                                    
                                    eye_button.configure(image=current_eye_state["icon"])
                                    password_label.configure(text=password_text)

                                eye_button = ctk.CTkButton(center_frame, image=current_eye, width=30, height=30, corner_radius=50, text="", command=partial(toggle_password, password_label, password, None, current_eye_state), fg_color="transparent", hover="None")
                                
                                eye_button.configure(command=partial(toggle_password, password_label, password, eye_button, current_eye_state))
                                eye_button.grid(row=j+2, column=k-1, padx=5, pady=10, sticky="w")
                            else:
                                self.create_label(center_frame, attribute, ("Arial", 12), j+2, k-2, 5, 10)
                            
                edit_button = ctk.CTkButton(center_frame, image=edit_icon, width=30, height=30, corner_radius=50, text="", fg_color="green", hover="None")
                edit_button.grid(row=j+2, column=k, padx=0, pady=10)    
                delete_button = ctk.CTkButton(center_frame, image=delete_icon, width=30, height=30, corner_radius=50, text="", command=lambda id=password_logs[j][0]: self.delete_password(id), fg_color="red", hover="None")
                delete_button.grid(row=j+2, column=k+1, padx=0, pady=10)    

    def settings_page(self):
        for widget in self.winfo_children():
            widget.grid_forget()

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        center_frame = ctk.CTkFrame(self)
        center_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

        for i in range(5):
            if i == 0:
                center_frame.grid_rowconfigure(i, weight=5)
            elif i == 1 or i == 3:
                center_frame.grid_rowconfigure(i, weight=3)
            else:
                center_frame.grid_rowconfigure(i, weight=1)

        for i in range(3):
            if i < 3:
                center_frame.grid_columnconfigure(i, weight=1)
            else:
                center_frame.grid_columnconfigure(i, weight=2)

        self.widget_texts["settings"] = self.create_label(center_frame, self.get_text("settings"), ("Arial", 36, "bold"), 0, 0, 20, (20, 0), "nw", 10)

        self.widget_texts["goback"] = self.create_button(center_frame, self.get_text("goback"), self.homepage, "#b48900", "#795c00", 32, 100, 0, 4, 20, (20, 0), "ne")
        
        # self.widget_texts["themecolor"] = self.create_label(center_frame, self.get_text("themecolor"), ("Arial", 24), 1, 0, 20, (20, 0), "w")

        themes = [
            {"text": self.get_text("dark"), "theme": "dark", "bg_color": "#333333", "fg_color": "white"},
            {"text": self.get_text("light"), "theme": "light", "bg_color": "#BBBBBB", "fg_color": "black"},
            {"text": self.get_text("system"), "theme": "system", "bg_color": "#0078D7", "fg_color": "white"}
        ]

        self.widget_texts["themelabel"] = self.create_label(center_frame, self.get_text("themelabel"), ("Arial", 20), 1, 0, 20, 0, "w", 10)

        for index, theme in enumerate(themes):
            self.widget_texts[f"theme_{theme['theme']}"] = self.create_button(
                center_frame, 
                theme["text"], 
                lambda theme=theme: self.set_theme(theme["theme"]), 
                theme["bg_color"],
                theme["fg_color"],
                30, 80, 2, index, (20, 0), 0
            )

        # colors = [
        #     {"text": self.get_text("blue"), "color": "blue"},
        #     {"text": self.get_text("dark-blue"), "color": "dark-blue"},
        #     {"text": self.get_text("green"), "color": "green"},
        # ]

        # self.widget_texts["colorlabel"] = self.create_label(center_frame, self.get_text("colorlabel"), ("Arial", 20), 3, 0, 20, 0)

        # for index, color in enumerate(colors):
        #     # self.create_button(center_frame, theme["text"], lambda theme=theme: self.set_theme(theme["theme"]), "red", "red", 30, 50, 2, index+1, 0, 0)
        #     self.widget_texts["color"] = self.create_button(center_frame, color["text"], "", "red", "red", 30, 50, 2, index+1, 0, 0)

        self.widget_texts["language"] = self.create_label(center_frame, self.get_text("language"), ("Arial", 20), 3, 0, 20, 0, "w", 10)

        english_icon = PhotoImage(file=self.english_icon_path)
        english_icon = english_icon.subsample(12, 12)

        turkish_icon = PhotoImage(file=self.turkish_icon_path)
        turkish_icon = turkish_icon.subsample(12, 12)

        german_icon = PhotoImage(file=self.german_icon_path)
        german_icon = german_icon.subsample(12, 12)

        english_button = ctk.CTkButton(
            center_frame, 
            text="", 
            image=english_icon,
            command=lambda: self.change_language("en"),
            fg_color="transparent",
            hover=None,
            width=20
        )
        english_button.grid(row=4, column=0, padx=20, pady=0, sticky="w")

        turkish_button = ctk.CTkButton(
            center_frame, 
            text="", 
            image=turkish_icon,
            command=lambda: self.change_language("tr"),
            fg_color="transparent",
            hover=None,
            width=20
        )
        turkish_button.grid(row=4, column=1, padx=20, pady=0, sticky="w")

        german_button = ctk.CTkButton(
            center_frame, 
            text="", 
            image=german_icon,
            command=lambda: self.change_language("de"),
            fg_color="transparent",
            hover=None,
            width=20
        )
        german_button.grid(row=4, column=2, padx=20, pady=0, sticky="w")

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

    def delete_password(self, id):
        title_confirm = self.get_text("delete_password_title")
        message_confirm = self.get_text("delete_password_message")
        title_success = self.get_text("delete_success_title")
        message_success = self.get_text("delete_success_message")

        confirm = messagebox.askyesno(title_confirm, message_confirm)

        if confirm:
            self.cursor.execute("DELETE FROM passwords WHERE id = ?", (id,))
            self.conn.commit()
            messagebox.showinfo(title_success, message_success)
            self.my_passwords_page()

    def set_theme(self, theme):
        self.current_theme = theme
        ctk.set_appearance_mode(self.current_theme)

        settings = self.load_settings()
        settings["theme"] = self.current_theme

        with open("data/settings.json", "w") as file:
            json.dump(settings, file, indent=4)

    def change_language(self, language):
        self.language = language

        self.load_language(self.language)

        settings = self.load_settings()
        settings["language"] = self.language

        with open("data/settings.json", "w") as file:
            json.dump(settings, file, indent=4)

        self.settings_page()

    def load_language(self, lang_code):
        with open("data/localization/language.json", "r", encoding="utf-8") as file:
            self.languages = json.load(file)
        self.language = lang_code

    def get_text(self, key):
        return self.languages.get(self.language, {}).get(key, key)

    def quit(self):
        self.destroy()

if __name__ == "__main__":
    app = PasswordManager()
    app.mainloop()