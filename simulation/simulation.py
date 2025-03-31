import csv
import os
import io
import time
import matplotlib.pyplot as plt
from matplotlib import cm
import streamlit as st
import pandas as pd
from datetime import datetime
from simple_pid import PID

plt.ion()

def run_simulation(TARGET_CONC, SIM_DURATION, Kp, Ki, Kd,
                   save_folder=None, base_filename="simulation_output",
                   disturbance_time=None, new_salt_conc=None,
                   is_streamlit=False, return_fig=False):

    # Constants
    TANK_VOLUME_MAX = 100.0

    SALT_CONC_IN_DEFAULT = 100.0
    SALT_CONC_IN = SALT_CONC_IN_DEFAULT

    FLOW_OUT = 1.5
    TIME_STEP = 1

    # State variables
    tank_volume = 50.0
    salt_mass = 0.0
    volume_log = []
    conc_log = []
    flow_log = []

    fig, ((ax1), (ax2), (ax3), (ax4)) = plt.subplots(4, 1, figsize=(6, 10))
    line1, = ax1.plot([], [], label='Concentration (g/L)', color='blue')
    line2, = ax2.plot([], [], label='Tank Volume (L)', color='green')
    line3, = ax3.plot([], [], label='Salt Flow (L/min)', color='orange')

    # Set plot properties
    ax1.axhline(y=TARGET_CONC, color='gray', linestyle='--', label='Target')
    ax1.set_ylabel("Conc. (g/L)")
    ax1.set_title("Live Simulation")
    ax1.grid(True)
    ax1.legend()

    ax2.set_ylabel("Volume (L)")
    ax2.grid(True)
    ax2.legend()

    ax3.set_ylabel("Salt Flow (L/min)")
    ax3.set_xlabel("Time (min)")
    ax3.grid(True)
    ax3.legend()

    # Tank (ax4) - starts empty, background as tank outline
    tank_bar = ax4.bar(0.5, 0, width=0.4, color='skyblue')[0]  # Live level
    ax4.set_xticks([])
    ax4.set_title("Tank Level & Saltiness")

    plt.tight_layout()

    # PID controller
    pid = PID(Kp=Kp, Ki=Ki, Kd=Kd, setpoint=TARGET_CONC)
    pid.output_limits = (0.0, 1.0)

    print("Time | Volume | Salt | Conc | Salt Flow")
    if is_streamlit:
        plot_placeholder = st.empty()

    for t in range(0, SIM_DURATION + 1, TIME_STEP):
        # 💥 Disturbance trigger
        if disturbance_time is not None and t == disturbance_time:
            SALT_CONC_IN = new_salt_conc or SALT_CONC_IN_DEFAULT
            print(f"⚠️ Disturbance triggered at {t} min → SALT_CONC_IN changed to {SALT_CONC_IN} g/L")

        current_conc = salt_mass / tank_volume

        error = TARGET_CONC - current_conc
        if abs(error) < 0.2:
            FLOW_SALT = 0.0
        elif current_conc > TARGET_CONC + 0.2:
            FLOW_SALT = 0.0
        else:
            FLOW_SALT = pid(current_conc)

        FLOW_WATER = max(0.0, FLOW_OUT - FLOW_SALT)
        inflow = FLOW_WATER + FLOW_SALT
        salt_in = FLOW_SALT * SALT_CONC_IN
        salt_out = FLOW_OUT * current_conc

        salt_mass += salt_in - salt_out
        salt_mass = max(0, salt_mass)

        tank_volume += inflow - FLOW_OUT
        tank_volume = max(0.01, min(tank_volume, TANK_VOLUME_MAX))

        current_conc = salt_mass / tank_volume
        volume_log.append((t, tank_volume))
        conc_log.append((t, current_conc))
        flow_log.append((t, FLOW_SALT))

        # Unpack data
        time_vals = [x[0] for x in volume_log]
        volume_vals = [x[1] for x in volume_log]
        conc_vals = [x[1] for x in conc_log]
        flow_vals = [x[1] for x in flow_log]

        # Update plot data
        line1.set_data(time_vals, conc_vals)
        line2.set_data(time_vals, volume_vals)
        line3.set_data(time_vals, flow_vals)

        # Update tank animation (fill height = volume, color = saltiness)
        tank_bar.set_height(tank_volume)

        # Normalize color: 0 = blue (fresh), high = darker blue/purple
        norm_conc = min(current_conc / TARGET_CONC, 1.5)  # Normalize to 1.5x target
        color = cm.viridis(norm_conc)
        tank_bar.set_color(color)

        # Update axes limits
        ax1.set_xlim(0, max(1, t))
        ax1.set_ylim(0, max(TARGET_CONC + 10, max(conc_vals)))
        ax2.set_xlim(0, max(1, t))
        ax2.set_ylim(0, TANK_VOLUME_MAX + 10)
        ax3.set_xlim(0, max(1, t))
        ax3.set_ylim(0, 1.1)
        ax4.set_xlim(0, 1)
        ax4.set_ylim(0, TANK_VOLUME_MAX)

        if is_streamlit:

            fig, axs = plt.subplots(4, 1, figsize=(6, 10))
            ax1, ax2, ax3, ax4 = axs

            ax1.plot(time_vals, conc_vals, label='Concentration (g/L)', color='blue')
            ax1.axhline(y=TARGET_CONC, color='gray', linestyle='--')
            ax1.set_ylabel("Conc. (g/L)")
            ax1.set_ylim(0, TARGET_CONC + 10)
            ax1.grid(True)
            ax1.set_title("Live Simulation")
            ax1.legend()

            ax2.plot(time_vals, volume_vals, label='Tank Volume (L)', color='green')
            ax2.set_ylabel("Volume (L)")
            ax2.set_ylim(0, TANK_VOLUME_MAX + 10)
            ax2.grid(True)
            ax2.set_title("Tank Volume Over Time")
            ax2.legend()
            
            ax3.plot(time_vals, flow_vals, label='Salt Flow (L/min)', color='orange')
            ax3.set_ylabel("Salt In (L/min)")
            ax3.set_ylim(0, 1.1)
            ax3.set_xlabel("Time (min)")
            ax3.grid(True)
            ax3.set_title("Salt Flow Rate")
            ax3.legend()

            norm_conc = min(current_conc / TARGET_CONC, 1.5)
            color = cm.viridis(norm_conc)
            ax4.bar(0.5, tank_volume, width=0.4, color=color)
            ax4.set_xlim(0, 1)
            ax4.set_ylim(0, TANK_VOLUME_MAX)
            ax4.set_title(f"Tank Level: {tank_volume:.1f} L | Conc: {current_conc:.1f} g/L")
            ax4.set_xticks([])

            fig.tight_layout()
            plot_placeholder.pyplot(fig)
            plt.close(fig)
            time.sleep(0.05)
        else:
            plt.pause(0.01)

        print(f"{t:4d} | {tank_volume:7.2f} | {salt_mass:6.2f} | {current_conc:6.2f} | {FLOW_SALT:6.2f}")

    plt.ioff()
    
    if not is_streamlit:
        plt.show()

    if not is_streamlit:
        # --- Export to CSV with timestamp ---
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        final_filename = f"{base_filename}_{timestamp}.csv"
        filepath = os.path.join(save_folder or os.getcwd(), final_filename)

        with open(filepath, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Time (min)", "Tank Volume (L)", "Salt Mass (g)", "Concentration (g/L)", "Salt Flow (L/min)"])

            for i in range(len(volume_log)):
                t = volume_log[i][0]
                vol = volume_log[i][1]
                conc = conc_log[i][1]
                salt = conc * vol
                flow = flow_log[i][1]
                writer.writerow([t, vol, salt, conc, flow])

        print(f"\n✅ Simulation results saved to: {filepath}\n")

    # Plotting
    time_vals = [t for t, _ in volume_log]
    volume = [v for _, v in volume_log]
    concentration = [c for _, c in conc_log]
    salt_flow = [f for _, f in flow_log]

    plt.figure(figsize=(10, 8))

    plt.subplot(3, 1, 1)
    plt.plot(time_vals, concentration, label='Concentration (g/L)', color='blue')
    plt.axhline(y=TARGET_CONC, color='gray', linestyle='--', label='Target')
    plt.ylabel("Conc. (g/L)")
    plt.title("Tank Simulation")
    plt.grid(True)
    plt.legend()

    plt.subplot(3, 1, 2)
    plt.plot(time_vals, volume, label='Tank Volume (L)', color='green')
    plt.ylabel("Volume (L)")
    plt.grid(True)
    plt.legend()

    plt.subplot(3, 1, 3)
    plt.plot(time_vals, salt_flow, label='Salt Flow (L/min)', color='orange')
    plt.ylabel("Salt In (L/min)")
    plt.xlabel("Time (min)")
    plt.grid(True)
    plt.legend()

    plt.tight_layout()

    if is_streamlit:
        df = pd.DataFrame({
            "Time (min)": [t for t, _ in volume_log],
            "Tank Volume (L)": [v for _, v in volume_log],
            "Salt Mass (g)": [c * v for (_, v), (_, c) in zip(volume_log, conc_log)],
            "Concentration (g/L)": [c for _, c in conc_log],
            "Salt Flow (L/min)": [f for _, f in flow_log],
        })

        csv_buffer = io.StringIO()
        df.to_csv(csv_buffer, index=False)

        # ✅ Skip final figure return to avoid duplicate plot
        return None, csv_buffer.getvalue()

# --- Save plot as PNG ---
    # Always prepare filename
    image_filename = final_filename.replace(".csv", ".png")
    image_filepath = os.path.join(save_folder or os.getcwd(), image_filename)

    if not is_streamlit:
        # Only save and show if running in desktop mode
        plt.savefig(image_filepath, dpi=300)
        print(f"🖼️  Plot image saved to: {image_filepath}")
        plt.show()
    else:
        return plt.gcf()



