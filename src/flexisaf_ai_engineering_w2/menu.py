"""Menu loop for the support desk."""

from pathlib import Path

from .errors import DuplicateRequestError
from .storage import load_requests
from .support_desk import SupportDesk
from .priority import has_urgent_keyword

Data_File = Path(__file__).resolve().parents[2]/ "data"/ "sample_requests.json"

Menu =  """
=== Smart Device Support Desk ===
1. Add a support request
2. Process the next request
3. Show how many requests are waiting
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
        request = desk.add_request(request_id, customer, device, firmware, issue, urgent=urgent)
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
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Please choose a number from the menu.")


if __name__ == "__main__":
    main()