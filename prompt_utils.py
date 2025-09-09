
# prompt_utils.py
"""
Canada REAL Engine - Complete Prompt & Utility Library
VERSION: 6.0 (Canada-Focused Production Stable)
PURPOSE: This file contains ALL prompts, resource maps, and helper
         functions for the Canada REAL Engine data generation process.
         It does not run any processes by itself.
"""
import datetime
import requests
import json
import os

# --- Helper functions (from your comprehensive version) ---
def word_count(text: str) -> int:
    return len(text.strip().split())

def validate_output(json_obj: dict) -> bool:
    if not isinstance(json_obj, dict): return False
    if not (isinstance(json_obj.get("headline"), str) and (isinstance(json_obj.get("summary"), str) or isinstance(json_obj.get("regional_content"), dict))): return False
    if not (isinstance(json_obj.get("kpis"), list) and len(json_obj.get("kpis", [])) >= 3): return False
    if json_obj.get("topic") in ["canada_immigration"] and json_obj.get("regional_content"):
        regional_content = json_obj.get("regional_content", {})
        required_regions = ["canada", "uk", "europe", "southeast-asia"]
        if not all(region in regional_content for region in required_regions): return False
        for region in required_regions:
            if region in regional_content:
                word_cnt = word_count(regional_content[region])
                if word_cnt < 80 or word_cnt > 120: return False
    relevance = json_obj.get("relevance", {})
    if not (isinstance(relevance, dict) and isinstance(relevance.get("program_suggestions", []), list) and isinstance(relevance.get("target_students", ""), str)): return False
    chart = json_obj.get("chart", {})
    if not (isinstance(chart, dict) and isinstance(chart.get("chart_type", ""), str) and isinstance(chart.get("data_points", []), list)): return False
    return True

# --- BASE PROMPT: For Canada general dashboard topics ---
CANADA_BASE_PROMPT = """
You are Canada REAL Engine Analyst, an expert in Canadian economic and immigration trends.
GOAL
▪ Write data-rich analysis focused on Canada with international comparisons.
▪ Use **trusted Canadian government sources** and official statistics where possible.
▪ **Synthesize findings from at least 2-3 different Canadian sources** for comprehensive analysis.
▪ Frame your response using **Canadian economic indicators** (GDP, employment, immigration targets).
▪ Inject ONE concrete comparison to a previous period (e.g., YoY % change), focusing on Canadian data.
▪ Vary wording every run—use synonyms or shuffle phrases. Avoid acronyms.
▪ Cite Canadian sources like Statistics Canada, IRCC, Bank of Canada, provincial agencies.
KPIS/INFOGRAPHIC CARDS
▪ Extract 3–4 key Canadian numeric metrics (short label/value pairs, e.g., "Canada Job Growth": "+99,300").
RELEVANCE
▪ Output a 'relevance' block detailing practical implications for Canada.
CHART
▪ Design a chart concept based on key Canadian values from your analysis.
LATEST RESOURCES REQUIREMENT:
▪ For the field "latest_resources", ALWAYS return an array of at least 10 highly relevant Canadian and international resources.
▪ Prioritize Canadian government sources, Statistics Canada, provincial agencies, and Canadian institutions.
▪ Include international sources for comparison (OECD, World Bank) but maintain Canada focus.
▪ Always rotate in at least 4 new Canadian sources with established core sources.
▪ Each resource must have a "title", "provider", and a working "url".
STRICT OUTPUT RULE:
Return only a single valid JSON object matching the format below.
JSON OUTPUT FORMAT
{
  "headline": "...",
  "summary": "...",
  "projection": 123.45,
  "kpis": [
    { "label": "Canada Metric Name", "value": "+4.2%" }
  ],
  "relevance": {
    "program_suggestions": ["..."],
    "target_students": "...",
    "country_advantage": "...",
    "policy_alert": "..."
  },
  "chart": {
    "chart_type": "bar",
    "x_axis": "Category",
    "y_axis": "Canadian Values",
    "data_points": [ { "label": "Ontario", "value": 78000 } ]
  },
  "latest_resources": [
    { "title": "...", "provider": "Statistics Canada", "url": "..." }
  ],
  "source": "Statistics Canada, IRCC, Bank of Canada",
  "last_updated": "2025-09-09T13:30:00Z"
}
""".strip()

# --- CANADA IMMIGRATION REGIONAL PROMPT ---
CANADA_IMMIGRATION_PROMPT = """
You are Canada REAL Engine Analyst, an expert in Canadian immigration and global mobility trends.
GOAL
▪ Generate focused Canadian immigration analysis with international comparisons for 4 regions.
▪ Each regional section should be **one cohesive paragraph (80-120 words)** focusing on Canada's position.
▪ Focus on **Canadian immigration policies, Express Entry, PNP, processing times, and targets**.
▪ Use **Canadian government data** from IRCC, provincial nominee programs, and official statistics.
▪ Make Canada section the primary focus with others as comparative context.
REGIONAL CONTENT REQUIREMENTS:
▪ **Canada**: Express Entry draws, Provincial Nominee Programs, permanent resident targets, study permit caps, processing times, recent policy changes. Include specific IRCC numbers.
▪ **United Kingdom**: Compare UK immigration with Canada's advantages - processing times, permanent residency pathways, post-study opportunities.
▪ **Europe**: Compare European immigration with Canada's competitive positioning, bilingual advantage, startup visa programs.
▪ **Southeast Asia**: Canada's relationship with Southeast Asian immigration - source countries, family class, skilled worker programs.
REGIONAL JSON OUTPUT FORMAT:
{
  "headline": "Canada Immigration Outlook: Strategic Reduction & Quality Focus for 2025",
  "regional_content": {
    "canada": "Canada-focused paragraph about immigration policies, Express Entry, PNP, targets with IRCC statistics...",
    "uk": "Comparison paragraph showing Canada's advantages over UK immigration pathways...", 
    "europe": "Comparison paragraph showing Canada's competitive position vs European programs...",
    "southeast-asia": "Canada's relationship with Southeast Asian migration patterns and programs..."
  },
  "kpis": [
    { "label": "2025 PR Target", "value": "395,000" },
    { "label": "Express Entry ITAs", "value": "33,404" },
    { "label": "BC PNP Reduction", "value": "50%" },
    { "label": "Study Permit Cap", "value": "437,000" }
  ],
  "relevance": {
    "program_suggestions": ["Canadian Immigration Law", "Public Policy", "International Business", "Global Affairs"],
    "target_students": "Students seeking Canadian immigration pathways, policy researchers, and international education professionals",
    "country_advantage": "Canada's comprehensive immigration system provides multiple pathways and competitive processing times",
    "policy_alert": "Major Canadian immigration policy shifts in 2025 affecting permanent residency and study permits"
  },
  "chart": {
    "chart_type": "bar",
    "x_axis": "Immigration Class",
    "y_axis": "2025 Targets",
    "data_points": [
      { "label": "Economic Class", "value": 232150 },
      { "label": "Family Class", "value": 94500 },
      { "label": "Refugees", "value": 58350 },
      { "label": "Other", "value": 10000 }
    ]
  },
  "latest_resources": [
    { "title": "IRCC Immigration Levels Plan 2025-2027", "provider": "IRCC", "url": "https://www.canada.ca/en/immigration-refugees-citizenship.html" }
  ],
  "source": "Immigration, Refugees and Citizenship Canada (IRCC)",
  "last_updated": "2025-09-09T13:30:00Z"
}
""".strip()

RESOURCE_MAP = {
    "canada_immigration": [],
    "canada_labour": [],
    "canada_tech_innovation": [],
    "canada_startup_ecosystem": [],
    "canada_regional_development": [],
    "canada_international_education": []
}

def get_prompt_for_topic(topic_id: str) -> str:
    if topic_id == "canada_immigration":
        return CANADA_IMMIGRATION_PROMPT
    return CANADA_BASE_PROMPT  # This covers all other Canada topics

def call_perplexity_api(prompt: str, topic_id: str) -> dict:
    api_key = os.environ.get("PERPLEXITY_API_KEY")
    if not api_key:
        print(f"ERROR: PERPLEXITY_API_KEY not set for Canada {topic_id}.")
        return None

    url = "https://api.perplexity.ai/chat/completions"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    payload = {
        "model": "sonar-pro", 
        "messages": [
            {"role": "system", "content": "You are a Canada REAL Engine analyst. Return only valid JSON focused on Canadian data."}, 
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 2000, 
        "temperature": 0.7
    }

    try:
        print(f"--> Calling Perplexity API for Canada topic: {topic_id}")
        response = requests.post(url, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        content = response.json()["choices"][0]["message"]["content"]
        start_index = content.find('{')
        end_index = content.rfind('}')
        if start_index != -1 and end_index > start_index:
            return json.loads(content[start_index:end_index+1])
        else:
            print(f"ERROR: Could not find valid JSON for Canada {topic_id}.")
            return None
    except Exception as e:
        print(f"API call FAILED for Canada {topic_id}: {e}")
        return None

def create_structured_fallback(topic_id: str) -> dict:
    print(f"--> Creating structured fallback for Canada topic: {topic_id}")
    fallback = {
        "headline": "Canada Data is Currently Being Refreshed", 
        "kpis": [{"label": "Status", "value": "Loading..."}], 
        "relevance": {}, 
        "chart": {"data_points": []}, 
        "source": "Canada REAL Engine", 
        "last_updated": datetime.datetime.now().isoformat(), 
        "topic": topic_id
    }

    if topic_id == "canada_immigration":
        fallback["regional_content"] = {
            "canada": "Loading Canadian immigration data...", 
            "uk": "Loading UK comparison data...", 
            "europe": "Loading European comparison data...", 
            "southeast-asia": "Loading Southeast Asian data..."
        }
    else:
        fallback["summary"] = "The latest Canadian analysis is being generated. Please check back shortly."

    return fallback
