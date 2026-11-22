# Product

A visitor describes what they want to hear and gets one album they can listen to right away. The app should feel like a small, well-chosen record collection. A good recommendation makes sense for the request and can still be a surprise.

## First release

- One page, one text field, one result at a time. Visitors can use the page without an account. Keep the English interface clear and comfortable on a phone.
- Start with albums across jazz rap, instrumental hip-hop and groove-oriented jazz. Treat late 1990s and 2000s releases as a starting point for discovery. The M0 sample determines the useful boundaries. Switching to tracks or narrowing to a single subgenre is a product decision.
- The result shows the artist, album title, release year when verified, a short reason based on the catalogue, and a listening link. The app links out to listen. A clearly labelled search link is acceptable when a reliable direct link is unavailable. (M1 demo exception by owner decision: no link and no year until M2; see backlog M1-01i/M1-01j.)
- Run on the existing Mikrus 2.1 under an included HTTPS subdomain. The public release must work at zero additional operating cost, including with external inference disabled.
- The owner decides when the experience is good enough to share. Use the live demo and playtest feedback to decide where to invest next.

Account features, listening history, audio hosting, playlists and a catalogue editing UI are outside the first release.

## Acceptance criteria

Use these IDs in the backlog, test names or test descriptions when they clarify the expected result. Each milestone implements the subset named in its work items.

### Result terms

- `Eligible`: a catalogue album that passes every hard requirement of the request on its recorded tags. `Unknown` never qualifies for a hard requirement.
- `Suitable`: an eligible album that also fits the soft preferences well on confirmed tags. This is the fit 2 outcome. `Sourced` tags can reach fit 2; `proposed` matches score at most fit 1.
- `Plausible`: an eligible album whose fit rests on thin or partial evidence, including every match on proposed tags. Proposed matches score at most fit 1.
- Fit scores: 0 unsuitable, 1 plausible, 2 strong. Until tags are sourced, correct outcomes are plausible picks (fit 1), never claimed as strong.
- `Proposed` tags count for trial ranking so the sample can be exercised before confirmation. `Sourced` tags (D08: two independent reputable sources agree, or one strong source agrees with MusicBrainz identity, both cited in `tag_basis`) count for visitor-facing use and release data. `Confirmed` tags passed an owner listening check on top of sources. Every trial reason must state the tag status until confirmation lands.

| ID | Expected behaviour | Example to check |
|---|---|---|
| **P01** | A visitor can describe a mood, a situation or a sound. The form accepts a nonblank description of up to 500 characters after trimming. Invalid input gets a clear message and never calls the provider. | Submit spaces. Then try `Late-night jazz with a steady beat and no vocals.` |
| **P02** | A successful response shows exactly one eligible catalogue album, with a reason supported by its attributes and a usable listening or search link. (M1 demo exception: no link and no year; full card returns with the catalogue in M2.) | The card presents a real artist and title. `Open listening link` points to the named service or clearly says it opens a search. (M1 demo: no link shown.) |
| **P03** | `Try another` keeps the intent and avoids recently shown albums when another suitable pick exists. If the eligible choices run out, explain that and let the visitor change the request. (M1 demo exception: no second pick; the same entry repeats by design until M2-03.) | Get two distinct instrumental picks for the same request when the catalogue contains them. |
| **P04** | Match explicit supported constraints such as `no vocals` when the catalogue can satisfy them. If no eligible album exists, say so and help the visitor revise the description. For a broad mood, allow several plausible picks. | Exclude a vocal album for `instrumental only`, even if its energy and mood fit the request well. |
| **P05** | Show that the request is in progress and limit duplicate submissions in the page. On a recoverable error, keep the description and provide a way to retry. | Temporarily disconnect the app while submitting a request. The description is still there when the visitor tries again. |
| **P06** | When the decision provider is unavailable or disabled, the local catalogue still provides a suitable result for eligible requests within the response deadline. | Simulate provider timeout or quota exhaustion for a description with a known local match. A single valid card appears. |
| **P07** | The form, messages, result and external link are usable at a narrow viewport and with a keyboard. Loading and errors can be understood without relying on colour alone. | Tab through the experience on a phone-sized viewport. Submit, read the status and reach the result or error. |
| **P08** | Keep use anonymous. Recent album IDs need only the current browser session. If the decision provider is enabled, tell the visitor that their description may go to the decision provider. The app keeps descriptions out of its persistent storage and logs. | Read the notice and check log and database output after a test submission that contains a made-up unique phrase. |

### Hard and soft requirements (M0)

- Hard constraints must hold; otherwise there is no eligible result. The album must be in the catalogue with a recorded identity source. `No vocals` and `instrumental only` mean strictly no vocal sound of any kind, including rap, sung or spoken parts, samples, dialogue, and backing vocals. Only a vocals value of `instrumental` backed by evidence satisfies them. `Unknown` never satisfies a hard constraint. P02, P04.
- Soft preferences only rank eligible albums. Mood, energy, and groove order the candidates but never disqualify one alone, and the reason must reflect the tags actually present. A broad mood may leave several plausible picks. P02, P04.
- M0 adds no new matching dimensions. Genre switches, dates outside the sample, track-level picks, tempo, key, and other fine-grained features are non-binding context. Never claim they were matched.
- No basis, no claim. Never state that a requirement was met without catalogue evidence. A partial match concerns soft preferences only (for example, groove fits but energy unverified); label it plainly. For a hard constraint, an unknown value excludes the album and is never a partial match. For a no-match case, say so and help the visitor revise the description. P04.
- The M0 sample sets the working boundary; it can move after the M0 experiment and the owner's listening check (E01).

Representative cases: an `instrumental only` request with one mood-matching vocal album and one weaker instrumental album picks the instrumental, because hard beats soft; with only the vocal album it reports no eligible result. `A quiet rainy evening, some groove` allows several plausible picks with reasons citing the groove and mood tags present. `1960s bebop`, outside the sample boundary, reports no eligible result and names the boundary instead of stretching a label.

## Catalogue quality

Start with a sample of about 30 albums. Expand to a first useful catalogue of roughly 60–100 albums if the sample works, then work towards a few hundred when they add recommendation coverage. The measure of coverage is the range of requests that get several plausible results.

- Record a stable ID, artist, title, release year or an explicit unknown value, and a source for identity. Distinguish an original release from reissues and remove duplicates.
- Keep a small vocabulary for energy, mood, groove and vocal presence. Use unknown for missing evidence. Keep the basis for descriptive claims separate from identity metadata. A generated suggestion is a draft pending evidence or a listening check.
- Confirm tags from the source set in [decisions](decisions.md#catalogue-tag-sources-d08): `sourced` needs two agreeing independent sources (or one strong source plus MusicBrainz), each cited in `tag_basis`. One credible `vocal` mention beats three `instrumental` claims.
- Use an offline import and validation step. Research and source-backed collection replace full listening; the owner judges samples and boundary coverage instead of every record, with listening as sampling QC on import batches.
- Record the source and reuse terms before including data in the release. Start from verified metadata and permitted metadata sources. Use artwork only after a rights decision.

[MusicBrainz's data licence](https://musicbrainz.org/doc/About/Data_License) distinguishes CC0 core data and separately licensed supplementary data. Follow its [API rate limits](https://musicbrainz.org/doc/MusicBrainz_API/Rate_Limiting) during any import. Check the terms of each additional source before using tags or other material.

## Review prompts

Try a quiet late-night mood, an energetic groove, a strong instrumental preference and a vague request. Ask for another after a good first pick. Look for places where the app loses the mood, overstates its knowledge, repeats an album or makes the listening link hard to find. Give the agent the observed outcome and what you expected.
