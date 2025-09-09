# auto_update_real_engine.py

"""
REAL Engine - Main Data Generation Script
VERSION: 6.0 (Production Stable)
PURPOSE: This is the ONLY script to run to update the dashboard data.
"""

import datetime
import json
import time
import os

# Import ALL the tools we need from our library file
from prompt_utils import call_perplexity_api, get_prompt_for_topic, create_structured_fallback, validate_output

# --- SCRIPT CONFIGURATION ---
RUN_INTERVAL_HOURS = 6
STATE_FILE = "last_run_timestamp.txt"
OUTPUT_JSON_FILE = "real-engine-data.json"

# --- Time-checking functions ---
def should_run_now():
    try:
        with open(STATE_FILE, 'r') as f:
            last_run_str = f.read().strip()
            if not last_run_str: return True
            last_run_time = datetime.datetime.fromisoformat(last_run_str)
            if datetime.datetime.now(datetime.timezone.utc) < last_run_time + datetime.timedelta(hours=RUN_INTERVAL_HOURS):
                print(f"🕒 Skipping run. Last successful run was at {last_run_time.strftime('%Y-%m-%d %H:%M:%S UTC')}.")
                return False
    except FileNotFoundError:
        print("🔍 No previous run data found. Starting initial run.")
        return True
    return True

def record_successful_run():
    with open(STATE_FILE, 'w') as f:
        f.write(datetime.datetime.now(datetime.timezone.utc).isoformat())
    print(f"\n✅ Run complete. Timestamp updated in {STATE_FILE}.")

def generate_dynamic_content_for_topic(topic_id: str) -> dict:
    """Calls the API for the given topic and validates the response structure."""
    api_response = call_perplexity_api(get_prompt_for_topic(topic_id), topic_id)
    if isinstance(api_response, dict):
        api_response['topic'] = topic_id # Add topic for validation
        if validate_output(api_response):
            print(f"✅ Success and validation passed for {topic_id}.")
            api_response["last_updated"] = datetime.datetime.now().isoformat()
            return api_response
        else:
            print(f"❌ API call for {topic_id} succeeded but returned an invalid JSON structure. Using fallback.")
            return create_structured_fallback(topic_id)
    else:
        print(f"❌ API call for {topic_id} failed entirely. Using fallback.")
        return create_structured_fallback(topic_id)

# --- The Main Function ---
def main():
    if not should_run_now():
        return
    print("🚀 Starting data generation cycle (Fully Dynamic Mode)...")
    all_data = {}
    sections = ['labour', 'student_mobility', 'tourism_labour', 'healthcare_mobility', 'housing', 'geopolitics', 'immigration', 'immigration_research', 'innovation']
    
    for index, topic_id in enumerate(sections):
        print(f"\n--- Processing Widget {index + 1}/{len(sections)}: {topic_id} ---")
        all_data[topic_id] = generate_dynamic_content_for_topic(topic_id)
        
        # A 5-second delay is a very safe value to ensure we do not get rate-limited.
        if index < len(sections) - 1:
             print(f"--> API call for {topic_id} processed. Waiting 5 seconds to be safe...")
             time.sleep(5)

    with open(OUTPUT_JSON_FILE, 'w') as f:
        json.dump(all_data, f, indent=2)
    print(f"\n✅ Data generation complete. File saved to '{OUTPUT_JSON_FILE}'.")
    record_successful_run()

if __name__ == "__main__":
    main()
