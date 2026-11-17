# Catalogue trial

First trial of the catalogue sample against realistic requests. It maps to
the current `catalog/m0-sample.csv` slice (M0-001 to M0-012) and grows with
the sample. P02, P03, P04.

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

## Cases

1. Vague: `Something mellow for a late evening.` Several plausible picks
   exist (M0-001 and M0-011 are calm with a late-night mood; M0-010 is calm
   and dark). Any of them is a plausible pick (fit 1, tags proposed) with
   a reason citing the calm tag and the recorded mood.
2. Strict instrumental: `Instrumental only, steady groove for working.`
   Eligible on recorded tags: all six instrumentals (M0-001, M0-007, M0-008,
   M0-009, M0-010, M0-011). Best ranked are the four with a steady groove;
   M0-009 (broken) and M0-010 (free) stay eligible because groove is soft,
   but rank lower for this request. M0-005 and M0-006 are out (vocal samples
   count as vocal under the strict rule) and M0-012 is out (vocals
   unknown). The reason must cite the instrumental tag, not the mood alone.
3. Alternatives: `Energetic beats with grit.` M0-003 and M0-006 both fit
   plausibly (fit 1, tags proposed).
   `Try another` must switch from one to the other, since another eligible
   pick exists. P03.
4. Gap in era and style: `1960s bebop.` No eligible album. M0-001 is from
   1969 but is not bebop; the result must not stretch the label. Say so and
   suggest what the slice does cover. P04.
5. Gap in coverage: `A female vocal jazz singer.` No eligible album exists
   in this slice. Say so and help revise the description. P04.
6. Mood contrast: `Dark and driving for a night drive.` M0-009
   (energetic, dark, broken) fits; M0-006 fits the energy with a gritty
   rather than dark mood, a partial soft match to label plainly.
   M0-009 is the instrumental answer when vocals are excluded.
7. Unknown handling: for `Instrumental only`, M0-012 (Tourist, vocals
   unknown) must never be returned. Unknown is not a partial match for a
   hard constraint. P04.
8. Strictness check: `Pure instrumental hip-hop, no voices at all.` No
   eligible album in this slice: the two sample-based records carry vocal
   samples and are tagged vocal. Explain the strict reading instead of
   bending it. P04.

## Good and bad outcomes

- Good: `Calm instrumental for the morning.` returns M0-001 with a reason
  citing the calm tag, the late-night mood, the steady groove, and the
  proposed status of the tags.
- Bad: returning M0-002 (vocal) for `instrumental only` because its mood
  fits. Hard beats soft; this violates P04.
- Bad: repeating M0-003 on `Try another` when M0-006 also fits. This
  violates P03.
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

## M0 evidence so far

Validator run is clean for the 12-row slice with every row flagged for the
listening check. This trial is mapped but not yet run against the full
sample; boundaries and tag corrections stay open until M0-01 covers about
30 candidates and the owner completes the listening check.
