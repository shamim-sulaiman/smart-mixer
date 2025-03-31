
# Smart Mixing Tank Simulator 🧪

A Python-based simulation of a smart mixing tank with live process control, real-time visualization, and optional PLC integration (mocked or real).

## Features

- ✅ Real-time control using PID
- ✅ Simulates tank volume, salt concentration, and flow
- ✅ Desktop GUI with Tkinter
- ✅ Web interface using Streamlit
- ✅ CSV export and (optional) PNG graph
- ✅ Modular design for future PLC integration (Modbus/OPC UA)
- ✅ Live animated plotting in browser

## Project Structure

```
smart_mixer/
├── simulation/       # Core simulation logic
├── desktop_gui/      # Tkinter-based GUI
├── web_app/          # Streamlit web interface
├── mock_plc/         # (Optional) PLC communication mock/stub
├── README.md
├── .gitignore
└── requirements.txt
```

## Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/shamim-sulaiman/smart-mixer.git
cd smart-mixer
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run desktop GUI

```bash
python desktop_gui/main.py
```

### 4. Run Streamlit app

```bash
streamlit run web_app/web_app.py
```

---
