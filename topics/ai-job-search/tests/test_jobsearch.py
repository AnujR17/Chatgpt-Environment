"""Behavior checks with fictional candidate data in disposable directories."""

import argparse
import contextlib
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import jobsearch as app


class JobSearchTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "data"
        app.init(self.root)
        self.db = app.connect(self.root)
        self.addCleanup(self.db.close)
        self.posting = Path(self.temp.name) / "posting.txt"
        self.posting.write_text("Build Python reporting tools. Remote role.\n", encoding="utf-8")
        self.profile = {
            "name": "Fictional Candidate", "headline": "Engineer",
            "target_roles": ["Backend engineer"], "locations": ["Remote"],
            "work_modes": ["remote"], "constraints": [],
            "facts": [{"id": "F001", "claim": "Built a Python reporting tool.",
                       "source": "Fictional candidate confirmation for test.", "confirmed": True}],
        }

    def add(self, **changes):
        fields = {"company": "Example Co", "role": "Engineer", "posting": str(self.posting),
                  "url": "https://example.com/jobs/42"}
        fields.update(changes)
        return app.add_job(self.db, argparse.Namespace(**fields))

    def prepare(self):
        app.write_json(self.root / "profile.json", self.profile)
        added = self.add()
        job = app.get_job(self.db, added["id"])
        app.prepare(self.db, self.root, job)
        return app.get_job(self.db, job["id"])

    def complete_review(self, job):
        packet = self.root / "packets" / job["id"]
        documents = {
            "evaluation.md": "Python tooling: direct evidence F001. Location: remote.\n",
            "cv.md": "# Fictional Candidate\n\nBuilt a Python reporting tool.\n",
            "cover-letter.md": "Dear hiring team,\n\nBuilt a Python reporting tool.\n",
        }
        for name, content in documents.items():
            (packet / name).write_text(content, encoding="utf-8")
        review = {
            "approved": True, "checks": {key: True for key in app.CHECKS},
            "claims": [{"document": name, "quote": "Built a Python reporting tool.", "fact_ids": ["F001"]}
                       for name in ("cv.md", "cover-letter.md")],
            "sha256": {name: app.digest((packet / name).read_bytes())
                       for name in (*app.REVIEWED, "profile.json", "posting.txt")},
            "notes": "Fictional data checked for test.",
        }
        app.write_json(packet / "review.json", review)
        return packet

    def test_end_to_end_review_submission_history_and_report(self):
        job = self.prepare()
        self.assertEqual(job["status"], "drafting")
        packet = self.complete_review(job)
        self.assertTrue(app.check_packet(self.root, job)["review_valid"])
        app.set_status(self.db, self.root, job, "ready", "Reviewed drafts")
        job = app.get_job(self.db, job["id"])
        app.set_status(self.db, self.root, job, "applied", "Candidate confirmed sent")
        job = app.get_job(self.db, job["id"])
        submitted = self.root / job["submitted_path"]
        original = (submitted / "cv.md").read_bytes()
        (packet / "cv.md").write_text("Later edits", encoding="utf-8")
        app.set_status(self.db, self.root, job, "interview", "Recruiter confirmed")
        self.assertEqual((submitted / "cv.md").read_bytes(), original)
        self.assertEqual(app.get_job(self.db, job["id"])["status"], "interview")
        history = self.db.execute("SELECT status FROM events ORDER BY id").fetchall()
        self.assertEqual([r[0] for r in history], ["saved", "drafting", "ready", "applied", "interview"])
        report = app.report(self.db, self.root)
        self.assertEqual(report["jobs"], 1)
        self.assertIn("interview", Path(report["report"]).read_text(encoding="utf-8"))

    def test_blank_profile_saves_job_but_cannot_prepare(self):
        job = app.get_job(self.db, self.add()["id"])
        with self.assertRaisesRegex(ValueError, "Profile incomplete"):
            app.prepare(self.db, self.root, job)
        self.assertFalse((self.root / "packets" / job["id"]).exists())

    def test_init_and_prepare_preserve_existing_edits(self):
        job = self.prepare()
        packet = self.root / "packets" / job["id"]
        (packet / "cv.md").write_text("Keep my draft", encoding="utf-8")
        app.init(self.root)
        self.assertEqual(app.read_json(self.root / "profile.json"), self.profile)
        with self.assertRaisesRegex(ValueError, "already exists"):
            app.prepare(self.db, self.root, job)
        self.assertEqual((packet / "cv.md").read_text(encoding="utf-8"), "Keep my draft")

    def test_url_deduplication_retains_requisition_ids(self):
        first = self.add(url="https://EXAMPLE.com/jobs?id=42&utm_source=mail#apply")
        duplicate = self.add(url="https://example.com/jobs?fbclid=abc&id=42")
        other = self.add(url="https://example.com/jobs?id=43")
        self.assertEqual(first["id"], duplicate["id"])
        self.assertTrue(duplicate["duplicate"])
        self.assertNotEqual(first["id"], other["id"])
        self.assertEqual(self.db.execute("SELECT count(*) FROM events").fetchone()[0], 2)

    def test_changed_posting_cannot_overwrite_original(self):
        job_id = self.add()["id"]
        before = self.posting.read_text(encoding="utf-8")
        self.posting.write_text("Different description", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "different text"):
            self.add()
        self.assertEqual(app.get_job(self.db, job_id)["posting"], before)

    def test_no_url_import_is_idempotent(self):
        first = self.add(url="")
        duplicate = self.add(url="")
        self.assertEqual(first["id"], duplicate["id"])
        self.assertTrue(duplicate["duplicate"])

    def test_posting_snapshot_preserves_unicode_and_original_line_endings(self):
        original = "Données et Python.\r\nRemote role.\r\n".encode("utf-8")
        self.posting.write_bytes(original)
        job = self.prepare()
        packet = self.root / "packets" / job["id"]
        self.assertEqual((packet / "posting.txt").read_bytes(), original)
        self.assertEqual(job["posting_sha256"], app.digest(original))

    def test_ready_rejects_templates_and_empty_audit(self):
        job = self.prepare()
        with self.assertRaisesRegex(ValueError, "not approved"):
            app.set_status(self.db, self.root, job, "ready", "")
        packet = self.complete_review(job)
        review = app.read_json(packet / "review.json")
        review["claims"] = []
        app.write_json(packet / "review.json", review)
        with self.assertRaisesRegex(ValueError, "claim-to-fact audit"):
            app.check_packet(self.root, job)
        self.assertEqual(app.get_job(self.db, job["id"])["status"], "drafting")

    def test_review_invalidates_after_draft_or_source_changes(self):
        job = self.prepare()
        packet = self.complete_review(job)
        (packet / "cv.md").write_text("Unsupported new assertion", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "hash does not match cv.md"):
            app.check_packet(self.root, job)
        self.complete_review(job)
        (packet / "posting.txt").write_text("Changed requirements", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "originally saved"):
            app.check_packet(self.root, job)

    def test_review_rejects_unknown_and_unconfirmed_fact_ids(self):
        self.profile["facts"].append({"id": "F002", "claim": "Unconfirmed skill.",
                                      "source": "Draft CV", "confirmed": False})
        job = self.prepare()
        packet = self.complete_review(job)
        review = app.read_json(packet / "review.json")
        for ids in (["F999"], ["F002"], [{"bad": "object"}]):
            with self.subTest(ids=ids):
                review["claims"][0]["fact_ids"] = ids
                app.write_json(packet / "review.json", review)
                with self.assertRaisesRegex(ValueError, "confirmed fact IDs"):
                    app.check_packet(self.root, job)

    def test_applied_requires_ready_and_checks_latest_drafts(self):
        job = self.prepare()
        with self.assertRaisesRegex(ValueError, "Mark a reviewed packet ready"):
            app.set_status(self.db, self.root, job, "applied", "")
        packet = self.complete_review(job)
        app.set_status(self.db, self.root, job, "ready", "")
        (packet / "cv.md").write_text("Unreviewed edit", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "hash does not match"):
            app.set_status(self.db, self.root, app.get_job(self.db, job["id"]), "applied", "")
        self.assertFalse((self.root / "submitted" / job["id"]).exists())

    def test_report_escapes_untrusted_fields(self):
        self.add(company="<script>alert('x')</script>", role="R&D <Engineer>")
        result = app.report(self.db, self.root)
        content = Path(result["report"]).read_text(encoding="utf-8")
        self.assertNotIn("<script>", content)
        self.assertIn("&lt;script&gt;", content)
        self.assertIn("R&amp;D &lt;Engineer&gt;", content)

    def test_invalid_inputs_do_not_produce_tracebacks(self):
        for value in ("../profile", "a" * 100, "000000000000"):
            with self.subTest(id=value):
                with self.assertRaises(ValueError):
                    app.get_job(self.db, value)
        for url in ("file:///etc/passwd", "https://user:password@example.com/jobs", "https://example.com:bad/jobs"):
            with self.subTest(url=url):
                with self.assertRaises(ValueError):
                    app.canonical_url(url)
        job = self.prepare()
        packet = self.complete_review(job)
        for content in ([], None, {"approved": True, "checks": []}):
            app.write_json(packet / "review.json", content)
            err = io.StringIO()
            with contextlib.redirect_stderr(err):
                code = app.main(["--data-dir", str(self.root), "check", job["id"]])
            self.assertEqual(code, 1)
            self.assertIn("error", json.loads(err.getvalue()))

    def test_profile_validation_rejects_bad_or_duplicate_facts(self):
        self.profile["facts"].append(dict(self.profile["facts"][0]))
        self.assertTrue(any("unique ID" in e for e in app.profile_errors(self.profile)))
        self.profile["facts"] = [{"id": [], "confirmed": "yes"}]
        self.assertTrue(app.profile_errors(self.profile))
        self.assertTrue(app.profile_errors([]))

    def test_cli_works_from_another_directory_and_returns_json(self):
        process = subprocess.run([sys.executable, str(Path(app.__file__).resolve()),
                                  "--data-dir", str(self.root), "list"],
                                 cwd=self.temp.name, capture_output=True, text=True, check=True)
        self.assertEqual(json.loads(process.stdout), [])


if __name__ == "__main__":
    unittest.main()
