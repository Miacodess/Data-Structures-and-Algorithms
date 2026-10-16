# Smart Device Support Desk: Module B2 (Week 2)

This is my Week 2 project for the AI engineering internship. The brief was to build a Python system that receives, organises and processes customer support requests, using the data structures from this module: dictionaries, sets, queues, stacks, recursion, plus searching and sorting.

I picked a theme that made the data structures easy to justify. The desk belongs to a company that sells smart devices such as meters, solar inverters and sensors. Some faults are annoying (a thermostat that won't join Wi-Fi) and some are dangerous (a battery casing that is overheating), so "urgent" has a real meaning instead of being a label I made up.

---

## Where the project stands

| Feature from the brief | Status |
|------------------------|--------|
| Add a new support request | Built |
| Store customer information in dictionaries | Built |
| Prevent duplicate request IDs with a set | Built |
| Process requests in order received with a queue | Built |
| Mark urgent requests as high priority | Built |
| Undo the most recent update with a stack | **Planned** |
| Search by ID or customer name | **Planned** |
| Sort by date, priority or status | **Planned** |
| Recursion to display replies in order | **Planned** |
| Compare two searching or sorting approaches | **Planned** |

---

## Setup and running

You need Python 3.12 or newer and [uv](https://docs.astral.sh/uv/).

```bash
git clone <repo-url>
cd FlexiSAF_AI_Engineering_W2
uv sync
```

- `git clone` downloads the project.
- `cd` moves into the project folder.
- `uv sync` creates a virtual environment and installs the dependencies listed in `uv.lock`.

Start the desk:

```bash
uv run support-desk
```

- `uv run` runs a command inside the project's environment, so there is nothing to activate by hand.
- `support-desk` is a command defined in `pyproject.toml` that starts the menu.

Run the tests:

```bash
uv run pytest -v
```

- `pytest` finds and runs every test file, and `-v` lists each test with its result.

---

## What the menu does today

1. **Add a support request.** You type an ID, customer name, device, firmware version and a description of the problem, and say whether it is urgent.
2. **Process the next request.** The desk hands you the next request that should be dealt with and marks it `in_progress`.
3. **Show how many requests are waiting.** It prints the urgent and normal queue sizes.

When the program starts, it loads `data/sample_requests.json`. That file has 12 records, and the last one deliberately repeats `REQ-005`, so every start-up shows the duplicate check working (`Loaded 11 requests (1 skipped)`). Two other records, `REQ-004` ("overheating") and `REQ-009` ("sparks"), get flagged as high priority because of the words in their description, without anyone ticking an urgent box.

---

## How it is organised

```
FlexiSAF_AI_Engineering_W2/
├── data/sample_requests.json
├── src/flexisaf_ai_engineering_w2/
│   ├── errors.py          # custom errors (duplicate ID)
│   ├── priority.py        # what counts as urgent
│   ├── support_desk.py    # the SupportDesk class: add, queues, process
│   ├── storage.py         # loading requests from a JSON file
│   └── menu.py            # the menu loop
├── tests/
│   ├── test_support_desk.py
│   └── test_storage.py
└── pyproject.toml
```

I split the code up so each file has one job. Before the split, one file held the errors, the urgency rules, the desk and the file loading, and I could see it getting crowded once undo, search, sorting and replies arrived. The imports only point one way (the menu uses storage, storage uses the desk, the desk uses errors and priority), which stops files importing each other in a circle.

---

## Which data structure for which feature

| Feature | Data structure | Why I chose it |
|---------|----------------|----------------|
| A request's details | **Dictionary** | A request has named fields (customer, device, issue, status), and a dictionary lets me read them by name. |
| All requests, looked up by ID | **Dictionary** keyed by request ID | Finding a request by its ID is one lookup, no matter how many requests exist. |
| Rejecting duplicate IDs | **Set** | The only question is "have I seen this ID?", and a set answers that quickly. It also remembers an ID even if a request is removed later. |
| Order received | **Queue** (`collections.deque`) | First in, first out is exactly what a queue does, and both ends are fast. |
| Urgent first | **A second queue** | Urgent requests wait in their own queue, which is always served before the normal one. It's easy to explain and to test. |
| Undo (**Planned**) | **Stack** (a list) | Undo reverses the *most recent* change first, which is last in, first out. |
| Search (**Planned**) | Dictionary index, and a linear scan | Part of the comparison between two approaches. |
| Sorting (**Planned**) | A sort I write, and Python's `sorted()` | The other part of that comparison. |
| Replies (**Planned**) | Nested lists, shown with recursion | A reply can have replies of its own, so the shape of the data repeats at every level. |

---

## Time and space complexity

For the parts that exist today. *n* is the number of requests.

| Operation | Time | Extra space | Notes |
|-----------|------|-------------|-------|
| Add a request | O(1) average | O(1) | One dictionary insert, one set insert, one queue append. |
| Duplicate check | O(1) average | none | Set membership. |
| Look up a request by ID | O(1) average | none | Dictionary lookup. |
| Process next request | O(1) | none | `popleft` on a deque. |
| Load a file of *n* records | O(n) | O(n) | Every record is added once. |
| Keyword check on one issue | O(k × m) | O(m) | k keywords, m characters of text. Both are small. |

The whole desk uses O(n) memory, because every request is stored once in the dictionary and its ID once in the set and in a queue. I used a deque because a plain list is slow at removing from the front.

The planned operations (undo, search, sort, replies) will be added to this table once I've measured them.

---

## Tests

There are 11 tests. They cover:

- storing a request's details
- rejecting a duplicate ID, including one that differs only in capitals or spaces
- rejecting an empty customer name
- serving requests in the order they arrived
- an urgent request jumping the queue
- a safety word such as "overheating" setting high priority
- processing from an empty desk
- processing changing the status
- loading a file that has a duplicate record
- loading a file that has a record with a missing field

Each test starts with a fresh `SupportDesk`, so tests can't affect one another. I kept the desk's logic away from `input()` and `print()` for that reason: a test can call it directly.

---

## Design decisions and trade-offs

- **The queues hold IDs, not whole requests.** There is one copy of each request, in the dictionary, so an update is visible everywhere. The cost is an extra lookup whenever I take someone off a queue.
- **Both a dictionary and a set know the IDs.** That's a little redundant, since the dictionary alone could answer "have I seen this ID?". I kept the set because the brief asks for it and because it keeps remembering an ID even if I later delete a request.
- **Two queues instead of a heap.** A heap would scale to many priority levels, but two queues are simpler and every operation is O(1). The brief only needs two levels.
- **A menu loop, not a command-line tool.** The queues and the undo stack live in memory, so the program has to stay running. A one-shot command like last week's would forget everything each time.
- **I changed the project layout once.** I started with plain files at the top level, then moved to a `src` package so the program can be started with `uv run support-desk`. The package version needs relative imports (`from .errors import ...`) and a more careful path to the data file, which was more to learn, but it makes the run instructions short.

---

## Problems I ran into

I'm keeping these because they taught me more than the parts that worked first time.

- **A script entry point that pointed at the wrong place.** The launcher imported `main` from the package's `__init__.py`, where it didn't exist. The target needs the form `package.module:function`, and mine was missing the `.menu`.
- **`.parent` versus `.parents`.** I indexed `.parent[2]` to climb to the project folder, which crashed with "PosixPath object is not subscriptable". It should be `.parents[2]`, which is a sequence of ancestor folders.
- **A missing import after splitting the code.** I moved `has_urgent_keyword` into `priority.py` but didn't import it back into the desk. Nine tests failed with one `NameError`, so the lesson was to fix the first root cause and re-run before reading everything else.

---

## Limitations and possible improvements

- **Nothing is saved.** Requests added while the program runs are lost when it quits. Saving back to the JSON file would fix that.
- **Marking an existing request urgent isn't possible yet.** A request has to be urgent when it is added. Moving one between queues means removing it from the middle of a deque, which is O(n).
- **Keyword matching is crude.** It looks for a word anywhere in the text, so a description mentioning a "firewall" would count as a fire. Matching whole words would be better.
- **Customer names are title-cased,** which turns "McDonald" into "Mcdonald".
- **Request IDs are typed by hand.** Generating them would remove the chance of a clash.
- **A processed request has no completion step yet.** It becomes `in_progress` and stays there.

---

## Planned

- **Update status and undo.** Every status change will push the old value onto a stack, and undo will pop it back.
- **Search by ID and by customer name.** ID search uses the dictionary. For names I'll compare a linear scan against a name index, and note the memory cost of the index.
- **Sort by date, priority or status.** I'll write one sort myself and compare it with `sorted()`.
- **Replies and follow-ups.** A recursive function will print a request's replies, indented by depth.
- **A benchmark** timing the approaches I'm comparing on generated data, with the results in a table here.

---

## How I worked

I used an AI assistant (Claude) while planning this project, drafting starter code, and working out what error messages meant. I wrote and ran the code myself and fixed the bugs I hit.

---
