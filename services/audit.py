EVENTS: list[dict] = []


def log(event: str, **fields) -> None:
    EVENTS.append({"event": event, **fields})
