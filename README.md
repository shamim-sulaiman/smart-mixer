
## Smart Mixing Tank Simulator (a PID simulator)

A Python-based simulation of a smart mixing tank with live process control, real-time visualization, and optional PLC integration (mocked or real).

### Features

- Real-time control using PID
- Simulates tank volume, salt concentration, and flow
- Desktop GUI with Tkinter
- Web interface using Streamlit
- CSV export and (optional) PNG graph
- Modular design for future PLC integration (Modbus/OPC UA)
- Live animated plotting in browser

### Project Structure

```
smart_mixer/
├── simulation/       # Core simulation logic
├── desktop_gui/      # Tkinter-based GUI
├── web_app/          # Streamlit web interface
├── README.md
├── .gitignore
└── requirements.txt
```

### How To Use

You can use the [web-based dashboard here](https://smart-mixer.streamlit.app/) or you can run locally by following steps below;

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
