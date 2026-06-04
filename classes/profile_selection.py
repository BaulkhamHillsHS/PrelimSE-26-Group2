import customtkinter as ctk
from assets import colours
import csv
import os
# Necessary Imports for the Profile Selection Frame



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
        
