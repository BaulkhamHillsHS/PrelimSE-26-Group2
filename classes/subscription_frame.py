import customtkinter as ctk
from assets import colours
import csv
import os

CSV_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "accounts.csv")

TIERS = ["Light Cream", "Whipped Cream", "Heavy Cream"]

TIER_INFO = {
    "Light Cream": {"price": "$5.99", "profiles": 1, "quality": "720p"},
    "Whipped Cream": {"price": "$9.99", "profiles": 2, "quality": "1080p"},
    "Heavy Cream": {"price": "$14.99", "profiles": 4, "quality": "4K"},
}

class SubscriptionFrame(ctk.CTkFrame):
    def __init__(self, parent, username):
        super().__init__(parent)
        self.username = username
        self.user_data = self._load_user_data()

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._build_current_plan_panel()
        self._build_plan_selection_panel()
    
    def _load_user_data(self):
        with open(CSV_PATH, newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row["username"] == self.username:
                    return row
        return None
    
    def _save_user_data(self):
        rows = []
        with open(CSV_PATH, newline="") as f:
            reader = csv.DictReader(f)
            fieldnames = reader.fieldnames
            for row in reader:
                if row["username"] == self.username:
                    rows.append(self.user_data)
                else:
                    rows.append(row)
                    
        with open(CSV_PATH, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
    
    def _build_current_plan_panel(self):
        pass
    
    def _build_plan_selection_panel(self):
        pass