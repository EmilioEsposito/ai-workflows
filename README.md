


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