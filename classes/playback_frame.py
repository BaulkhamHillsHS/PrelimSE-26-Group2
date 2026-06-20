import customtkinter as ctk
from data.content import Content


class PlaybackFrame(ctk.CTkFrame):
    def __init__(self, parent, content, on_back=None):
        super().__init__(parent, fg_color="#000000")
        self._content = content
        self.on_back = on_back

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._build_ui()

    def _build_ui(self):
        ctk.CTkButton(self, text="< Back", width=90, height=32,
                      corner_radius=10, fg_color="#333333",
                      hover_color="#555555", text_color="white",
                      font=("Segoe UI", 12, "bold"),
                      command=self.on_back).place(x=20, y=20)

        center = ctk.CTkFrame(self, fg_color="#000000")
        center.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(center, text=self._content.get_title(),
                     font=("Segoe UI", 40, "bold"),
                     text_color="white").pack(pady=(0, 8))

        ctk.CTkLabel(center,
                     text=self._content.get_type_label(),
                     font=("Segoe UI", 13, "bold"),
                     text_color="white",
                     fg_color="#2d2d2d",
                     corner_radius=6).pack(pady=(0, 15))

        ctk.CTkLabel(center,
                     text=f"{self._content.get_year()}  |  {self._content.get_rating()}/10",
                     font=("Segoe UI", 15),
                     text_color="#999999").pack(pady=(0, 20))

        ctk.CTkLabel(center, text=self._content.get_description(),
                     font=("Segoe UI", 14),
                     text_color="#bbbbbb",
                     wraplength=520, justify="center").pack(pady=(0, 25))

        for line in self._content.get_info_lines():
            ctk.CTkLabel(center, text=line,
                         font=("Segoe UI", 14),
                         text_color="#777777").pack(pady=3)

        ctk.CTkButton(center, text="▶  Play", width=200, height=50,
                      corner_radius=25, fg_color="#e50914",
                      hover_color="#ff0f1f", text_color="white",
                      font=("Segoe UI", 16, "bold")).pack(pady=(35, 0))

