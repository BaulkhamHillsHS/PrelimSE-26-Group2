import customtkinter as ctk
from assets import colours
from classes.data_control import load_user_data, save_user_data, TIER_INFO, TIERS

class SubscriptionFrame(ctk.CTkFrame):
    def __init__(self, parent, email):
        super().__init__(parent)
        self.email = email
        self.user_data = load_user_data(self.email)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._build_current_plan_panel()
        self._build_plan_selection_panel()
    
    def _build_current_plan_panel(self):
        # Panel (left) to show the user's current subscription details
        panel = ctk.CTkFrame(self, fg_color=colours.SECONDARY, corner_radius=20)
        panel.grid(row=0, column=0, sticky="nsew", padx=(20, 10), pady=20)
        panel.grid_columnconfigure(0, weight=1)

        inner = ctk.CTkFrame(panel, fg_color="transparent")
        inner.place(relx=0.5, rely=0.5, anchor="center")
        inner.grid_columnconfigure(0, weight=1)

        header = ctk.CTkLabel(inner, text="Your Plan",
                              font=("Segoe UI", 28, "bold"),
                              text_color=colours.TEXT_DARK)
        header.grid(row=0, column=0, pady=(0, 25))

        tier_label = ctk.CTkLabel(inner, text=self.user_data["tier"],
                                  font=("Segoe UI", 36, "bold"),
                                  text_color=colours.TEXT_DARK)
        tier_label.grid(row=1, column=0, pady=(0, 10))

        divider = ctk.CTkFrame(inner, height=2, fg_color=colours.DARK_ACCENT)
        divider.grid(row=2, column=0, sticky="ew", padx=40, pady=10)
        
        # Display other subscription details (profiles, payment method, email)
        details = [
            f"Profiles: {self.user_data['profiles']}",
            f"Payment: {self.user_data['payment']}",
            f"Email: {self.user_data['email']}",
        ]
        for i, detail in enumerate(details):
            lbl = ctk.CTkLabel(inner, text=detail,
                               font=("Segoe UI", 16),
                               text_color=colours.TEXT_DARK)
            lbl.grid(row=3 + i, column=0, pady=4)
    
    def _build_plan_selection_panel(self):
        # Panel (right) to show the available subscription plans (plan cards) and allows the user to select a new one
        panel = ctk.CTkFrame(self, fg_color=colours.PRIMARY, corner_radius=20)
        panel.grid(row=0, column=1, sticky="nsew", padx=(10, 20), pady=20)
        panel.grid_columnconfigure((0, 1, 2), weight=1)
        panel.grid_rowconfigure(0, weight=0)
        panel.grid_rowconfigure(1, weight=1)

        header = ctk.CTkLabel(panel, text="Available Plans",
                              font=("Segoe UI", 28, "bold"),
                              text_color=colours.TEXT_DARK)
        header.grid(row=0, column=0, columnspan=3, pady=(20, 30))

        # Create a card for each subscription tier
        for i, tier in enumerate(TIERS):
            self._build_plan_card(panel, tier, i + 1)
    
    def _build_plan_card(self, parent, tier, col):
        # Helper function to create a subscription plan card with the given tier and place it in the given column
        info = TIER_INFO[tier]
        current_tier = self.user_data["tier"]

        card = ctk.CTkFrame(parent, fg_color=colours.SECONDARY, corner_radius=20)
        card.grid(row=1, column=col - 1, sticky="nsew", padx=10, pady=(0, 20))
        card.grid_columnconfigure(0, weight=1)
        card.grid_rowconfigure(0, weight=1)

        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.grid(row=0, column=0, padx=25, pady=30)
        inner.grid_columnconfigure(0, weight=1)

        name = ctk.CTkLabel(inner, text=tier,
                            font=("Segoe UI", 24, "bold"),
                            text_color=colours.TEXT_DARK)
        name.pack(pady=(10, 5))

        price = ctk.CTkLabel(inner, text=info["price"] + "/mo",
                             font=("Segoe UI", 18),
                             text_color=colours.TEXT_DARK)
        price.pack(pady=(0, 15))
        
        quality = ctk.CTkLabel(inner, text=info["quality"],
                               font=("Segoe UI", 14),
                               text_color=colours.TEXT_DARK)
        quality.pack(pady=(0, 15))
        
        if tier == current_tier:
            btn = ctk.CTkButton(inner, text="Current Plan",
                                state="disabled",
                                fg_color=colours.DARK_ACCENT,
                                font=("Segoe UI", 14, "bold"))
            btn.pack(pady=(10, 0))
        else:
            current_idx = TIERS.index(current_tier)
            target_idx = TIERS.index(tier)
            if target_idx > current_idx:
                text = "Upgrade"
                color = colours.ACCENT
            else:
                text = "Downgrade"
                color = colours.DARK_ACCENT

            btn = ctk.CTkButton(inner, text=text,
                                fg_color=color,
                                font=("Segoe UI", 14, "bold"),
                                command=lambda t=tier: self._show_payment_popup(t))
            btn.pack(pady=(10, 0))
    
    def _show_payment_popup(self, new_tier):
        info = TIER_INFO[new_tier]

        # Make payment confirmation popup
        popup = ctk.CTkToplevel(self)
        popup.title("Confirm Payment")
        popup.configure(fg_color=colours.SECONDARY)
        popup.resizable(False, False)
        
        # Center the popup on the screen and make it modal
        popup_width = 400
        popup_height = 320
        screen_w = popup.winfo_screenwidth()
        screen_h = popup.winfo_screenheight()
        popup.geometry(f"{popup_width}x{popup_height}+{(screen_w - popup_width)//2}+{(screen_h - popup_height)//2}")
        popup.transient(self.winfo_toplevel())
        popup.grab_set()
        popup.focus()
        
        main = ctk.CTkFrame(popup, fg_color="transparent")
        main.pack(expand=True, fill="both", padx=30, pady=25)
        main.grid_columnconfigure(0, weight=1)
        
        # TODO: Add more details to the payment popup
        
        pay_btn = ctk.CTkButton(main, text=f"Pay {info['price']}",
                                width=200, height=42,
                                corner_radius=12, fg_color=colours.DARK_ACCENT,
                                hover_color=colours.ACCENT, text_color=colours.TEXT_LIGHT,
                                font=("Segoe UI", 14, "bold"),
                                command=lambda: self._process_payment(popup, new_tier))
        pay_btn.grid(row=0, column=0, pady=(0, 4))
    
    def _process_payment(self, popup, new_tier):        
        self.after(2000, lambda: self._payment_complete(popup, new_tier)) # Simulate payment processing delay
        
    def _payment_complete(self, popup, new_tier):
        self.user_data["tier"] = new_tier
        self.user_data["profiles"] = str(TIER_INFO[new_tier]["profiles"])
        save_user_data(self.user_data)
        popup.destroy()
        for widget in self.winfo_children():
            widget.destroy()
        self._build_current_plan_panel()
        self._build_plan_selection_panel()