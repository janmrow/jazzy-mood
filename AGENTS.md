# Project instructions

Deliver a small, useful album recommender that can run on the owner's existing Mikrus 2.1 at no additional operating cost. Write project material, UI copy and test examples in plain English.

Use Polish in conversation with the owner. Keep documentation, code, tests, UI copy and handoffs in plain English.

## Read on entry

1. [Backlog](docs/backlog.md) for the active milestone, ready work and dependencies.
2. [Delivery](docs/delivery.md) for task selection, checks, review, commits and handoff.
3. [Product](docs/product.md) and the relevant part of [quality](docs/quality.md) for acceptance criteria and evidence.
4. Read [architecture](docs/architecture.md), [decisions](docs/decisions.md), [operations](docs/operations.md) or [roadmap](docs/roadmap.md) when the work touches them.

## Working agreement

These rules guide the `delivery` agent. Reviewers use their own role instructions and the relevant project rules as review criteria.

- Implement the smallest complete change within the active milestone. Split larger work in the backlog. Keep the project usable and leave enough evidence for the next session to resume from Git and the backlog.
- Use Python, FastAPI, React, TypeScript, Vite, SQLite and Docker Compose. The app runs as one service and continues to recommend from its local catalogue with the decision provider disabled (local selection). Follow the architecture decisions. Ask the owner when a change requires a different stack, service, recurring cost, privacy boundary or product commitment.
- Derive tests from acceptance examples, contracts and failure modes. Only mark evidence you observed. Keep local and CI checks aligned. Routine checks use fixture data and a simulated provider.
- Preserve existing user changes. Use a local branch for delivery and stage only files for the current change. Local commits within the active milestone are authorized. The owner controls publishing, production access and milestone acceptance.
- Keep credentials and production configuration outside the project workspace used by coding agents. Keep visitor descriptions out of logs, stored catalogue data, fixtures and handoffs. Use only catalogue data with recorded provenance and suitable reuse terms.
- Keep each requirement in its named source. Link from the backlog and tests. Change product rules or acceptance expectations when the owner changes the requirement, and record the decision.

## Review roles

The `delivery` agent implements and coordinates. `quality-review` checks the change against the requirements and test evidence. `engineering-review` checks the effects on data, contracts, operations and the agreed architecture. Reviewers report findings from the proposed diff and do not edit it. See the [review rules](docs/delivery.md#3-review-rules) for when each role is required.
