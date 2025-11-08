
# AI Workflows

Collection of AI-powered automation workflows.

## Scripts

### Buildium Bank Transaction Processor (`buildium_stagehand.py`)

Automates processing of bank transactions in Buildium using BrowserBase and Stagehand:
- Logs into Buildium with MFA/OTP support
- Finds unmatched bank transactions (e.g., Duquesne Light payments)
- Creates check entries with proper vendor and property allocations

**Requirements:**
```bash
# Required environment variables
BROWSERBASE_API_KEY=
BROWSERBASE_PROJECT_ID=
OPENAI_API_KEY=
BUILDIUM_EMAIL=
BUILDIUM_PASSWORD=
OPEN_PHONE_API_KEY=  # for MFA/OTP
```

**Usage:**
```bash
uv run python buildium_stagehand.py
```

---

# Local Development Setup

## First Time Setup
### Python
```bash
# cd ~/ai-workflows
uv venv
uv sync
```

### Temporal Server

https://learn.temporal.io/getting_started/python/dev_environment/?os=mac

```bash
brew install temporal
```

```bash
echo '\n\n# Temporal' >> .env
echo 'TEMPORAL_ADDRESS="localhost:7233"\n' >> .env
```

## Run Temporal Server

```bash
temporal server start-dev --db-filename local_temporal_db.db

# Server:  localhost:7233
# UI:      http://localhost:8233
# Metrics: http://localhost:49650/metrics
```



# Railway 

* [Temporal Project](https://railway.com/project/6860099f-b8b8-4892-a116-1764e45bb6ec?environmentId=2f879f9e-56ea-4746-b9a1-72b0e25a379f)