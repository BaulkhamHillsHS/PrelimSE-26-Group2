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
    def _build_browse_panel(self):
        # Scrollable grid of placeholder posters
        panel = ctk.CTkScrollableFrame(self, fg_color=colours.PRIMARY, corner_radius=20)
        panel.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))
 
        for col in range(4):
            panel.grid_columnconfigure(col, weight=1)
 
        ctk.CTkLabel(panel, text="Browse",
                     font=("Segoe UI", 22, "bold"),
                     text_color=colours.TEXT_DARK).grid(row=0, column=0, columnspan=4,
                                                         sticky="w", padx=10, pady=(15, 15))
 
        row = 1
        col = 0
        for title in TITLES:
            self._build_poster_card(panel, title, row, col)
            col += 1
            if col == 4:
                col = 0
                row += 1
 
    
    def _build_poster_card(self, parent, title, row, col):
        # Individual placeholder poster card (no real image, just a coloured block)
        card = ctk.CTkFrame(parent, width=180, height=240,
                            fg_color=colours.SECONDARY, corner_radius=14)
        card.grid(row=row, column=col, padx=12, pady=12)
        card.grid_propagate(False)
        card.grid_columnconfigure(0, weight=1)
 
        poster = ctk.CTkFrame(card, width=160, height=170,
                              corner_radius=10, fg_color=colours.DARK_ACCENT)
        poster.grid(row=0, column=0, padx=10, pady=(10, 8))
        poster.grid_propagate(False)
 
        ctk.CTkLabel(card, text=title,
                     font=("Segoe UI", 13, "bold"),
                     text_color=colours.TEXT_DARK,
                     wraplength=160, justify="center").grid(row=1, column=0, padx=10, pady=(0, 10))
 
        for widget in (card, poster):
            widget.bind("<Enter>", lambda e, c=card: c.configure(fg_color=colours.ACCENT))
            widget.bind("<Leave>", lambda e, c=card: c.configure(fg_color=colours.SECONDARY))