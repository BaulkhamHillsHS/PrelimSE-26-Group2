import customtkinter as ctk
from assets import colours
import csv
import os
import pyotp
import qrcode
from io import BytesIO
from PIL import Image

CSV_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "accounts.csv")

# Google Authenticator (TOTP 2FA)
# Testing flag: set to True to skip Google Authenticator verification entirely
SKIP_2FA = False

# Login screen frame with username/password and CSV authentication
class LoginFrame(ctk.CTkFrame):
    def __init__(self, parent, on_success=None):
        super().__init__(parent)
        
        self.on_success = on_success
        # Store callback function to call on successful login

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._build_branding_panel()
        self._build_login_panel()
    
    def _build_branding_panel(self):
        # Branding panel frame on the left side with logo and app name
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
        # Login form panel on the right side with entries and login button
        login = ctk.CTkFrame(self, fg_color="transparent")
        login.grid(row=0, column=1, sticky="nsew", padx=(10, 20), pady=20)
        login.grid_columnconfigure(0, weight=1)

        heading = ctk.CTkLabel(login, text="Welcome Back",
                               font=("Segoe UI", 32, "bold"), 
                               text_color=colours.TEXT_DARK)
        heading.pack(pady=(80, 15))

        description = ctk.CTkLabel(login, text="Sign in to continue streaming",
                                   font=("Segoe UI", 16), text_color=colours.TEXT_DARK)
        description.pack(pady=(0, 40))

        self.username_entry = ctk.CTkEntry(login, width=350, height=45,
                                           placeholder_text="Email Address",
                                           border_width=0,fg_color=colours.BACKGROUND,
                                           text_color=colours.TEXT_DARK)
        self.username_entry.pack(pady=10)
        self.username_entry.bind("<Return>", lambda e: self.login()) # Allow pressing Enter to trigger login

        self.password_entry = ctk.CTkEntry(login, width=350, height=45,
                                           placeholder_text="Password", show="●",
                                           border_width=0, fg_color=colours.BACKGROUND,
                                           text_color=colours.TEXT_DARK)
        self.password_entry.pack(pady=10)
        self.password_entry.bind("<Return>", lambda e: self.login()) # Allow pressing Enter to trigger login

        # TODO: Implement remember me functionality
        remember_checkbox = ctk.CTkCheckBox(login, text="Remember me", 
                                            text_color=colours.TEXT_DARK,
                                            checkbox_width=20, checkbox_height=20,
                                            fg_color=colours.DARK_ACCENT,
                                            hover_color=colours.ACCENT)
        remember_checkbox.pack(pady=(15, 20))
        
        self.error_label = ctk.CTkLabel(login, text="",
                                        font=("Segoe UI", 13),
                                        text_color=colours.ERROR)
        self.error_label.pack(pady=(0, 5))

        login_button = ctk.CTkButton(login, text="Login", width=350, height=50, 
                                     corner_radius=12, fg_color=colours.DARK_ACCENT,
                                     hover_color=colours.ACCENT, text_color=colours.TEXT_LIGHT,
                                     font=("Segoe UI", 16, "bold"), command=self.login)
        login_button.pack(pady=10)
    
    def _load_user_row(self, email):
        with open(CSV_PATH, newline="") as f:
            for row in csv.DictReader(f):
                if row["email"] == email:
                    return row
        return None
    
    def login(self):
        # Get entered email and password
        email = self.username_entry.get().strip()
        password = self.password_entry.get()

        if not email or not password:
            self.error_label.configure(text="Please enter email and password.")
            return

        row = self._load_user_row(email)
        if row is None or row["password"] != password:
            self.error_label.configure(text="Invalid email or password.")
            return
        self._pending_row = row # Store user data for use during 2FA verification
        
        if SKIP_2FA:
            # Skip 2FA verification so we can test login without needing to set up Google Authenticator
            if self.on_success:
                self.on_success(email)
            return
        
        existing_secret = row.get("totp_secret", "").strip()
        if existing_secret:
            self._pending_secret = existing_secret
            self._is_new_user = False
        else:
            self._pending_secret = pyotp.random_base32() # Generate random secret if user doesn't have one yet
            self._is_new_user = True
        
        self._show_totp_popup()
    
    def _show_totp_popup(self):
        self._totp_popup = ctk.CTkToplevel(self)
        self._totp_popup.title("Two-Factor Authentication")
        self._totp_popup.configure(fg_color=colours.SECONDARY)
        self._totp_popup.resizable(False, False)
        
        popup_width = 420
        popup_height = 460 if self._is_new_user else 280 # If no 2FA set up yet, popup needs to be taller to show QR code and secret
        screen_w = self._totp_popup.winfo_screenwidth()
        screen_h = self._totp_popup.winfo_screenheight()
        x = (screen_w - popup_width) // 2
        y = (screen_h - popup_height) // 2
        self._totp_popup.geometry(f"{popup_width}x{popup_height}+{x}+{y}") # Center the popup on the screen
        
        # Popup must be transient and grab focus so user has to interact with it before returning to main window
        self._totp_popup.transient(self.winfo_toplevel())
        self._totp_popup.grab_set() # Block interaction with main window
        self._totp_popup.focus()
        
        main = ctk.CTkFrame(self._totp_popup, fg_color="transparent")
        main.pack(expand=True, fill="both", padx=30, pady=25)
        main.grid_columnconfigure(0, weight=1)

        heading = ctk.CTkLabel(main, text="Two-Factor Authentication",
                               font=("Segoe UI", 20, "bold"),
                               text_color=colours.TEXT_DARK)
        heading.grid(row=0, column=0, pady=(0, 12))
        
        totp = pyotp.TOTP(self._pending_secret)
        
        if self._is_new_user: # No 2FA set up yet
            uri = totp.provisioning_uri(self._pending_row["email"], issuer_name="StreamCream")
            qr = qrcode.make(uri, box_size=5, border=2).convert("RGB")
            qr_buffer = BytesIO()
            qr.save(qr_buffer, format="PNG")
            qr_buffer.seek(0)
            qr_ctk_image = ctk.CTkImage(Image.open(qr_buffer), size=(140, 140))
            
            instructions = ctk.CTkLabel(main,
                                        text="Scan this QR code with Google Authenticator,\nthen enter the 6-digit code below.",
                                        font=("Segoe UI", 13), text_color=colours.TEXT_DARK,
                                        justify="center")
            instructions.grid(row=1, column=0, pady=(0, 8))
            
            qr_label = ctk.CTkLabel(main, text="")
            qr_label.configure(image=qr_ctk_image, text="")
            qr_label.grid(row=2, column=0, pady=(0, 4))

            secret_label = ctk.CTkLabel(
                main, text=f"Secret: {self._pending_secret}",
                font=("Segoe UI", 11, "bold"), text_color=colours.DARK_ACCENT
            )
            secret_label.grid(row=3, column=0, pady=(0, 8))
            
            entry_row = 4 # Code entry starts at row 4 for new users since we have extra instructions and QR code
        
        else:
            returning_label = ctk.CTkLabel(main, text="Enter the 6-digit code from your authenticator app.",
                                           font=("Segoe UI", 13), text_color=colours.TEXT_DARK, justify="center")
            returning_label.grid(row=1, column=0, pady=(0, 8))
            
            entry_row = 2 # Code entry starts at row 2 for existing users since we only have one instruction label

        entry = ctk.CTkEntry(main, width=200, height=42, placeholder_text="000000", border_width=0,
                             fg_color=colours.BACKGROUND, text_color=colours.TEXT_DARK, font=("Segoe UI", 18, "bold"), 
                             justify="center")
        entry.grid(row=entry_row, column=0, pady=(0, 8))
        
        error_label = ctk.CTkLabel(main, text="", font=("Segoe UI", 13), text_color=colours.ERROR)
        error_label.grid(row=entry_row + 1, column=0, pady=(0, 4))
        
        verify_btn = ctk.CTkButton(main, text="Verify Code", width=200, height=42,
                                   corner_radius=12, fg_color=colours.DARK_ACCENT,
                                   hover_color=colours.ACCENT, text_color=colours.TEXT_LIGHT,
                                   font=("Segoe UI", 14, "bold"), command=lambda: self._verify_totp(entry, error_label))
        verify_btn.grid(row=entry_row + 2, column=0, pady=(0, 4))
        
        entry.bind("<Return>", lambda e: self._verify_totp(entry, error_label))
        entry.focus()
    
    def _verify_totp(self, entry, error_label):
        entered_code = entry.get().strip()
        
        if not entered_code.isdigit() or len(entered_code) != 6:
            error_label.configure(text="Please enter a valid 6-digit code.")
            return
        
        totp = pyotp.TOTP(self._pending_secret)
        
        if totp.verify(entered_code, valid_window=1): # Allow 30s window before or after
            if self._is_new_user:
                self._save_totp_secret(self._pending_row["email"], self._pending_secret)
            self._close_popup()
            if self.on_success:
                self.on_success(self._pending_row["username"])
        else:
            error_label.configure(text="Invalid authenticator code. Try again.")
    
    def _close_popup(self):
        self._totp_popup.grab_release()
        self._totp_popup.destroy()
    
    def _save_totp_secret(self, email, secret):
        rows = []
        with open(CSV_PATH, newline="") as f:
            reader = csv.DictReader(f)
            fieldnames = reader.fieldnames
            for row in reader:
                if row["email"] == email:
                    row["totp_secret"] = secret
                rows.append(row)

        with open(CSV_PATH, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
            