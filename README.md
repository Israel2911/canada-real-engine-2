
# Canada REAL Engine Automation

🍁 **Canada-focused version of REAL Engine generating AI-powered Canadian economic intelligence**

This script generates AI-powered insights for:
- 🇨🇦 **Canada Immigration Pathways & Trends**
- 💼 **Canadian Labour Market & Skills Gap** 
- 🚀 **Canada Digital Economy & AI Strategy**
- 🏢 **Start-up Visa & Entrepreneur Programs**
- 📍 **Regional Economic Development**
- 🎓 **International Education Strategy**

It outputs a combined JSON (`real-engine-data.json`) that powers your Canada dashboard.

## Run it
```bash
pip install -r requirements.txt
python auto_update_real_engine.py
```

## Deploy to Render
1. Create a Web Service (not Cron Job)
2. Connect this repo
3. **Build Command**: `pip install -r requirements.txt`
4. **Start Command**: `python app.py`
5. Environment Variable: `PERPLEXITY_API_KEY=your_key_here`

## Access Your Dashboard
- **Dashboard**: `https://your-service.onrender.com/`
- **API**: `https://your-service.onrender.com/data`

## Key Features
- ✅ **Canada-focused content** with international comparisons
- ✅ **Real-time data** from Canadian government sources
- ✅ **Interactive charts** with Chart.js visualizations
- ✅ **Red/white Canadian theme** with maple leaf branding
- ✅ **Mobile responsive** design
- ✅ **API compatibility** for external integrations

## Data Sources
- Immigration, Refugees and Citizenship Canada (IRCC)
- Statistics Canada
- Bank of Canada
- Provincial Economic Development Agencies
- Canadian Bureau for International Education

---
**Built for Canadian Economic Intelligence** 🍁
