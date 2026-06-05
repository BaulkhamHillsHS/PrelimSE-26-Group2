import customtkinter as ctk
from assets import colours
import csv
import os
# Necessary Imports for the Profile Selection Frame

CSV_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "accounts.csv")

TIER_PROFILE_LIMITS = {
    "Light Cream": 1,
    "Whipped Cream": 2,
    "Heavy Cream": 4,
}
# Limits for number of profile based on the subscription plan they have

class ProfileSelectionFrame(ctk.CTkFrame):
    def __init__(self, parent, username, on_profile_selected=None):  # Created a function similarly to the login_frame py and subscriptio_frame py to handle profile selection
        super().__init__(parent)
        self.username = username
        self.on_profile_selected = on_profile_selected
        self.user_data = self._load_user_data()
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
 
        self._build_header()
        self._build_profiles_panel()
 
    def _load_user_data(self):
        with open(CSV_PATH, newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row["username"] == self.username:
                    return row
        return None
        
    def _build_header(self):
        header = ctk.CTkFrame(self, fg_color=colours.SECONDARY, corner_radius=20)
        header.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 10))
        header.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(header, text="StreamCream",
                     font=("Segoe UI", 28, "bold"),
                     text_color=colours.TEXT_DARK).grid(row=0, column=0, pady=(20, 4))
 
        ctk.CTkLabel(header, text="Who's watching?",
                     font=("Segoe UI", 16),
                     text_color=colours.TEXT_DARK).grid(row=1, column=0, pady=(0, 20))
 # Function built to create the header of the profile selection frame
 
    def _build_profiles_panel(self):
        panel = ctk.CTkFrame(self, fg_color=colours.PRIMARY, corner_radius=20)
        panel.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))
        panel.grid_columnconfigure(0, weight=1)
        panel.grid_rowconfigure(0, weight=1)
        panel.grid_rowconfigure(1, weight=0)
        
 