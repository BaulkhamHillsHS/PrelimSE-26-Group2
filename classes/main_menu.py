import customtkinter as ctk
from assets import colours
 
# Hardcoded placeholder titles to let users browse on main menu
TITLES = [
    "The Last Voyage", "Crimson Tide", "Night Falls", "Golden Hour",
    "Echoes of Tomorrow", "Silver Lining", "The Long Road", "Starlight",
    "Hidden Depths", "Wildfire", "Paper Moon", "Open Skies",
]
 
class MainMenuFrame(ctk.CTkFrame):
    def __init__(self, parent, email, profile_name, on_sign_out=None):
        super().__init__(parent)
        self.email = email
        self.profile_name = profile_name
        self.on_sign_out = on_sign_out
 
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
 
        self._build_header()
        self._build_browse_panel()
 
    def _build_header(self):
        # Top bar with app name, current profile, and sign out button
        header = ctk.CTkFrame(self, fg_color=colours.SECONDARY, corner_radius=20)
        header.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 10))
        header.grid_columnconfigure(0, weight=1)
        header.grid_columnconfigure(1, weight=0)
        header.grid_columnconfigure(2, weight=0)
 
        ctk.CTkLabel(header, text="StreamCream",
                     font=("Segoe UI", 24, "bold"),
                     text_color=colours.TEXT_DARK).grid(row=0, column=0, padx=(20, 10), pady=15, sticky="w")
 
        ctk.CTkLabel(header, text=self.profile_name,
                     font=("Segoe UI", 14, "bold"),
                     text_color=colours.TEXT_DARK).grid(row=0, column=1, padx=10, pady=15)
 
        ctk.CTkButton(header, text="Sign Out", width=110, height=36,
                      corner_radius=10, fg_color=colours.DARK_ACCENT,
                      hover_color=colours.ACCENT, text_color=colours.TEXT_LIGHT,
                      font=("Segoe UI", 13, "bold"),
                      command=self.on_sign_out).grid(row=0, column=2, padx=(10, 20), pady=15)