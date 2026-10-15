import json

from flexisaf_ai_engineering_w2.storage import load_requests
from flexisaf_ai_engineering_w2.support_desk import SupportDesk


def test_load_requests_skips_duplicates(tmp_path):
    records = [
        {"id": "REQ-001", "customer": "A", "device": "D", "firmware": "1", "issue": "x", "created": "t1"},
        {"id": "REQ-001", "customer": "A", "device": "D", "firmware": "1", "issue": "x", "created": "t2"},
        {"id": "REQ-002", "customer": "B", "device": "D", "firmware": "1", "issue": "y", "created": "t3"},
    ]
    path = tmp_path / "requests.json"
    path.write_text(json.dumps(records))

    desk = SupportDesk()
    assert load_requests(desk, path) == (2, 1)
    assert len(desk.requests) == 2


def test_load_requests_skips_records_with_missing_fields(tmp_path):
    records = [
        {"id": "REQ-001", "customer": "A", "device": "D", "firmware": "1", "created": "t1"},
        {"id": "REQ-002", "customer": "B", "device": "D", "firmware": "1", "issue": "y", "created": "t3"},
    ]
    path = tmp_path / "requests.json"
    path.write_text(json.dumps(records))

    desk = SupportDesk()
    assert load_requests(desk, path) == (1, 1)