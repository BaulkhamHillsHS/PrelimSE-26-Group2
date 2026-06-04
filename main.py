import customtkinter as ctk
from assets import colours
from classes.login_frame import LoginFrame
from classes.subscription_frame import SubscriptionFrame


class App(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("StreamCream")

        self.configure(fg_color=colours.BACKGROUND)
        self.minsize(800, 600)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        self.current_frame = None
        self._show_login()
        
        self.after(10, lambda: self.state("zoomed"))
    
    def _show_login(self):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = LoginFrame(self, on_success=self._on_login_success)
        self.current_frame.grid(row=0, column=0, sticky="nsew")
    
    def _on_login_success(self, username):
        self.current_frame.destroy()
        self.current_frame = SubscriptionFrame(self, username)
        self.current_frame.grid(row=0, column=0, sticky="nsew")
         
        
if __name__ == "__main__":
    app = App()
    app.mainloop()