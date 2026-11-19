# Catalogue sample notes (M0)

Owner-facing schema note for `m0-sample.csv`. The canonical machine
rules live in `tools/validate_catalog.py`; this file states them in
plain language.

## Columns

`candidate_id`, `artist`, `title`, `year`, `identity_source`,
`reuse_note`, `energy`, `mood`, `groove`, `vocals`, `tag_basis`,
`tag_status`. All columns are required; no extra columns are accepted.

## Vocabulary

- `energy`: one of `calm`, `moderate`, `energetic`, `unknown`.
- `mood`: one or more of `late-night`, `warm`, `dark`, `bright`,
  `gritty`, `smooth`, `unknown`.
- `groove`: one or more of `steady`, `swung`, `broken`, `free`,
  `unknown`.
- `vocals`: one of `instrumental`, `vocal`, `unknown`.
- `tag_status`: `proposed` (draft pending evidence or a listening
  check), `sourced` (two independent reputable sources agree, or one
  strong source agrees with MusicBrainz identity — see D08), or
  `confirmed` (owner listening check on top of sources).

## Multi-tag convention

Use `;` between labels with no empty segments: `warm;gritty` is valid,
`warm;;dark`, leading `;warm` and trailing `warm;` are rejected.
`unknown` stands alone and is never combined with other labels.

## Hard rules for matching

- `instrumental` means strictly no vocal sound of any kind, including
  rap, sung or spoken parts, samples, dialogue, and backing vocals.
- `unknown` never satisfies a hard constraint such as `instrumental
  only` or `no vocals`.
- `tag_basis` records the evidence behind the descriptive tags and is
  required whenever any descriptive tag is not `unknown`. For `sourced`
  rows it cites each source (D08). A clean
  validator run means schema-clean only; release use requires
  `sourced` or `confirmed` tags, and `proposed` rows must never be
  promoted as ground truth.
