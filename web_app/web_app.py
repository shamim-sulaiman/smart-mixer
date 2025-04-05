import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import streamlit as st
from simulation.simulation import run_simulation

st.set_page_config(page_title="Smart Mixing Tank Simulator", layout="centered")

st.title("🧪 Smart Mixing Tank Simulator")
with st.expander("📘 About this simulator", expanded=True):
    st.markdown("""
    This app simulates a continuously stirred tank mixer where **water and salt** are combined, and the goal is to maintain a **target salt concentration**.

    **Key features:**
    - 💧 Water and salt inflow are controlled via a **PID controller**
    - ⚙️ The system simulates **mass balance** in real time
    - 📊 Outputs include **tank volume**, **salt flow**, and **concentration**
    - 💥 Optional disturbances simulate real-world process variability
    - 🧠 Ideal for control logic testing, tuning, and process engineering education

    Built with `Python`, `Streamlit`, `matplotlib`, and `simple-pid`.


    © 2025 Shamim Sulaiman · MIT License · Built with Streamlit
    """)
    
st.sidebar.header("Simulation Settings")

# Input widgets
target_conc = st.sidebar.number_input("🎯 Target Concentration (g/L)", 1.0, 50.0, 10.0)
duration = st.sidebar.slider("⏱️ Duration (min)", 1, 120, 60)
kp = st.sidebar.number_input("Kp", 0.0, 1.0, 0.05)
ki = st.sidebar.number_input("Ki", 0.0, 1.0, 0.005)
kd = st.sidebar.number_input("Kd", 0.0, 1.0, 0.01)

st.sidebar.markdown("---")

disturb_time = st.sidebar.slider("💥 Disturbance Time (min)", 0, duration, 30)
new_salt_conc = st.sidebar.number_input("New Salt Conc. After Disturbance (g/L)", 0.0, 100.0, 20.0)

# Run button
if st.button("🚀 Run Simulation"):
    with st.spinner("Running simulation..."):
        fig, csv_data = run_simulation(
            TARGET_CONC=target_conc,
            SIM_DURATION=duration,
            Kp=kp, Ki=ki, Kd=kd,
            disturbance_time=disturb_time,
            new_salt_conc=new_salt_conc,
            is_streamlit=True,
            return_fig=True
        )
    if fig:
        st.pyplot(fig)

    # CSV Download
    if csv_data:
        st.download_button(
            "⬇️ Download CSV",
            csv_data,
            file_name="simulation_output.csv",
            mime="text/csv"
        )




