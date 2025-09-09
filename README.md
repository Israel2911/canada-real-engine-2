# REAL Engine Automation

This script generates AI-powered insights for:
- Labour Market
- Student Mobility
- Tourism Labour

It outputs a combined JSON (`real-engine-data.json`) that powers your Wix dashboard.

## Run it

```bash
pip install -r requirements.txt
python auto_update_real_engine.py
```

## Deploy to Render

1. Create a Cron Job
2. Connect this repo
3. Command: `python auto_update_real_engine.py`
4. Schedule: `0 */3 * * *` (every 3 hours)
