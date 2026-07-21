# Automated Job Application Tracker Skill

A general-purpose Codex skill that automatically organizes manually supplied job descriptions, recruiter notes, and application summaries into consistent, updateable Obsidian records.

This repository contains:

- A Codex skill definition and reference guide
- A command-line interface implemented with the Python standard library
- Obsidian Markdown and Bases generation logic
- Tests for track inference, Markdown rendering, file naming, and vault writes

> This public repository contains only the skill, implementation, and tests. It does not include personal inbox content, application-tracker data, or private vault exports.

## Features

- Read a job description or profile from a text file or standard input
- Record company, role, status, source, location, deadline, contact, and application date
- Infer an `AI/ML`, `Quant`, `Research`, `Data Science`, `Education`, or `Other` track from the source text
- Generate Obsidian Markdown with YAML Properties
- Write directly to an Obsidian vault and optionally refresh `Job Applications.base`
- Preserve the original job description for later email matching and record updates
- Run automatically through Codex or directly through the CLI

## Requirements

- Python 3.11 or later
- Optional: Obsidian, when writing to a vault or using Bases views

The CLI has no third-party runtime dependencies.

## Install for Codex

```bash
git clone https://github.com/DengZhiyuan-math/automated-job-application-tracker-skill.git
cd automated-job-application-tracker-skill

python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e .

mkdir -p "$HOME/.codex/skills"
ln -s "$(pwd)/skills/organize-job-applications" \
  "$HOME/.codex/skills/organize-job-applications"
```

Open a new Codex task, then invoke the skill explicitly:

```text
$organize-job-applications Organize this job description and record it in my Obsidian application tracker.
```

If the destination already exists, inspect it before removing or replacing the existing skill directory or symbolic link.

## Install the CLI

### Install from source

```bash
git clone https://github.com/DengZhiyuan-math/automated-job-application-tracker-skill.git
cd automated-job-application-tracker-skill

python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e .
```

Verify the installation:

```bash
manual-job-profile --help
```

You can also run the module without installing it:

```bash
PYTHONPATH=src python -m hermes.skills.manual_job_profile --help
```

## Quick start

### Generate Markdown from a saved job description

```bash
manual-job-profile \
  --input job.md \
  --company "Harmattan AI" \
  --role "Deep Learning Intern" \
  --status applied \
  --output ./job-notes/harmattan-ai-deep-learning-intern.md
```

### Write clipboard content to an Obsidian vault

On macOS:

```bash
pbpaste | manual-job-profile \
  --company "Harmattan AI" \
  --role "Deep Learning Intern" \
  --status drafting \
  --vault "$HOME/Obsidian/Main"
```

By default, the note is written under:

```text
<vault>/Hermes Job Tracker/Job Applications/
```

The command also creates or refreshes:

```text
<vault>/Hermes Job Tracker/Job Applications/Job Applications.base
```

Add `--no-base` to skip the Bases file.

### Print Markdown to stdout

When neither `--vault` nor `--output` is supplied, the generated Markdown is printed to standard output:

```bash
manual-job-profile \
  --input job.md \
  --company "Example Labs" \
  --role "Research Engineer"
```

## Output modes

| Option | Result |
| --- | --- |
| `--vault <path>` | Write under the selected vault folder and refresh the Bases file by default |
| `--output <path>` | Write one explicit Markdown file |
| Neither option | Print Markdown to standard output |

When `--output` and `--vault` are both supplied, the note is written to the explicit `--output` path. The Bases file is still refreshed under the vault unless `--no-base` is supplied.

## CLI options

| Option | Description | Default |
| --- | --- | --- |
| `--input` | Job description or profile text file; omit to read stdin | Standard input |
| `--vault` | Obsidian vault root | None |
| `--folder` | Target folder inside the vault | `Hermes Job Tracker/Job Applications` |
| `--output` | Explicit Markdown output path | None |
| `--no-base` | Skip the Bases file when writing to a vault | Disabled |
| `--company` | Company name | `Unknown Company` |
| `--role` | Role title | `Unknown Role` |
| `--status` | Application status | `drafting` |
| `--track` | Explicit role track; omit to infer it from the text | Inferred |
| `--source` | Source such as `manual`, `email`, or `linkedin` | `manual` |
| `--location` | Role location | `unknown` |
| `--deadline` | Application or assessment deadline | `unknown` |
| `--contact` | Recruiter or contact | `unknown` |
| `--application-date` | Application date | Current date |
| `--notes` | Initial content for Hermes Notes | Empty |

## Supported statuses

```text
drafting
applied
confirmation_received
waiting
recruiter_replied
interview_scheduled
assessment_pending
assessment_submitted
rejected
offer
withdrawn
no_response
```

Spaces in a status are normalized to underscores. Unsupported values cause the command to fail.

The following statuses set `needs_action: true`:

```text
drafting
waiting
recruiter_replied
interview_scheduled
assessment_pending
```

## Generated records

Each application note contains:

- Obsidian YAML Properties
- Company, role, status, track, date, source, location, and contact fields
- A `needs_action` flag
- `Snapshot`, `Next Action`, `Fit Notes`, and `Hermes Notes` sections
- The complete original job description or profile text

The default filename format is:

```text
YYYY-MM-DD-<company>-<role>.md
```

`Job Applications.base` defines `Active`, `Needs Action`, and `All Applications` table views.

## Codex skill

The skill entry point is:

```text
skills/organize-job-applications/SKILL.md
```

The detailed CLI reference is:

```text
skills/organize-job-applications/references/manual_job_profile.md
```

Keep `skills/organize-job-applications` intact and copy or link it under `~/.codex/skills/`. The skill calls the installed `manual-job-profile` command, so install the CLI as described above.

Generated Markdown retains compatibility fields such as `Hermes Notes` and `hermes/job-tracker` to avoid breaking existing Obsidian data.

## Project structure

```text
.
|-- skills/organize-job-applications/
|   |-- SKILL.md
|   |-- agents/openai.yaml
|   `-- references/manual_job_profile.md
|-- src/hermes/skills/manual_job_profile.py
|-- tests/test_manual_job_profile.py
|-- pyproject.toml
`-- README.md
```

## Development and testing

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
```

The test suite covers:

- Track inference
- Major Markdown sections
- Default filename sanitization
- CLI writes for both the application note and Obsidian Bases file

After changing the implementation, also inspect the CLI help:

```bash
PYTHONPATH=src python -m hermes.skills.manual_job_profile --help
```

## Data and privacy

The tool reads and writes local text only. It does not upload job descriptions, contacts, or application records. Do not commit real vault contents, inbox exports, access tokens, or generated records containing personal data to the public repository.

## Maintenance

The core implementation lives in `src/hermes/skills/manual_job_profile.py`. If the README, skill reference, and implementation disagree, treat the implementation and tests as authoritative, then update the documentation.

## License

The package metadata declares the project under the MIT License.
