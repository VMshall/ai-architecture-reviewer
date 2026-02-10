# ai-architecture-reviewer

AI architecture reviewer — expert feedback on system design with severity-ranked concerns and scalability analysis

## Setup
```bash
cp .env.example .env  # add ANTHROPIC_API_KEY
pip install -r requirements.txt
uvicorn src.api:app --reload
```
