import json
from contextlib import contextmanager
from contextvars import ContextVar
from typing import Any, Iterator

from pydantic.json import pydantic_encoder


def to_json(data: Any) -> str:
    return json.dumps(data, default=pydantic_encoder)


def from_json(raw: str) -> Any:
    return json.loads(raw)


@contextmanager
def set_context_var(var: ContextVar, value) -> Iterator[None]:
    token = var.set(value)
    try:
        yield
    finally:
        var.reset(token)
