
from flask import Flask, jsonify, render_template_string
from flask_cors import CORS
import json
import os

app = Flask(__name__)
# Enable Cross-Origin Resource Sharing for all domains
CORS(app)

@app.route("/")
def index():
    """Serve the Canada REAL Engine Dashboard"""
    # Check if we should serve the dashboard or just the health check
    if os.path.exists("real-engine-data.json"):
        return render_canada_dashboard()
    else:
        return "✅ Canada REAL Engine API is live"

def render_canada_dashboard():
    """Render the complete Canada REAL Engine dashboard"""
    html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <title>Canada REAL Engine | Intelligence Dashboard 2025</title>
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <style>
    /* Canada-focused styling with red/white theme */
    body { font-family: Arial, sans-serif; background: #f4f6f8; margin: 0; padding: 20px; color: #333; }
    .container { max-width: 1200px; margin: auto; }
    header { text-align: center; margin-bottom: 40px; }
    header h1 { 
      font-size: 30px; 
      color: #d32f2f; 
      margin: 0;
      border-bottom: 3px solid #d32f2f;
      padding-bottom: 10px;
      display: inline-block;
    }
    header h1::before { content: "🍁 "; }
    .topic-section { 
      background: #fff; 
      padding: 25px; 
      margin-bottom: 30px; 
      border-radius: 10px; 
      box-shadow: 0 4px 12px rgba(0,0,0,0.05);
      border-left: 5px solid #d32f2f;
    }
    .topic-section h2 { 
      font-size: 24px; 
      color: #d32f2f; 
      border-bottom: 2px solid #ffebee; 
      padding-bottom: 10px; 
      margin: 0 0 20px 0; 
    }
    .content-grid { display: grid; grid-template-columns: 2fr 1fr; gap: 30px; }
    .main-text-content .headline { 
      font-size: 20px; 
      font-weight: bold; 
      color: #d32f2f; 
      margin-bottom: 15px; 
    }
    .main-text-content .summary { 
      font-size: 14px; 
      line-height: 1.7; 
      color: #444; 
      margin-bottom: 10px; 
      text-align: justify;
    }
    .main-text-content .last-updated { 
      font-size: 12px; 
      color: #888; 
      margin-top: 12px; 
    }
    .infographic-sidebar { 
      background: #f9fcff; 
      padding: 20px; 
      border-radius: 8px; 
      border: 1px solid #ffcdd2; 
      min-width: 220px; 
    }
    .infographic-sidebar h3 { 
      font-size: 16px; 
      color: #d32f2f; 
      margin-top: 0; 
      margin-bottom: 15px; 
    }
    .kpi-card-container { 
      display: flex; 
      flex-direction: column; 
      gap: 10px; 
      margin-bottom: 20px; 
    }
    .kpi-card { 
      background: #ffebee; 
      border-left: 5px solid #d32f2f; 
      border-radius: 6px; 
      padding: 10px 12px; 
      box-shadow: 0 2px 6px rgba(211,47,47,0.1);
    }
    .kpi-card.negative { 
      border-left-color: #c0392b; 
      background: #fff1f0;
    }
    .kpi-label { 
      font-size: 12px; 
      color: #c62828; 
      margin-bottom: 4px; 
      font-weight: 500;
    }
    .kpi-value { 
      font-size: 19px; 
      font-weight: bold; 
      color: #b71c1c; 
    }
    .chart-container { width: 100%; height: 170px; margin-bottom: 5px; }
    .chart-source { 
      font-size: 11px; 
      color: #888; 
      text-align: right; 
      margin-top: 3px; 
    }
    .regional-sections { margin-top: 10px; }
    .region-section { 
      margin-bottom: 25px; 
      border-left: 4px solid #ddd; 
      padding-left: 15px; 
    }
    .region-section.canada { 
      border-left-color: #d32f2f; 
      background: #fafafa;
      padding: 15px;
      border-radius: 5px;
    }
    .region-section.uk { border-left-color: #1976d2; }
    .region-section.europe { border-left-color: #388e3c; }
    .region-section.southeast-asia { border-left-color: #f57c00; }
    .region-heading { 
      font-size: 16px; 
      font-weight: bold; 
      color: #d32f2f; 
      margin-bottom: 10px; 
      display: flex; 
      align-items: center; 
      gap: 8px; 
    }
    .region-heading .flag-emoji { font-size: 18px; }
    .region-content { 
      font-size: 14px; 
      line-height: 1.6; 
      color: #444; 
      text-align: justify; 
      margin-bottom: 0; 
    }

    @media (max-width: 900px) { 
      .content-grid { grid-template-columns: 1fr; } 
      .infographic-sidebar { margin-top: 25px; } 
    }

    @media (max-width: 600px) {
      .content-grid { grid-template-columns: 1fr !important; gap: 0 !important; }
      .infographic-sidebar { 
        width: 100% !important; 
        min-width: 0 !important; 
        max-width: 100% !important; 
        box-sizing: border-box !important; 
        margin: 0 !important; 
      }
    }
  </style>
</head>
<body>
<div class="container">
<header><h1>Canada REAL Engine | Economic Intelligence Dashboard 2025</h1></header>
<div id="dashboard-container"></div>
</div>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.3/dist/chart.umd.js"></script>
<script>
const chartInstances = {};
const apiUrl = '/data';
const sections = [
  { id: 'canada_immigration', title: '🇨🇦 Canada Immigration Pathways & Trends' },
  { id: 'canada_labour', title: '💼 Canadian Labour Market & Skills Gap' },
  { id: 'canada_tech_innovation', title: '🚀 Canada Digital Economy & AI Strategy' },
  { id: 'canada_startup_ecosystem', title: '🏢 Start-up Visa & Entrepreneur Programs' },
  { id: 'canada_regional_development', title: '📍 Regional Economic Development' },
  { id: 'canada_international_education', title: '🎓 International Education Strategy' }
];

function createDashboardPanels() {
  const container = document.getElementById('dashboard-container');
  if (!container) return;

  container.innerHTML = '';

  sections.forEach(section => {
    if (section.id === 'canada_immigration') {
      container.innerHTML += `
        <section class="topic-section" id="${section.id}-section">
          <h2>${section.title}</h2>
          <div class="content-grid">
            <div class="main-text-content">
              <div class="headline" id="${section.id}-headline">Loading Canadian immigration insights...</div>
              <div class="last-updated" id="${section.id}-last-updated"></div>
              <div class="regional-sections">
                <div class="region-section canada">
                  <div class="region-heading"><span class="flag-emoji">🇨🇦</span> Canada Focus</div>
                  <div class="region-content" id="${section.id}-canada-content">Loading Canada-specific data...</div>
                </div>
                <div class="region-section uk">
                  <div class="region-heading"><span class="flag-emoji">🇬🇧</span> vs. United Kingdom</div>
                  <div class="region-content" id="${section.id}-uk-content">Loading UK comparison...</div>
                </div>
                <div class="region-section europe">
                  <div class="region-heading"><span class="flag-emoji">🇪🇺</span> vs. Europe</div>
                  <div class="region-content" id="${section.id}-europe-content">Loading European comparison...</div>
                </div>
                <div class="region-section southeast-asia">
                  <div class="region-heading"><span class="flag-emoji">🌏</span> Southeast Asia Source</div>
                  <div class="region-content" id="${section.id}-southeast-asia-content">Loading Asian trends...</div>
                </div>
              </div>
            </div>
            <aside class="infographic-sidebar">
              <h3>Key Metrics</h3>
              <div class="kpi-card-container" id="${section.id}-kpi-cards"></div>
              <div class="chart-container"><canvas id="${section.id}-chart"></canvas></div>
              <div class="chart-source" id="${section.id}-chart-source"></div>
            </aside>
          </div>
        </section>
      `;
    } else {
      container.innerHTML += `
        <section class="topic-section" id="${section.id}-section">
          <h2>${section.title}</h2>
          <div class="content-grid">
            <div class="main-text-content">
              <div class="headline" id="${section.id}-headline">Loading...</div>
              <div class="summary" id="${section.id}-summary"></div>
              <div class="last-updated" id="${section.id}-last-updated"></div>
            </div>
            <aside class="infographic-sidebar">
              <h3>Key Metrics</h3>
              <div class="kpi-card-container" id="${section.id}-kpi-cards"></div>
              <div class="chart-container"><canvas id="${section.id}-chart"></canvas></div>
              <div class="chart-source" id="${section.id}-chart-source"></div>
            </aside>
          </div>
        </section>
      `;
    }
  });
}

function isNegativeKPI(value) {
  if (typeof value !== 'string') return false;
  return /^-\d|^-|−|^↓/.test(value.trim());
}

function safeSetContent(elementId, content) {
  const element = document.getElementById(elementId);
  if (element) {
    element.innerHTML = content;
    return true;
  }
  return false;
}

function createChartSafely(id, chartData) {
  if (typeof Chart === 'undefined') {
    setTimeout(() => createChartSafely(id, chartData), 1000);
    return;
  }

  const chartEl = document.getElementById(`${id}-chart`);
  if (!chartEl) return;

  if (chartInstances[id]) {
    chartInstances[id].destroy();
  }

  if (chartData && Array.isArray(chartData.data_points)) {
    const labels = chartData.data_points.map(point => point.label);
    const data = chartData.data_points.map(point => point.value);

    try {
      chartInstances[id] = new Chart(chartEl, {
        type: chartData.chart_type || 'bar',
        data: {
          labels: labels,
          datasets: [{
            data: data,
            backgroundColor: chartData.chart_type === 'doughnut' 
              ? ['#d32f2f', '#c62828', '#b71c1c', '#f44336'] 
              : '#d32f2f',
            borderColor: '#fff',
            borderWidth: chartData.chart_type === 'doughnut' ? 2 : 1
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: { 
            legend: { 
              display: chartData.chart_type === 'doughnut',
              labels: { color: '#d32f2f' }
            } 
          },
          scales: chartData.chart_type === 'doughnut' ? {} : {
            y: { 
              beginAtZero: true, 
              ticks: { color: '#d32f2f' }, 
              grid: { color: '#ffcdd2' } 
            },
            x: { 
              ticks: { color: '#d32f2f' }, 
              grid: { display: false } 
            }
          }
        }
      });
    } catch (error) {
      console.error(`Chart creation failed for ${id}:`, error);
    }
  }
}

function updateImmigrationContent(id, sectionData) {
  if (sectionData.regional_content) {
    const regions = ['canada', 'uk', 'europe', 'southeast-asia'];
    regions.forEach(region => {
      const contentElement = document.getElementById(`${id}-${region}-content`);
      if (contentElement) {
        const content = sectionData.regional_content[region];
        contentElement.innerHTML = content || 'Content not available for this region.';
      }
    });
  }
}

function updateDashboard(data) {
  sections.forEach(section => {
    const id = section.id;
    const sectionData = data[id] || {};

    safeSetContent(`${id}-headline`, sectionData.headline || 'Data Unavailable');

    if (id === 'canada_immigration') {
      safeSetContent(`${id}-last-updated`, sectionData.last_updated ? 
        `Last updated: ${new Date(sectionData.last_updated).toLocaleString()}` : '');
      updateImmigrationContent(id, sectionData);
    } else {
      safeSetContent(`${id}-summary`, sectionData.summary || 'Summary could not be loaded.');
      safeSetContent(`${id}-last-updated`, sectionData.last_updated ? 
        `Last updated: ${new Date(sectionData.last_updated).toLocaleString()}` : '');
    }

    const kpiDiv = document.getElementById(`${id}-kpi-cards`);
    if (kpiDiv && sectionData.kpis) {
      kpiDiv.innerHTML = '';
      sectionData.kpis.forEach(kpi => {
        kpiDiv.innerHTML += `
          <div class="kpi-card${isNegativeKPI(kpi.value) ? ' negative' : ''}">
            <div class="kpi-label">${kpi.label}</div>
            <div class="kpi-value">${kpi.value}</div>
          </div>
        `;
      });
    }

    if (sectionData.chart) {
      createChartSafely(id, sectionData.chart);
    }

    safeSetContent(`${id}-chart-source`, sectionData.source ? `Source: ${sectionData.source}` : '');
  });
}

function loadRealEngineData() {
  fetch(`${apiUrl}?ts=${Date.now()}`)
    .then(response => response.json())
    .then(data => updateDashboard(data))
    .catch(error => {
      console.error('Data loading error:', error);
      // Show error message in dashboard
      const container = document.getElementById('dashboard-container');
      if (container) {
        container.innerHTML = '<div style="text-align:center;padding:50px;color:#d32f2f;"><h2>🍁 Canada REAL Engine</h2><p>Loading Canadian economic intelligence...</p></div>';
      }
    });
}

window.onload = () => {
  createDashboardPanels();
  loadRealEngineData();
};
</script>
</body>
</html>
    """
    return render_template_string(html_template)

@app.route("/data")
def get_data():
    """Serves the latest data from the JSON file."""
    file_path = os.path.abspath("real-engine-data.json")
    print(f"🧾 Serving Canada REAL Engine data from: {file_path}")

    if not os.path.exists(file_path):
        print(f"❌ Error: Canada data file not found at {file_path}")
        return jsonify({"error": "Canada data file not found. The data generation process may not have run yet."}), 404

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return jsonify(data)
    except json.JSONDecodeError:
        print(f"❌ Error: Could not decode JSON from {file_path}. The file may be empty or corrupted.")
        return jsonify({"error": "Failed to read Canada data file. It may be temporarily unavailable."}), 500

if __name__ == "__main__":
    # The application runs on the port provided by the hosting environment (e.g., Render) or defaults to 10000.
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
