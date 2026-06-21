import customtkinter as ctk
from assets import colours
from data.content import CATEGORIES
from classes.data_control import get_watchlist, remove_from_watchlist

class MainMenuFrame(ctk.CTkFrame):
    def __init__(self, parent, email, profile_name, on_sign_out=None, on_settings=None, on_play=None):
        super().__init__(parent)
        self.email = email
        self.profile_name = profile_name
        self.on_sign_out = on_sign_out
        self.on_settings = on_settings
        self.on_play = on_play
        self._panel = None
 
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
 
        self._build_header()
        self.after(200, self._build_browse_panel) # Delay to avoid lag when switching to main menu
 
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
        if self._panel:
            self._panel.destroy() # Refresh browse panel, important when updating watchlist
            
        panel = ctk.CTkScrollableFrame(self, fg_color=colours.PRIMARY, corner_radius=20)
        panel.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))
        panel.grid_columnconfigure(0, weight=1)
        self._panel = panel

        row_index = 0
        
        ### Build watchlist section ###
        watchlist = get_watchlist(self.email, self.profile_name)
        ctk.CTkLabel(panel, text="My Watchlist",
                     font=("Segoe UI", 20, "bold"),
                     text_color=colours.TEXT_DARK).grid(
                         row=row_index, column=0, sticky="w", padx=15, pady=(20, 5))
        row_index += 1

        if watchlist:
            scroll_row = ctk.CTkScrollableFrame(
                panel, fg_color=colours.BACKGROUND,
                corner_radius=12, orientation="horizontal", height=270)
            scroll_row.grid(row=row_index, column=0, sticky="ew", padx=10, pady=(0, 5))
            row_index += 1

            for col, content in enumerate(watchlist):
                self._build_poster_card(scroll_row, content, col, watchlist=True)
        else:
            ctk.CTkLabel(panel,
                         text="Your watchlist is empty. Browse titles and add them from the play screen!",
                         font=("Segoe UI", 13),
                         text_color=colours.TEXT_DARK).grid(
                             row=row_index, column=0, sticky="w", padx=15, pady=(0, 10))
            row_index += 1
        
        ### Build each category section ###
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

            for col, content in enumerate(items):
                self._build_poster_card(scroll_row, content, col)

    
    def _build_poster_card(self, parent, content, col, watchlist=False):
        card = ctk.CTkFrame(parent, width=180, height=230 + 30 * watchlist, # Make watchlist card 30 pixels taller
                            fg_color=colours.SECONDARY, corner_radius=14)
        card.grid(row=0, column=col, padx=10, pady=10 - 5 * watchlist) # Less padding for watchlist card to make room for button
        card.grid_propagate(False)
        card.grid_columnconfigure(0, weight=1)

        poster = ctk.CTkFrame(card, width=160, height=170,
                              corner_radius=10, fg_color=content.get_color())
        poster.grid(row=0, column=0, padx=10, pady=(10, 8))
        poster.grid_propagate(False)

        ctk.CTkLabel(poster, text="🎬",
                     font=("Segoe UI", 36),
                     text_color=colours.TEXT_LIGHT).place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(card, text=content.get_title(),
                     font=("Segoe UI", 13, "bold"),
                     text_color=colours.TEXT_DARK,
                     wraplength=160, justify="center").grid(
                         row=1, column=0, padx=10, pady=(0, 10))
        
        if watchlist: # Add "Remove from watchlist" button if it's a watchlist card
            ctk.CTkButton(card, text="✕  Remove", height=24,
                      corner_radius=8, fg_color="#c0392b",
                      hover_color="#e74c3c", text_color="white",
                      font=("Segoe UI", 10, "bold"),
                      command=lambda c=content: self._remove_from_watchlist(c)).grid(
                          row=2, column=0, padx=10, pady=(0, 10))

        for widget in (card, poster):
            widget.bind("<Button-1>", lambda e, c=content: self._on_card_click(c))
            widget.bind("<Enter>", lambda e, c=card: c.configure(fg_color=colours.ACCENT))
            widget.bind("<Leave>", lambda e, c=card: c.configure(fg_color=colours.SECONDARY))
        card.bind("<Button-1>", lambda e, c=content: self._on_card_click(c))
        card.bind("<Enter>", lambda e, c=card: c.configure(fg_color=colours.ACCENT))
        card.bind("<Leave>", lambda e, c=card: c.configure(fg_color=colours.SECONDARY))
    
    def _on_card_click(self, content):
        if self.on_play:
            self.on_play(content)
        
    def _remove_from_watchlist(self, content):
        remove_from_watchlist(self.email, self.profile_name, content) # Remove from watchlist
        self._build_browse_panel() # Rebuild/refresh browse panel