import os
import customtkinter as ctk
import json

class PasswordManager(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.geometry("300x500")
        self.title("Password Manager")

        settings = self.load_settings()
        self.current_theme = settings.get("theme")
        self.language = settings.get("language")

        ctk.set_appearance_mode(self.current_theme)
        # self.load_language(self.language)

        self.widgets()

    def create_label(self, frame, text, font, row, column, padx, pady, sticky="w"):
        label = ctk.CTkLabel(
            frame, 
            text=text, 
            font=font
        )
        label.grid(row=row, column=column, padx=padx, pady=pady, sticky=sticky)

    def create_button(self, frame, text, command, fg_color, hover_color, row, column, padx, pady, sticky="w"):
        button = ctk.CTkButton(
            frame,
            text=text,
            command=command,
            fg_color=fg_color,
            hover_color=hover_color
        )
        button.grid(row=row, column=column, padx=padx, pady=pady, sticky=sticky)

    def create_entry(self, frame, placeholder_text, width, row, column, padx, pady, sticky="w"):
        entry = ctk.CTkEntry(
            frame,
            placeholder_text=placeholder_text,
            corner_radius=5,
            width=width
        )
        entry.grid(row=row, column=column, padx=padx, pady=pady, sticky=sticky)

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

        self.create_label(self, "Securely store and manage\nyour passwords", ("Helvetica", 20), 0, 0, 20, 20)

        center_frame = ctk.CTkFrame(self)
        center_frame.grid(row=1, column=0, padx=20, pady=20)

        self.create_button(center_frame, "Login", self.login_page, "green", "#006400", 0, 0, 20, 20)
        self.create_button(center_frame, "Sign up", self.signup_page, "red", "#8B0000", 1, 0, 20, 20)
        self.create_button(center_frame, "Quit", self.quit, "#DAA520", "#B8860B", 2, 0, 20, 20)

    def login_page(self):
        for widget in self.winfo_children():
            widget.grid_forget()

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.create_label(self, "Login", ("Helvetica", 20), 0, 0, 20, 20)
        
        center_frame = ctk.CTkFrame(self)
        center_frame.grid(row=1, column=0, padx=20, pady=20)

        self.create_label(center_frame, "Username", ("Helvetica", 15), 0, 0, 20, 5)
        self.create_entry(center_frame, "...", 200, 1, 0, 20, 0)

        self.create_label(center_frame, "Password", ("Helvetica", 15), 2, 0, 20, 5)
        self.create_entry(center_frame, "...", 200, 3, 0, 20, 0)

        self.create_button(center_frame, "Submit", self.homepage, "#DAA520", "#B8860B", 4, 0, 20, 20)
    
    def signup_page(self):
        return

    def homepage(self):
        for widget in self.winfo_children():
            widget.grid_forget()

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        header = ctk.CTkLabel(
            self,
            text="Welcome!",
            font=("Helvetica", 20)
        )
        header.grid(row=0, column=0, padx=20, pady=20)

        center_frame = ctk.CTkFrame(self)
        center_frame.grid(row=1, column=0, padx=20, pady=20)

        add_password_button = ctk.CTkButton(
            center_frame,
            text="Add Password",
            command=self.add_password_page,
            fg_color="green",
            hover_color="#006400"
        )
        add_password_button.grid(row=0, column=0, padx=20, pady=20)

        password_list_button = ctk.CTkButton(
            center_frame,
            text="My Passwords",
            command=self.my_passwords_page,
            fg_color="blue",
            hover_color="darkblue"
        )
        password_list_button.grid(row=1, column=0, padx=20, pady=20)

        settings_button = ctk.CTkButton(
            center_frame,
            text="Settings",
            command=self.settings_page,
            fg_color="#DAA520",
            hover_color="#B8860B"
        )
        settings_button.grid(row=2, column=0, padx=20, pady=20)

        logout_button = ctk.CTkButton(
            center_frame,
            text="Logout",
            command=self.welcome_page,
            fg_color="red",
            hover_color="#8B0000"
        )
        logout_button.grid(row=3, column=0, padx=20, pady=20)

    def add_password_page(self):
        return
    
    def my_passwords_page(self):
        return
    
    def settings_page(self):
        return

    def quit(self):
        self.destroy()

if __name__ == "__main__":
    app = PasswordManager()
    app.mainloop()