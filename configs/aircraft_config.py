import pandas as pd
import os

class aircraft:
    def __init__(self , name):
        self.name = name

        # Load CSV
        csv_path = os.path.join(os.path.dirname(__file__), "../data/aircraft_profiles.csv")
        df = pd.read_csv(csv_path)

        # Match the profile
        profile = df[df["name"] == name]
        if profile.empty:
            raise ValueError(f"Aircraft profile '{name}' not found in aircraft_profiles.csv")

        # Extract values
        row = profile.iloc[0]

        # Assign parameters
        self.max_takeoff_Mass = row["max_takeoff_Mass"]
        self.empty_Mass = row["empty_Mass"]
        self.fuel_capacity = row["fuel_capacity"]
        self.wing_area = row["wing_area"]
        self.aspect_ratio = row["aspect_ratio"]
        self.height_com = row["height_com"]
        self.cdo = row["cdo"]
        self.clto = row["clto"]
        self.oswald_eff = row["oswald_eff"]
        self.engine_thrust = row["engine_thrust"]
        self.sfc = row["sfc"]
