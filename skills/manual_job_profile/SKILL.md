---
name: manual_job_profile
description: "Manual job profile intake for Hermes Job Tracker: turn a pasted JD/profile into an Obsidian-ready application note and Bases database entry."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [job-tracking, obsidian, manual-intake, profile, jd, markdown, bases]
---

# Manual Job Profile Intake

Use this skill when a job application or role description is supplied manually instead of being extracted from email.

The canonical implementation lives in:
- `src/hermes/skills/manual_job_profile.py`
- CLI entrypoint: `manual-job-profile`
- Dispatcher: `src/hermes/skills/manual_job_profile.py`

## What it does

- Parses a pasted JD/profile or a text file
- Infers or accepts overrides for:
  - company
  - role title
  - status
  - track
  - source
  - location
  - deadline
  - contact
  - application date
- Renders an Obsidian-ready Markdown note
- Optionally writes the note into an Obsidian vault folder
- Optionally refreshes an Obsidian Bases `.base` file

## Primary usage

### From a saved file

```bash
python -m hermes.skills.manual_job_profile \
  --input job.md \
  --company "Harmattan AI" \
  --role "Deep Learning Intern" \
  --status applied \
  --vault "$HOME/Obsidian/Main"
```

### Fast path from pasted stdin

For the fastest write path, pipe the pasted JD/profile directly into the CLI and write into the vault in one step, avoiding a temporary file.

```bash
pbpaste | python -m hermes.skills.manual_job_profile \
  --status drafting \
  --vault "$HOME/Obsidian"
```

If you only want stdout and will paste the Markdown elsewhere yourself, omit `--vault`.

```bash
pbpaste | python -m hermes.skills.manual_job_profile \
  --status drafting
```

### Output modes

- `--vault <path>`: write the note into the vault folder and refresh the `.base` database
- `--output <path>`: write a single Markdown file explicitly
- neither option: print Markdown to stdout

## Defaults and conventions

- Default folder: `Hermes Job Tracker/Job Applications`
- Default `.base` file: `Job Applications.base`
- Default status: `drafting`
- Default source: `manual`
- Default application date: today

## Notes

- Prefer explicit overrides when the source text is incomplete.
- Keep status values aligned with the tracker’s allowed set.
- Preserve the raw JD/profile text in the note so later email updates can be matched against the same company-role pair.
- If the company name is not explicitly present, use `Unknown Company` instead of inferring from branding, logos, generic company descriptors, or search-engine snippets.
- If the user later clarifies the company name, update the existing note in place (company field, filename, title, and notes) rather than creating a second record.
- If the user says they already applied, set `status: applied`; otherwise keep the default `drafting` until application is confirmed.
- Prefer `Quant` when the role is primarily trading, portfolio construction, risk management, systematic investing, commodities, or market-structure work, even if the posting also mentions ML/AI or modeling.
- Prefer `AI/ML` when the role is centered on model development, applied ML, analytics, or LLM/agentic applications outside direct trading/portfolio/risk work.
- For hybrid seat titles like "Quant Researcher / ML Modelling / Algo Strategies", classify by the *primary economic loop*: if ideas become trades, optimizers, sizing, costs, or execution, keep `Quant`.
- Prefer direct stdin-to-vault writes for speed when the user pasted the JD in chat; avoid temp files unless they improve reviewability.
- Use a temp file only when the pasted JD needs cleaning, deduping, or a careful pre-save inspection.
- If the same company has multiple distinct roles, keep separate notes keyed by company-role pair rather than merging them into one company-only entry.
- For analytics/data-engineering roles, prefer `Data Science` when the core work is ETL/ELT, SQL+Python automation, BI dashboards, reporting, or finance/controlling analytics; reserve `Other` for generic ops/IT roles without a clear data/analytics function.
- Do not upgrade a role to `AI/ML` merely because it mentions AI tools; classify by the main workflow, not by buzzwords.
## Current references

- `references/manual_job_profile.md` — expanded usage guide, CLI options, note structure, and matching guidance.
- `references/manual_email_intake.md` — concise rules for email-sourced manual intake, explicit-applied handling, and conservative email-type classification.
- `references/manual_email_rejection_intake.md` — session-specific rejection-email update pattern and identifier-preservation notes.
- `references/manual_data_engineering_classification.md` — session notes on classifying ETL/BI/data-engineering roles and updating rejection follow-ups.
- `references/manual_intake_clarification_and_deduping.md` — session notes on late company-name clarification, duplicate avoidance, and conservative track selection.
- `references/company_inference_pitfall.md` — conservative rule for keeping `Unknown Company` when the employer is not explicit.

## Verification

After creating or editing the skill, confirm it appears in your local skill list.

If the code and the documentation diverge, treat `src/hermes/skills/manual_job_profile.py` as the source of truth.
