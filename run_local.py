import json
import base64
from main import entry_point

def run_local():
    """
    Simulates a Pub/Sub trigger to run the pipeline locally.
    """
    # ---------------------------------
    # 1. Create a fake Pub/Sub event
    # ---------------------------------
    payload = {"source": "youtube"}
    message = base64.b64encode(json.dumps(payload).encode("utf-8")).decode("utf-8")
    
    event = {
        "data": message
    }

    # ---------------------------------
    # 2. Call the entry point
    # ---------------------------------
    try:
        entry_point(event, None)
    except Exception as e:
        print(f"[ERROR] Pipeline failed: {e}")

if __name__ == "__main__":
    run_local()
