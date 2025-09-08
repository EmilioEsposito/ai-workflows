


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

## Run Temporal Server

```bash
temporal server start-dev --db-filename local_temporal_db.db

# Server:  localhost:7233
# UI:      http://localhost:8233
# Metrics: http://localhost:49650/metrics
```



