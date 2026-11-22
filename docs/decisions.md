# Decisions

Record new decisions here when they materially change user behaviour, deployment, data handling or running cost. A short entry is enough. State the decision, the reason and the evidence that would change it. Mark proposals distinctly from adopted decisions.

## Adopted for the first release

| ID | Decision | Reason and revisit trigger |
| --- | --- | --- |
| **D01** | Deliver one recommendation from an anonymous form. Use one album per result, linked out for listening. (M1 demo exception by owner decision 2026-11-22: no link until M2-03.) | A simple experience supports quick discovery and keeps scope small. Revisit the album boundary if M0 playtests strongly favour tracks. |
| **D02** | Use React, TypeScript and Vite for the frontend and Python with FastAPI for the backend. Ship one Compose service. | This exposes the browser/API boundary and supports the owner's learning goals while keeping the deployed topology small. Changes need a concrete product or operations reason. |
| **D03** | Use SQLite on local storage for the first release. | The small catalogue is read often and updated occasionally. This keeps data setup and recovery simple and still supports SQL and migrations. Revisit PostgreSQL if observed write contention, multiple instances or an agreed learning experiment warrants it. |
| **D04** | Use the existing Mikrus 2.1 and its named HTTPS subdomain. Design for zero incremental running cost. | Reuse paid-for capacity and validate deployment early. Consider an upgrade only after measuring headroom and identifying a bottleneck that needs it. A purchase is the owner's decision. |
| **D05** | Keep the catalogue and local matching sufficient on their own. A typed provider may improve intent understanding with one call per request. | The route still works when a provider is slow, unavailable or free quota ends. The backend can enforce catalogue membership, eligibility and intentional variation. |
| **D06** | Track requirements and progress in Git. Use one reviewer for ordinary behaviour changes and both for the first complete product slice or changes with larger consequences. The review table in `docs/delivery.md` governs which gate applies. | This keeps the agent autonomous and gives reviewers independent context where it is worth the cost. The [delivery pilot](delivery.md#pilot-the-harness) checks whether the workflow actually runs as intended. |
| **D07** | Build the app and its documentation in plain English. Track behaviour, tests and outcomes with a small set of stable criteria. | This makes the repo a useful portfolio piece and lets a fresh agent act on written evidence. Broader language support is evaluated from representative inputs. |
| **D08** | Confirm catalogue tags from reputable sources instead of full listening. `sourced` means two independent reputable sources agree on the tag, or one strong source agrees with MusicBrainz identity; the owner accepted this threshold on 2026-11-19. Release and matching run on `sourced` tags; listening becomes sampling QC, not the gate. | Listening to hundreds of records does not scale to the 500-album target. Revisit if source agreement proves unreliable in sampling QC or if a source changes its terms. |

### Catalogue tag sources (D08)

Tags are confirmed from reputable sources; no full listening is required.
Each `sourced` tag cites its sources in `tag_basis`. The four approved
sources, all free of charge:

- **MusicBrainz** — identity (release-group URL, year) from CC0 core
  data; community tags and genre as corroboration only (supplementary
  data is CC BY-NC-SA, acceptable for this non-commercial project with
  attribution). Respect the [API rate limits](https://musicbrainz.org/doc/MusicBrainz_API/Rate_Limiting).
- **Discogs** — release titles, track listings, identifiers and
  **credits** are CC0 (credits settle the strict vocal rule); use the
  [monthly CC0 dumps](https://www.discogs.com/developers/) for bulk and
  the free API (token, 60 requests/minute authenticated) for spot
  checks. Do not store API content longer than necessary and never
  display content more than six hours old per the [API Terms of Use](https://support.discogs.com/hc/articles/360009334593-API-Terms-of-Use);
  style/genre fields have ambiguous licensing and count only as weak
  corroboration.
- **Last.fm API** — crowd tags (mood words) via the free API key, strictly
  non-commercial use with attribution and a link back per the [API Terms of Service](https://www.last.fm/api/tos);
  recontact Last.fm before any commercial use. No sub-licensing.
- **Wikipedia / Wikidata** — personnel facts for instrumental proof and
  years (Wikidata structured data is CC0; article text is CC BY-SA, so
  record facts with a link, never republish text).

Threshold: two independent reputable sources agree, or one strong source
(Discogs credits or monthly dump, Last.fm top tags, Wikipedia personnel)
agrees with MusicBrainz identity. Conflicts resolve strict: one credible
`vocal` mention beats three `instrumental` claims. Release and matching
run on `sourced` tags; listening is sampling QC on import batches, and
the M0 rows stay `proposed` until the M2-01 upgrade.

## To resolve with evidence

| ID | Open decision | How to decide |
| --- | --- | --- |
| **E01** | Final catalogue boundary and useful coverage | M0 compares mood and intent coverage across about 30 records. Check rights and sourcing effort, how well the data supports tags, and whether the owner enjoys the picks. |
| **E02** | Whether to enable decision inference for visitors | M3 compares local and provider-assisted picks on the same synthetic descriptions. Check fit, hard constraints, response time, terms for visitor text and actual free-plan behaviour. Enable the runtime provider only after the owner accepts the result. |
| **E03** | Runtime budgets for the actual VPS | M1 records basic headroom and public route behaviour, including the checked viewport widths. M3 sets the P06 response deadline value and the per-request caps. M4 verifies the release image, the latency baseline and the recovery steps, and sets the release latency threshold from that baseline. Change resources only in response to measured evidence. |

### Provider options for E02

- **Clef Flash on Workers AI** is the first zero-cost candidate. [The model reference](https://developers.cloudflare.com/workers-ai/models/clef-flash/) documents typed choices and REST access. [Workers AI pricing](https://developers.cloudflare.com/workers-ai/platform/pricing/) lists a daily free allocation, and the [error reference](https://developers.cloudflare.com/workers-ai/platform/errors/) documents a quota response. Confirm the model and the free plan on the actual account before activation. Use a free configuration without paid overflow.
- **TypeSafe Jev** is a comparison candidate for typed decisions. [TypeSafe's model documentation](https://docs.typesafe.ai/introduction) explains its outputs. Its [direct pricing](https://help.typesafe.ai/articles/5187202169-how-much-does-jev-cost) meters input, and [Cloudflare documents billing for third-party models](https://developers.cloudflare.com/ai-gateway/usage/worker-binding-methods/). Use Jev for a separate, owner-authorized trial if it can answer a useful question. It is not a required cost of the release.
- **OpenCode and the coding model** are development tools. The user may select Muse Spark 1.3 Contributor in OpenCode if available from their provider. [Meta documents the Contributor terms](https://dev.meta.ai/docs/muse-spark). [OpenCode Console](https://opencode.ai/docs/console/api/inference/) reserves its free chat models for use within OpenCode. Keep runtime and development credentials and decisions independent.

Recheck provider terms and quotas at M3 before sending visitor text. For Cloudflare, start with [Workers AI data usage](https://developers.cloudflare.com/workers-ai/platform/data-usage/). Account configuration and the selected route determine what policies apply.
