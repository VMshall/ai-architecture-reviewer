import os
import re
import json
import anthropic

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))


def review_architecture(design_doc: str, system_type: str, scale_requirements: str) -> dict:
    prompt = f"""You are a principal engineer reviewing a system architecture design.

System type: {system_type}
Scale requirements: {scale_requirements}

Design document:
{design_doc[:8000]}

Respond ONLY with valid JSON:
{{
  "overall_score": integer 1-10,
  "summary": "string — 2-3 sentence executive summary",
  "strengths": ["string — specific architectural strengths"],
  "concerns": [
    {{
      "severity": "critical|major|minor",
      "issue": "string — specific architectural problem",
      "impact": "string — what goes wrong at scale or under failure",
      "recommendation": "string — concrete fix"
    }}
  ],
  "scalability_analysis": "string — 2-3 sentences on horizontal/vertical scaling limits",
  "reliability_analysis": "string — 2-3 sentences on failure modes and resilience",
  "security_notes": ["string — security concerns to address"],
  "alternative_approaches": [
    {{"approach": "string", "tradeoffs": "string"}}
  ],
  "questions_to_consider": ["string — important design questions not addressed in the doc"]
}}

Apply CAP theorem, 12-factor principles, failure mode analysis, and production readiness standards."""

    response = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=2500,
        messages=[{"role": "user", "content": prompt}],
    )
    raw = response.content[0].text.strip()
    raw = re.sub(r"^```[a-z]*\n?", "", raw)
    raw = re.sub(r"\n?```$", "", raw)
    return json.loads(raw)
