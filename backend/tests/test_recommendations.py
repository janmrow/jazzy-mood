"""API checks for the M1 first slice (P01, P02, P08).

Derives assertions from product behaviour: blank and oversized input is
rejected before selection, a valid description returns exactly one
fixture album with a reason and a listening link, recent IDs exclude the
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
    assert album["year"] == FIXTURE_ALBUMS[0]["year"]
    assert album["listening_url"].startswith("https://")
    assert album["listening_label"]
    assert "fixture" in album["reason"].lower()
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
