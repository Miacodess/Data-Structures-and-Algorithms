# Smart Device Support Desk

A command-line support desk for smart device issues (smart meters, solar inverters, and similar). Requests are queued automatically, and safety-related problems are served before everything else.

Built for FlexiSAF AI Engineering, Week 2.

## Features

- Add support requests with customer, device, firmware version and issue description
- Automatic priority: a request is marked **high** if it is flagged urgent or its description mentions a safety keyword (for example *overheating*, *smoke*, *fire*)
- Two queues: urgent requests are served first, then normal ones in the order received
- Duplicate request IDs are rejected (case and whitespace are ignored)
- Bulk loading from a JSON file, skipping duplicates and incomplete records
- Simple interactive menu

## Project structure

```
FlexiSAF_AI_Engineering_W2/
├── data/
│   └── sample_requests.json
├── src/flexisaf_ai_engineering_w2/
│   ├── __init__.py
│   ├── errors.py        # DuplicateRequestError
│   ├── menu.py          # interactive menu loop (entry point)
│   ├── priority.py      # urgent keyword rules
│   ├── storage.py       # load requests from JSON
│   └── support_desk.py  # SupportDesk class and queues
├── tests/
│   ├── test_storage.py
│   └── test_support_desk.py
└── pyproject.toml
```

## Getting started

Requires Python 3.10+ and [uv](https://docs.astral.sh/uv/).

```bash
git clone <your-repo-url>
cd FlexiSAF_AI_Engineering_W2
uv sync
```

## Usage

```bash
uv run support-desk
```

You will see this menu:

```
=== Smart Device Support Desk ===
1. Add a support request
2. Process the next request
3. Show how many requests are waiting
0. Quit
```

Sample requests from `data/sample_requests.json` are loaded on startup. If the file is missing, the desk starts empty.

## Sample data format

```json
[
  {
    "id": "REQ-001",
    "customer": "Amina Bello",
    "device": "Smart meter SM-200",
    "firmware": "2.1.0",
    "issue": "Display is blank",
    "created": "2026-10-01 08:00",
    "urgent": false
  }
]
```

`urgent` is optional and defaults to `false`. Records with missing fields or duplicate IDs are skipped.

## How priority works

1. If the request is marked urgent, it is **high** priority.
2. Otherwise, if the issue text contains a safety keyword (`overheating`, `fire`, `burning`, `shock`, `sparks`, `smoke`, `swollen`), it is **high** priority.
3. Everything else is **normal**.

High-priority requests are always processed before normal ones. Within each group, requests are served first in, first out.

## Running the tests

```bash
uv run pytest -v
```

## Possible next steps

- Save the desk state back to JSON on exit
- Add replies to requests and a "resolved" status
- Search and filter by customer or device