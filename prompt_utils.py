# prompt_utils.py

"""
REAL Engine - Complete Prompt & Utility Library
VERSION: 6.0 (Production Stable)
PURPOSE: This file contains ALL prompts, resource maps, and helper
         functions for the REAL Engine data generation process.
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
    if json_obj.get("topic") in ["immigration", "immigration_research"] and json_obj.get("regional_content"):
        regional_content = json_obj.get("regional_content", {})
        required_regions = ["canada", "uk", "europe", "southeast-asia"]
        if not all(region in regional_content for region in required_regions): return False
        for region in required_regions:
            if region in regional_content:
                word_cnt = word_count(regional_content[region])
                if json_obj.get("topic") == "immigration" and (word_cnt < 80 or word_cnt > 120): return False
                elif json_obj.get("topic") == "immigration_research" and (word_cnt < 90 or word_cnt > 140): return False
    relevance = json_obj.get("relevance", {})
    if not (isinstance(relevance, dict) and isinstance(relevance.get("program_suggestions", []), list) and isinstance(relevance.get("target_students", ""), str)): return False
    chart = json_obj.get("chart", {})
    if not (isinstance(chart, dict) and isinstance(chart.get("chart_type", ""), str) and isinstance(chart.get("data_points", []), list)): return False
    return True

# --- BASE PROMPT: For all general dashboard topics ---
BASE_PROMPT = """
You are REAL Engine Analyst, an expert in global economic and educational trends.
GOAL
▪ Write data-rich analysis based on the supplied topic.
▪ If no numbers are provided, use **trusted inference and global data benchmarks** to generate all numeric values.
▪ **Synthesize findings from at least 2-3 different sources** from the RESOURCE_MAP for a multi-faceted analysis.
▪ Frame your response using **economics-informed reasoning** (e.g., macroeconomic indicators, labor dynamics, capital flows).
▪ Inject ONE concrete comparison to a previous period (e.g., YoY % change), which can be inferred if necessary.
▪ Vary wording every run—use synonyms or shuffle phrases. Avoid acronyms.
▪ Cite each sentence with the appropriate source from the RESOURCE_MAP using inline markdown links, e.g. [OECD](https://www.oecd.org/).
KPIS/INFOGRAPHIC CARDS
▪ Extract 3–4 key numeric metrics (short label/value pairs, e.g., "Job Vacancy Growth": "+4.2%") for sidebar info cards.
RELEVANCE
▪ Output a 'relevance' block detailing practical implications.
CHART
▪ Design a chart concept based on key numeric values from your analysis.
LATEST RESOURCES REQUIREMENT:
▪ For the field "latest_resources", ALWAYS return an array of at least 10 highly relevant, sector-diverse, and up-to-date resources (reports, rankings, courses, data portals, government dashboards, etc.) for the current year.
▪ In every API call, select the most recently published or trending resources available online.
▪ DO NOT simply copy the same 10 from the previous data refresh—always search for new studies, government bulletins, new ranking releases, high-impact sector news, or new open courses.
▪ At least 2-3 items should be from university or academic, 2-3 from public sector/government/NGO, and the rest can be industry or private sector.
▪ Always rotate in at least 4 new links/citations with the established core sources (OECD, WIPO, IRCC, WHO, etc.), keeping the array varied and fresh every time.
▪ Each resource must have a "title", "provider", and a working "url".
STRICT OUTPUT RULE:
Return only a single valid JSON object matching the format below.
Do not include any explanation, commentary, or text before or after the JSON object.  
Any extra words outside the JSON will cause critical application errors.
JSON OUTPUT FORMAT
{
  "headline": "...",
  "summary": "...",
  "projection": 123.45,
  "kpis": [
    { "label": "Job Vacancy Growth", "value": "+4.2%" },
    { "label": "Healthcare Vacancies", "value": "92,000" },
    { "label": "Tech Growth", "value": "+8.1%" }
  ],
  "relevance": {
    "program_suggestions": ["..."],
    "target_students": "...",
    "country_advantage": "...",
    "policy_alert": "..."
  },
  "chart": {
    "chart_type": "bar",
    "x_axis": "Sector",
    "y_axis": "Estimated Vacancies",
    "data_points": [ { "label": "Healthcare", "value": 78000 } ]
  },
  "latest_resources": [
    { "title": "...", "provider": "...", "url": "..." }
    // at least 10, minimum 4 new per run
  ],
  "source": "...",
  "last_updated": "2025-08-07T19:00:00Z"
}
""".strip()

# --- IMMIGRATION PATHWAYS REGIONAL PROMPT ---
IMMIGRATION_PATHWAYS_PROMPT = """
You are REAL Engine Analyst, an expert in global immigration and mobility trends.
GOAL
▪ Generate focused immigration pathway analysis for 4 specific regions with clear policy focus.
▪ Each regional section should be **one cohesive paragraph (80-120 words)** focusing on visa policies and regulatory changes.
▪ Focus on **current policy developments, visa statistics, processing times, and regulatory updates** for each region.
▪ Use **trusted inference and global data benchmarks** to generate specific numeric values.
▪ **Synthesize findings from immigration sources** in the RESOURCE_MAP with proper citations.
▪ Make each paragraph **standalone and policy-focused** for immigration practitioners and students.
LATEST RESOURCES REQUIREMENT:
▪ For the field "latest_resources", ALWAYS return an array of at least 10 highly relevant, sector-diverse, and up-to-date resources for the current year.
▪ In every API call, select the most recently published or trending resources available online.
▪ DO NOT simply copy the same 10 from the previous data refresh—always search for new policy bulletins, agency statistics, new visa/program guides, new academic or advocacy research.
▪ At least 2-3 items should be from academic/university, 2-3 from public sector/government/NGO, the rest industry or independent.
▪ Always rotate in at least 4 new sources with core authorities (IRCC, UK Home Office, OECD, EU Commission, etc.), ensuring the list is fresh and varied.
▪ Each resource must have a "title", "provider", and a working "url".
REGIONAL CONTENT REQUIREMENTS:
▪ **Canada**: Express Entry draws, Provincial Nominee Programs, International Student Program quotas, processing times, policy updates. Include specific numbers (visa quotas, approval rates, waiting periods).
▪ **United Kingdom**: Post-Brexit skilled worker visa statistics, Health and Care Worker visa programs, student visa policy changes, Graduate Route updates. Include concrete statistics and policy timeline updates.
▪ **Europe**: EU Blue Card reforms, Schengen mobility changes, country-specific initiatives (Germany, Netherlands, France), visa processing improvements. Include EU-wide statistics and bilateral agreements.
▪ **Southeast Asia**: Digital nomad visa launches, work visa trends, regional mobility agreements (ASEAN), investment visa programs. Include country-specific data from Thailand, Singapore, Malaysia.
REGIONAL JSON OUTPUT FORMAT:
{
  "headline": "Immigration Pathways: Policy Updates and Visa Trends 2025",
  "regional_content": {
    "canada": "Policy-focused paragraph about Canada immigration pathways with visa statistics and regulatory updates...",
    "uk": "Policy-focused paragraph about UK immigration changes with specific metrics and timeline updates...", 
    "europe": "Policy-focused paragraph about European immigration policies with EU-specific data and reforms...",
    "southeast-asia": "Policy-focused paragraph about Southeast Asian visa programs and regional mobility trends..."
  },
  "kpis": [
    { "label": "Canada Express Entry", "value": "+15.2%" },
    { "label": "UK Skilled Worker Visas", "value": "284,000" },
    { "label": "EU Blue Card Growth", "value": "+22%" },
    { "label": "SEA Digital Nomad Visas", "value": "12 countries" }
  ],
  "relevance": {
    "program_suggestions": ["International Business", "Public Policy", "Immigration Law", "Global Affairs"],
    "target_students": "Students seeking immigration pathways, policy researchers, and international education professionals",
    "country_advantage": "Comprehensive policy intelligence provides strategic advantage for immigration planning and institutional guidance",
    "policy_alert": "Major immigration policy shifts across regions in 2025 affecting visa processing and eligibility requirements"
  },
  "chart": {
    "chart_type": "bar",
    "x_axis": "Region",
    "y_axis": "Visa Approval Growth (%)",
    "data_points": [
      { "label": "Canada", "value": 15.2 },
      { "label": "UK", "value": 8.7 },
      { "label": "Europe", "value": 22.0 },
      { "label": "Southeast Asia", "value": 18.5 }
    ]
  },
  "latest_resources": [
    { "title": "...", "provider": "...", "url": "..." }
    // at least 10, minimum 4 new per run
  ],
  "source": "IRCC, UK Home Office, European Commission, ASEAN Secretariat",
  "last_updated": "2025-08-07T19:00:00Z"
}
""".strip()

# --- IMMIGRATION RESEARCH REGIONAL PROMPT ---
IMMIGRATION_RESEARCH_PROMPT = """
You are REAL Engine Analyst, an expert in immigration behavioral sciences and cultural integration research.
GOAL:
- Generate scientific analysis of cultural integration for 4 regions.
- Each regional section must be one paragraph (90-140 words) focusing on research findings.
- Address mental health support, discrimination research, and cultural integration studies.
- Incorporate research on 'civic sense'—the shared values and community responsibilities that foster social cohesion.
- Use trusted research data from sources like Oxford Migration Institute, Migration Policy Institute, and university research centers.
LATEST RESOURCES REQUIREMENT:
- For the field "latest_resources", ALWAYS return an array of at least 10 current, diverse, and reputable migration/integration/civic sense resources for the current year.
- Always rotate in new academic or policy research, breaking news, new indicators, new courses, and substantial findings from both academic and public sectors, as well as new NGO/advocacy reports.
- Never simply reuse the same exact set in consecutive refreshes.
- Each resource must have a "title", "provider", and a working "url".
REGIONAL CONTENT REQUIREMENTS:
- **Canada**: Focus on integration models, mental health programs (e.g., CAMH), and research on civic sense development and community participation among new residents.
- **United Kingdom**: Focus on NHS migrant mental health services, campus safety programs, community cohesion studies, and civic education initiatives for immigrants.
- **Europe**: Focus on anti-discrimination policies (e.g., IMISCOE), the impact of rising nationalism, and research into civic citizenship and inclusion for migrants.
- **Southeast Asia**: Focus on cultural tension research (e.g., from NUS), community harmony initiatives, and studies on how volunteering and community engagement impact migrant belonging.
REGIONAL JSON OUTPUT FORMAT:
{
  "headline": "Immigration Research: Cultural Integration & Civic Sense",
  "regional_content": {
    "canada": "A research-focused paragraph about cultural integration studies, civic sense, and mental health programs in Canada...",
    "uk": "A research-focused paragraph referencing UK academic studies on behavioral health, community cohesion, and civic education...",
    "europe": "A research-focused paragraph citing European research on anti-discrimination, civic citizenship, and intercultural programs...",
    "southeast-asia": "A research-focused paragraph referencing Southeast Asian academic research on cultural dynamics, community harmony, and civic participation..."
  },
  "kpis": [
    { "label": "Civic Participation Rate", "value": "+12%" },
    { "label": "Integration Success Rate", "value": "78%" },
    { "label": "Mental Health Support Need", "value": "High" }
  ],
  "relevance": {
    "program_suggestions": ["Migration Studies", "Cultural Psychology", "Civic Education Policy"],
    "target_students": "Graduate students in behavioral sciences, mental health professionals, and policy analysts.",
    "country_advantage": "Evidence-based research on civic sense provides a foundation for building more cohesive communities.",
    "policy_alert": "Lack of civic education can be a barrier to long-term migrant integration and well-being."
  },
  "chart": {
    "chart_type": "bar",
    "x_axis": "Region",
    "y_axis": "Reported Sense of Belonging",
    "data_points": [
      { "label": "Canada", "value": 8.1 },
      { "label": "UK", "value": 7.2 },
      { "label": "Europe", "value": 7.5 }
    ]
  },
  "latest_resources": [
    { "title": "...", "provider": "...", "url": "..." }
    // at least 10, minimum 4 new per run
  ],
  "source": "Oxford IMI, Migration Policy Institute, Journal of Ethnic and Migration Studies",
  "last_updated": "2025-08-08T01:00:00Z"
}
""".strip()



RESOURCE_MAP = {
    "labour": [],
    "student_mobility": [],
    "tourism_labour": [],
    "healthcare_mobility": [],
    "immigration": [],
    "immigration_research": [],
    "innovation": []
}



def get_prompt_for_topic(topic_id: str) -> str:
    if topic_id == "immigration":
        return IMMIGRATION_PATHWAYS_PROMPT
    if topic_id == "immigration_research":
        return IMMIGRATION_RESEARCH_PROMPT
    return BASE_PROMPT  # This covers all other topics by default


def call_perplexity_api(prompt: str, topic_id: str) -> dict:
    api_key = os.environ.get("PERPLEXITY_API_KEY")
    if not api_key:
        print(f"ERROR: PERPLEXITY_API_KEY not set for {topic_id}.")
        return None
    url = "https://api.perplexity.ai/chat/completions"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    payload = {
        "model": "sonar-pro", "messages": [{"role": "system", "content": "You are a REAL Engine analyst. Return only valid JSON."}, {"role": "user", "content": prompt}],
        "max_tokens": 2000, "temperature": 0.7
    }
    try:
        print(f"--> Calling Perplexity API for topic: {topic_id}")
        response = requests.post(url, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        content = response.json()["choices"][0]["message"]["content"]
        start_index = content.find('{')
        end_index = content.rfind('}')
        if start_index != -1 and end_index > start_index:
            return json.loads(content[start_index:end_index+1])
        else:
            print(f"ERROR: Could not find valid JSON for {topic_id}.")
            return None
    except Exception as e:
        print(f"API call FAILED for {topic_id}: {e}")
        return None

def create_structured_fallback(topic_id: str) -> dict:
    print(f"--> Creating structured fallback for topic: {topic_id}")
    fallback = {"headline": "Data is Currently Being Refreshed", "kpis": [{"label": "Status", "value": "Loading..."}], "relevance": {}, "chart": {"data_points": []}, "source": "REAL Engine", "last_updated": datetime.datetime.now().isoformat(), "topic": topic_id}
    if topic_id in ["immigration", "immigration_research"]:
        fallback["regional_content"] = {"canada": "Loading...", "uk": "Loading...", "europe": "Loading...", "southeast-asia": "Loading..."}
    else:
        fallback["summary"] = "The latest analysis is being generated. Please check back shortly."
    return fallback
