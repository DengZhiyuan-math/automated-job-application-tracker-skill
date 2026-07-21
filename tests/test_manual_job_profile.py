from __future__ import annotations

from pathlib import Path
import os
import subprocess
import sys
import tempfile
import textwrap
import unittest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))

from hermes.skills.manual_job_profile import build_profile, default_note_filename, infer_track, main, render_markdown


class ManualJobProfileTests(unittest.TestCase):
    def test_track_inference(self):
        self.assertEqual(infer_track("LLM agentic systems and RAG"), "AI/ML")
        self.assertEqual(infer_track("FX derivatives trading and volatility models"), "Quant")
        self.assertEqual(infer_track("scientific research thesis on algorithms"), "Research")
        self.assertEqual(infer_track("SQL dashboards and ETL reporting"), "Data Science")
        self.assertEqual(infer_track("teaching assistant for math"), "Education")
        self.assertEqual(infer_track("general operations role"), "Other")

    def test_render_contains_expected_sections(self):
        profile = build_profile(
            "LLM evaluation and agentic systems",
            company="Zenline AI",
            role="Founding Forward Deployed Engineer",
            status="applied",
            application_date="2026-07-16",
            notes="User said they applied.",
        )
        md = render_markdown(profile)
        self.assertIn("type: job_application", md)
        self.assertIn("# Zenline AI - Founding Forward Deployed Engineer", md)
        self.assertIn("## Snapshot", md)
        self.assertIn("## Job Description", md)
        self.assertIn("User said they applied.", md)
        self.assertIn("LLM evaluation and agentic systems", md)

    def test_default_filename_is_sanitized(self):
        profile = build_profile(
            "quant trading role",
            company="coni + partner",
            role="Quantitativer Analyst IB / Pricing Derivate",
            status="applied",
            application_date="2026-07-16",
        )
        self.assertEqual(
            default_note_filename(profile),
            "2026-07-16-coni-partner-quantitativer-analyst-ib-pricing-derivate.md",
        )

    def test_cli_writes_output_and_base(self):
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            src = td / "jd.txt"
            src.write_text("AI agents for engineering tools", encoding="utf-8")
            vault = td / "vault"
            env = os.environ.copy()
            env["PYTHONPATH"] = str(ROOT / "src")
            out = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "hermes.skills.manual_job_profile",
                    "--input",
                    str(src),
                    "--company",
                    "Jet Aviation",
                    "--role",
                    "AI Intern",
                    "--status",
                    "applied",
                    "--vault",
                    str(vault),
                ],
                cwd=ROOT,
                env=env,
                check=True,
                capture_output=True,
                text=True,
            )
            note_path = Path(out.stdout.strip())
            self.assertTrue(note_path.exists())
            self.assertIn("Jet Aviation", note_path.read_text(encoding="utf-8"))
            base = vault / "Hermes Job Tracker/Job Applications/Job Applications.base"
            self.assertTrue(base.exists())
            self.assertIn("All Applications", base.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
