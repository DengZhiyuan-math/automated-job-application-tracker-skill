# Manual Job Profile Reference

This reference expands the manual job profile flow used by Hermes Job Tracker.
It is the canonical companion note for the `manual_job_profile` skill.

Source implementation:
- `src/hermes/skills/manual_job_profile.py`
- CLI entrypoint: `manual-job-profile`
- Dispatcher: `src/hermes/skills/manual_job_profile.py`

## Purpose

Use the manual profile flow when the job application is not fully recoverable from email.
Typical inputs include:
- a pasted job description
- a saved JD/profile text file
- a recruiter note with partial metadata
- a company-specific application summary

Hermes turns the input into:
- an Obsidian Markdown note
- optional Obsidian Bases metadata
- a consistent job-application record that can later be updated from email replies

## Example usage

### From a saved JD/profile file

```bash
python -m hermes.skills.manual_job_profile \
  --input job.md \
  --company "Harmattan AI" \
  --role "Deep Learning Intern" \
  --status applied \
  --vault "$HOME/Obsidian/Main"
```

### From pasted stdin

```bash
pbpaste | python -m hermes.skills.manual_job_profile \
  --status drafting \
  --folder "Hermes Job Tracker/Job Applications"
```

### Write to a specific Markdown file

```bash
python -m hermes.skills.manual_job_profile \
  --input job.md \
  --output ./job-notes/harmattan-ai-deep-learning-intern.md
```

## Supported CLI options

The parser in `manual_job_profile.py` accepts:

- `--input`: read JD/profile text from a file
- `--vault`: write into an Obsidian vault folder
- `--folder`: custom folder inside the vault
- `--output`: write one Markdown file directly
- `--no-base`: skip refreshing the Obsidian `.base` file
- `--company`: override company name
- `--role`: override role title
- `--status`: set application status
- `--track`: override track
- `--source`: set source, such as LinkedIn or company website
- `--location`: override location
- `--deadline`: set deadline or assessment due date
- `--contact`: recruiter/contact person
- `--application-date`: override the application date
- `--notes`: initial Hermes notes

## Default conventions

- Default folder: `Hermes Job Tracker/Job Applications`
- Default `.base` file: `Job Applications.base`
- Default status: `drafting`
- Default source: `manual`
- Default application date: today

## Status behavior

Allowed status values are enforced in the code. Common values include:
- `drafting`
- `applied`
- `confirmation_received`
- `waiting`
- `recruiter_replied`
- `interview_scheduled`
- `assessment_pending`
- `assessment_submitted`
- `rejected`
- `offer`
- `withdrawn`
- `no_response`

Statuses such as `drafting`, `recruiter_replied`, `interview_scheduled`, `assessment_pending`, and `follow_up_optional` are treated as needing action.

## Track inference

If `--track` is omitted, Hermes infers a track from the raw text.
Recognized values in the implementation include:
- AI/ML
- Quant
- Research
- Education
- Data Science
- Other

## Generated note structure

A generated note typically contains:

- YAML frontmatter for Obsidian Properties
- `type: job_application`
- company, role, status, track, date, and contact fields
- `needs_action`
- fit-score placeholders
- a next-action section
- the raw JD/profile text

## Generated Bases file

When `--vault` is used, Hermes also writes a `.base` file in the same folder.
The table views are meant to surface:
- Active applications
- Needs Action items
- All Applications

## Matching and deduping guidance

The manual profile flow preserves the raw JD/profile text so later emails can be matched back to the same company-role pair.
When new email messages arrive later, update the existing record instead of creating a duplicate entry.

## Source of truth

If documentation and code differ, treat the code as authoritative:
- `src/hermes/skills/manual_job_profile.py`

## Verification

After changes, confirm the skill is installed and visible.
