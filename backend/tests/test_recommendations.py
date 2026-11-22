"""API checks for the M1 first slice (P01, P02, P08).

Derives assertions from product behaviour: blank and oversized input is
rejected before selection, a valid description returns exactly one
fixture album with a reason and no listening or search link, recent IDs exclude the
first pick, and visitor text never reaches the logs.
"""

import logging

from fastapi.testclient import TestClient

from backend.app.fixture import FIXTURE_ALBUMS
from backend.app.main import app

client = TestClient(app)

VALID = "Late-night jazz with a steady beat and no vocals."


def test_healthz_is_ok_without_provider():
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
    assert response.headers.get("x-request-id")


def test_valid_description_returns_one_fixture_album():
    response = client.post(
        "/api/recommendations", json={"description": VALID, "recent_ids": []}
    )
    assert response.status_code == 200
    body = response.json()
    assert body["mode"] == "local"
    album = body["album"]
    assert album["id"] == FIXTURE_ALBUMS[0]["id"]
    assert album["artist"] and album["title"]
    assert album.get("year") is None
    assert "listening_url" not in album
    assert "listening_label" not in album
    assert "fixture" in album["reason"].lower()
    assert "ignores your description" in album["reason"].lower()
    assert album["tag_status"] == "fixture"
    assert "x-request-id" in response.headers


def test_spaces_only_description_is_rejected():
    response = client.post("/api/recommendations", json={"description": "   "})
    assert response.status_code == 422


def test_empty_description_is_rejected():
    response = client.post("/api/recommendations", json={"description": ""})
    assert response.status_code == 422


def test_oversized_description_is_rejected():
    response = client.post("/api/recommendations", json={"description": "x" * 501})
    assert response.status_code == 422


def test_exactly_500_characters_is_accepted():
    response = client.post("/api/recommendations", json={"description": "y" * 500})
    assert response.status_code == 200


def test_surrounding_spaces_do_not_count_against_the_limit():
    response = client.post(
        "/api/recommendations", json={"description": "  " + "z" * 500 + "  "}
    )
    assert response.status_code == 200


def test_recent_ids_exclude_the_first_pick():
    first_id = FIXTURE_ALBUMS[0]["id"]
    response = client.post(
        "/api/recommendations",
        json={"description": VALID, "recent_ids": [first_id]},
    )
    assert response.status_code == 200
    assert response.json()["album"]["id"] == FIXTURE_ALBUMS[1]["id"]


def test_exhausted_recent_ids_fall_back_to_first():
    all_ids = [album["id"] for album in FIXTURE_ALBUMS]
    response = client.post(
        "/api/recommendations", json={"description": VALID, "recent_ids": all_ids}
    )
    assert response.status_code == 200
    assert response.json()["album"]["id"] == FIXTURE_ALBUMS[0]["id"]


def test_too_many_recent_ids_are_rejected():
    response = client.post(
        "/api/recommendations",
        json={"description": VALID, "recent_ids": [f"FIX-{i:03d}" for i in range(21)]},
    )
    assert response.status_code == 422


def test_blank_recent_ids_are_rejected():
    response = client.post(
        "/api/recommendations", json={"description": VALID, "recent_ids": ["   "]}
    )
    assert response.status_code == 422
    assert response.headers.get("x-request-id")


def test_padded_recent_ids_are_trimmed_and_accepted():
    first_id = FIXTURE_ALBUMS[0]["id"]
    response = client.post(
        "/api/recommendations",
        json={"description": VALID, "recent_ids": [f"  {first_id}  "]},
    )
    assert response.status_code == 200
    assert response.json()["album"]["id"] == FIXTURE_ALBUMS[1]["id"]


def test_oversized_recent_ids_are_rejected():
    response = client.post(
        "/api/recommendations",
        json={"description": VALID, "recent_ids": ["x" * 65]},
    )
    assert response.status_code == 422


def test_exactly_64_char_recent_ids_are_accepted():
    response = client.post(
        "/api/recommendations",
        json={"description": VALID, "recent_ids": ["x" * 64]},
    )
    assert response.status_code == 200


def test_unhandled_error_returns_json_500_with_request_id(monkeypatch):
    import backend.app.main as main_module

    def _boom(_recent_ids):
        raise RuntimeError("boom")

    monkeypatch.setattr(main_module, "select_album", _boom)
    quiet = TestClient(app, raise_server_exceptions=False)
    response = quiet.post("/api/recommendations", json={"description": VALID})
    assert response.status_code == 500
    assert response.json() == {"detail": "Internal Server Error"}
    assert response.headers.get("x-request-id")


def test_empty_fixture_returns_503(monkeypatch):
    import backend.app.main as main_module

    monkeypatch.setattr(main_module, "FIXTURE_ALBUMS", [])
    response = client.post("/api/recommendations", json={"description": VALID})
    assert response.status_code == 503
    assert response.headers.get("x-request-id")


def test_visitor_text_stays_out_of_logs(caplog):
    unique_phrase = "breezy apricot umbrella 7q9z"
    with caplog.at_level(logging.INFO, logger="jazzy_mood"):
        response = client.post(
            "/api/recommendations",
            json={"description": f"Quiet groove with {unique_phrase}"},
        )
    assert response.status_code == 200
    logged = "\n".join(record.getMessage() for record in caplog.records)
    assert unique_phrase not in logged


def test_rejected_input_stays_out_of_logs(caplog):
    unique_phrase = "quartz lantern epilogue 3x8k"
    with caplog.at_level(logging.INFO, logger="jazzy_mood"):
        blank = client.post("/api/recommendations", json={"description": "   "})
        oversized = client.post(
            "/api/recommendations",
            json={"description": unique_phrase + "x" * 500},
        )
    assert blank.status_code == 422
    assert oversized.status_code == 422
    assert blank.headers.get("x-request-id")
    assert oversized.headers.get("x-request-id")
    logged = "\n".join(record.getMessage() for record in caplog.records)
    assert unique_phrase not in logged


def test_unknown_api_paths_return_json_404_not_index():
    responses = [
        client.get("/api/no-such-route"),
        client.post("/api/no-such-route", json={"description": "x"}),
        client.get("/api"),
        client.get("/api/"),
        client.options("/api/no-such-route"),
    ]
    for response in responses:
        assert response.status_code == 404
        assert response.headers["content-type"].startswith("application/json")
        assert response.json() == {"detail": "Not Found"}
        assert response.headers.get("x-request-id")
    head_response = client.head("/api/no-such-route")
    assert head_response.status_code == 404
    assert head_response.headers.get("x-request-id")


def test_fixture_selection_returns_copies():
    from backend.app.fixture import select_album

    all_ids = [album["id"] for album in FIXTURE_ALBUMS]
    for recent in ([], all_ids):
        picked = select_album(recent)
        picked["artist"] = "MUTATED"
    assert select_album([])["artist"] == FIXTURE_ALBUMS[0]["artist"]
    assert select_album(all_ids)["artist"] == FIXTURE_ALBUMS[0]["artist"]
    assert FIXTURE_ALBUMS[0]["artist"] != "MUTATED"


def test_fixture_matches_api_contract():
    from backend.app.main import Album

    for album in FIXTURE_ALBUMS:
        validated = Album(**album)
        assert validated.id == album["id"]
        assert album["tag_status"] == "fixture"
