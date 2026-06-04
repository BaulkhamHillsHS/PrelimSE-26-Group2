import customtkinter as ctk
from assets import colours
import csv
import os
# Necessary Imports for the Profile Selection Frame



TIER_PROFILE_LIMITS = {
    "Light Cream": 1,
    "Whipped Cream": 2,
    "Heavy Cream": 4,
}
# Limits for number of profile based on the subscription plan they have

class ProfileSelectionFrame(ctk.CTkFrame):
    
