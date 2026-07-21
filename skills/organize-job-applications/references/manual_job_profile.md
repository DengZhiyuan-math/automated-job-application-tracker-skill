# Job Application Organizer Reference

Use this reference for exact CLI behavior. Treat `src/hermes/skills/manual_job_profile.py` as authoritative when working inside the repository.

## Input and output

Read input from `--input <file>` when provided; otherwise read standard input.

Choose one of these output modes:

| Mode | Behavior |
| --- | --- |
| `--vault <path>` | Write a generated note under the vault folder and refresh `Job Applications.base` |
| `--output <path>` | Write a generated note to one explicit path |
| Neither | Print the generated Markdown to stdout |

When both `--output` and `--vault` are supplied, write the note to `--output` and refresh the Bases file under the vault unless `--no-base` is supplied.

## CLI options

| Option | Purpose | Default |
| --- | --- | --- |
| `--input` | Source JD/profile file | stdin |
| `--vault` | Obsidian vault root | none |
| `--folder` | Folder inside the vault | `Hermes Job Tracker/Job Applications` |
| `--output` | Explicit Markdown output path | none |
| `--no-base` | Skip Bases refresh | false |
| `--company` | Company name | `Unknown Company` |
| `--role` | Role title | `Unknown Role` |
| `--status` | Application status | `drafting` |
| `--track` | Explicit role track | inferred |
| `--source` | Application source | `manual` |
| `--location` | Role location | `unknown` |
| `--deadline` | Application or assessment deadline | `unknown` |
| `--contact` | Recruiter or contact | `unknown` |
| `--application-date` | Application date | current date |
| `--notes` | Initial organizer notes | empty |

## Allowed statuses

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

The CLI normalizes spaces to underscores and rejects unsupported values.

The following statuses set `needs_action: true`:

- `drafting`
- `waiting`
- `recruiter_replied`
- `interview_scheduled`
- `assessment_pending`

## Track inference

The implementation recognizes these tracks:

- `AI/ML`
- `Quant`
- `Research`
- `Data Science`
- `Education`
- `Other`

Inference is keyword-based. Supply `--track` when context calls for a more reliable classification.

## Generated record

The note contains YAML properties, a snapshot, next action, fit notes, organizer notes, and the original job description. The default filename is:

```text
YYYY-MM-DD-<company>-<role>.md
```

The Bases file defines `Active`, `Needs Action`, and `All Applications` views.

## Privacy

Process records locally. Do not commit personal inbox exports, private Vault contents, tokens, or generated application notes containing personal data to the public repository.
