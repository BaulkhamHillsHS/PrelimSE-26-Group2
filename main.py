import customtkinter as ctk
from assets import colours
from classes.login_frame import LoginFrame

class App(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("StreamCream")
        self.state("zoomed")

        self.configure(fg_color=colours.BACKGROUND)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        login_frame = LoginFrame(self)
        login_frame.grid(row=0, column=0, sticky="nsew")

if __name__ == "__main__":
    app = App()
    app.mainloop()