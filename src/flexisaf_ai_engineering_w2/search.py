"""Finding requests by ID or by customer name."""

from .support_desk import SupportDesk


def find_by_id(desk: SupportDesk, request_id: str) -> dict | None:
    """Look an ID up in the dictionary. One step, however many requests there are."""
    return desk.requests.get(request_id.strip().upper())


def find_by_id_linear(requests: list[dict], request_id: str) -> dict | None:
    """Check every request in turn until the ID matches. Kept for the comparison."""
    wanted = request_id.strip().upper()
    for request in requests:
        if request["id"] == wanted:
            return request
    return None


def find_by_customer(desk: SupportDesk, text: str) -> list[dict]:
    """Return every request whose customer name contains the text, ignoring capitals."""
    wanted = text.strip().lower()
    if not wanted:
        return []
    matches = []
    for request in desk.requests.values():
        if wanted in request["customer"].lower():
            matches.append(request)
    return matches
