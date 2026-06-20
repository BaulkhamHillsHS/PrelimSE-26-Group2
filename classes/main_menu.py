import customtkinter as ctk
from assets import colours
from data.content import CATEGORIES

class MainMenuFrame(ctk.CTkFrame):
    def __init__(self, parent, email, profile_name, on_sign_out=None, on_settings=None):
        super().__init__(parent)
        self.email = email
        self.profile_name = profile_name
        self.on_sign_out = on_sign_out
        self.on_settings = on_settings
 
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
        
        ctk.CTkButton(header, text="Settings", width=100, height=36,
                      corner_radius=10, fg_color=colours.DARK_ACCENT,
                      hover_color=colours.ACCENT, text_color=colours.TEXT_LIGHT,
                      font=("Segoe UI", 13, "bold"),
                      command=self.on_settings).grid(row=0, column=2, padx=5, pady=15)
 
        ctk.CTkButton(header, text="Sign Out", width=110, height=36,
                      corner_radius=10, fg_color=colours.DARK_ACCENT,
                      hover_color=colours.ACCENT, text_color=colours.TEXT_LIGHT,
                      font=("Segoe UI", 13, "bold"),
                      command=self.on_sign_out).grid(row=0, column=3, padx=(10, 20), pady=15)
        
    def _build_browse_panel(self):
        panel = ctk.CTkScrollableFrame(self, fg_color=colours.PRIMARY, corner_radius=20)
        panel.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))
        panel.grid_columnconfigure(0, weight=1)

        row_index = 0
        for category, items in CATEGORIES.items():
            ctk.CTkLabel(panel, text=category,
                         font=("Segoe UI", 20, "bold"),
                         text_color=colours.TEXT_DARK).grid(
                             row=row_index, column=0, sticky="w", padx=15, pady=(20, 5))
            row_index += 1

            scroll_row = ctk.CTkScrollableFrame(
                panel, fg_color=colours.BACKGROUND,
                corner_radius=12, orientation="horizontal", height=250)
            scroll_row.grid(row=row_index, column=0, sticky="ew", padx=10, pady=(0, 5))
            row_index += 1

            for col, (title, color) in enumerate(items):
                self._build_poster_card(scroll_row, title, color, col)
 
    
    def _build_poster_card(self, parent, title, color, col):
        card = ctk.CTkFrame(parent, width=180, height=230,
                            fg_color=colours.SECONDARY, corner_radius=14)
        card.grid(row=0, column=col, padx=10, pady=10)
        card.grid_propagate(False)
        card.grid_columnconfigure(0, weight=1)

        poster = ctk.CTkFrame(card, width=160, height=170,
                              corner_radius=10, fg_color=color)
        poster.grid(row=0, column=0, padx=10, pady=(10, 8))
        poster.grid_propagate(False)

        ctk.CTkLabel(poster, text="🎬",
                     font=("Segoe UI", 36),
                     text_color=colours.TEXT_LIGHT).place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(card, text=title,
                     font=("Segoe UI", 13, "bold"),
                     text_color=colours.TEXT_DARK,
                     wraplength=160, justify="center").grid(
                         row=1, column=0, padx=10, pady=(0, 10))

        for widget in (card, poster):
            widget.bind("<Enter>", lambda e, c=card: c.configure(fg_color=colours.ACCENT))
            widget.bind("<Leave>", lambda e, c=card: c.configure(fg_color=colours.SECONDARY))