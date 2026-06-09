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
        
        # Profile cards container
        cards_frame = ctk.CTkFrame(panel, fg_color="transparent")
        cards_frame.grid(row=0, column=0, pady=30)
 
        num_profiles = int(self.user_data["profiles"])
        for i in range(num_profiles):
            self._build_profile_card(cards_frame, f"Profile {i + 1}", i)
 
        # Add profile card if under tier limit
        limit = TIER_PROFILE_LIMITS.get(self.user_data["tier"], 1)
        if num_profiles < limit:
            self._build_add_card(cards_frame, num_profiles)
 
        # Sign out button
        ctk.CTkButton(panel, text="Sign Out", width=160, height=40,
                      corner_radius=12, fg_color=colours.DARK_ACCENT,
                      hover_color=colours.ACCENT, text_color=colours.TEXT_LIGHT,
                      font=("Segoe UI", 14, "bold"),
                      command=self._sign_out).grid(row=1, column=0, pady=(0, 20))
    
    def _build_profile_card(self, parent, name, index):
        card = ctk.CTkFrame(parent, width=140, height=180,
                            fg_color=colours.SECONDARY, corner_radius=16)
        card.grid(row=0, column=index, padx=20)
        card.grid_propagate(False)
        card.grid_columnconfigure(0, weight=1)
 
        avatar = ctk.CTkFrame(card, width=80, height=80,
                              corner_radius=40, fg_color=colours.DARK_ACCENT)
        avatar.grid(row=0, column=0, pady=(25, 8))
        avatar.grid_propagate(False)
 
        ctk.CTkLabel(avatar, text=name[0],
                     font=("Segoe UI", 28, "bold"),
                     text_color=colours.TEXT_LIGHT).place(relx=0.5, rely=0.5, anchor="center")
 
        ctk.CTkLabel(card, text=name,
                     font=("Segoe UI", 13, "bold"),
                     text_color=colours.TEXT_DARK).grid(row=1, column=0, pady=(0, 20))
 
        for widget in card.winfo_children():
            widget.bind("<Button-1>", lambda e, n=name: self._select_profile(n))
            widget.bind("<Enter>", lambda e, c=card: c.configure(fg_color=colours.ACCENT))
            widget.bind("<Leave>", lambda e, c=card: c.configure(fg_color=colours.SECONDARY))
        card.bind("<Button-1>", lambda e, n=name: self._select_profile(n))
        card.bind("<Enter>", lambda e, c=card: c.configure(fg_color=colours.ACCENT))
        card.bind("<Leave>", lambda e, c=card: c.configure(fg_color=colours.SECONDARY))
    
    def _build_add_card(self, parent, index):
        card = ctk.CTkFrame(parent, width=140, height=180,
                            fg_color=colours.SECONDARY, corner_radius=16,
                            border_width=2, border_color=colours.DARK_ACCENT)
        card.grid(row=0, column=index, padx=20)
        card.grid_propagate(False)
        card.grid_columnconfigure(0, weight=1)
 
        ctk.CTkLabel(card, text="+",
                     font=("Segoe UI", 48, "bold"),
                     text_color=colours.DARK_ACCENT).grid(row=0, column=0, pady=(25, 4))
 
        ctk.CTkLabel(card, text="Add Profile",
                     font=("Segoe UI", 13),
                     text_color=colours.TEXT_DARK).grid(row=1, column=0)
 
        card.bind("<Button-1>", lambda e: self._add_profile_dialog())
        card.bind("<Enter>", lambda e: card.configure(fg_color=colours.ACCENT))
        card.bind("<Leave>", lambda e: card.configure(fg_color=colours.SECONDARY))
    
    def _select_profile(self, name):
        if self.on_profile_selected:
            self.on_profile_selected(self.username, name)
 
    def _sign_out(self):
        if self.on_sign_out:
            self.on_sign_out()
 
    def _save_user_data(self):
        rows = []
        with open(CSV_PATH, newline="") as f:
            reader = csv.DictReader(f)
            fieldnames = reader.fieldnames
            for row in reader:
                rows.append(self.user_data if row["username"] == self.username else row)
        with open(CSV_PATH, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
    # Have create multiple functions each to handle their own part of profile selection
