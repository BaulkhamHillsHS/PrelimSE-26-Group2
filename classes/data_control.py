import csv
import os

CSV_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "accounts.csv")

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