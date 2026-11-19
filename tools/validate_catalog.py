"""Validate the M0 catalogue sample before it is imported anywhere.

Canonical schema for ``catalog/m0-sample.csv``. The future importer can
reuse this module instead of retyping the format by hand.

Columns (all required in the header):

- ``candidate_id``: stable label such as ``M0-001``. Nonblank, unique,
  ``^[A-Za-z0-9][A-Za-z0-9_-]*$``.
- ``artist``, ``title``: nonblank. Duplicates are compared
  case-insensitively after trimming; reissues of the same album are
  duplicates.
- ``year``: ``unknown`` or a four-digit year 1900-2100.
- ``identity_source``: nonblank source for identity (URL or source ID).
- ``reuse_note``: nonblank reuse and provenance terms. A note containing
  ``needs-review`` flags the row for a rights check.
- ``energy``: single label from ``calm``, ``moderate``, ``energetic``,
  ``unknown``.
- ``mood``: ``;``-separated labels from ``late-night``, ``warm``,
  ``dark``, ``bright``, ``gritty``, ``smooth``, ``unknown``.
  ``unknown`` must stand alone.
- ``groove``: ``;``-separated labels from ``steady``, ``swung``,
  ``broken``, ``free``, ``unknown``. ``unknown`` must stand alone.
- ``vocals``: single label from ``instrumental``, ``vocal``,
  ``unknown``. ``instrumental`` means strictly no vocal sound of any
  kind, including rap, sung or spoken parts, samples, dialogue, and
  backing vocals.
- ``tag_basis``: basis for the descriptive claims. Required when
  ``tag_status`` is ``confirmed`` or when any descriptive tag is not
  ``unknown``.
- ``tag_status``: ``confirmed``, ``sourced`` or ``proposed``.
  ``proposed`` means a draft pending evidence or a listening check and
  flags the row for review. ``sourced`` means two independent reputable
  sources agree on the tags, or one strong source agrees with MusicBrainz
  identity, with each source cited in ``tag_basis`` (D08); ``sourced``
  rows pass without a review flag. ``confirmed`` means an owner
  listening check on top of sources.

No extra columns are accepted. Empty ``;`` segments (``warm;;dark``,
leading or trailing ``;``) are rejected so the stored tag set cannot
differ from the validated view.

Validation never proves reuse rights. Rows with ``tag_status`` set to
``proposed`` or a ``reuse_note`` containing ``needs-review`` are
reported for a manual check. Release use requires ``sourced`` or
``confirmed`` tags; ``proposed`` rows must never be promoted as ground
truth.

Future importer notes (M2-01): ``validate_file`` returns
``(errors, reviews, count)`` and signals an unreadable file with a
``ReadError(str)`` first element, so callers must branch on
``isinstance(errors[0], ReadError)`` before treating errors as row
problems. There is no schema version column yet; additive evolution
(link, artwork, new labels) must arrive with a versioned schema
change. Known P04 trade-offs for M2-01 hardening: bare ``hum`` is
deliberately not a vocal word (avoids false positives on non-vocal
hum), benign wording such as ``chorus form`` may need rewording, and
clause-scoped double negatives are approximate. Always validate with
:func:`check_multi` or :func:`validate_file`, never normalize with
:func:`split_labels` alone.

Usage::

    python3 tools/validate_catalog.py catalog/m0-sample.csv

Exit code 0 means no errors (rows may still need review), 1 means
validation errors, 2 means the file could not be read.
"""

from __future__ import annotations

import argparse
import csv
import re
import sys

REQUIRED_COLUMNS = [
    "candidate_id",
    "artist",
    "title",
    "year",
    "identity_source",
    "reuse_note",
    "energy",
    "mood",
    "groove",
    "vocals",
    "tag_basis",
    "tag_status",
]

ENERGY_VALUES = {"calm", "moderate", "energetic", "unknown"}
MOOD_VALUES = {"late-night", "warm", "dark", "bright", "gritty", "smooth", "unknown"}
GROOVE_VALUES = {"steady", "swung", "broken", "free", "unknown"}
VOCALS_VALUES = {"instrumental", "vocal", "unknown"}
STATUS_VALUES = {"confirmed", "sourced", "proposed"}

ID_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_-]*$")
YEAR_PATTERN = re.compile(r"^(\d{4}|unknown)$")
VOCAL_WORD = re.compile(
    r"\bvocal(s|ist(s)?)?\b|\brap(ped|ping|per|s)?\b|\bsing\b|\bsinging\b|\bsings\b|\bsang\b|\bsung\b|\bsinger(s)?\b"
    r"|\bspoken\b|\bsample(d|s)?\b|\bsampling\b|\bdialogue(s)?\b"
    r"|\bvoice(s|d)?\b|\blyric(s)?\b|\bchoir(s)?\b|\bchorus(es)?\b|\bMCs?\b|\bemcee(s)?\b"
    r"|\bbeatbox(ing|er(s)?|ed)?\b|\bwhistl(e|es|ing|ed)\b|\bhum(ming|med|s)\b"
    r"|\byodel(l)?(ing|led|s|er)?\b|\bscat(ting|s)?\b|\ba[-\s]?capp?ella\b",
    re.IGNORECASE,
)
SOUND_WORD = (
    r"vocal(s|ist(s)?)?|rap(ped|ping|per|s)?|sing|singing|sings|sang|sung|singer(s)?"
    r"|spoken|sample(d|s)?|sampling|dialogue(s)?|voice(s|d)?|lyric(s)?"
    r"|choir(s)?|chorus(es)?|MCs?|emcee(s)?|beatbox(ing|er(s)?|ed)?"
    r"|whistl(e|es|ing|ed)|hum(ming|med|s)|yodel(l)?(ing|led|s|er)?"
    r"|scat(ting|s)?|a[-\s]?capp?ella"
)
NO_VOCAL_WORD = re.compile(
    rf"\b(no|without|non)\b[\w\s,;/-]*?\b({SOUND_WORD})\b|\b({SOUND_WORD})-free\b",
    re.IGNORECASE,
)
NEGATED_DENIAL_WORD = re.compile(r"\bnot\b|n['\u2019]t\b|\bnever\b", re.IGNORECASE)


def _denial_spans(basis: str) -> list[tuple[int, int]]:
    """Spans of vocal denials such as ``no vocals`` or ``vocal-free``.

    A denial in a clause containing ``not``/``n't``/``never`` (for
    example ``not without vocals`` or ``isn't without vocals``) is a
    double negative that affirms vocals, so it is not a denial span.
    Only the current clause (after the last ``.`` or ``;``) is checked,
    so ``Not a remix. Without vocals`` still counts as a denial.
    """
    spans = []
    for match in NO_VOCAL_WORD.finditer(basis):
        clause = re.split(r"[.;]", basis[: match.start()])[-1]
        if NEGATED_DENIAL_WORD.search(clause):
            continue
        spans.append(match.span())
    return spans


def _vocal_claim_problem(vocals: str, basis: str, where: str) -> list[str]:
    """Check a ``tag_basis`` against the ``vocals`` tag (P04).

    Every vocal-word mention must be covered by a denial for
    ``instrumental`` to hold, so ``No lyrics; whistling melody`` still
    fails. Symmetrically, ``vocal`` fails when the basis only denies
    vocals, such as ``No vocals; instrumental only``.
    """
    hits = list(VOCAL_WORD.finditer(basis))
    if not hits:
        return []
    denials = _denial_spans(basis)
    affirmed = [
        hit
        for hit in hits
        if not any(start <= hit.start() and hit.end() <= end for start, end in denials)
    ]
    if vocals == "instrumental" and affirmed:
        return [f"{where}: vocals 'instrumental' contradicts a tag_basis mentioning vocals"]
    if vocals == "vocal" and not affirmed:
        return [f"{where}: vocals 'vocal' contradicts a tag_basis denying vocals"]
    return []

DESCRIPTIVE = ("energy", "mood", "groove", "vocals")


class ReadError(str):
    """A file-read failure. A str subclass so main() can detect it
    without depending on the message text."""


def split_labels(raw: str) -> list[str]:
    """Split a ``;``-separated field, keeping empty segments visible.

    Empty strings in the result mean the input had ``;;`` or a leading
    or trailing ``;`` and must be treated as invalid. Use
    :func:`check_multi` for validation; do not normalize with this
    function alone.
    """
    return [part.strip() for part in raw.split(";")]


def check_multi(value: str, allowed: set[str], column: str, where: str) -> list[str]:
    if not value.strip():
        return [f"{where}: {column} is blank"]
    labels = split_labels(value)
    if any(label == "" for label in labels):
        return [f"{where}: {column} has an empty segment"]
    problems = [f"{where}: {column} has unknown value {label!r}" for label in labels if label not in allowed]
    if "unknown" in labels and len(labels) > 1:
        problems.append(f"{where}: {column} mixes 'unknown' with other labels")
    return problems


def validate_rows(rows: list[dict[str, str]]) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    reviews: list[str] = []
    seen_ids: dict[str, str] = {}
    seen_albums: dict[tuple[str, str], str] = {}

    for row in rows:
        lineno = row.get("_lineno", "?")
        row_id = row.get("candidate_id", "").strip()
        where = f"row {lineno} ({row_id or 'no id'})"

        for column in ("candidate_id", "artist", "title", "identity_source", "reuse_note", "tag_status"):
            if not row.get(column, "").strip():
                errors.append(f"{where}: {column} is blank")

        if row_id:
            if not ID_PATTERN.match(row_id):
                errors.append(f"{where}: candidate_id {row_id!r} has a bad format")
            if row_id in seen_ids:
                errors.append(f"{where}: duplicate candidate_id {row_id!r} (first seen at {seen_ids[row_id]})")
            else:
                seen_ids[row_id] = f"row {lineno}"

        album = (row.get("artist", "").strip().casefold(), row.get("title", "").strip().casefold())
        if all(album):
            if album in seen_albums:
                errors.append(f"{where}: duplicate album (first seen at {seen_albums[album]})")
            else:
                seen_albums[album] = f"row {lineno}"

        year = row.get("year", "").strip()
        if not YEAR_PATTERN.match(year):
            errors.append(f"{where}: year {year!r} must be YYYY or 'unknown'")
        elif year != "unknown" and not 1900 <= int(year) <= 2100:
            errors.append(f"{where}: year {year!r} is outside 1900-2100")

        energy = row.get("energy", "").strip()
        if energy not in ENERGY_VALUES:
            errors.append(f"{where}: energy has unknown value {energy!r}")
        errors.extend(check_multi(row.get("mood", ""), MOOD_VALUES, "mood", where))
        errors.extend(check_multi(row.get("groove", ""), GROOVE_VALUES, "groove", where))
        vocals = row.get("vocals", "").strip()
        if vocals not in VOCALS_VALUES:
            errors.append(f"{where}: vocals has unknown value {vocals!r}")

        status = row.get("tag_status", "").strip()
        if status and status not in STATUS_VALUES:
            errors.append(f"{where}: tag_status has unknown value {status!r}")
        basis = row.get("tag_basis", "").strip()
        tags = {column: row.get(column, "").strip() for column in DESCRIPTIVE}
        if status == "confirmed" and not basis:
            errors.append(f"{where}: confirmed tags need a tag_basis")
        if status == "sourced" and not basis:
            errors.append(f"{where}: sourced tags need a tag_basis citing each source")
        if any(value and value != "unknown" for value in tags.values()) and not basis:
            errors.append(f"{where}: non-unknown tags need a tag_basis")
        if all(value == "unknown" for value in tags.values()) and status in ("confirmed", "sourced"):
            errors.append(f"{where}: {status} status with all tags unknown is contradictory")
        errors.extend(_vocal_claim_problem(vocals, basis, where))

        if status == "proposed":
            reviews.append(f"{where}: tag_status proposed, needs evidence or listening check")
        if "needs-review" in row.get("reuse_note", "").casefold():
            reviews.append(f"{where}: reuse_note needs a rights review")

    return errors, reviews


def validate_file(path: str) -> tuple[list[str], list[str], int]:
    try:
        with open(path, newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            if reader.fieldnames is None:
                return ["no header row found"], [], 0
            header = [name.strip() for name in reader.fieldnames]
            errors = [f"missing required column {name!r}" for name in REQUIRED_COLUMNS if name not in header]
            seen: dict[str, int] = {}
            for name in header:
                if name in seen:
                    errors.append(f"duplicate column {name!r}")
                else:
                    seen[name] = 1
            errors.extend(f"unexpected column {name!r}" for name in header if name not in REQUIRED_COLUMNS)
            rows = []
            extra_values: list[tuple[int, list[str]]] = []
            for lineno, raw in enumerate(reader, start=2):
                if raw.get(None):
                    extra_values.append((lineno, raw[None]))
                cleaned = {(key.strip() if key else ""): (value.strip() if value else "") for key, value in raw.items() if key}
                cleaned["_lineno"] = lineno
                rows.append(cleaned)
    except (OSError, UnicodeDecodeError) as exc:
        return [ReadError(f"cannot read file: {exc}")], [], 0
    if not rows:
        errors.append("no data rows found")
    for lineno, extra in sorted(extra_values):
        errors.append(f"row {lineno}: extra values without a column: {extra!r}")
    row_errors, reviews = validate_rows(rows)
    return errors + row_errors, reviews, len(rows)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate the M0 catalogue sample CSV.")
    parser.add_argument("path", help="path to catalog/m0-sample.csv")
    args = parser.parse_args(argv)
    errors, reviews, count = validate_file(args.path)
    if errors and isinstance(errors[0], ReadError):
        print(f"ERROR {errors[0]}")
        return 2
    for line in errors:
        print(f"ERROR {line}")
    for line in reviews:
        print(f"REVIEW {line}")
    if errors:
        print(f"checked {count} rows: {len(errors)} errors, {len(reviews)} need review")
        return 1
    print(f"OK checked {count} rows: {len(reviews)} need review")
    return 0


if __name__ == "__main__":
    sys.exit(main())
