# Operations

The first release uses the owner's existing Mikrus 2.1 and an included named HTTPS subdomain. The target is zero additional operating cost. Production runs one versioned application image with persistent local storage. The owner controls server access, DNS actions and when a release is shared.

## Early deployment in M1

1. Check Docker Compose, host architecture, memory and disk availability on the actual VPS. The nominal plan has 1 GB of RAM and 10 GB of disk. Existing services and images also use those resources.
2. Build the release image locally or in CI for the VPS architecture. Tag it with a version or a commit ID. Start that image locally and check the form, API and `/healthz`. Use the same tagged image for the server smoke test.
3. Use one documented transfer path. A saved image archive transferred over SSH is sufficient for a first release and avoids depending on a registry. Load it on the VPS, start it with the Compose file and retain the tag of the previous usable version. Record the actual commands in this runbook when the image exists.
4. In the Mikrus panel, map a named subdomain to the chosen application port. Verify that the host port is available over IPv6 to the Mikrus proxy and that the public HTTPS link loads from another network. Mikrus manages the certificate for the included subdomain. Confirm any proxy settings that the app uses for request details.
5. Capture the release tag, URL, smoke test, app status, memory and disk observations. Run the app with local selection for this first check. Treat an unverified live step as open in the handoff.

See the [Mikrus offer](https://mikr.us/) and [subdomain setup guide](https://wiki.mikr.us/darmowa_subdomena_dla_vps/). Measure the actual VPS before deciding whether more capacity is needed.

## Runtime modes and controls

- Local mode is the default and requires no inference credentials. Keep deployment and provider settings outside source control. Keep live credentials away from the coding agents' workspace and put the true app credentials only in the runtime environment.
- Enable model mode after M3 establishes benefit, account availability, known terms for visitor text and a provider-enforced no-overspend boundary. Use a free setup with paid overflow disabled. Handle provider quota responses with local selection. Recheck the actual configuration if the account, model or plan changes.
- Bound request size, provider calls and concurrent work. Use one short provider deadline and at most one provider call per valid request. Apply a global cap before starting an external call. A per-client limit can be added once the proxy's client identity is understood. Use only forwarding information from the trusted ingress when computing it.
- Provide a setting for returning the app to local mode without code changes. Confirm that the site continues to recommend from the local catalogue when the provider is disabled or unreachable.
- Show visitors a short description of any external inference near the form before enabling it. Keep prompts, raw provider responses and credentials out of application logs and stored data. Review the host and any proxy logging separately before making privacy claims.

## Health and logs

- `/healthz` checks local readiness and works without the decision provider. A routine smoke check submits a synthetic description and verifies a valid result. Use the response and its request ID to follow a request through the app logs.
- Log structured events to stdout. Include timestamp, request ID, route, status and elapsed time. For recommendations, include the selection mode and a safe provider outcome such as `timeout`, `quota`, `invalid_response` or `disabled`. Keep full request URLs and descriptions out of these fields.
- Use a bounded Docker logging configuration from the first deployed version. [Docker documents the local driver and rotation](https://docs.docker.com/engine/logging/drivers/local/). Check size and retention on the VPS during M4. Review counts of failures, timeouts and fallbacks before adding monitoring services.

## Backup, restart and rollback

1. Keep the versioned catalogue source or import needed to rebuild SQLite and the image tag needed to run it. Store a consistent SQLite snapshot before catalogue migrations and keep a copy off the VPS on the owner's machine. Use [SQLite's backup mechanism](https://www.sqlite.org/backup.html) for a live database or stop writes before taking a file copy.
2. Restore into an isolated directory or test volume first. Check database integrity and schema version, inspect the expected catalogue version and exercise one recommendation. Record the source of the backup, how long the restore took and the result.
3. Restart the application with its persistent volume and exercise the form and links. Then deploy the prior image during a rollback rehearsal. Confirm schema compatibility first. If a migration makes the prior image incompatible, restore the matching snapshot before starting that image.
4. For a service incident, check `/healthz`, the latest local logs and VPS resource use. Switch to local selection when the provider is the problem. If the release is unhealthy, roll back to the known image and compatible data, then verify the live link again.

## Evidence before sharing

Keep the link, exact release tag, test results, observed resource headroom and restore or rollback notes together. Exercise the [quality playtest](quality.md#owner-playtest) and confirm the zero-cost path with inference disabled. If inference is enabled, confirm the applicable free limit and test the quota fallback. The owner releases the link after accepting the result.
