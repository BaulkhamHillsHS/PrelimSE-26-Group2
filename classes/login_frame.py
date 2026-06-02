import customtkinter as ctk
from assets import colours

class LoginFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

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
        pass
    
    def login(self):
        pass