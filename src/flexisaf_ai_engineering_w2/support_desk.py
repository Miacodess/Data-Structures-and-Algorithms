"""Support desk core: stores requests and decides who is served next."""

from collections import deque
from datetime import datetime

from .errors import DuplicateRequestError
from .priority import has_urgent_keyword


class SupportDesk:
    def __init__(self) -> None:
        self.requests = {}
        self.seen_ids = set()
        self.urgent_queue = deque()
        self.normal_queue = deque()

    def add_request(
        self,
        request_id: str,
        customer: str,
        device: str,
        firmware: str,
        issue: str,
        created: str | None = None,
        urgent: bool = False,
    ) -> dict:
        """Create a request, reject duplicate IDs and join the right queue."""
        request_id = request_id.strip().upper()
        if request_id in self.seen_ids:
            raise DuplicateRequestError(f"Request ID {request_id} already exists!")
        if not customer.strip() or not issue.strip():
            raise ValueError("Customer name and issue cannot be empty")

        if created is None:
            created = datetime.now().strftime("%Y-%m-%d %H:%M")
        priority = "high" if urgent or has_urgent_keyword(issue) else "normal"

        request = {
            "id": request_id,
            "customer": customer.strip().title(),
            "device": device.strip(),
            "firmware": firmware.strip(),
            "issue": issue.strip(),
            "priority": priority,
            "status": "open",
            "created": created,
            "replies": [],
        }

        self.requests[request_id] = request
        self.seen_ids.add(request_id)
        if priority == "high":
            self.urgent_queue.append(request_id)
        else:
            self.normal_queue.append(request_id)
        return request  # now runs for both queues

    def process_next(self) -> dict | None:
        """Take the next request: urgent ones first, then in order received."""
        if self.urgent_queue:
            request_id = self.urgent_queue.popleft()
        elif self.normal_queue:
            request_id = self.normal_queue.popleft()
        else:
            return None

        request = self.requests[request_id]
        request["status"] = "in_progress"
        return request

    def queue_sizes(self) -> tuple[int, int]:
        """Return (urgent waiting, normal waiting)."""
        return len(self.urgent_queue), len(self.normal_queue)