import customtkinter as ctk
from assets import colours

class SettingsFrame(ctk.CTkFrame):
    def __init__(self, parent, email, profile_name,
                 on_back=None, on_subscription=None,
                 on_switch_profile=None, on_sign_out=None):
        super().__init__(parent)
        self.email = email
        self.profile_name = profile_name
        self.on_back = on_back
        self.on_subscription = on_subscription
        self.on_switch_profile = on_switch_profile
        self.on_sign_out = on_sign_out

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)

        self._build_header()
        self._build_settings_panel()

    def _build_header(self):
        header = ctk.CTkFrame(self, fg_color=colours.SECONDARY, corner_radius=20)
        header.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 10))
        header.grid_columnconfigure(0, weight=1)
        header.grid_columnconfigure(1, weight=0)

        if self.on_back:
            ctk.CTkButton(header, text="< Back to Browse", width=140, height=36,
                          corner_radius=10, fg_color=colours.DARK_ACCENT,
                          hover_color=colours.ACCENT, text_color=colours.TEXT_LIGHT,
                          font=("Segoe UI", 13, "bold"),
                          command=self.on_back).grid(row=0, column=0, padx=(15, 10), pady=12, sticky="w")

        ctk.CTkLabel(header, text="StreamCream",
                     font=("Segoe UI", 20, "bold"),
                     text_color=colours.TEXT_DARK).grid(row=0, column=1, padx=(10, 20), pady=12, sticky="e")

    def _build_settings_panel(self):
        panel = ctk.CTkFrame(self, fg_color=colours.PRIMARY, corner_radius=20)
        panel.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))
        panel.grid_columnconfigure(0, weight=1)
        panel.grid_rowconfigure(0, weight=1)

        card = ctk.CTkFrame(panel, fg_color=colours.SECONDARY, corner_radius=20)
        card.grid(row=0, column=0, padx=100, pady=60)
        card.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(card, text="Settings",
                     font=("Segoe UI", 28, "bold"),
                     text_color=colours.TEXT_DARK).grid(row=0, column=0, pady=(30, 25))

        ctk.CTkLabel(card, text=f"Profile: {self.profile_name}",
                     font=("Segoe UI", 14),
                     text_color=colours.TEXT_DARK).grid(row=1, column=0, pady=(0, 20))

        ctk.CTkButton(card, text="Manage Subscription", width=260, height=44,
                      corner_radius=12, fg_color=colours.DARK_ACCENT,
                      hover_color=colours.ACCENT, text_color=colours.TEXT_LIGHT,
                      font=("Segoe UI", 15, "bold"),
                      command=self.on_subscription).grid(row=2, column=0, pady=6)

        ctk.CTkButton(card, text="Switch Profile", width=260, height=44,
                      corner_radius=12, fg_color=colours.DARK_ACCENT,
                      hover_color=colours.ACCENT, text_color=colours.TEXT_LIGHT,
                      font=("Segoe UI", 15, "bold"),
                      command=self.on_switch_profile).grid(row=3, column=0, pady=6)

        ctk.CTkButton(card, text="Sign Out", width=260, height=44,
                      corner_radius=12, fg_color=colours.DARK_ACCENT,
                      hover_color=colours.ACCENT, text_color=colours.TEXT_LIGHT,
                      font=("Segoe UI", 15, "bold"),
                      command=self.on_sign_out).grid(row=4, column=0, pady=6)

        ctk.CTkLabel(card, text="",
                     font=("Segoe UI", 12),
                     text_color=colours.TEXT_DARK).grid(row=5, column=0, pady=(10, 30))

