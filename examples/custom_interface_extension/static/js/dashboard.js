/**
 * LEWIS Custom Dashboard JavaScript
 * Real-time dashboard functionality with WebSocket integration
 */

class LewisCustomDashboard {
    constructor(config) {
        this.config = config;
        this.socket = null;
        this.refreshInterval = null;
        this.isConnected = false;
        this.currentTheme = config.theme || 'dark';
        
        this.init();
    }
    
    init() {
        this.setupWebSocket();
        this.setupEventListeners();
        this.initializeComponents();
        this.startAutoRefresh();
    }
    
    setupWebSocket() {
        this.socket = io(this.config.socketUrl);
        
        this.socket.on('connect', () => {
            console.log('Connected to LEWIS custom interface');
            this.isConnected = true;
            this.updateConnectionStatus(true);
            this.requestInitialData();
        });
        
        this.socket.on('disconnect', () => {
            console.log('Disconnected from LEWIS custom interface');
            this.isConnected = false;
            this.updateConnectionStatus(false);
        });
        
        this.socket.on('metrics_update', (data) => {
            this.updateMetrics(data);
        });
        
        this.socket.on('scan_started', (data) => {
            this.handleScanStarted(data);
        });
        
        this.socket.on('scan_progress', (data) => {
            this.handleScanProgress(data);
        });
        
        this.socket.on('threat_alert', (data) => {
            this.handleThreatAlert(data);
        });
    }
    
    setupEventListeners() {
        // Theme toggle
        document.getElementById('theme-toggle').addEventListener('click', () => {
            this.toggleTheme();
        });
        
        // Refresh toggle
        document.getElementById('refresh-toggle').addEventListener('click', () => {
            this.toggleAutoRefresh();
        });
        
        // Window resize handler
        window.addEventListener('resize', () => {
            this.handleResize();
        });
    }
    
    initializeComponents() {
        this.initializeNetworkChart();
        this.initializeThreatMap();
        this.loadInitialData();
    }
    
    requestInitialData() {
        if (this.socket && this.isConnected) {
            this.socket.emit('request_metrics');
        }
    }
    
    updateConnectionStatus(connected) {
        const statusIndicator = document.getElementById('connection-status');
        if (statusIndicator) {
            statusIndicator.textContent = connected ? '🟢' : '🔴';
            statusIndicator.title = connected ? 'Connected' : 'Disconnected';
        }
    }
    
    updateMetrics(data) {
        // Update overview metrics
        this.updateElement('active-scans', data.active_scans);
        this.updateElement('threats-detected', data.threats_detected);
        this.updateElement('critical-alerts', data.critical_alerts);
        this.updateElement('system-health', `${data.system_health}%`);
        
        // Update resource usage
        this.updateProgressBar('cpu-progress', 'cpu-value', data.cpu_usage);
        this.updateProgressBar('memory-progress', 'memory-value', data.memory_usage);
        
        // Update network chart
        if (data.network_activity) {
            this.updateNetworkChart(data.network_activity);
        }
        
        // Update recent activities
        if (data.recent_activities) {
            this.updateRecentActivities(data.recent_activities);
        }
    }
    
    updateElement(id, value) {
        const element = document.getElementById(id);
        if (element) {
            element.textContent = value;
        }
    }
    
    updateProgressBar(progressId, valueId, percentage) {
        const progressBar = document.getElementById(progressId);
        const valueElement = document.getElementById(valueId);
        
        if (progressBar) {
            progressBar.style.width = `${percentage}%`;
        }
        
        if (valueElement) {
            valueElement.textContent = `${percentage}%`;
        }
    }
    
    initializeNetworkChart() {
        const chartContainer = document.getElementById('network-chart');
        if (!chartContainer) return;
        
        const data = [{
            x: [],
            y: [],
            name: 'Inbound',
            type: 'scatter',
            mode: 'lines+markers',
            line: { color: '#3498db' }
        }, {
            x: [],
            y: [],
            name: 'Outbound',
            type: 'scatter',
            mode: 'lines+markers',
            line: { color: '#e74c3c' }
        }];
        
        const layout = {
            title: 'Network Traffic',
            xaxis: { title: 'Time' },
            yaxis: { title: 'Bandwidth (Mbps)' },
            paper_bgcolor: 'rgba(0,0,0,0)',
            plot_bgcolor: 'rgba(0,0,0,0)',
            font: { color: this.currentTheme === 'dark' ? '#ecf0f1' : '#212529' }
        };
        
        Plotly.newPlot('network-chart', data, layout, { responsive: true });
    }
    
    updateNetworkChart(networkData) {
        const currentTime = new Date().toLocaleTimeString();
        
        Plotly.extendTraces('network-chart', {
            x: [[currentTime], [currentTime]],
            y: [[networkData.inbound], [networkData.outbound]]
        }, [0, 1]);
    }
    
    initializeThreatMap() {
        const canvas = document.getElementById('threat-map');
        if (!canvas) return;
        
        const ctx = canvas.getContext('2d');
        ctx.fillStyle = this.currentTheme === 'dark' ? '#34495e' : '#f8f9fa';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        
        // Draw world map outline (simplified)
        ctx.strokeStyle = this.currentTheme === 'dark' ? '#ecf0f1' : '#212529';
        ctx.lineWidth = 2;
        ctx.strokeRect(50, 50, 300, 200);
        
        // Add threat indicators
        this.drawThreatIndicators(ctx);
    }
    
    drawThreatIndicators(ctx) {
        const threats = [
            { x: 100, y: 100, severity: 'high' },
            { x: 200, y: 150, severity: 'critical' },
            { x: 300, y: 120, severity: 'medium' }
        ];
        
        threats.forEach(threat => {
            const color = this.getThreatColor(threat.severity);
            ctx.fillStyle = color;
            ctx.beginPath();
            ctx.arc(threat.x, threat.y, 8, 0, 2 * Math.PI);
            ctx.fill();
        });
    }
    
    getThreatColor(severity) {
        const colors = {
            'critical': '#e74c3c',
            'high': '#f39c12',
            'medium': '#3498db',
            'low': '#27ae60'
        };
        return colors[severity] || '#95a5a6';
    }
    
    updateRecentActivities(activities) {
        const activityList = document.getElementById('activity-list');
        if (!activityList) return;
        
        activityList.innerHTML = '';
        
        activities.forEach(activity => {
            const activityElement = this.createActivityElement(activity);
            activityList.appendChild(activityElement);
        });
    }
    
    createActivityElement(activity) {
        const activityItem = document.createElement('div');
        activityItem.className = 'activity-item';
        
        const icon = document.createElement('div');
        icon.className = `activity-icon ${activity.type}`;
        icon.textContent = this.getActivityIcon(activity.type);
        
        const content = document.createElement('div');
        content.className = 'activity-content';
        
        const title = document.createElement('div');
        title.className = 'activity-title';
        title.textContent = this.getActivityTitle(activity);
        
        const details = document.createElement('div');
        details.className = 'activity-details';
        details.textContent = this.getActivityDetails(activity);
        
        content.appendChild(title);
        content.appendChild(details);
        
        const time = document.createElement('div');
        time.className = 'activity-time';
        time.textContent = this.formatTime(activity.timestamp);
        
        activityItem.appendChild(icon);
        activityItem.appendChild(content);
        activityItem.appendChild(time);
        
        return activityItem;
    }
    
    getActivityIcon(type) {
        const icons = {
            'scan_completed': '🔍',
            'threat_detected': '⚠️',
            'scan_started': '🚀',
            'vulnerability_found': '🔓',
            'system_update': '🔄'
        };
        return icons[type] || '📋';
    }
    
    getActivityTitle(activity) {
        const titles = {
            'scan_completed': 'Scan Completed',
            'threat_detected': 'Threat Detected',
            'scan_started': 'Scan Started',
            'vulnerability_found': 'Vulnerability Found',
            'system_update': 'System Update'
        };
        return titles[activity.type] || 'Activity';
    }
    
    getActivityDetails(activity) {
        switch (activity.type) {
            case 'scan_completed':
                return `Target: ${activity.target}`;
            case 'threat_detected':
                return `Source: ${activity.source} - Severity: ${activity.severity}`;
            case 'scan_started':
                return `Target: ${activity.target}`;
            default:
                return activity.description || 'No details available';
        }
    }
    
    formatTime(timestamp) {
        return new Date(timestamp).toLocaleTimeString();
    }
    
    toggleTheme() {
        this.currentTheme = this.currentTheme === 'dark' ? 'light' : 'dark';
        document.documentElement.setAttribute('data-theme', this.currentTheme);
        
        // Update charts with new theme
        this.updateChartsTheme();
    }
    
    updateChartsTheme() {
        const color = this.currentTheme === 'dark' ? '#ecf0f1' : '#212529';
        
        Plotly.relayout('network-chart', {
            'font.color': color,
            'paper_bgcolor': 'rgba(0,0,0,0)',
            'plot_bgcolor': 'rgba(0,0,0,0)'
        });
        
        // Redraw threat map with new theme
        this.initializeThreatMap();
    }
    
    startAutoRefresh() {
        this.refreshInterval = setInterval(() => {
            if (this.socket && this.isConnected) {
                this.socket.emit('request_metrics');
            }
        }, this.config.refreshInterval * 1000);
    }
    
    toggleAutoRefresh() {
        const button = document.getElementById('refresh-toggle');
        if (this.refreshInterval) {
            clearInterval(this.refreshInterval);
            this.refreshInterval = null;
            button.textContent = '▶️';
            button.title = 'Start auto-refresh';
        } else {
            this.startAutoRefresh();
            button.textContent = '⏸️';
            button.title = 'Pause auto-refresh';
        }
    }
    
    loadInitialData() {
        // Load initial dashboard data
        fetch('/custom/api/metrics')
            .then(response => response.json())
            .then(data => this.updateMetrics(data))
            .catch(error => console.error('Failed to load initial data:', error));
    }
    
    handleScanStarted(data) {
        this.showNotification(`Scan started on ${data.target}`, 'info');
    }
    
    handleScanProgress(data) {
        // Update scan progress in UI
        console.log(`Scan progress: ${data.progress}% for ${data.target}`);
    }
    
    handleThreatAlert(data) {
        this.showNotification(`Threat detected: ${data.description}`, 'warning');
    }
    
    showNotification(message, type = 'info') {
        // Create and show notification
        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        notification.textContent = message;
        
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.remove();
        }, 5000);
    }
    
    handleResize() {
        // Handle responsive layout changes
        Plotly.Plots.resize('network-chart');
    }
}

/**
 * Scan Results Manager
 * Handles scan results interface functionality
 */
class ScanResultsManager {
    constructor(config) {
        this.config = config;
        this.currentPage = 1;
        this.totalPages = 1;
        this.resultsPerPage = config.resultsPerPage || 25;
        this.currentFilters = {};
        this.selectedResults = new Set();
        
        this.init();
    }
    
    init() {
        this.setupEventListeners();
        this.loadResults();
        if (this.config.autoRefresh) {
            this.startAutoRefresh();
        }
    }
    
    setupEventListeners() {
        // Filter event listeners
        document.getElementById('scan-type').addEventListener('change', () => this.applyFilters());
        document.getElementById('severity').addEventListener('change', () => this.applyFilters());
        document.getElementById('date-range').addEventListener('change', () => this.applyFilters());
        document.getElementById('search-box').addEventListener('input', () => this.applyFilters());
        
        // Control event listeners
        document.getElementById('select-all').addEventListener('click', () => this.toggleSelectAll());
        document.getElementById('export-selected').addEventListener('click', () => this.exportSelected());
        document.getElementById('remediate-selected').addEventListener('click', () => this.remediateSelected());
        
        // Pagination
        document.getElementById('prev-page').addEventListener('click', () => this.previousPage());
        document.getElementById('next-page').addEventListener('click', () => this.nextPage());
        
        // Table sorting
        document.querySelectorAll('.sortable').forEach(header => {
            header.addEventListener('click', (e) => this.sortBy(e.target.dataset.sort));
        });
        
        // Modal handlers
        document.querySelector('.modal-close').addEventListener('click', () => this.closeModal());
        document.getElementById('modal-close-btn').addEventListener('click', () => this.closeModal());
    }
    
    async loadResults() {
        try {
            const params = new URLSearchParams({
                page: this.currentPage,
                per_page: this.resultsPerPage,
                ...this.currentFilters
            });
            
            const response = await fetch(`/custom/api/scan-results?${params}`);
            const data = await response.json();
            
            this.renderResults(data.results);
            this.updatePagination(data.pagination);
            this.updateSummary(data.summary);
            
        } catch (error) {
            console.error('Error loading scan results:', error);
        }
    }
    
    renderResults(results) {
        const tbody = document.getElementById('results-tbody');
        tbody.innerHTML = '';
        
        results.forEach(result => {
            const row = this.createResultRow(result);
            tbody.appendChild(row);
        });
    }
    
    createResultRow(result) {
        const row = document.createElement('tr');
        row.className = `result-row severity-${result.severity}`;
        row.innerHTML = `
            <td><input type="checkbox" value="${result.id}" class="result-checkbox"></td>
            <td>${this.formatDate(result.timestamp)}</td>
            <td>${result.target}</td>
            <td><span class="scan-type-badge">${result.scan_type}</span></td>
            <td><span class="severity-badge ${result.severity}">${result.severity}</span></td>
            <td class="finding-cell">${this.truncate(result.finding, 50)}</td>
            <td><span class="status-badge ${result.status}">${result.status}</span></td>
            <td>
                <button class="btn-action" onclick="scanResults.viewDetails('${result.id}')">👁️</button>
                <button class="btn-action" onclick="scanResults.exportResult('${result.id}')">📊</button>
                <button class="btn-action" onclick="scanResults.remediate('${result.id}')">🛠️</button>
            </td>
        `;
        
        return row;
    }
    
    applyFilters() {
        this.currentFilters = {
            scan_type: document.getElementById('scan-type').value,
            severity: document.getElementById('severity').value,
            date_range: document.getElementById('date-range').value,
            search: document.getElementById('search-box').value
        };
        
        this.currentPage = 1;
        this.loadResults();
    }
    
    startAutoRefresh() {
        setInterval(() => {
            this.loadResults();
        }, this.config.refreshInterval * 1000);
    }
    
    formatDate(timestamp) {
        return new Date(timestamp).toLocaleString();
    }
    
    truncate(text, length) {
        return text.length > length ? text.substring(0, length) + '...' : text;
    }
}

/**
 * Threat Map Manager
 * Handles interactive threat map functionality
 */
class ThreatMapManager {
    constructor(config) {
        this.config = config;
        this.map = null;
        this.threatLayers = {};
        this.heatMapLayer = null;
        this.clusterGroup = null;
        this.markers = [];
        this.isHeatMapMode = false;
        this.isClusterMode = true;
        
        this.init();
    }
    
    init() {
        this.initializeMap();
        this.setupEventListeners();
        this.loadThreats();
    }
    
    initializeMap() {
        // Initialize Leaflet map
        this.map = L.map('threat-map').setView([39.8283, -98.5795], this.config.defaultZoom);
        
        // Add tile layer
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '© OpenStreetMap contributors',
            maxZoom: this.config.maxZoom
        }).addTo(this.map);
        
        // Initialize cluster group
        this.clusterGroup = L.markerClusterGroup({
            maxClusterRadius: 50,
            spiderfyOnMaxZoom: true,
            showCoverageOnHover: false
        });
        
        this.map.addLayer(this.clusterGroup);
    }
    
    setupEventListeners() {
        // Map controls
        document.getElementById('threat-type').addEventListener('change', () => this.filterThreats());
        document.getElementById('time-range').addEventListener('change', () => this.filterThreats());
        document.getElementById('severity-filter').addEventListener('change', () => this.filterThreats());
        
        // Toggle controls
        document.getElementById('heat-map-toggle').addEventListener('click', () => this.toggleHeatMap());
        document.getElementById('cluster-toggle').addEventListener('click', () => this.toggleClustering());
        document.getElementById('export-map').addEventListener('click', () => this.exportMap());
        
        // Stats panel
        document.getElementById('toggle-stats').addEventListener('click', () => this.toggleStatsPanel());
        
        // Theme toggle
        document.getElementById('theme-toggle').addEventListener('click', () => this.toggleTheme());
        
        // Fullscreen
        document.getElementById('fullscreen').addEventListener('click', () => this.toggleFullscreen());
    }
    
    async loadThreats() {
        try {
            const params = new URLSearchParams({
                threat_type: document.getElementById('threat-type').value,
                time_range: document.getElementById('time-range').value,
                min_severity: document.getElementById('severity-filter').value
            });
            
            const response = await fetch(`/custom/api/threats?${params}`);
            const data = await response.json();
            
            this.renderThreats(data.threats);
            this.updateStats(data.stats);
            
        } catch (error) {
            console.error('Error loading threats:', error);
        }
    }
    
    renderThreats(threats) {
        // Clear existing markers
        this.clusterGroup.clearLayers();
        this.markers = [];
        
        threats.forEach(threat => {
            const marker = this.createThreatMarker(threat);
            this.markers.push(marker);
            this.clusterGroup.addLayer(marker);
        });
        
        if (this.isHeatMapMode) {
            this.updateHeatMap();
        }
    }
    
    createThreatMarker(threat) {
        const icon = this.getThreatIcon(threat.severity, threat.type);
        const marker = L.marker([threat.latitude, threat.longitude], { icon });
        
        marker.bindPopup(this.createPopupContent(threat));
        marker.on('click', () => this.showThreatDetails(threat));
        
        return marker;
    }
    
    getThreatIcon(severity, type) {
        const colors = {
            critical: '#dc3545',
            high: '#fd7e14',
            medium: '#ffc107',
            low: '#28a745',
            info: '#17a2b8'
        };
        
        return L.divIcon({
            className: `threat-marker ${severity}`,
            html: `<div style="background-color: ${colors[severity]}; width: 20px; height: 20px; border-radius: 50%; border: 2px solid white;"></div>`,
            iconSize: [20, 20],
            iconAnchor: [10, 10]
        });
    }
    
    createPopupContent(threat) {
        return `
            <div class="threat-popup">
                <h4>${threat.type}</h4>
                <p><strong>Severity:</strong> <span class="severity-${threat.severity}">${threat.severity}</span></p>
                <p><strong>Source:</strong> ${threat.source_ip}</p>
                <p><strong>Time:</strong> ${new Date(threat.timestamp).toLocaleString()}</p>
                <button onclick="threatMap.showThreatDetails('${threat.id}')">View Details</button>
            </div>
        `;
    }
    
    toggleHeatMap() {
        this.isHeatMapMode = !this.isHeatMapMode;
        
        if (this.isHeatMapMode) {
            this.updateHeatMap();
            document.getElementById('heat-map-toggle').classList.add('active');
        } else {
            if (this.heatMapLayer) {
                this.map.removeLayer(this.heatMapLayer);
            }
            document.getElementById('heat-map-toggle').classList.remove('active');
        }
    }
    
    updateHeatMap() {
        if (this.heatMapLayer) {
            this.map.removeLayer(this.heatMapLayer);
        }
        
        const heatData = this.markers.map(marker => {
            const latLng = marker.getLatLng();
            return [latLng.lat, latLng.lng, 1]; // intensity can be based on threat severity
        });
        
        this.heatMapLayer = L.heatLayer(heatData, {
            radius: this.config.heatMapRadius,
            blur: this.config.heatMapBlur,
            maxZoom: 17
        }).addTo(this.map);
    }
    
    filterThreats() {
        this.loadThreats();
    }
    
    startRealTimeUpdates() {
        if (this.config.autoRefresh) {
            setInterval(() => {
                this.loadThreats();
            }, this.config.refreshInterval * 1000);
        }
    }
    
    showThreatDetails(threatId) {
        // Show threat details in modal
        fetch(`/custom/api/threats/${threatId}`)
            .then(response => response.json())
            .then(threat => {
                document.getElementById('threat-modal-title').textContent = `${threat.type} - ${threat.severity}`;
                document.getElementById('threat-modal-body').innerHTML = this.formatThreatDetails(threat);
                document.getElementById('threat-modal').style.display = 'block';
            })
            .catch(error => console.error('Error loading threat details:', error));
    }
    
    formatThreatDetails(threat) {
        return `
            <div class="threat-details">
                <div class="detail-group">
                    <label>Threat Type:</label>
                    <span>${threat.type}</span>
                </div>
                <div class="detail-group">
                    <label>Severity:</label>
                    <span class="severity-${threat.severity}">${threat.severity}</span>
                </div>
                <div class="detail-group">
                    <label>Source IP:</label>
                    <span>${threat.source_ip}</span>
                </div>
                <div class="detail-group">
                    <label>Target:</label>
                    <span>${threat.target}</span>
                </div>
                <div class="detail-group">
                    <label>Description:</label>
                    <span>${threat.description}</span>
                </div>
                <div class="detail-group">
                    <label>First Seen:</label>
                    <span>${new Date(threat.first_seen).toLocaleString()}</span>
                </div>
                <div class="detail-group">
                    <label>Last Seen:</label>
                    <span>${new Date(threat.last_seen).toLocaleString()}</span>
                </div>
                <div class="detail-group">
                    <label>Count:</label>
                    <span>${threat.count}</span>
                </div>
            </div>
        `;
    }
}

// Global functions for button actions
function startQuickScan() {
    const target = prompt('Enter target IP or hostname:');
    if (target && window.dashboard.socket) {
        window.dashboard.socket.emit('start_scan', {
            target: target,
            scan_type: 'quick'
        });
    }
}

function viewReports() {
    window.location.href = '/custom/reports';
}

function emergencyStop() {
    if (confirm('Are you sure you want to stop all active scans?')) {
        if (window.dashboard.socket) {
            window.dashboard.socket.emit('emergency_stop');
        }
    }
}

function exportData() {
    window.open('/custom/api/export', '_blank');
}

// Initialize dashboard when DOM is loaded
function initializeDashboard(config) {
    document.addEventListener('DOMContentLoaded', () => {
        window.dashboard = new LewisCustomDashboard(config);
    });
}

// Export for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = LewisCustomDashboard;
}
