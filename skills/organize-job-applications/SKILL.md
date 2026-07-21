---
name: organize-job-applications
description: Organize and record job applications from pasted job descriptions, recruiter notes, saved text files, or application summaries. Use when Codex needs to create or update structured Obsidian job-application notes, keep a job tracker consistent, infer a role track, record application status, or generate an Obsidian Bases view through the manual-job-profile CLI.
---

# Organize Job Applications

Turn manually supplied job information into consistent, updateable application records.

## Workflow

1. Read the supplied JD, recruiter note, or application summary.
2. Extract explicit values for company, role, status, source, location, deadline, contact, and application date.
3. Keep missing company and role values as `Unknown Company` and `Unknown Role`; do not invent them from branding or search snippets.
4. Decide whether to update an existing company-role record before creating a new note.
5. Prefer an explicit track when the user provides one. Otherwise allow the CLI to infer it from the source text.
6. Run `manual-job-profile` with the appropriate input and output mode.
7. Report the written note path and whether `Job Applications.base` was refreshed.

## Choose an output mode

- Use `--vault <path>` to write into an Obsidian vault and refresh the Bases file.
- Use `--output <path>` to write one explicit Markdown file.
- Omit both to print Markdown to stdout for review.
- Add `--no-base` when the user does not want the Bases file updated.

Prefer stdout first when important metadata is ambiguous or the user wants to review the record. Prefer a direct vault write when the input is clear and the target vault is known.

## Run the CLI

From a saved file:

```bash
manual-job-profile \
  --input job.md \
  --company "Example Labs" \
  --role "Research Engineer" \
  --status applied \
  --vault "/path/to/vault"
```

From stdin:

```bash
pbpaste | manual-job-profile \
  --company "Example Labs" \
  --role "Research Engineer" \
  --status drafting \
  --vault "/path/to/vault"
```

If `manual-job-profile` is unavailable, tell the user to install this repository with `python -m pip install -e .`. Do not silently reimplement the renderer.

## Apply record rules

- Set `status: applied` only when the user says the application was submitted; otherwise retain `drafting`.
- Preserve the original JD/profile text for later matching and updates.
- Keep distinct roles at the same company as separate company-role records.
- Update an existing record in place when later information only clarifies the company, role, status, or contact.
- Prefer `Quant` for trading, portfolio, pricing, risk, market-structure, or execution work.
- Prefer `AI/ML` for model development, applied ML, LLM, or agentic work outside a direct trading loop.
- Prefer `Data Science` for ETL/ELT, SQL/Python automation, BI, dashboards, reporting, and analytics.
- Do not classify a role as `AI/ML` merely because it mentions AI tools.

## Verify

After writing a record:

- Confirm the Markdown file exists at the reported path.
- Confirm its YAML contains `type: job_application`, company, role, status, track, and `needs_action`.
- When using `--vault` without `--no-base`, confirm `Job Applications.base` exists in the tracker folder.
- Avoid printing private JD, contact, or Vault contents unless the user asks to inspect them.

Read [references/manual_job_profile.md](references/manual_job_profile.md) when exact CLI options, allowed statuses, defaults, or generated-note structure are needed.
