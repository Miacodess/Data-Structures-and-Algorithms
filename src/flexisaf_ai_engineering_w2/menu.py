"""Menu loop for the support desk."""

from pathlib import Path

from .errors import DuplicateRequestError, RequestNotFoundError
from .storage import load_requests
from .support_desk import VALID_STATUSES, SupportDesk
from .search import find_by_customer, find_by_id
from .priority import has_urgent_keyword
from .sorting import sort_requests

Data_File = Path(__file__).resolve().parents[2] / "data" / "sample_requests.json"

Menu = """
=== Smart Device Support Desk ===
1. Add a support request
2. Process the next request
3. Show how many requests are waiting
4. Update a request's status
5. Undo the last status update
6. Search for a request
7. List requests, sorted
0. Quit
"""


def show_request(request: dict) -> None:
    print(f"  ID:        {request['id']}")
    print(f"  Customer:  {request['customer']}")
    print(f"  Device:    {request['device']} (firmware {request['firmware']})")
    print(f"  Issue:     {request['issue']}")
    print(f"  Priority:  {request['priority']}")
    print(f"  Status:    {request['status']}")
    print(f"  Received:  {request['created']}")


def add_request_flow(desk: SupportDesk) -> None:
    request_id = input("Request ID (e.g. REQ-020): ")
    customer = input("Customer name: ")
    device = input("Device (e.g. Solar inverter SI-5000): ")
    firmware = input("Firmware version: ")
    issue = input("Describe the problem: ")
    urgent = input("Mark as urgent? (y/n): ").strip().lower() == "y"

    try:
        request = desk.add_request(
            request_id, customer, device, firmware, issue, urgent=urgent
        )
    except DuplicateRequestError as error:
        print(f"Not added: {error}.")
    except ValueError as error:
        print(f"Not added: {error}.")
    else:
        print(f"Added {request['id']} with {request['priority']} priority.")


def process_flow(desk: SupportDesk) -> None:
    request = desk.process_next()
    if request is None:
        print("No requests are waiting.")
    else:
        print("Now processing:")
        show_request(request)


def update_status_flow(desk: SupportDesk) -> None:
    request_id = input("Request ID: ")
    print("Statuses: " + ", ".join(VALID_STATUSES))
    new_status = input("New status: ").strip().lower()

    try:
        request = desk.update_status(request_id, new_status)
    except (RequestNotFoundError, ValueError) as error:
        print(f"Not updated: {error}.")
    else:
        print(f"{request['id']} is now {request['status']}.")


def undo_flow(desk: SupportDesk) -> None:
    request = desk.undo_last_update()
    if request is None:
        print("Nothing to undo.")
    else:
        print(f"Undone: {request['id']} is back to {request['status']}.")

def show_summary(request: dict) -> None:
    print(
        f"  {request['id']} | {request['created']} | {request['priority']:6} | "
        f"{request['status']:16} | {request['customer']}"
    )


def search_flow(desk: SupportDesk) -> None:
    choice = input("Search by (1) request ID or (2) customer name: ").strip()

    if choice == "1":
        request = find_by_id(desk, input("Request ID: "))
        if request is None:
            print("No request with that ID.")
        else:
            show_request(request)
    elif choice == "2":
        matches = find_by_customer(desk, input("Customer name (or part of it): "))
        if not matches:
            print("No matching customers.")
        else:
            print(f"{len(matches)} found:")
            for request in matches:
                show_summary(request)
    else:
        print("Please choose 1 or 2.")

def sort_flow(desk: SupportDesk) -> None:
    field = input("Sort by (date/priority/status): ").strip().lower()
    own_sort = input("Use my own insertion sort instead of sorted()? (y/n): ").strip().lower()
    method = "insertion" if own_sort == "y" else "builtin"

    try:
        ordered = sort_requests(list(desk.requests.values()), field, method)
    except ValueError as error:
        print(f"Cannot sort: {error}.")
        return

    print(f"{len(ordered)} requests, sorted by {field}:")
    for request in ordered:
        show_summary(request)

def main() -> None:
    desk = SupportDesk()
    try:
        loaded, skipped = load_requests(desk, Data_File)
    except FileNotFoundError:
        print(f"Sample data not found at {Data_File}. Starting with an empty desk.")
    else:
        print(f"Loaded {loaded} requests ({skipped} skipped).")

    while True:
        print(Menu)
        choice = input("Choose an option: ").strip()

        if choice == "1":
            add_request_flow(desk)
        elif choice == "2":
            process_flow(desk)
        elif choice == "3":
            urgent, normal = desk.queue_sizes()
            print(f"Waiting: {urgent} urgent, {normal} normal.")
        elif choice == "4":
            update_status_flow(desk)
        elif choice == "5":
            undo_flow(desk)
        elif choice == "6":
            search_flow(desk)
        elif choice == "7":
            sort_flow(desk)
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Please choose a number from the menu.")


if __name__ == "__main__":
    main()
