import pytest

from flexisaf_ai_engineering_w2.errors import RequestNotFoundError
from flexisaf_ai_engineering_w2.support_desk import SupportDesk


def make_desk():
    desk = SupportDesk()
    desk.add_request("REQ-001", "Amina Bello", "Smart meter", "1.0", "Display is blank")
    desk.add_request("REQ-002", "Tunde Balogun", "Weather sensor", "1.0", "No readings")
    return desk


def test_update_status_changes_the_request():
    desk = make_desk()
    request = desk.update_status("REQ-001", "resolved")
    assert request["status"] == "resolved"


def test_invalid_status_is_rejected():
    desk = make_desk()
    with pytest.raises(ValueError):
        desk.update_status("REQ-001", "flying")
    assert desk.requests["REQ-001"]["status"] == "open"


def test_unknown_request_is_rejected():
    desk = make_desk()
    with pytest.raises(RequestNotFoundError):
        desk.update_status("REQ-999", "resolved")


def test_undo_restores_the_previous_status():
    desk = make_desk()
    desk.update_status("REQ-001", "resolved")
    request = desk.undo_last_update()
    assert request["status"] == "open"


def test_undo_goes_back_newest_first():
    desk = make_desk()
    desk.update_status("REQ-001", "in_progress")
    desk.update_status("REQ-002", "resolved")
    desk.update_status("REQ-001", "closed")

    assert desk.undo_last_update()["status"] == "in_progress"  # REQ-001 back one step
    assert desk.undo_last_update()["status"] == "open"  # REQ-002 undone
    assert desk.undo_last_update()["status"] == "open"  # REQ-001 undone


def test_undo_with_nothing_to_undo_returns_none():
    assert SupportDesk().undo_last_update() is None
