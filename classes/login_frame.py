import customtkinter as ctk
from assets import colours
import csv
import os

CSV_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "accounts.csv")

class LoginFrame(ctk.CTkFrame):
    def __init__(self, parent, on_success=None):
        super().__init__(parent)
        
        self.on_success = on_success

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._build_branding_panel()
        self._build_login_panel()
    
    def _build_branding_panel(self):
        branding = ctk.CTkFrame(
            self,
            fg_color=colours.SECONDARY,
            corner_radius=20
        )
        branding.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(20, 10),
            pady=20
        )

        branding.grid_rowconfigure((0, 1, 2, 3), weight=1)
        branding.grid_columnconfigure(0, weight=1)

        # Logo placeholder
        logo = ctk.CTkFrame(
            branding,
            width=180,
            height=180,
            corner_radius=90,
            fg_color=colours.DARK_ACCENT
        )
        logo.grid(row=0, column=0, pady=(50, 20))
        logo.grid_propagate(False)

        logo_label = ctk.CTkLabel(
            logo,
            text="LOGO",
            font=("Segoe UI", 24, "bold"),
            text_color=colours.TEXT_LIGHT
        )
        logo_label.place(relx=0.5, rely=0.5, anchor="center")

        title = ctk.CTkLabel(
            branding,
            text="StreamCream",
            font=("Segoe UI", 40, "bold"),
            text_color=colours.TEXT_DARK
        )
        title.grid(row=1, column=0, pady=(0, 10))

        subtitle = ctk.CTkLabel(
            branding,
            text="Unlimited streaming.\nAnytime. Anywhere.",
            font=("Segoe UI", 18),
            justify="center",
            text_color=colours.TEXT_DARK
        )
        subtitle.grid(row=2, column=0)
    
    def _build_login_panel(self):
        login = ctk.CTkFrame(self, fg_color="transparent")
        login.grid(row=0, column=1, sticky="nsew", padx=(10, 20), pady=20)
        login.grid_columnconfigure(0, weight=1)

        heading = ctk.CTkLabel(login, text="Welcome Back",
                               font=("Segoe UI", 32, "bold"), 
                               text_color=colours.TEXT_DARK)
        heading.pack(pady=(80, 15))

        description = ctk.CTkLabel(login, text="Sign in to continue streaming",
                                   font=("Segoe UI", 16), text_color=colours.TEXT_DARK)
        description.pack(pady=(0, 40))

        self.username_entry = ctk.CTkEntry(login, width=350, height=45,
                                           placeholder_text="Email Address",
                                           border_width=0,fg_color=colours.BACKGROUND,
                                           text_color=colours.TEXT_DARK)
        self.username_entry.pack(pady=10)

        self.password_entry = ctk.CTkEntry(login, width=350, height=45,
                                           placeholder_text="Password", show="●",
                                           border_width=0, fg_color=colours.BACKGROUND,
                                           text_color=colours.TEXT_DARK)
        self.password_entry.pack(pady=10)

        remember_checkbox = ctk.CTkCheckBox(login, text="Remember me", 
                                            text_color=colours.TEXT_DARK,
                                            checkbox_width=20, checkbox_height=20,
                                            fg_color=colours.DARK_ACCENT,
                                            hover_color=colours.ACCENT)
        remember_checkbox.pack(pady=(15, 20))
        
        self.error_label = ctk.CTkLabel(login, text="",
                                        font=("Segoe UI", 13),
                                        text_color=colours.ERROR)
        self.error_label.pack(pady=(0, 5))

        login_button = ctk.CTkButton(login, text="Login", width=350, height=50, 
                                     corner_radius=12, fg_color=colours.DARK_ACCENT,
                                     hover_color=colours.ACCENT, text_color=colours.TEXT_LIGHT,
                                     font=("Segoe UI", 16, "bold"), command=self.login)
        login_button.pack(pady=10)
    
    def login(self):
        email = self.username_entry.get().strip()
        password = self.password_entry.get()

        if not email or not password:
            self.error_label.configure(text="Please enter email and password.")
            return

        with open(CSV_PATH, newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row["email"] == email and row["password"] == password:
                    if self.on_success:
                        self.on_success(row["username"]) 
                        # For testing purposes, switching to subscription page
                        # TODO: Transition to main app interface once implemented
                    return

        self.error_label.configure(text="Invalid email or password.")