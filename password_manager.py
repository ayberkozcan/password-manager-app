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

        header = ctk.CTkLabel(
            self,
            text="Securely store and manage\nyour passwords",
            font=("Helvetica", 20)
        )
        header.grid(row=0, column=0, padx=20, pady=20)

        center_frame = ctk.CTkFrame(self)
        center_frame.grid(row=1, column=0, padx=20, pady=20)

        login_button = ctk.CTkButton(
            center_frame,
            text="Login",
            command=self.login_page,
            fg_color="green",
            hover_color="#006400"
        )
        login_button.grid(row=0, column=0, padx=20, pady=20)

        sign_up_button = ctk.CTkButton(
            center_frame,
            text="Sign up",
            command=self.signup_page,
            fg_color="red",
            hover_color="#8B0000"
        )
        sign_up_button.grid(row=1, column=0, padx=20, pady=20)

        quit_button = ctk.CTkButton(
            center_frame,
            text="Quit",
            command=self.quit,
            fg_color="#DAA520",
            hover_color="#B8860B"
        )
        quit_button.grid(row=2, column=0, padx=20, pady=20)

    def login_page(self):
        return
    
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
            fg_color="red",
            hover_color="#8B0000"
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