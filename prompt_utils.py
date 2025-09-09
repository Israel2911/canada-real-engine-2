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

# -------- SECTION-SPECIFIC PROMPTS --------

CANADA_LABOUR_PROMPT = """
You are Canada REAL Engine Analyst, an expert in Canadian labour market trends.
GOAL
▪ Write a data-rich analysis of Canada’s labour market in 2025, using latest public and academic resources.
▪ Cover national and sectoral job creation, unemployment trends, tech skills gap, workforce demographics, and wage growth.
▪ Synthesize findings from at least three credible sources (Statistics Canada, Actalent, Job Bank, OECD, etc.).
▪ ALWAYS cite statistics, policy updates, or workforce news with inline markdown links to the RESOURCE_MAP.
▪ Inject concrete historical comparison (e.g., YoY job growth, current vs previous quarter).
▪ At least two Canadian government/official sources and one international comparison required.
KPIS/INFOGRAPHIC CARDS
▪ Extract 3–4 key numeric indicators (e.g., “Q2 Job Growth: +99,300”, “Tech Unemployment: 3.3%”, “Wage Growth: +3.4% YoY”).
CHART
▪ Design a chart with major sectors (tech, health, education, manufacturing), statistical breakdowns.
RESOURCES
▪ "latest_resources" must list at least 10 credible, rotating, sector-diverse items: 3+ Canadian gov/stat, 2 academic, 2 industry. Always rotate at least 4 each run.
STRICT OUTPUT RULE: Only output the requested JSON, nothing more.
"""

CANADA_TECH_PROMPT = """
You are Canada REAL Engine Analyst in the digital, technology, and AI sector.
GOAL
▪ Analyze growth, innovation, AI adoption, tech investment, and digital job market in Canada's 2025 digital economy.
▪ Compare Ontario, Quebec, BC, Alberta; mention AI, cyber, and digital skills.
▪ ALWAYS cite tech salary growth, market size (CAGR), regional breakdown, and significant policy news. Synthesize at least two government/industry and one academic source.
KPIS/INFOGRAPHIC CARDS: digital market size, AI investment, regional shares, CAGR.
CHART: Provincial/sector bar/doughnut.
RESOURCES: At least 10, with government, tech councils, and academic/industry mix.
STRICT OUTPUT RULE: Output JSON object only.
"""

CANADA_STARTUP_PROMPT = """
You are Canada REAL Engine Analyst for entrepreneurship and start-up immigration.
GOAL
▪ Profile Canada's start-up ecosystem, Start-up Visa, entrepreneur migration, sector distribution, and federal/provincial innovation.
▪ Include Tech Network priorities, application caps, PR, and work permit news.
▪ Synthesize insights from IRCC, Global Affairs, regional startup hubs, and innovation clusters.
KPIS: SUV PRs, annual caps, sector split, work permit changes.
CHART: Startup sector chart.
RESOURCES: 10+ links; rotate government, council, academic, sector reports.
STRICT OUTPUT RULE: Output JSON object only.
"""

CANADA_REGIONAL_PROMPT = """
You are Canada REAL Engine Analyst focused on regional economic development.
GOAL
▪ Discuss 2025 economic trends in Prairies, Atlantic, Ontario, Quebec, BC, with investment, sector, and trade contrast.
▪ Use quarterly growth figures and cite Bank of Canada, StatsCan, TD Economics, and regional policy authorities.
KPIS, CHART, RESOURCES: As above, require 2+ Canadian government/financial, 1+ academic, all credible and varied.
STRICT OUTPUT RULE: Output JSON object only.
"""

CANADA_EDUCATION_PROMPT = """
You are Canada REAL Engine Analyst for international education and student mobility.
GOAL
▪ Summarize recent study permit caps, PGWP updates, major program focus (STEM, healthcare), and effects on provincial allocations.
▪ Synthesize from IRCC, CBIE, MEQ, and leading academic or news analysis.
KPIS, CHART, RESOURCES: Require 10+ credible, fresh links; 3+ government/statistical, 2+ academic, rotate 4+ sources per run.
STRICT OUTPUT RULE: Output JSON object only.
"""

CANADA_IMMIGRATION_PROMPT = """
You are Canada REAL Engine Analyst, specializing in immigration and global mobility.
GOAL
▪ Generate focused Canadian immigration policy summary and international comparison, with 4 regional sections.
▪ For each region (Canada, UK, Europe, Southeast Asia), present a policy-focused (80-120 word) paragraph with detailed visa strategy, numbers, and recent regulatory news.
▪ Use IRCC, UK Home Office, EU, and ASEAN sources as required. Cite all data points.
KPIS, CHART, RESOURCES: As above; 10+ links, rotating government, academic, statistical sector, and policy reports.
STRICT OUTPUT RULE: Output JSON object only.
"""

CANADA_BASE_PROMPT = """
You are Canada REAL Engine Analyst, expert in Canadian economic policy.
GOAL
▪ Write data-rich, multi-source analysis focused on your topic with at least one major source-cited comparison to previous years/trends.
▪ Leverage Canadian and global resources with clear citation and numeric rigor. Use at least three citations and a "latest_resources" section with 10+ diverse, fresh sources.
▪ Output JSON object only (no comments or extra text).
"""

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
    if topic_id == "canada_labour":
        return CANADA_LABOUR_PROMPT
    if topic_id == "canada_tech_innovation":
        return CANADA_TECH_PROMPT
    if topic_id == "canada_startup_ecosystem":
        return CANADA_STARTUP_PROMPT
    if topic_id == "canada_regional_development":
        return CANADA_REGIONAL_PROMPT
    if topic_id == "canada_international_education":
        return CANADA_EDUCATION_PROMPT
    return CANADA_BASE_PROMPT

def call_perplexity_api(prompt: str, topic_id: str) -> dict:
    api_key = os.environ.get("PERPLEXITY_API_KEY")
    if not api_key:
        print(f"ERROR: PERPLEXITY_API_KEY not set for {topic_id}.")
        return None
    url = "https://api.perplexity.ai/chat/completions"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    payload = {
        "model": "sonar-pro",
        "messages": [
            {"role": "system", "content": "You are a Canada REAL Engine analyst. Only output valid strict JSON; no comments or extra text."},
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
