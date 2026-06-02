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
        pass
    
    def _build_login_panel(self):
        pass
    
    def login(self):
        pass