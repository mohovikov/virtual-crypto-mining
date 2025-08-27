def get_version() -> str:
    try:
        with open("version", "r", encoding="utf-8") as f:
            return f.read().strip()
    except FileNotFoundError:
        return "unknown"