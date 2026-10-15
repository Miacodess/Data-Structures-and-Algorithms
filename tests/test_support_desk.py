import pytest

from flexisaf_ai_engineering_w2.errors import DuplicateRequestError
from flexisaf_ai_engineering_w2.support_desk import SupportDesk


def add(desk, request_id, issue="Display is blank", **kwargs):
    """Small helper so each test stays short."""
    return desk.add_request(
        request_id, "Amina Bello", "Smart meter SM-200", "2.1.0", issue, **kwargs
    )


def test_add_request_stores_details():
    desk = SupportDesk()
    request = add(desk, "req-001", created="2026-10-01 08:00")
    assert request["id"] == "REQ-001"
    assert request["customer"] == "Amina Bello"
    assert request["status"] == "open"
    assert desk.requests["REQ-001"] is request


def test_duplicate_id_is_rejected():
    desk = SupportDesk()
    add(desk, "REQ-001")
    with pytest.raises(DuplicateRequestError):
        add(desk, "REQ-001")
    assert len(desk.requests) == 1


def test_duplicate_check_ignores_case_and_spaces():
    desk = SupportDesk()
    add(desk, "REQ-001")
    with pytest.raises(DuplicateRequestError):
        add(desk, "  req-001 ")


def test_empty_customer_is_rejected():
    desk = SupportDesk()
    with pytest.raises(ValueError):
        desk.add_request("REQ-001", "  ", "Meter", "1.0", "Broken")


def test_requests_are_served_in_order_received():
    desk = SupportDesk()
    add(desk, "REQ-001")
    add(desk, "REQ-002")
    add(desk, "REQ-003")
    assert desk.process_next()["id"] == "REQ-001"
    assert desk.process_next()["id"] == "REQ-002"
    assert desk.process_next()["id"] == "REQ-003"


def test_urgent_request_jumps_the_queue():
    desk = SupportDesk()
    add(desk, "REQ-001")
    add(desk, "REQ-002", urgent=True)
    assert desk.process_next()["id"] == "REQ-002"
    assert desk.process_next()["id"] == "REQ-001"


def test_safety_keyword_marks_high_priority():
    desk = SupportDesk()
    request = add(desk, "REQ-001", issue="The battery is OVERHEATING")
    assert request["priority"] == "high"


def test_process_next_on_empty_desk_returns_none():
    assert SupportDesk().process_next() is None


def test_processing_changes_status():
    desk = SupportDesk()
    add(desk, "REQ-001")
    assert desk.process_next()["status"] == "in_progress"
