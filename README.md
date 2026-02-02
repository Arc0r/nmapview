# Nmap Scan Viewer

A Flask web application for visualizing nmap scan results in a user-friendly interface.

## Features

- 📊 **Interactive Dashboard**: View scan statistics and charts at a glance
- 🔎 **Collapsible Hosts**: Expand/collapse IP addresses to see details
- 🔓 **Port Details**: Click on ports to see detailed information and script outputs
- 🎛️ **Advanced Filters**: Fixed filter panel with port state toggles, exclude ports/services, and service-based filtering
- 🔍 **Search & Sort**: Search across hosts/ports and sort by IP, name, or status
- 🎨 **Modern UI**: Beautiful gradient design with smooth animations
- 📱 **Responsive**: Works on desktop and mobile devices

## Installation

1. Install Python dependencies:
Create the python environment and source it.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Make sure your nmap XML file is in the scans directory

```bash
nmap -oX ./scans/output.xml 0.0.0.0/0
```

## Usage

Run the Flask application:
```bash
python app.py
```

Then open your browser and navigate to `http://localhost:5000`

## File Structure

```
.
├── app.py                 # Flask application
├── requirements.txt       # Python dependencies
├── scans/                 # Nmap scan results (XML format)
│   ├── physi_16.xml
│   ├── physi_17.xml
│   ├── physi_18.xml
│   └── physi_19.xml
├── templates/
│   └── index.html         # HTML template with styling and interactivity
├── webview.sh             # Convenience script (if used)
└── README.md              # This file
```

## How to Use

1. **View Hosts**: The main page displays all discovered hosts with their IP addresses and status
2. **Expand Host**: Click on any host row to expand and see open ports
3. **Port Details**: Click on any port to see additional details like service name, state, CPEs, and scripts
4. **Filter**: Use the fixed right-side panel to filter by state, exclude ports/services, or select services
5. **Search & Sort**: Use the top controls to search and sort the host list

## Nmap XML Generation

If you need to generate a new nmap scan file:

```bash
nmap -oX output.xml <target>
```

Replace `<target>` with your target network or IP range.

## Color Legend

- 🟢 **Green**: Host/Port is UP or OPEN
- 🔴 **Red**: Host/Port is DOWN or CLOSED
- 🟡 **Yellow**: Port is FILTERED

## License

MIT License
