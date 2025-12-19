from typing import Any, Dict


def require_str(data: Dict[str, Any], field: str) -> str:
    value = data.get(field)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"Field '{field}' must be a non-empty string")
    return value.strip()


def require_float(data: Dict[str, Any], field: str) -> float:
    value = data.get(field)
    if not isinstance(value, (int, float)):
        raise ValueError(f"Field '{field}' must be a number")
    return float(value)


def require_int(data: Dict[str, Any], field: str) -> int:
    value = data.get(field)
    if not isinstance(value, int):
        raise ValueError(f"Field '{field}' must be an integer")
    return value
