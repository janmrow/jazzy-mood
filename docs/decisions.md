# Decisions

Record new decisions here when they materially change user behaviour, deployment, data handling or running cost. A short entry is enough. State the decision, the reason and the evidence that would change it. Mark proposals distinctly from adopted decisions.

## Adopted for the first release

| ID | Decision | Reason and revisit trigger |
|---|---|---|
| **D01** | Deliver one recommendation from an anonymous form. Use one album per result, linked out for listening. | A simple experience supports quick discovery and keeps scope small. Revisit the album boundary if M0 playtests strongly favour tracks. |
| **D02** | Use React, TypeScript and Vite for the frontend and Python with FastAPI for the backend. Ship one Compose service. | This exposes the browser/API boundary and supports the owner's learning goals while keeping the deployed topology small. Changes need a concrete product or operations reason. |
| **D03** | Use SQLite on local storage for the first release. | The small catalogue is read often and updated occasionally. This keeps data setup and recovery simple and still supports SQL and migrations. Revisit PostgreSQL if observed write contention, multiple instances or an agreed learning experiment warrants it. |
| **D04** | Use the existing Mikrus 2.1 and its named HTTPS subdomain. Design for zero incremental running cost. | Reuse paid-for capacity and validate deployment early. Consider an upgrade only after measuring headroom and identifying a bottleneck that needs it. A purchase is the owner's decision. |
| **D05** | Keep the catalogue and local matching sufficient on their own. A typed provider may improve intent understanding with one call per request. | The route still works when a provider is slow, unavailable or free quota ends. The backend can enforce catalogue membership, eligibility and intentional variation. |
| **D06** | Track requirements and progress in Git. Use one reviewer for ordinary behaviour changes and both for the first complete product slice or changes with larger consequences. The review table in `docs/delivery.md` governs which gate applies. | This keeps the agent autonomous and gives reviewers independent context where it is worth the cost. The [delivery pilot](delivery.md#pilot-the-harness) checks whether the workflow actually runs as intended. |
| **D07** | Build the app and its documentation in plain English. Track behaviour, tests and outcomes with a small set of stable criteria. | This makes the repo a useful portfolio piece and lets a fresh agent act on written evidence. Broader language support is evaluated from representative inputs. |

## To resolve with evidence

| ID | Open decision | How to decide |
|---|---|---|
| **E01** | Final catalogue boundary and useful coverage | M0 compares mood and intent coverage across about 30 records. Check rights and sourcing effort, how well the data supports tags, and whether the owner enjoys the picks. |
| **E02** | Whether to enable decision inference for visitors | M3 compares local and model-assisted picks on the same synthetic descriptions. Check fit, hard constraints, response time, terms for visitor text and actual free-plan behaviour. Enable the runtime provider only after the owner accepts the result. |
| **E03** | Runtime budgets for the actual VPS | M1 records basic headroom and public route behaviour. M4 verifies the release image, the latency baseline and the recovery steps. Change resources only in response to measured evidence. |

### Model options for E02

- **Clef Flash on Workers AI** is the first zero-cost candidate. [The model reference](https://developers.cloudflare.com/workers-ai/models/clef-flash/) documents typed choices and REST access. [Workers AI pricing](https://developers.cloudflare.com/workers-ai/platform/pricing/) lists a daily free allocation, and the [error reference](https://developers.cloudflare.com/workers-ai/platform/errors/) documents a quota response. Confirm the model and the free plan on the actual account before activation. Use a free configuration without paid overflow.
- **TypeSafe Jev** is a comparison candidate for typed decisions. [TypeSafe's model documentation](https://docs.typesafe.ai/introduction) explains its outputs. Its [direct pricing](https://help.typesafe.ai/articles/5187202169-how-much-does-jev-cost) meters input, and [Cloudflare documents billing for third-party models](https://developers.cloudflare.com/ai-gateway/usage/worker-binding-methods/). Use Jev for a separate, owner-authorized trial if it can answer a useful question. It is not a required cost of the release.
- **OpenCode and the coding model** are development tools. The user may select Muse Spark 1.3 Contributor in OpenCode if available from their provider. [Meta documents the Contributor terms](https://dev.meta.ai/docs/muse-spark). [OpenCode Console](https://opencode.ai/docs/console/api/inference/) reserves its free chat models for use within OpenCode. Keep runtime and development credentials and decisions independent.

Recheck provider terms and quotas at M3 before sending visitor text. For Cloudflare, start with [Workers AI data usage](https://developers.cloudflare.com/workers-ai/platform/data-usage/). Account configuration and the selected route determine what policies apply.
