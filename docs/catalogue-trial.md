# Catalogue trial

First trial of the catalogue sample against realistic requests. It maps to
the full M0 sample in `catalog/m0-sample.csv` (M0-001 to M0-030). P02, P03, P04.

## Terms

- `Eligible`: a catalogue album that passes every hard requirement of the
  request on its recorded tags. During the trial, proposed tags count;
  the listening check confirms them before any release use. Unknown never
  qualifies for a hard requirement.
- `Suitable`: an eligible album that also fits the soft preferences well
  on confirmed tags. This is the fit 2 outcome and needs the listening
  check behind it.
- `Plausible`: an eligible album whose fit rests on thin or partial
  evidence, including every match on proposed tags, which score at most
  fit 1. The listening check decides what becomes suitable.
- Fit scores follow the release rubric: 0 unsuitable, 1 plausible,
  2 strong. Until tags are confirmed, correct trial outcomes are plausible
  picks (fit 1), never claimed as strong.

All tags in the 30-row sample are `proposed`. Every reason below is
therefore a fit 1 claim that needs the owner listening check.

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
9. Strictness check: `Pure instrumental hip-hop, no voices at all.` No
   eligible album in this sample: the two sample-based records (M0-005,
   M0-006) carry vocal samples and are tagged vocal, and the uncertain
   sample-based record (M0-026) is unknown and therefore excluded. Explain
   the strict reading instead of bending it. P04.
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

## Owner feedback format

```text
input: <the exact description tried>
observed: <the album and reason shown>
expected: <the album or behaviour wanted>
impact: <what this changes: criterion, bug, or new work>
```

## Recommendation

Keep the album as the unit. The 30-row sample covers jazz rap,
sample-based instrumental hip-hop and groove-led jazz with enough
contrast for vague moods, strict instrumental filtering and repeat
picks on both the energetic and warm sides. That matches the product
direction for the first release.

Keep all 30 candidates for now. None is out of scope on style or era:
the 1969 record anchors the late-night mood, and the 1990s and 2000s
records carry the proposed discovery range. The two gaps above (1960s
bebop, female vocal jazz) are outside the agreed starting styles and do
not require new imports for M1.

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
Pytest reports `25 passed`. The trial above references M0-001 to M0-030.
Boundaries and tag corrections stay open until the owner completes the
listening check and accepts the catalogue boundary (E01).
