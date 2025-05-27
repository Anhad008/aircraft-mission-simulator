from configs.aircraft_config import aircraft
from configs.mission_config import mission
from models.mission_simulator import sim_takeoff, sim_climb, sim_cruise, sim_descent, sim_landing
from plots.visualizer import plot_altitude_profile, plot_tas_profile, plot_fuel_profile
from utils.logger import log_to_csv


def main():
    # Setup 
    aircraft1 = aircraft("EmbraerE190")
    mission1 = mission()

    # --- Takeoff ---
    takeoff_time, takeoff_dist, takeoff_vel = sim_takeoff(aircraft1, mission1)
    v_takeoff_final = takeoff_vel[-1]

    # --- Climb ---
    climb_time, climb_altitude, climb_tas_log, climb_fuel_log = sim_climb(aircraft1, mission1, v_takeoff_final)
    climb_time = [t + takeoff_time[-1] for t in climb_time]

    # --- Cruise ---
    initial_fuel_cruise = climb_fuel_log[-1]
    cruise_time, cruise_altitude, cruise_tas_log, cruise_fuel_log = sim_cruise(
        aircraft1, mission1, initial_fuel_cruise
    )
    cruise_time = [t + climb_time[-1] for t in cruise_time]

    # --- Descent ---
    initial_descent_alt = cruise_altitude[-1]  # meters
    initial_fuel_descent = cruise_fuel_log[-1]
    initial_descent_vel = cruise_tas_log[-1]
    descent_time, descent_altitude, descent_tas_log, descent_fuel_log = sim_descent(
        aircraft1, mission1, initial_descent_alt, initial_fuel_descent, initial_descent_vel
    )
    descent_time = [t + cruise_time[-1] for t in descent_time]

    # --- Landing ---
    landing_speed = descent_tas_log[-1]
    initial_fuel_landing = descent_fuel_log[-1]
    landing_time, landing_dist, landing_vel, landing_fuel_log = sim_landing(
        aircraft1, mission1, landing_speed, initial_fuel_landing
    )
    landing_time = [t + descent_time[-1] for t in landing_time]

    # Takeoff & Landing logs
    takeoff_altitude = [climb_altitude[0]] * len(takeoff_time)
    takeoff_fuel = [mission1.initial_fuel + mission1.reserve_fuel] * len(takeoff_time)
    landing_altitude = [descent_altitude[-1]] * len(landing_time)

    total_time = landing_time[-1]
    total_fuel = landing_fuel_log[-1]

    # --- Output Summary ---
    print("\n===== MISSION SUMMARY =====")
    print(f"Takeoff Distance: {takeoff_dist[-1]:.2f} m in {takeoff_time[-1]:.2f} s")
    print(f"Top of Climb: {climb_altitude[-1]:.2f} m in {climb_time[-1]:.1f} s")
    print(f"Cruise Range: {mission1.range / 1000:.1f} km in {cruise_time[-1] - cruise_time[0]:.1f} s")
    print(f"Descent to: {descent_altitude[-1]:.2f} m in {descent_time[-1] - descent_time[0]:.1f} s")
    print(f"Landing Roll Distance: {landing_dist[-1]:.2f} m in {landing_time[-1] - landing_time[0]:.1f} s")
    print(f"Total Mission Time: {total_time:.1f} s")
    print(f"Final Fuel Remaining: {total_fuel:.2f} kg")
    print("===========================\n")


    # Cumulative Logs with phases for plotting
    total_time_log_phases = [takeoff_time , climb_time , cruise_time , descent_time , landing_time]
    total_fuel_log_phases = [takeoff_fuel , climb_fuel_log , cruise_fuel_log , descent_fuel_log , landing_fuel_log]
    total_tas_log_phases = [takeoff_vel , climb_tas_log , cruise_tas_log , descent_tas_log , landing_vel]
    total_altitude_log_phases = [takeoff_altitude , climb_altitude , cruise_altitude , descent_altitude , landing_altitude]

    phase_labels = ["Takeoff", "Climb", "Cruise", "Descent", "Landing"]

    plot_altitude_profile(total_time_log_phases, total_altitude_log_phases, phase_labels)
    plot_tas_profile(total_time_log_phases, total_tas_log_phases, phase_labels)
    plot_fuel_profile(total_time_log_phases, total_fuel_log_phases, phase_labels)

    # Cumulative Logs for data 
    total_time_log = takeoff_time + climb_time + cruise_time + descent_time + landing_time
    total_altitude_log = takeoff_altitude + climb_altitude + cruise_altitude + descent_altitude + landing_altitude
    total_tas_log = takeoff_vel + climb_tas_log + cruise_tas_log + descent_tas_log + landing_vel
    total_fuel_log = takeoff_fuel + climb_fuel_log + cruise_fuel_log + descent_fuel_log + landing_fuel_log

    data_log = list(zip(total_time_log, total_altitude_log, total_tas_log, total_fuel_log))
    headers = ["Time (s)", "Altitude (m)", "TAS (m/s)", "Fuel Remaining (kg)"]
    log_to_csv("output.csv", headers, data_log)
    


if __name__ == "__main__":
    main()
