import json, datetime, uuid

def emit_event(event_type, pipeline_id, task_id, status, context=None):
    event = {
        "event_id": str(uuid.uuid4()),
        "event_type": event_type,
        "pipeline_id": pipeline_id,
        "task_id": task_id,
        "status": status,
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "context": context or {}
    }
    print(json.dumps(event))  # later → Kafka / DB
