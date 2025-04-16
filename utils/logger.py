import json
from datetime import datetime

def log_terminal_json(data: dict):
    log_entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "user input": data["user_input"],
        "flow": "streamlit to custom engine ",
        "status": "PASSED",
        "latency": f"{data['latency']}s",
        "output": data["response"],
        "token": data["tokens"],
        "time": f"{data['latency']}s"
    }
    print(json.dumps(log_entry, indent=4))
