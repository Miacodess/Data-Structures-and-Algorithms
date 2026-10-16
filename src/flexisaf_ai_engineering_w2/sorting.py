"""Sorting support requests by date, priority or status."""

PRIORITY_ORDER = {"high": 0, "normal": 1}
STATUS_ORDER = {
    "open": 0,
    "in_progress": 1,
    "waiting_customer": 2,
    "resolved": 3,
    "closed": 4,
}


def by_date(request: dict) -> str:
    # Dates look like "2026-10-01 08:05", so comparing them as text puts them in time order.
    return request["created"]


def by_priority(request: dict) -> int:
    return PRIORITY_ORDER[request["priority"]]


def by_status(request: dict) -> int:
    return STATUS_ORDER[request["status"]]


SORT_KEYS = {"date": by_date, "priority": by_priority, "status": by_status}


def insertion_sort(items: list[dict], key) -> list[dict]:
    """Sort by hand: take each item and slide it left until it sits in the right place."""
    result = list(items)  # work on a copy so the original list is untouched
    for i in range(1, len(result)):
        current = result[i]
        j = i - 1
        while j >= 0 and key(result[j]) > key(current):
            result[j + 1] = result[j]
            j -= 1
        result[j + 1] = current
    return result


def sort_requests(
    requests: list[dict], field: str, method: str = "builtin"
) -> list[dict]:
    """Return a new sorted list. method is 'builtin' (sorted) or 'insertion' (my own)."""
    if field not in SORT_KEYS:
        raise ValueError("Sort field must be one of: " + ", ".join(SORT_KEYS))
    key = SORT_KEYS[field]

    if method == "builtin":
        return sorted(requests, key=key)
    if method == "insertion":
        return insertion_sort(requests, key)
    raise ValueError("Method must be 'builtin' or 'insertion'")
