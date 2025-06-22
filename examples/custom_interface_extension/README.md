# Custom Interface Extension Example

This example demonstrates how to create a custom web interface extension for LEWIS with specialized dashboards and functionality.

## 📁 Structure

```
custom_interface_extension/
├── __init__.py
├── manifest.json
├── extension.py
├── templates/
│   ├── dashboard.html
│   ├── scan_results.html
│   └── threat_map.html
├── static/
│   ├── css/
│   │   └── custom.css
│   └── js/
│       └── dashboard.js
├── api/
│   ├── __init__.py
│   └── routes.py
├── config/
│   └── interface.yaml
└── README.md
```

## 🎯 Features

- Custom security dashboard with real-time metrics
- Interactive threat visualization maps
- Advanced scan result filtering and analysis
- Custom reporting interfaces
- Mobile-responsive design
- Dark/light theme support

## 🚀 Installation

```bash
# Install the extension
lewis extension install examples/custom_interface_extension

# Enable the extension
lewis extension enable custom-interface

# Start with custom interface
lewis dashboard --interface custom --port 8080
```

## 💻 Usage

Access the custom interface at: `http://localhost:8080/custom`

### Available Endpoints

- `/custom/dashboard` - Main security dashboard
- `/custom/scans` - Scan management interface
- `/custom/threats` - Threat visualization map
- `/custom/reports` - Custom reporting interface
- `/custom/api/metrics` - Real-time metrics API

## 🎨 Customization

### Themes
```css
/* static/css/custom.css */
:root {
  --primary-color: #2c3e50;
  --secondary-color: #3498db;
  --success-color: #27ae60;
  --warning-color: #f39c12;
  --danger-color: #e74c3c;
}

.dashboard-widget {
  background: var(--primary-color);
  border-radius: 8px;
  padding: 20px;
  margin: 10px;
}
```

### Custom Components
```javascript
// static/js/dashboard.js
class ThreatMap {
  constructor(containerId) {
    this.container = document.getElementById(containerId);
    this.init();
  }
  
  init() {
    // Initialize interactive threat map
    this.map = new LeafletMap(this.container);
    this.loadThreats();
  }
  
  loadThreats() {
    // Load and display threat data
    fetch('/custom/api/threats')
      .then(response => response.json())
      .then(data => this.renderThreats(data));
  }
}
```

## 📊 Configuration

```yaml
# config/interface.yaml
custom_interface:
  theme: "dark"
  refresh_interval: 5
  max_results_per_page: 50
  charts:
    enabled: true
    animation: true
    real_time: true
  maps:
    provider: "openstreetmap"
    default_zoom: 10
  notifications:
    desktop: true
    sound: false
    severity_threshold: "medium"
```

See the source files for complete implementation details.
