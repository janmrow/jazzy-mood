# Roadmap

Each milestone ends in something the owner can try. The [backlog](backlog.md) holds the active milestone and the work for it. The [delivery workflow](delivery.md) covers the handoff between implementation and acceptance.

| Milestone | Deliverable | Owner acceptance |
|---|---|---|
| **M0 · Prove the catalogue** | About 30 candidates with traceable metadata and a small trial of what the catalogue can recommend. | Try a few mood descriptions, inspect representative sources, and choose the first catalogue boundary. Decide whether the album format still makes sense. |
| **M1 · Deliver the first link** | A working form, API and result from a test catalogue. First CI checks, one image, and an early HTTPS smoke test on Mikrus. | Open the supplied URL, submit a description, and see one result. Try the form on a phone and with a keyboard. Confirm basic resource headroom on the real VPS. |
| **M2 · Make it worth using** | A useful, validated SQLite catalogue with local matching, repeat handling and listening links. | Ask for similar alternatives and make a few contrasting requests. Check that the results respect explicit preferences. Confirm the app works with runtime inference disabled. |
| **M3 · Measure the model's value** | A comparison of local and typed model-assisted decisions, with failure handling and quota controls. | Compare picks for the same descriptions. Exercise timeout, bad responses and quota exhaustion. Decide whether to enable the free provider and agree what its notice should say. |
| **M4 · Release to friends** | A versioned release, operational checks, demonstrated recovery and clear instructions for keeping it running. | Try the deployment and recovery steps with the agent's evidence. Check the mobile experience, open the listening links and share the release when ready. |

The local recommendation path becomes useful at M2 and remains available for release if the model trial falls short. An approved free model can be enabled when it meets the criteria in [quality](quality.md) and [decisions](decisions.md).

After the first release, use feedback to select the next improvement. Expand music coverage where requests lack alternatives. Use deeper k6 or mutation testing when you can name the bottleneck or decision logic you want to investigate. Keep each experiment attached to a product or maintenance question.
