import customtkinter as ctk
from assets import colours
from data.data_control import load_user_data, save_user_data, load_profiles, add_profile, TIER_PROFILE_LIMITS

class ProfileSelectionFrame(ctk.CTkFrame):
    def __init__(self, parent, email, on_profile_selected=None, on_sign_out=None, on_back=None):  # Created a function similarly to the login_frame py and subscriptio_frame py to handle profile selection
        super().__init__(parent)
        self.email = email
        self.on_profile_selected = on_profile_selected
        self.on_sign_out = on_sign_out
        self.on_back = on_back
        self.user_data = load_user_data(self.email)
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
 
        self._build_header()
        self._build_profiles_panel()
        
    def _build_header(self):
        header = ctk.CTkFrame(self, fg_color=colours.SECONDARY, corner_radius=20)
        header.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 10))
        header.grid_columnconfigure(0, weight=1)
        
        if self.on_back: # If there is a back function, add a back button to the header
            ctk.CTkButton(header, text="< Back", width=90, height=32,
                          corner_radius=10, fg_color=colours.DARK_ACCENT,
                          hover_color=colours.ACCENT, text_color=colours.TEXT_LIGHT,
                          font=("Segoe UI", 12, "bold"),
                          command=self.on_back).grid(row=0, column=0, padx=(15, 10), pady=(12, 0), sticky="w")

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
        
        self._profile_names = load_profiles(self.email)
        for i, name in enumerate(self._profile_names):
            self._build_profile_card(cards_frame, name, i)
        
        # Add profile card if under tier limit
        limit = TIER_PROFILE_LIMITS.get(self.user_data["tier"], 1)
        if len(self._profile_names) < limit:
            self._build_add_card(cards_frame, len(self._profile_names))
 
        # Sign out button
        ctk.CTkButton(panel, text="Sign Out", width=160, height=40,
                      corner_radius=12, fg_color=colours.DARK_ACCENT,
                      hover_color=colours.ACCENT, text_color=colours.TEXT_LIGHT,
                      font=("Segoe UI", 14, "bold"),
                      command=self.on_sign_out).grid(row=1, column=0, pady=(0, 20))
    
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
            widget.bind("<Button-1>", lambda e, n=name: self.on_profile_selected(self.email, n))
            widget.bind("<Enter>", lambda e, c=card: c.configure(fg_color=colours.ACCENT))
            widget.bind("<Leave>", lambda e, c=card: c.configure(fg_color=colours.SECONDARY))
        card.bind("<Button-1>", lambda e, n=name: self.on_profile_selected(self.email, n))
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
            self.on_profile_selected(self.email, name)
    
    def _refresh_profiles(self): # Delete and rebuild
        for widget in self.winfo_children():
            widget.destroy()
        self._build_header()
        self._build_profiles_panel()
    
    def _add_profile_dialog(self):
        popup = ctk.CTkToplevel(self)
        popup.title("Add Profile")
        popup.configure(fg_color=colours.SECONDARY)
        popup.resizable(False, False)
        popup_width, popup_height = 340, 200
        screen_w = popup.winfo_screenwidth()
        screen_h = popup.winfo_screenheight()
        popup.geometry(f"{popup_width}x{popup_height}+{(screen_w - popup_width)//2}+{(screen_h - popup_height)//2}")
        popup.transient(self.winfo_toplevel())
        popup.grab_set()
        popup.focus()
 
        main = ctk.CTkFrame(popup, fg_color="transparent")
        main.pack(expand=True, fill="both", padx=30, pady=25)
        main.grid_columnconfigure(0, weight=1)
 
        ctk.CTkLabel(main, text="New Profile Name", font=("Segoe UI", 18, "bold"),
                     text_color=colours.TEXT_DARK).grid(row=0, column=0, pady=(0, 12))
 
        name_entry = ctk.CTkEntry(main, width=240, height=40, placeholder_text="e.g. Kids, Dad...",
                                  border_width=0, fg_color=colours.BACKGROUND, text_color=colours.TEXT_DARK)
        name_entry.grid(row=1, column=0, pady=(0, 0))
 
        error_label = ctk.CTkLabel(main, text="", font=("Segoe UI", 12), text_color=colours.ERROR)
        error_label.grid(row=2, column=0)
        
        def save():
            name = name_entry.get().strip()
            if not name:
                error_label.configure(text="Profile name cannot be empty")
                return
            if name in self._profile_names:
                error_label.configure(text="Profile name already exists")
                return
            error_label.configure(text="")
            add_profile(self.email, name)
            self.user_data["profiles"] = str(int(self.user_data["profiles"]) + 1)
            save_user_data(self.user_data)
            popup.destroy()
            self._refresh_profiles()

        ctk.CTkButton(main, text="Save", width=120, height=36,
                      corner_radius=12, fg_color=colours.DARK_ACCENT,
                      hover_color=colours.ACCENT, text_color=colours.TEXT_LIGHT,
                      font=("Segoe UI", 14, "bold"),
                      command=save).grid(row=3, column=0, pady=(4, 0))

        name_entry.bind("<Return>", lambda e: save())
