import customtkinter as ctk
from assets import colours

class ProfileSelection(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._build_profile_panel()
    
    def _build_profile_panel(self):
        pass

