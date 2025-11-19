# protocol.py
import json, uuid
from datetime import datetime, timezone

def make_header(action, path, size=0, h=None, sender=None, compressed=False):
    return json.dumps({
        "id": str(uuid.uuid4()),
        "action": action,        # create | modify | delete
        "path": path,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "size": size,
        "hash": h,
        "sender": sender,
        "compressed": compressed
    }).encode('utf-8')

def parse_header(b):
    return json.loads(b.decode('utf-8'))
