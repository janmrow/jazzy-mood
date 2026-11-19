"""Tests for the M0 catalogue sample validator.

Each test builds a small CSV fixture, so a failure points at the exact
check that broke. P02, P04.
"""

import textwrap

import pytest

from tools.validate_catalog import main, validate_file

HEADER = (
    "candidate_id,artist,title,year,identity_source,reuse_note,"
    "energy,mood,groove,vocals,tag_basis,tag_status"
)

GOOD_ROW = (
    "M0-001,Alice Coltrane,Journey in Satchidananda,1970,"
    "https://musicbrainz.org/release-group/example1,CC0 core data,"
    "calm,late-night;warm,steady,instrumental,"
    "Verified instrumental from liner notes,confirmed"
)


def write_csv(tmp_path, body):
    path = tmp_path / "sample.csv"
    path.write_text(textwrap.dedent(body), encoding="utf-8")
    return str(path)


def test_valid_catalogue_passes(tmp_path):
    path = write_csv(
        tmp_path,
        f"""\
        {HEADER}
        {GOOD_ROW}
        M0-002,The Heliocentrics,Out There,2007,https://example.org/source2,needs-review: blog scan,moderate,dark,broken,unknown,Proposed from a blog description; needs a listening check,proposed
        """,
    )
    errors, reviews, count = validate_file(path)
    assert errors == []
    assert count == 2
    assert any("M0-002" in line and "proposed" in line for line in reviews)
    assert any("M0-002" in line and "rights review" in line for line in reviews)


def test_missing_column_is_rejected(tmp_path):
    path = write_csv(tmp_path, "candidate_id,artist\nM0-001,Someone\n")
    errors, _, _ = validate_file(path)
    assert any("missing required column 'title'" in line for line in errors)


def test_blank_required_value_is_rejected(tmp_path):
    path = write_csv(
        tmp_path,
        f"""\
        {HEADER}
        M0-001,,Journey in Satchidananda,1970,https://example.org/s,CC0,calm,warm,steady,vocal,Heard singing,confirmed
        """,
    )
    errors, _, _ = validate_file(path)
    assert any("artist is blank" in line for line in errors)


@pytest.mark.parametrize(
    "column,value",
    [
        ("energy", "sleepy"),
        ("mood", "sleepy"),
        ("groove", "sleepy"),
        ("vocals", "sometimes"),
        ("tag_status", "maybe"),
    ],
)
def test_unknown_tag_values_are_rejected(tmp_path, column, value):
    fields = GOOD_ROW.split(",")
    index = HEADER.split(",").index(column)
    fields[index] = value
    path = write_csv(tmp_path, f"{HEADER}\n{','.join(fields)}\n")
    errors, _, _ = validate_file(path)
    assert any(column in line for line in errors)


def test_unknown_mixed_with_labels_is_rejected(tmp_path):
    fields = GOOD_ROW.split(",")
    fields[HEADER.split(",").index("mood")] = "unknown;warm"
    path = write_csv(tmp_path, f"{HEADER}\n{','.join(fields)}\n")
    errors, _, _ = validate_file(path)
    assert any("mixes 'unknown'" in line for line in errors)


def test_duplicate_ids_are_rejected(tmp_path):
    path = write_csv(tmp_path, f"{HEADER}\n{GOOD_ROW}\n{GOOD_ROW}\n")
    errors, _, _ = validate_file(path)
    assert any("duplicate candidate_id" in line for line in errors)


def test_bad_id_format_is_rejected(tmp_path):
    fields = GOOD_ROW.split(",")
    fields[HEADER.split(",").index("candidate_id")] = "bad id!"
    path = write_csv(tmp_path, f"{HEADER}\n{','.join(fields)}\n")
    errors, _, _ = validate_file(path)
    assert any("bad format" in line for line in errors)


def test_duplicate_albums_are_rejected(tmp_path):
    second = GOOD_ROW.replace("M0-001", "M0-009")
    path = write_csv(tmp_path, f"{HEADER}\n{GOOD_ROW}\n{second}\n")
    errors, _, _ = validate_file(path)
    assert any("duplicate album" in line for line in errors)


def test_duplicate_albums_ignore_case_and_space(tmp_path):
    second = GOOD_ROW.replace("M0-001,Alice Coltrane,Journey in Satchidananda", "M0-009,  alice coltrane ,journey in satchidananda ")
    path = write_csv(tmp_path, f"{HEADER}\n{GOOD_ROW}\n{second}\n")
    errors, _, _ = validate_file(path)
    assert any("duplicate album" in line for line in errors)


def test_bad_year_is_rejected(tmp_path):
    fields = GOOD_ROW.split(",")
    fields[HEADER.split(",").index("year")] = "1899"
    path = write_csv(tmp_path, f"{HEADER}\n{','.join(fields)}\n")
    errors, _, _ = validate_file(path)
    assert any("year" in line for line in errors)


def test_confirmed_without_basis_is_rejected(tmp_path):
    fields = GOOD_ROW.split(",")
    fields[HEADER.split(",").index("tag_basis")] = ""
    path = write_csv(tmp_path, f"{HEADER}\n{','.join(fields)}\n")
    errors, _, _ = validate_file(path)
    assert any("need a tag_basis" in line for line in errors)


def test_confirmed_all_unknown_is_contradictory(tmp_path):
    path = write_csv(
        tmp_path,
        f"""\
        {HEADER}
        M0-003,Quiet Band,Silence,unknown,https://example.org/s3,CC0,unknown,unknown,unknown,unknown,,confirmed
        """,
    )
    errors, _, _ = validate_file(path)
    assert any("contradictory" in line for line in errors)


def test_instrumental_with_vocal_basis_is_contradictory(tmp_path):
    fields = GOOD_ROW.split(",")
    fields[HEADER.split(",").index("tag_basis")] = "Features guest vocals in the second half"
    path = write_csv(tmp_path, f"{HEADER}\n{','.join(fields)}\n")
    errors, _, _ = validate_file(path)
    assert any("contradicts" in line for line in errors)


@pytest.mark.parametrize("basis", ["No vocal content; verified instrumental from liner notes", "Vocal-free mix confirmed by the label"])
def test_instrumental_with_no_vocal_basis_passes(tmp_path, basis):
    fields = GOOD_ROW.split(",")
    fields[HEADER.split(",").index("tag_basis")] = basis
    path = write_csv(tmp_path, f"{HEADER}\n{','.join(fields)}\n")
    errors, _, _ = validate_file(path)
    assert errors == []


def test_extra_values_without_column_are_rejected(tmp_path):
    path = write_csv(tmp_path, f"{HEADER}\n{GOOD_ROW},stray value\n")
    errors, _, _ = validate_file(path)
    assert any("extra values without a column" in line for line in errors)


def test_empty_file_is_rejected(tmp_path):
    path = write_csv(tmp_path, "")
    errors, _, _ = validate_file(path)
    assert errors != []


def test_header_only_is_rejected(tmp_path):
    path = write_csv(tmp_path, f"{HEADER}\n")
    errors, _, _ = validate_file(path)
    assert any("no data rows" in line for line in errors)


def test_cli_reports_ok_and_counts(tmp_path, capsys):
    path = write_csv(tmp_path, f"{HEADER}\n{GOOD_ROW}\n")
    assert main([path]) == 0
    assert "OK checked 1 rows" in capsys.readouterr().out


def test_cli_fails_on_errors(tmp_path):
    path = write_csv(tmp_path, f"{HEADER}\n{GOOD_ROW}\n{GOOD_ROW}\n")
    assert main([path]) == 1


def test_cli_missing_file_returns_two(capsys):
    assert main(["/tmp/does-not-exist-jazzy-mood.csv"]) == 2
    assert "cannot read" in capsys.readouterr().out


def test_empty_segments_are_rejected(tmp_path):
    fields = GOOD_ROW.split(",")
    fields[HEADER.split(",").index("mood")] = "warm;;dark"
    path = write_csv(tmp_path, f"{HEADER}\n{','.join(fields)}\n")
    errors, _, _ = validate_file(path)
    assert any("empty segment" in line for line in errors)


def test_trailing_separator_is_rejected(tmp_path):
    fields = GOOD_ROW.split(",")
    fields[HEADER.split(",").index("groove")] = "steady;"
    path = write_csv(tmp_path, f"{HEADER}\n{','.join(fields)}\n")
    errors, _, _ = validate_file(path)
    assert any("empty segment" in line for line in errors)


def test_duplicate_columns_are_rejected(tmp_path):
    path = write_csv(tmp_path, f"{HEADER},artist\n{GOOD_ROW},Someone\n")
    errors, _, _ = validate_file(path)
    assert any("duplicate column 'artist'" in line for line in errors)


def test_unexpected_column_is_rejected(tmp_path):
    path = write_csv(tmp_path, f"{HEADER},cover_art\n{GOOD_ROW},http://example.org/x\n")
    errors, _, _ = validate_file(path)
    assert any("unexpected column 'cover_art'" in line for line in errors)


@pytest.mark.parametrize("column", ["identity_source", "reuse_note"])
def test_blank_provenance_is_rejected(tmp_path, column):
    fields = GOOD_ROW.split(",")
    fields[HEADER.split(",").index(column)] = ""
    path = write_csv(tmp_path, f"{HEADER}\n{','.join(fields)}\n")
    errors, _, _ = validate_file(path)
    assert any(f"{column} is blank" in line for line in errors)


def test_proposed_without_basis_is_rejected(tmp_path):
    fields = GOOD_ROW.split(",")
    fields[HEADER.split(",").index("tag_basis")] = ""
    fields[HEADER.split(",").index("tag_status")] = "proposed"
    path = write_csv(tmp_path, f"{HEADER}\n{','.join(fields)}\n")
    errors, _, _ = validate_file(path)
    assert any("non-unknown tags need a tag_basis" in line for line in errors)


def test_instrumental_with_rap_basis_is_rejected(tmp_path):
    fields = GOOD_ROW.split(",")
    fields[HEADER.split(",").index("tag_basis")] = "Features rap verses throughout"
    path = write_csv(tmp_path, f"{HEADER}\n{','.join(fields)}\n")
    errors, _, _ = validate_file(path)
    assert any("contradicts" in line for line in errors)


def test_instrumental_with_denied_sample_basis_passes(tmp_path):
    fields = GOOD_ROW.split(",")
    fields[HEADER.split(",").index("tag_basis")] = "No samples; verified instrumental trio"
    path = write_csv(tmp_path, f"{HEADER}\n{','.join(fields)}\n")
    errors, _, _ = validate_file(path)
    assert errors == []
