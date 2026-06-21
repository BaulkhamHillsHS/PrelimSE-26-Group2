import csv
import os
from data.content import CATEGORIES

CSV_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "accounts.csv")
PROFILES_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "profiles.csv")
WATCHLIST_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "watchlist.csv")

WATCHLIST_FIELDNAMES = ["email", "profile_name", "title", "type_label", "year"]

TIERS = ["Light Cream", "Whipped Cream", "Heavy Cream"]

TIER_INFO = {
    "Light Cream": {"price": "$5.99", "profiles": 1, "quality": "720p"},
    "Whipped Cream": {"price": "$9.99", "profiles": 2, "quality": "1080p"},
    "Heavy Cream": {"price": "$14.99", "profiles": 4, "quality": "4K"},
}

TIER_PROFILE_LIMITS = {
    "Light Cream": 1,
    "Whipped Cream": 2,
    "Heavy Cream": 4,
}

def load_user_data(email):
    with open(CSV_PATH, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["email"] == email:
                return row
    return None
    
def save_user_data(user_data):
    rows = []
    with open(CSV_PATH, newline="") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        for row in reader:
            if row["email"] == user_data["email"]:
                rows.append(user_data)
            else:
                rows.append(row)
                
    with open(CSV_PATH, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

def save_totp_secret(email, secret):
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

def load_profiles(email):
    profiles = []
    with open(PROFILES_PATH, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["email"] == email:
                profiles.append(row["profile_name"])
    return profiles

def add_profile(email, profile_name):
    with open(PROFILES_PATH, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([email, profile_name])

def is_in_watchlist(email, profile_name, content):
    with open(WATCHLIST_PATH, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if (row["email"] == email
                    and row["profile_name"] == profile_name
                    and row["title"] == content.get_title()
                    and row["type_label"] == content.get_type_label()
                    and row["year"] == str(content.get_year())):
                return True
    return False
        
def add_to_watchlist(email, profile_name, content):
    if is_in_watchlist(email, profile_name, content):
        return
    with open(WATCHLIST_PATH, "a", newline="") as f:
        reader = csv.DictReader(f)
        writer = csv.DictWriter(f, fieldnames=WATCHLIST_FIELDNAMES)
        writer.writerow({
            "email": email,
            "profile_name": profile_name,
            "title": content.get_title(),
            "type_label": content.get_type_label(),
            "year": content.get_year(),
        })

def remove_from_watchlist(email, profile_name, content):
    rows = []
    with open(WATCHLIST_PATH, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if not (row["email"] == email
                    and row["profile_name"] == profile_name
                    and row["title"] == content.get_title()
                    and row["type_label"] == content.get_type_label()
                    and row["year"] == str(content.get_year())):
                rows.append(row)
    with open(WATCHLIST_PATH, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=WATCHLIST_FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)
        