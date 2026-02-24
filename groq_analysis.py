import json
import os
from pathlib import Path
from groq import Groq 

def load_local_env() -> None:
    env_path = Path(__file__).resolve().parent / ".env"
    if not env_path.exists():
        return 
    
    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key , value = line.split("=",1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key]=value

load_local_env()
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise RuntimeError("Missing GROQ API KEY in environment.")

client = Groq(api_key=api_key)
def analyze_with_groq(data):
    """
    Analyze structured lead response from bolna_summary_transcript.json.
    """

    summary = data["summary"]
    transcript = data["transcript"]

    prompt = f"""
lead name: Ajay

You are an AI Lead Qualification Agent.

Analyze the following structured lead interaction and return ONLY valid JSON with:

- intent_level (low / medium / high)
- budget_fit (low / moderate / high)
- timeline_readiness (immediate / soon / later / unclear)
- followup_ready (true / false)
- faq_engagement_level (low / medium / high)
- overall_interest_score (1 to 10 integer)

Summary:
{summary}

Transcript:
{transcript}

Return ONLY JSON.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )

    raw_output = response.choices[0].message.content.strip()

    if raw_output.startswith("```"):
        raw_output = raw_output.replace("```json", "").replace("```", "").strip()

    try:
        return json.loads(raw_output)
    except json.JSONDecodeError:
        print("Groq returned invalid JSON.")
        print("Raw Output:")
        print(raw_output)
        return None
