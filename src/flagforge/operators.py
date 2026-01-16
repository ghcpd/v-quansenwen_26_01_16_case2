from __future__ import annotations

import re
from typing import Any, Iterable


def op_eq(left: Any, right: Any) -> bool:
    return left == right


def op_neq(left: Any, right: Any) -> bool:
    return left != right


def op_in(left: Any, right: Any) -> bool:
    if isinstance(right, (list, tuple, set)):
        return left in right
    return False


def op_contains(left: Any, right: Any) -> bool:
    if left is None:
        return False
    if isinstance(left, str) and isinstance(right, str):
        return right in left
    if isinstance(left, (list, tuple, set)):
        return right in left
    return False


def op_gt(left: Any, right: Any) -> bool:
    try:
        return left > right
    except TypeError:
        return False


def op_gte(left: Any, right: Any) -> bool:
    try:
        return left >= right
    except TypeError:
        return False


def op_lt(left: Any, right: Any) -> bool:
    try:
        return left < right
    except TypeError:
        return False


def op_lte(left: Any, right: Any) -> bool:
    try:
        return left <= right
    except TypeError:
        return False


def op_regex(left: Any, right: Any) -> bool:
    if not isinstance(left, str) or not isinstance(right, str):
        return False
    try:
        return re.search(right, left) is not None
    except re.error:
        return False


OPS = {
    "eq": op_eq,
    "neq": op_neq,
    "in": op_in,
    "contains": op_contains,
    "gt": op_gt,
    "gte": op_gte,
    "lt": op_lt,
    "lte": op_lte,
    "regex": op_regex,
}
