_ISSUED: dict[str, str] = {}


def issue(approver: str, payload_hash: str) -> str:
    token = f"{approver}:{payload_hash[:12]}"
    _ISSUED[token] = payload_hash
    return token


def validate(token: str | None, payload_hash: str, single_use: bool = True) -> bool:
    if not token or _ISSUED.get(token) != payload_hash:
        return False
    if single_use:
        del _ISSUED[token]
    return True
