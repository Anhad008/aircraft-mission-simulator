import matplotlib.pyplot as plt


def plot_segmented_metric(time_log, metric_log, phase_labels, ylabel, title):
    """
    Generic function to plot a segmented flight metric across all phases.
    time_log: List of time arrays per phase
    metric_log: List of metric arrays per phase (e.g., altitude, fuel, tas)
    phase_labels: List of phase names for the legend
    """

    plt.style.use('seaborn-v0_8-whitegrid')  # Cleaner than default or 'ggplot'

    plt.rcParams.update({
        'font.size': 12,
        'font.family': 'serif',  # or 'sans-serif'
        'axes.titlesize': 14,
        'axes.labelsize': 13,
        'legend.fontsize': 11
    })

    plt.figure(figsize=(12, 6))
    for i in range(len(time_log)):
        t = time_log[i]
        y = metric_log[i]
        label = phase_labels[i]
        if len(t) == len(y):
            plt.plot(t, y, label=label)
    plt.xlabel("Time (s)")
    plt.ylabel(ylabel)
    plt.title(title)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def plot_altitude_profile(time_log, altitude_log, phase_labels):
    """
    Plots altitude (m) vs time for each phase.
    """
    plot_segmented_metric(time_log, altitude_log, phase_labels, "Altitude (ft)", "Altitude vs Time")

def plot_tas_profile(time_log, tas_log, phase_labels):
    """
    Plots True Airspeed (m/s) vs time for each phase.
    """
    plot_segmented_metric(time_log, tas_log, phase_labels, "True Airspeed (m/s)", "TAS vs Time")

def plot_fuel_profile(time_log, fuel_log, phase_labels):
    """
    Plots Fuel Remaining (kg) vs time for each phase.
    """
    plot_segmented_metric(time_log, fuel_log, phase_labels, "Fuel Remaining (kg)", "Fuel vs Time")
