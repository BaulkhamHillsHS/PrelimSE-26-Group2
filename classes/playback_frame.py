import customtkinter as ctk
from data.content import Content
from classes.data_control import add_to_watchlist, remove_from_watchlist, is_in_watchlist


class PlaybackFrame(ctk.CTkFrame):
    def __init__(self, parent, content, email, profile_name, on_back=None):
        super().__init__(parent, fg_color="#000000")
        self._content = content
        self._email = email
        self._profile_name = profile_name
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
        
        self._watchlist_btn = ctk.CTkButton(
            center, width=200, height=36,
            corner_radius=18,
            font=("Segoe UI", 13, "bold"),
            command=self._toggle_watchlist,
        )
        self._watchlist_btn.pack(pady=(0, 0))
        self._update_watchlist_button()
    
    def _update_watchlist_button(self):
        if is_in_watchlist(self._email, self._profile_name, self._content):
            self._watchlist_btn.configure(text="- Remove from Watchlist",fg_color="#333333", hover_color="#555555")
        else:
            self._watchlist_btn.configure(text="+ Add to Watchlist",fg_color="#2d6a4f",hover_color="#40916c")
    
    def _toggle_watchlist(self):
        if is_in_watchlist(self._email, self._profile_name, self._content):
            remove_from_watchlist(self._email, self._profile_name, self._content)
        else:
            add_to_watchlist(self._email, self._profile_name, self._content)
        self._update_watchlist_button()
