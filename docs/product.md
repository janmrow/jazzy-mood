# Product

A visitor describes what they want to hear and gets one album they can listen to right away. The app should feel like a small, well-chosen record collection. A good recommendation makes sense for the request and can still be a surprise.

## First release

- One page, one text field, one result at a time. Visitors can use the page without an account. Keep the English interface clear and comfortable on a phone.
- Start with albums across jazz rap, instrumental hip-hop and groove-oriented jazz. Treat late 1990s and 2000s releases as a starting point for discovery. The M0 sample determines the useful boundaries. Switching to tracks or narrowing to a single subgenre is a product decision.
- The result shows the artist, album title, release year when verified, a short reason based on the catalogue, and a listening link. The app links out to listen. A clearly labelled search link is acceptable when a reliable direct link is unavailable.
- Run on the existing Mikrus 2.1 under an included HTTPS subdomain. The public release must work at zero additional operating cost, including with the decision provider disabled.
- The owner decides when the experience is good enough to share. Use the live demo and playtest feedback to decide where to invest next.

Account features, listening history, audio hosting, playlists and a catalogue editing UI are outside the first release.

## Acceptance criteria

Use these IDs in the backlog, test names or test descriptions when they clarify the expected result. Each milestone implements the subset named in its work items.

| ID | Expected behaviour | Example to check |
|---|---|---|
| **P01** | A visitor can describe a mood, a situation or a sound. The form accepts a nonblank description of up to 500 characters after trimming. Invalid input gets a clear message and never calls the provider. | Submit spaces. Then try `Late-night jazz with a steady beat and no vocals.` |
| **P02** | A successful response shows exactly one eligible catalogue album, with a reason supported by its attributes and a usable listening or search link. | The card presents a real artist and title. `Open listening link` points to the named service or clearly says it opens a search. |
| **P03** | `Try another` keeps the intent and avoids recently shown albums when another suitable pick exists. If the eligible choices run out, explain that and let the visitor change the request. | Get two distinct instrumental picks for the same request when the catalogue contains them. |
| **P04** | Match explicit supported constraints such as `no vocals` when the catalogue can satisfy them. If no eligible album exists, say so and help the visitor revise the description. For a broad mood, allow several plausible picks. | Exclude a vocal album for `instrumental only`, even if its energy and mood fit the request well. |
| **P05** | Show that the request is in progress and limit duplicate submissions in the page. On a recoverable error, keep the description and provide a way to retry. | Temporarily disconnect the app while submitting a request. The description is still there when the visitor tries again. |
| **P06** | When the decision provider is unavailable or disabled, the local catalogue still provides a suitable result for eligible requests within the response deadline. The numeric deadline is set at M3 (see E02/E03). | Simulate provider timeout or quota exhaustion for a description with a known local match. A single valid card appears. |
| **P07** | The form, messages, result and external link are usable at a narrow viewport and with a keyboard. Checked widths are recorded when M1-01 lands. Loading and errors can be understood without relying on colour alone. | Tab through the experience on a phone-sized viewport. Submit, read the status and reach the result or error. |
| **P08** | Keep use anonymous. Recent album IDs need only the current browser session. If the decision provider is enabled, tell the visitor that their description may go to the decision provider. The app keeps descriptions out of its persistent storage and logs. | Read the notice and check log and database output after a test submission that contains a made-up unique phrase. |

## Catalogue quality

Start with a sample of about 30 albums. Expand to a first useful catalogue of roughly 60–100 albums if the sample works, then work towards a few hundred when they add recommendation coverage. The measure of coverage is the range of requests that get several plausible results.

- Record a stable ID, artist, title, release year or an explicit unknown value, and a source for identity. Distinguish an original release from reissues and remove duplicates.
- Keep a small vocabulary for energy, mood, groove and vocal presence. Use unknown for missing evidence. Keep the basis for descriptive claims separate from identity metadata. A generated suggestion is a draft pending evidence or a listening check.
- Use an offline import and validation step. Research and model assistance can help collect and normalize candidates. The owner listens to a representative sample, including records the importer flagged, and decides whether the data supports the product.
- Record the source and reuse terms before including data in the release. Start from verified metadata and permitted metadata sources. Use artwork only after a rights decision.

[MusicBrainz's data licence](https://musicbrainz.org/doc/About/Data_License) distinguishes CC0 core data and separately licensed supplementary data. Follow its [API rate limits](https://musicbrainz.org/doc/MusicBrainz_API/Rate_Limiting) during any import. Check the terms of each additional source before using tags or other material.

## Review prompts

Try a quiet late-night mood, an energetic groove, a strong instrumental preference and a vague request. Ask for another after a good first pick. Look for places where the app loses the mood, overstates its knowledge, repeats an album or makes the listening link hard to find. Give the agent the observed outcome and what you expected.
