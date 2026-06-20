import customtkinter as ctk
from assets import colours
from classes.login_frame import LoginFrame
from classes.subscription_frame import SubscriptionFrame
from classes.profile_selection import ProfileSelectionFrame
from classes.main_menu import MainMenuFrame
from classes.settings_frame import SettingsFrame
from classes.playback_frame import PlaybackFrame

# Main app entry point for StreamCream GUI
# Starts with login

class App(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("StreamCream")

        self.configure(fg_color=colours.BACKGROUND)
        self.minsize(800, 600)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        self.current_frame = None
        self._email = None
        self._profile_name = None
        self._show_login()
        
        # Maximise window after short delay (doesn't work without delay for some reason)
        self.after(10, lambda: self.state("zoomed"))
    
    def _show_login(self):
        # Destroy existing frame and show login screen
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = LoginFrame(self, on_success=self._on_login_success)
        self.current_frame.grid(row=0, column=0, sticky="nsew")
    
    def _on_login_success(self, email):
        self._email = email
        self._show_profile_selection()
    
    def _show_profile_selection(self, on_back=None):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = ProfileSelectionFrame(self, self._email,
                                                   on_profile_selected=self._on_profile_selected,
                                                   on_sign_out=self._show_login,
                                                   on_back=on_back)
        self.current_frame.grid(row=0, column=0, sticky="nsew")
    
    def _on_profile_selected(self, email, profile_name):
        self._email = email
        self._profile_name = profile_name
        self._show_main_menu()

    def _show_main_menu(self):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = MainMenuFrame(self, self._email, self._profile_name,
                                           on_sign_out=self._show_login,
                                           on_settings=self._show_settings,
                                           on_play=self._show_playback)
        self.current_frame.grid(row=0, column=0, sticky="nsew")
    
    def _show_settings(self):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = SettingsFrame(self, self._email, self._profile_name,
                                           on_back=self._show_main_menu,
                                           on_subscription=self._show_subscription,
                                           on_switch_profile=lambda: self._show_profile_selection(on_back=self._show_main_menu),
                                           on_sign_out=self._show_login)
        self.current_frame.grid(row=0, column=0, sticky="nsew")

    def _show_subscription(self):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = SubscriptionFrame(self, self._email, on_back=self._show_main_menu)
        self.current_frame.grid(row=0, column=0, sticky="nsew")
    
    def _show_playback(self, content):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = PlaybackFrame(
            self, content,
            on_back=self._show_main_menu,
        )
        self.current_frame.grid(row=0, column=0, sticky="nsew")
         
    
if __name__ == "__main__":
    app = App()
    app.mainloop()