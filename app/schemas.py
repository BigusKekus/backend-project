from __future__ import annotations
from typing import Any
from flask import Request

class ApiError(Exception):
    def __init__(self, message: str, status_code: int = 400):
        super().__init__(message)
        self.message = message
        self.status_code = status_code

def get_json(request: Request) -> dict[str, Any]:
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        raise ApiError("JSON body is required", 400)
    return data

def require_str(data: dict[str, Any], key: str) -> str:
    val = data.get(key)
    if not isinstance(val, str) or not val.strip():
        raise ApiError(f"'{key}' must be a non-empty string", 400)
    return val.strip()

def require_int(data: dict[str, Any], key: str) -> int:
    val = data.get(key)
    if isinstance(val, bool):
        raise ApiError(f"'{key}' must be an integer", 400)
    try:
        return int(val)
    except Exception as exc:
        raise ApiError(f"'{key}' must be an integer", 400) from exc

def require_float(data: dict[str, Any], key: str) -> float:
    val = data.get(key)
    if isinstance(val, bool):
        raise ApiError(f"'{key}' must be a number", 400)
    try:
        return float(val)
    except Exception as exc:
        raise ApiError(f"'{key}' must be a number", 400) from exc

def query_int(args: dict[str, Any], key: str) -> int | None:
    if key not in args or args.get(key) in (None, ""):
        return None
    try:
        return int(args.get(key))
    except Exception as exc:
        raise ApiError(f"Query param '{key}' must be an integer", 400) from exc
