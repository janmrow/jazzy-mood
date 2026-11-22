"""Synthetic demo fixture for the M1 first slice (P01, P02).

These records are NOT catalogue data. They exist so the form-to-result
flow, validation, loading, error recovery and the browser journey can be
exercised before the versioned SQLite catalogue lands in M2-01. Every
reason states the fixture status in plain language. Release use requires
`sourced` or `confirmed` catalogue tags; fixture rows must never be
treated as catalogue evidence.
"""

from __future__ import annotations

from typing import TypedDict


class FixtureAlbum(TypedDict):
    """Typed shape of one synthetic demo record.

    The keys mirror the API `Album` contract so a drift between fixture
    and response fails the parity test instead of reaching a visitor.
    Fixture rows stay code-only and clearly labelled; the versioned
    SQLite catalogue in M2-01 replaces them instead of copying them.
    """

    id: str
    artist: str
    title: str
    year: int
    listening_url: str
    listening_label: str
    reason: str
    tag_status: str


FIXTURE_ALBUMS: list[FixtureAlbum] = [
    {
        "id": "FIX-001",
        "artist": "Blue Line Trio",
        "title": "Night Loop",
        "year": 2004,
        "listening_url": "https://www.youtube.com/results?search_query=Blue+Line+Trio+Night+Loop",
        "listening_label": "Search listening options",
        "reason": (
            "Fixture demo pick: calm instrumental with a steady groove "
            "(fixture tags, not catalogue evidence)."
        ),
        "tag_status": "fixture",
    },
    {
        "id": "FIX-002",
        "artist": "Copper Five",
        "title": "Warm Circuit",
        "year": 2001,
        "listening_url": "https://www.youtube.com/results?search_query=Copper+Five+Warm+Circuit",
        "listening_label": "Search listening options",
        "reason": (
            "Fixture demo pick: moderate energy with a warm mood and a steady "
            "groove, vocal (fixture tags, not catalogue evidence)."
        ),
        "tag_status": "fixture",
    },
    {
        "id": "FIX-003",
        "artist": "Paper Planes Quartet",
        "title": "Grit Relay",
        "year": 1998,
        "listening_url": "https://www.youtube.com/results?search_query=Paper+Planes+Quartet+Grit+Relay",
        "listening_label": "Search listening options",
        "reason": (
            "Fixture demo pick: energetic with a gritty mood and a broken groove, "
            "vocal (fixture tags, not catalogue evidence)."
        ),
        "tag_status": "fixture",
    },
]


def select_album(recent_ids: list[str] | None = None) -> FixtureAlbum:
    """Return the first fixture album outside recent_ids, else the first.

    Deterministic so tests and the browser journey are reproducible.
    Respects the architecture rule that the browser may send a small list
    of recent catalogue IDs to allow variation. P03 repeat handling
    arrives in M2-03; this is only first-not-recent fallback.

    Returns a copy: mutating the result must never pollute the global
    fixture for later picks in the same process. Records stay flat
    (str/int only), so a shallow copy suffices; revisit with
    copy.deepcopy if a nested mutable field ever appears.
    """
    seen = {item.strip() for item in (recent_ids or []) if item and item.strip()}
    for album in FIXTURE_ALBUMS:
        if album["id"] not in seen:
            return FixtureAlbum(**album)
    return FixtureAlbum(**FIXTURE_ALBUMS[0])
