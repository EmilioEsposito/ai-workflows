https://learn.temporal.io/getting_started/python/hello_world_in_python/


## Terminal 1: Run Temporal Server

```bash
temporal server start-dev --db-filename local_temporal_db.db

# Server:  localhost:7233
# UI:      http://localhost:8233
# Metrics: http://localhost:49650/metrics
```

## Terminal 2: Run Worker

```bash
python hello_world_temporal/run_worker.py
```

## Terminal 3: Run Workflow

```bash
python hello_world_temporal/run_workflow.py
```

