# Catalogue trial

First trial of the catalogue sample against realistic requests. It maps to
the full M0 sample in `catalog/m0-sample.csv` (M0-001 to M0-030). P02, P03, P04.

## Terms

Result terms (`Eligible`, `Suitable`, `Plausible`, fit 0–2, `proposed` vs
`confirmed`) follow [product](product.md#result-terms). Trial-specific
rules: proposed tags count for ranking here, so every correct outcome
below is a fit 1 claim that needs the owner listening check; `unknown`
never qualifies for a hard requirement.

## Cases

1. Vague: `Something mellow for a late evening.` Several plausible picks
   exist. M0-001 and M0-011 are calm with a late-night mood and a steady
   groove; M0-023 is calm and dark with a steady groove; M0-030 is calm
   and warm with a steady groove. Any of them is a plausible pick
   (fit 1, tags proposed) with a reason citing the calm tag and the
   recorded mood. Uncertain: whether M0-030 feels mellow enough with
   vocals; needs the listening check.
2. Strict instrumental: `Instrumental only, steady groove for working.`
   Eligible on recorded tags: all 13 instrumentals (M0-001, M0-007,
   M0-008, M0-009, M0-010, M0-011, M0-019, M0-020, M0-021, M0-022,
   M0-023, M0-024, M0-025). Best ranked are the 10 with a steady groove;
   M0-009 (broken) and M0-010 and M0-020 (free) stay eligible because
   groove is soft, but rank lower for this request. Vocal rows are out,
   including sample-based M0-005 and M0-006 where vocal samples count as
   vocal under the strict rule. Unknown rows M0-012 and M0-026 are out.
   The reason must cite the instrumental tag, not the mood alone. P04.
3. Alternatives, energetic grit: `Energetic beats with grit.` Four
   plausible picks exist in the full sample (M0-003, M0-006, M0-013,
   M0-020 all carry energetic energy with a gritty mood). `Try another`
   must switch to a different eligible pick while the intent stays the
   same, since other eligible picks exist. P03. Uncertain: whether M0-020
   feels like beats or live-band funk; needs the listening check.
4. Alternatives, warm vocal groove: `Something warm with vocals for the
   daytime.` Several plausible picks include M0-004, M0-014, M0-028 and
   M0-030 (all carry a warm mood with vocal presence; other warm vocal
   rows such as M0-002 and M0-027 also exist). `Try another` must
   again move to another eligible pick. This pair of alternative cases
   shows the full sample supports repeats on both the energetic and the
   warm side. P03.
5. Gap in era and style: `1960s bebop.` No eligible album. M0-001 is from
   1969 but is not bebop; the result must not stretch the label. Say so and
   suggest what the sample does cover (1990s and 2000s groove, jazz rap
   and instrumental funk). P04.
6. Gap in coverage: `A female vocal jazz singer.` No eligible album exists
   in the 30-row sample. The sample records no documented female vocal
   jazz record. Say so and help revise the description. P04.
7. Mood contrast: `Dark and driving for a night drive.` M0-009
   (energetic, dark, broken, instrumental) fits; M0-017 (energetic, dark,
   broken, vocal) fits with vocals; M0-008 (moderate, dark, steady,
   instrumental) is a calmer instrumental option. M0-009 is the
   instrumental answer when vocals are excluded. All fit 1 until the
   listening check. Uncertain: whether M0-017 reads as driving or as
   drum-and-bass pressure; needs the listening check.
8. Unknown handling: for `Instrumental only`, M0-012 (Tourist, vocals
   unknown) and M0-026 (Madlib, vocals unknown) must never be returned.
   Unknown is not a partial match for a hard constraint. P04.
9. Strictness check: `Pure instrumental hip-hop, no voices at all.` This
   is a combined request: it asks for the sample-based hip-hop subset of
   the catalogue AND zero voices. No eligible album exists for that
   combination: the two sample-based records (M0-005, M0-006) carry vocal
   samples and are tagged vocal, and the uncertain sample-based record
   (M0-026) is unknown and therefore excluded. (A plain `instrumental`
   request is broader: all 13 instrumentals satisfy it.) Explain the
   strict reading instead of bending it. P04.
10. Soft preference: `Smooth and steady, nothing harsh.` Plausible picks
    include M0-024 (smooth, steady, instrumental) and M0-029 (smooth,
    steady, vocal). M0-015 is smooth but swung, so it stays eligible only
    as a lower-ranked option when steady is read as a soft preference, and
    its reason must cite the swung groove honestly. The reason should name
    the smooth tag and the recorded groove, and say the tags are proposed.
    Uncertain: whether smooth means the same across funk and rap records;
    needs the listening check.

## Good and bad outcomes

- Good: `Calm instrumental for the morning.` returns M0-001 with a reason
  citing the calm tag, the late-night mood, the steady groove, and the
  proposed status of the tags.
- Bad: returning M0-002 (vocal) for `instrumental only` because its mood
  fits. Hard beats soft; this violates P04.
- Bad: repeating M0-003 on `Try another` when M0-006 and M0-013 also fit.
  This violates P03.
- Bad: justifying a pick with `because it is from 1969`. The year does not
  support a mood claim; the reason must rest on catalogue tags. This
  violates P02.
- Bad: recommending an album that is not in the catalogue. Only catalogue
  rows are eligible. This violates P02.

## Owner next steps

1. Listen to the 10 cases above; priority rows are M0-005, M0-006 and
   M0-026 (vocal presence on sample-based records) and M0-012 (unknown
   vocals). Confirm or correct each proposed tag.
2. Spot-check 2–3 identity sources (MusicBrainz links in
   `catalog/m0-sample.csv`) and years, including the 1969 anchor M0-001.
3. Record each correction with the feedback format below (input,
   observed, expected, impact).
4. Decide the catalogue boundary (E01): keep the 1969 record and the
   edge rows in scope, call pure instrumental hip-hop the first widening
   priority, and confirm bebop and female vocal jazz stay out of scope.
5. Accept the milestone by saying `I accept M0. Start M1.` No release use
   may consume `proposed` rows as truth; M2-01 must enforce
   `confirmed`-only imports.

## Owner feedback format

```text
input: <the exact description tried>
observed: <the album and reason shown>
expected: <the album or behaviour wanted>
impact: <what this changes: criterion, bug, or new work>
```

## Recommendation

Keep the album as the unit. The 30-row sample covers jazz rap,
sample-based hip-hop with strict vocal tagging, and groove-led
jazz and funk with enough contrast for vague moods, strict
instrumental filtering and repeat picks on both the energetic and
warm sides. That matches the product direction for the first release.
Note the limit inside that coverage: no pure sample-based
instrumental hip-hop is eligible (M0-005 and M0-006 are tagged vocal
for vocal samples, M0-026 is unknown), so that narrow request still
has no match in case 9.

Keep all 30 candidates for now. None is out of scope on style or era:
the 1969 record anchors the late-night mood, and the 1990s and 2000s
records carry the proposed discovery range. The three gaps above
(1960s bebop, female vocal jazz, pure instrumental hip-hop) need an
explicit boundary call: the first two sit outside the agreed starting
styles and do not require new imports for M1, while the third sits
inside the starting styles and sets the first widening priority after
the listening check. Repeat depth is strong for energetic grit and
warm vocal requests but thinner for late-night-only, smooth-only,
free-groove or swung requests, so do not claim broad repeat coverage
beyond the tested cases.

Before widening the import, improve the data in this order: first
complete the owner listening check on all proposed tags, with strict
attention to vocal presence on sample-based records (M0-005, M0-006,
M0-026) and on M0-012; second confirm years and identity sources for
the rows the owner spot-checks; third keep the `;` multi-tag convention
and the unknown handling unchanged so the future importer stays simple.
Do not add listening links or artwork to the sample until reuse terms
for those fields are decided.

## M0 evidence so far

Validator run is clean for the 30-row sample with every row flagged for
the listening check: `python3 tools/validate_catalog.py
catalog/m0-sample.csv` reports `OK checked 30 rows: 30 need review`.
A clean validator run means schema-clean only; it says nothing about
musical truth. Pytest reports `34 passed`. The trial above references
M0-001 to M0-030. Boundaries and tag corrections stay open until the
owner completes the listening check and accepts the catalogue boundary
(E01). Release use requires `confirmed` tags; `proposed` rows must never
be promoted as ground truth, and M2-01 must enforce that gate.
