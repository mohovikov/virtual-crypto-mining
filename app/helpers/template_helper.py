from flask import request


def get_version() -> str:
    try:
        with open("version", "r", encoding="utf-8") as f:
            return f.read().strip()
    except FileNotFoundError:
        return "unknown"

def is_active(endpoint):
    return "active" if request.endpoint == endpoint else ""

def is_active_prefix(prefix):
    return "active" if str(request.endpoint).startswith(prefix) else ""