from flexisaf_ai_engineering_w2.search import (
    find_by_customer,
    find_by_id,
    find_by_id_linear,
)
from flexisaf_ai_engineering_w2.support_desk import SupportDesk


def make_desk():
    desk = SupportDesk()
    desk.add_request("REQ-001", "Amina Bello", "Smart meter", "1.0", "Display is blank")
    desk.add_request("REQ-002", "Tunde Balogun", "Weather sensor", "1.0", "No readings")
    desk.add_request("REQ-003", "Amina Bello", "Thermostat", "1.0", "Wi-Fi drops")
    return desk


def test_find_by_id_ignores_case_and_spaces():
    desk = make_desk()
    assert find_by_id(desk, "  req-002 ")["customer"] == "Tunde Balogun"


def test_find_by_id_returns_none_when_missing():
    assert find_by_id(make_desk(), "REQ-999") is None


def test_linear_search_finds_the_same_request():
    desk = make_desk()
    requests = list(desk.requests.values())
    assert find_by_id_linear(requests, "req-003") is find_by_id(desk, "REQ-003")


def test_linear_search_returns_none_when_missing():
    desk = make_desk()
    assert find_by_id_linear(list(desk.requests.values()), "REQ-999") is None


def test_find_by_customer_matches_part_of_a_name_ignoring_case():
    matches = find_by_customer(make_desk(), "amina")
    assert [request["id"] for request in matches] == ["REQ-001", "REQ-003"]


def test_find_by_customer_with_no_match_returns_empty_list():
    assert find_by_customer(make_desk(), "zzz") == []


def test_find_by_customer_with_empty_text_returns_empty_list():
    assert find_by_customer(make_desk(), "   ") == []
