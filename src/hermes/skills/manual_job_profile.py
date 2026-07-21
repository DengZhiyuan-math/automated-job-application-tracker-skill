"""Hermes manual job profile skill.

This module renders a structured job application note from a pasted
job description or partial application metadata.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
import re
import sys
from typing import Iterable

ALLOWED_STATUSES = {
    "drafting",
    "applied",
    "confirmation_received",
    "waiting",
    "recruiter_replied",
    "interview_scheduled",
    "assessment_pending",
    "assessment_submitted",
    "rejected",
    "offer",
    "withdrawn",
    "no_response",
}

ACTION_STATUSES = {
    "drafting",
    "waiting",
    "recruiter_replied",
    "interview_scheduled",
    "assessment_pending",
}

DEFAULT_FOLDER = "Hermes Job Tracker/Job Applications"
DEFAULT_BASE = "Job Applications.base"


@dataclass(slots=True)
class JobProfile:
    company: str = "Unknown Company"
    role: str = "Unknown Role"
    status: str = "drafting"
    track: str = "Other"
    source: str = "manual"
    location: str = "unknown"
    deadline: str = "unknown"
    contact: str = "unknown"
    application_date: str = ""
    notes: str = ""
    raw_text: str = ""
    output: str = ""

    @property
    def needs_action(self) -> bool:
        return self.status in ACTION_STATUSES

    @property
    def email_type(self) -> str:
        return self.source if self.source in {"manual", "email", "linkedin", "company_website"} else "manual"


def _slugify(value: str, fallback: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = re.sub(r"-+", "-", value).strip("-")
    return value or fallback


def _quoted(v: str | bool | int) -> str:
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, int):
        return str(v)
    text = str(v)
    text = text.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{text}"'


def _yaml_lines(profile: JobProfile) -> list[str]:
    return [
        "---",
        "type: job_application",
        f"company: {_quoted(profile.company)}",
        f"role_title: {_quoted(profile.role)}",
        f"status: {_quoted(profile.status)}",
        f"current_status: {_quoted(profile.status)}",
        f"track: {_quoted(profile.track)}",
        f"application_date: {_quoted(profile.application_date or 'unknown')}",
        f"needs_action: {_quoted(profile.needs_action)}",
        f"location: {_quoted(profile.location)}",
        f"source: {_quoted(profile.source)}",
        'url: ""',
        f"deadline: {_quoted(profile.deadline)}",
        f"contact: {_quoted(profile.contact)}",
        'contact_email: "unknown"',
        f"email_type: {_quoted(profile.email_type)}",
        'resume_version: ""',
        "referral_used: false",
        "cover_letter_used: false",
        "math_relevance: 3",
        "ai_relevance: 3",
        "finance_relevance: 1",
        "strategic_value: 3",
        'visa_risk: "unknown"',
        "tags:",
        "  - hermes/job-tracker",
        "  - job/application",
        f"  - track/{_slugify(profile.track, 'other')}",
        "---",
    ]


def infer_track(text: str) -> str:
    t = text.lower()
    ai_score = sum(k in t for k in ["llm", "agentic", "agent", "machine learning", "deep learning", "rag", "nlp", "foundation model", "ai"])
    quant_score = sum(k in t for k in ["quant", "trading", "derivative", "derivatives", "fx", "volatility", "hedging", "portfolio", "risk", "alpha", "pricing"])
    research_score = sum(k in t for k in ["research", "scientist", "thesis", "phd", "lab", "experimental", "publication", "algorithm"])
    education_score = sum(k in t for k in ["teacher", "teaching", "tutor", "education", "student learning", "curriculum"])
    ds_score = sum(k in t for k in ["data science", "data scientist", "etl", "data engineering", "analytics", "sql", "dashboard", "reporting", "data pipeline"])

    scores = {
        "AI/ML": ai_score,
        "Quant": quant_score,
        "Research": research_score,
        "Education": education_score,
        "Data Science": ds_score,
    }
    best = max(scores, key=scores.get)
    if scores[best] <= 0:
        return "Other"
    # break ties by preferred ordering
    ordered = ["AI/ML", "Quant", "Research", "Data Science", "Education"]
    max_score = max(scores.values())
    for key in ordered:
        if scores[key] == max_score:
            return key
    return best


def parse_application_date(value: str | None) -> str:
    if not value:
        return date.today().isoformat()
    return value


def normalize_status(value: str) -> str:
    status = (value or "drafting").strip().lower().replace(" ", "_")
    if status not in ALLOWED_STATUSES:
        raise ValueError(f"Unsupported status: {value}")
    return status


def build_profile(
    raw_text: str,
    *,
    company: str | None = None,
    role: str | None = None,
    status: str = "drafting",
    track: str | None = None,
    source: str = "manual",
    location: str = "unknown",
    deadline: str = "unknown",
    contact: str = "unknown",
    application_date: str | None = None,
    notes: str = "",
) -> JobProfile:
    company = company or "Unknown Company"
    role = role or "Unknown Role"
    status = normalize_status(status)
    application_date = parse_application_date(application_date)
    track = track or infer_track(raw_text or f"{company} {role}")
    return JobProfile(
        company=company,
        role=role,
        status=status,
        track=track,
        source=source,
        location=location,
        deadline=deadline,
        contact=contact,
        application_date=application_date,
        notes=notes,
        raw_text=raw_text.strip(),
    )


def render_markdown(profile: JobProfile) -> str:
    lines = _yaml_lines(profile)
    body = [
        "",
        f"# {profile.company} - {profile.role}",
        "",
        "## Snapshot",
        "",
        f"- Status: `{profile.status}`",
        f"- Track: `{profile.track}`",
        f"- Location: {profile.location}",
        f"- Source: {profile.source}",
        f"- Email type: {profile.email_type}",
        f"- Application date: {profile.application_date}",
        f"- Deadline: {profile.deadline}",
        f"- Contact: {profile.contact}",
        "- Contact email: unknown",
        "- URL: none",
        "",
        "## Next Action",
        "",
        "- Wait for confirmation or recruiter response." if profile.status == "applied" else ("- None required." if not profile.needs_action else "- Follow up."),
        "",
        "## Fit Notes",
        "",
        "- Math relevance: 3/5",
        "- AI relevance: 3/5",
        "- Finance relevance: 1/5",
        "- Strategic value: 3/5",
        "- Visa risk: unknown",
        "- Resume version: ",
        "- Referral: ",
        "",
        "## Hermes Notes",
        "",
        profile.notes or "Manual job profile generated from pasted text.",
        "",
        "## Job Description",
        "",
        profile.raw_text or "",
    ]
    return "\n".join(lines + body).rstrip() + "\n"


def default_note_filename(profile: JobProfile) -> str:
    return f"{profile.application_date}-{_slugify(profile.company, 'unknown-company')}-{_slugify(profile.role, 'unknown-role')}.md"


BASE_FILE_CONTENT = """filters:
  and:
    - file.ext == \"md\"
    - file.inFolder(\"Hermes Job Tracker/Job Applications\")
    - type == \"job_application\"
properties:
  company:
    displayName: Company
  role_title:
    displayName: Role
  status:
    displayName: Status
  track:
    displayName: Track
  application_date:
    displayName: Applied
  needs_action:
    displayName: Needs Action
  deadline:
    displayName: Deadline
  source:
    displayName: Source
  location:
    displayName: Location
  resume_version:
    displayName: Resume
views:
  - type: table
    name: Active
    filters:
      and:
        - status != \"withdrawn\"
        - status != \"offer\"
    order:
      - file.name
      - company
      - role_title
      - status
      - track
      - application_date
      - deadline
      - needs_action
    sort:
      - property: status
        direction: ASC
      - property: track
        direction: ASC
  - type: table
    name: Needs Action
    filters:
      and:
        - needs_action == true
    order:
      - file.name
      - company
      - role_title
      - status
      - deadline
      - contact
  - type: table
    name: All Applications
    order:
      - file.name
      - company
      - role_title
      - status
      - track
      - application_date
      - source
      - location
"""


def write_note(profile: JobProfile, output: Path, *, write_base: bool = False, vault_root: Path | None = None) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_markdown(profile), encoding="utf-8")
    if write_base and vault_root is not None:
        base_path = vault_root / DEFAULT_FOLDER / DEFAULT_BASE
        base_path.parent.mkdir(parents=True, exist_ok=True)
        base_path.write_text(BASE_FILE_CONTENT, encoding="utf-8")
    return output


def _read_input(path: str | None) -> str:
    if path:
        return Path(path).read_text(encoding="utf-8")
    return sys.stdin.read()


def build_arg_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="manual-job-profile")
    p.add_argument("--input")
    p.add_argument("--vault")
    p.add_argument("--folder", default=DEFAULT_FOLDER)
    p.add_argument("--output")
    p.add_argument("--no-base", action="store_true")
    p.add_argument("--company")
    p.add_argument("--role")
    p.add_argument("--status", default="drafting")
    p.add_argument("--track")
    p.add_argument("--source", default="manual")
    p.add_argument("--location", default="unknown")
    p.add_argument("--deadline", default="unknown")
    p.add_argument("--contact", default="unknown")
    p.add_argument("--application-date")
    p.add_argument("--notes", default="")
    return p


def main(argv: Iterable[str] | None = None) -> int:
    args = build_arg_parser().parse_args(list(argv) if argv is not None else None)
    raw = _read_input(args.input)
    profile = build_profile(
        raw,
        company=args.company,
        role=args.role,
        status=args.status,
        track=args.track,
        source=args.source,
        location=args.location,
        deadline=args.deadline,
        contact=args.contact,
        application_date=args.application_date,
        notes=args.notes,
    )

    if args.output:
        output = Path(args.output)
    elif args.vault:
        output = Path(args.vault) / args.folder / default_note_filename(profile)
    else:
        sys.stdout.write(render_markdown(profile))
        return 0

    write_note(profile, output, write_base=bool(args.vault and not args.no_base), vault_root=Path(args.vault) if args.vault else None)
    sys.stdout.write(str(output) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
