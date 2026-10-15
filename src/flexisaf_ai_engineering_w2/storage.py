"""Loading support requests from files."""

import json

from .errors import DuplicateRequestError


def load_requests(desk, path) -> tuple[int, int]:
    """Load requests from a JSON file. Return (loaded, skipped)."""
    with open(path) as file:
        records = json.load(file)

    loaded = 0
    skipped = 0
    for record in records:
        try:
            desk.add_request(
                record["id"],
                record["customer"],
                record["device"],
                record["firmware"],
                record["issue"],
                created=record["created"],
                urgent=record.get("urgent", False),
            )
        except (DuplicateRequestError, ValueError, KeyError):
            skipped += 1
        else:
            loaded += 1
    return loaded, skipped