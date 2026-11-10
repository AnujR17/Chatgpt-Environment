#!/usr/bin/env python3
"""Local records for an agent-assisted job search. Python standard library only."""

import argparse
import hashlib
import html
import json
import os
from pathlib import Path
import re
import shutil
import sqlite3
import sys
import tempfile
from datetime import datetime, timezone
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit


DEFAULT_DATA = Path(__file__).resolve().parent / "private"
STATUSES = ("saved", "drafting", "ready", "applied", "screening", "interview",
            "offer", "rejected", "withdrawn")
DOCUMENTS = ("evaluation.md", "cv.md", "cover-letter.md", "interview.md")
REVIEWED = DOCUMENTS[:3]
CHECKS = ("factual_accuracy", "requirements_coverage", "no_placeholders")
PROFILE = {
    "name": "", "headline": "", "target_roles": [], "locations": [],
    "work_modes": [], "constraints": [], "facts": [],
}


def now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def digest(data):
    return hashlib.sha256(data).hexdigest()


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def text_value(value):
    return isinstance(value, str) and bool(value.strip())


def profile_errors(profile):
    if not isinstance(profile, dict):
        return ["Profile must be a JSON object."]
    errors = []
    if not text_value(profile.get("name")):
        errors.append("Add your name.")
    for field in ("target_roles", "locations"):
        items = profile.get(field)
        if not isinstance(items, list) or not items or not all(map(text_value, items)):
            errors.append(f"{field} must be a nonempty list of text values.")
    facts = profile.get("facts")
    if not isinstance(facts, list):
        return errors + ["facts must be a list."]
    ids = set()
    for fact in facts:
        if not isinstance(fact, dict):
            errors.append("Every fact must be an object.")
            continue
        fid = fact.get("id")
        if not isinstance(fid, str) or not re.fullmatch(r"F\d{3,}", fid) or fid in ids:
            errors.append("Each fact needs a unique ID such as F001.")
        elif fid:
            ids.add(fid)
        for field in ("claim", "source"):
            if not text_value(fact.get(field)):
                errors.append(f"Fact {fid}: add {field}.")
        if not isinstance(fact.get("confirmed"), bool):
            errors.append(f"Fact {fid}: confirmed must be true or false.")
    if not any(isinstance(f, dict) and f.get("confirmed") is True for f in facts):
        errors.append("Add at least one fact confirmed by the candidate.")
    return errors


def canonical_url(value):
    if not value:
        return ""
    parsed = urlsplit(value.strip())
    if parsed.scheme not in ("http", "https") or not parsed.hostname or parsed.username or parsed.password:
        raise ValueError("Use an http(s) posting URL without embedded credentials.")
    _ = parsed.port  # Validate port syntax even though the CLI does not fetch URLs.
    query = [(k, v) for k, v in parse_qsl(parsed.query, keep_blank_values=True)
             if not k.lower().startswith("utm_") and k.lower() not in ("gclid", "fbclid")]
    return urlunsplit((parsed.scheme.lower(), parsed.netloc.lower(), parsed.path or "/",
                       urlencode(sorted(query)), ""))


def connect(root):
    if not (root / "tracker.sqlite3").is_file():
        raise ValueError("Run init first.")
    db = sqlite3.connect(root / "tracker.sqlite3")
    db.row_factory = sqlite3.Row
    db.execute("PRAGMA foreign_keys = ON")
    return db


def get_job(db, job_id):
    if not re.fullmatch(r"[0-9a-f]{12}", job_id):
        raise ValueError("Use the full 12-character job ID returned by add or list.")
    row = db.execute("SELECT * FROM jobs WHERE id = ?", (job_id,)).fetchone()
    if row is None:
        raise ValueError(f"Unknown job: {job_id}")
    return dict(row)


def init(root):
    root.mkdir(parents=True, exist_ok=True, mode=0o700)
    if not (root / "profile.json").exists():
        write_json(root / "profile.json", PROFILE)
    (root / "packets").mkdir(exist_ok=True)
    with sqlite3.connect(root / "tracker.sqlite3") as db:
        db.executescript("""
            CREATE TABLE IF NOT EXISTS jobs (
                id TEXT PRIMARY KEY, company TEXT NOT NULL, role TEXT NOT NULL,
                url TEXT NOT NULL, posting TEXT NOT NULL, posting_sha256 TEXT NOT NULL,
                created_at TEXT NOT NULL, updated_at TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'saved', submitted_path TEXT
            );
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY, job_id TEXT NOT NULL REFERENCES jobs(id),
                at TEXT NOT NULL, status TEXT NOT NULL, note TEXT NOT NULL
            );
        """)
    return {"data_dir": str(root), "profile": str(root / "profile.json")}


def add_job(db, args):
    company, role = args.company.strip(), args.role.strip()
    posting = Path(args.posting).read_bytes().decode("utf-8")
    if not company or not role or not posting.strip():
        raise ValueError("Company, role and posting must not be empty.")
    url = canonical_url(args.url)
    posting_hash = digest(posting.encode("utf-8"))
    key = url or json.dumps([company.casefold(), role.casefold(), posting_hash])
    job_id = digest(key.encode("utf-8"))[:12]
    existing = db.execute("SELECT * FROM jobs WHERE id = ?", (job_id,)).fetchone()
    if existing:
        if existing["posting_sha256"] != posting_hash:
            raise ValueError("This posting URL is already saved with different text; original retained. "
                             "Use a distinct requisition URL for a different job.")
        return {"id": job_id, "duplicate": True, "status": existing["status"]}
    timestamp = now()
    with db:
        db.execute("INSERT INTO jobs (id, company, role, url, posting, posting_sha256, "
                   "created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                   (job_id, company, role, url, posting, posting_hash, timestamp, timestamp))
        db.execute("INSERT INTO events (job_id, at, status, note) VALUES (?, ?, 'saved', ?)",
                   (job_id, timestamp, "Posting imported; source text is untrusted data."))
    return {"id": job_id, "duplicate": False, "status": "saved"}


def prepare(db, root, job):
    profile = read_json(root / "profile.json")
    errors = profile_errors(profile)
    if errors:
        raise ValueError("Profile incomplete: " + " ".join(errors))
    destination = root / "packets" / job["id"]
    if destination.exists():
        raise ValueError("Packet already exists; edit it in place. Existing drafts were preserved.")
    staging = Path(tempfile.mkdtemp(prefix=".prepare-", dir=root / "packets"))
    try:
        write_json(staging / "profile.json", profile)
        write_json(staging / "job.json", {k: v for k, v in job.items() if k != "posting"})
        (staging / "posting.txt").write_text(job["posting"], encoding="utf-8")
        templates = {
            "evaluation.md": "# Role evaluation\n\n[[Map every stated requirement to confirmed fact IDs, an honest gap, or an unknown.]]\n\n[[Assess location, work authorization, seniority and other constraints. Give a reasoned recommendation; do not invent salary or fit percentages.]]\n",
            "cv.md": "# [[Candidate name]]\n\n[[Draft a tailored CV using only confirmed profile facts. Preserve employers, dates, credentials and metrics exactly.]]\n",
            "cover-letter.md": "[[Draft a concise letter linking confirmed experience to this role. Do not invent company research, motivations or achievements.]]\n",
            "interview.md": "# Interview preparation\n\n[[Create role-specific questions, evidence-based STAR story outlines, honest gap answers, and questions for the employer.]]\n",
        }
        for name, content in templates.items():
            (staging / name).write_text(content, encoding="utf-8")
        write_json(staging / "review.json", {
            "approved": False, "checks": {key: False for key in CHECKS},
            "claims": [], "notes": "",
            "sha256": {name: "" for name in (*REVIEWED, "profile.json", "posting.txt")},
        })
        staging.rename(destination)
    finally:
        if staging.exists():
            shutil.rmtree(staging)
    with db:
        db.execute("UPDATE jobs SET status = 'drafting', updated_at = ? WHERE id = ?", (now(), job["id"]))
        db.execute("INSERT INTO events (job_id, at, status, note) VALUES (?, ?, 'drafting', ?)",
                   (job["id"], now(), "Created packet with frozen profile and original posting."))
    return {"id": job["id"], "packet": str(destination), "status": "drafting",
            "note": "Templates only. Ask Codex to evaluate, draft and review this packet."}


def check_packet(root, job):
    packet = root / "packets" / job["id"]
    review = read_json(packet / "review.json")
    if not isinstance(review, dict):
        raise ValueError("review.json must be an object.")
    errors = []
    if review.get("approved") is not True:
        errors.append("Review is not approved.")
    checks = review.get("checks")
    if not isinstance(checks, dict) or any(checks.get(key) is not True for key in CHECKS):
        errors.append("Complete every review check.")
    profile = read_json(packet / "profile.json")
    errors.extend(profile_errors(profile))
    if errors:
        raise ValueError(" ".join(errors))
    facts = {f["id"] for f in profile["facts"] if f.get("confirmed") is True}
    contents = {}
    hashes = review.get("sha256")
    if not isinstance(hashes, dict):
        raise ValueError("Review sha256 must be an object.")
    for name in (*REVIEWED, "profile.json", "posting.txt"):
        content = (packet / name).read_bytes()
        if hashes.get(name) != digest(content):
            errors.append(f"Review hash does not match {name}; review the current file.")
        if name in REVIEWED:
            contents[name] = content.decode("utf-8")
            if not contents[name].strip() or re.search(r"\[\[.*?\]\]", contents[name], re.S):
                errors.append(f"Finish {name}; it is empty or contains placeholders.")
    if digest((packet / "posting.txt").read_bytes()) != job["posting_sha256"]:
        errors.append("Packet posting differs from the originally saved posting.")
    claims = review.get("claims")
    if not isinstance(claims, list) or not claims:
        errors.append("Add a claim-to-fact audit to review.json.")
    else:
        for claim in claims:
            if not isinstance(claim, dict):
                errors.append("Each audited claim must be an object.")
                continue
            document, quote, ids = claim.get("document"), claim.get("quote"), claim.get("fact_ids")
            if document not in REVIEWED or not text_value(quote) or quote not in contents.get(document, ""):
                errors.append("Every audited claim needs an exact quote from a reviewed document.")
            if not isinstance(ids, list) or not ids or any(not isinstance(fid, str) or fid not in facts for fid in ids):
                errors.append("Every audited claim must cite confirmed fact IDs from the packet profile.")
    if errors:
        raise ValueError(" ".join(errors))
    return {"id": job["id"], "review_valid": True,
            "note": "Structure, references and hashes checked. Factual truth still depends on the review."}


def set_status(db, root, job, status, note):
    submitted = job["submitted_path"]
    if status == "ready":
        check_packet(root, job)
    if status == "applied" and submitted is None:
        if job["status"] != "ready":
            raise ValueError("Mark a reviewed packet ready before recording an application as sent.")
        check_packet(root, job)
        destination = root / "submitted" / job["id"]
        destination.parent.mkdir(exist_ok=True)
        if destination.exists():
            raise ValueError("A submission snapshot already exists; it was preserved. Reconcile the tracker before retrying.")
        shutil.copytree(root / "packets" / job["id"], destination)
        submitted = str(destination.relative_to(root))
    timestamp = now()
    with db:
        db.execute("UPDATE jobs SET status = ?, updated_at = ?, submitted_path = ? WHERE id = ?",
                   (status, timestamp, submitted, job["id"]))
        db.execute("INSERT INTO events (job_id, at, status, note) VALUES (?, ?, ?, ?)",
                   (job["id"], timestamp, status, note))
    return {"id": job["id"], "status": status, "submitted_path": submitted}


def report(db, root):
    rows = db.execute("SELECT id, company, role, status, url, updated_at FROM jobs ORDER BY updated_at DESC").fetchall()
    # No remote scripts, assets or raw URLs: report content is escaped local text.
    parts = ["<!doctype html><html lang='en'><meta charset='utf-8'>",
             "<meta name='viewport' content='width=device-width,initial-scale=1'>",
             "<meta http-equiv='Content-Security-Policy' content=\"default-src 'none'; style-src 'unsafe-inline'\">",
             "<title>My job search</title><style>body{font:16px system-ui;background:#f5f5f0;color:#172b26;max-width:1100px;margin:40px auto;padding:0 20px}table{border-collapse:collapse;width:100%;background:white}td,th{padding:14px;text-align:left;border-bottom:1px solid #ddd;overflow-wrap:anywhere}div{overflow-x:auto}p{color:#52635e}</style>",
             "<h1>My job search</h1>", f"<p>{len(rows)} saved roles · Generated {html.escape(now())} (UTC)</p>",
             "<div><table><thead><tr><th>ID</th><th>Company</th><th>Role</th><th>Status</th><th>Updated (UTC)</th></tr></thead><tbody>"]
    for row in rows:
        parts.append("<tr>" + "".join(f"<td>{html.escape(str(row[key]))}</td>"
                                    for key in ("id", "company", "role", "status", "updated_at")) + "</tr>")
    parts.append("</tbody></table></div></html>")
    path = root / "report.html"
    path.write_text("\n".join(parts), encoding="utf-8")
    return {"report": str(path), "jobs": len(rows)}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", type=Path, default=DEFAULT_DATA,
                        help="Local data directory; custom paths must be kept out of Git yourself.")
    commands = parser.add_subparsers(dest="command", required=True)
    for name in ("init", "profile-check", "list", "report"):
        commands.add_parser(name)
    add = commands.add_parser("add", help="Import plain UTF-8 posting text; does not fetch URLs.")
    add.add_argument("--company", required=True)
    add.add_argument("--role", required=True)
    add.add_argument("--posting", required=True)
    add.add_argument("--url", default="")
    for name in ("show", "prepare", "check", "status"):
        sub = commands.add_parser(name)
        sub.add_argument("id")
        if name == "status":
            sub.add_argument("status", choices=STATUSES)
            sub.add_argument("--note", default="")
    args = parser.parse_args(argv)
    os.umask(0o077)
    root = args.data_dir.expanduser().resolve()
    db = None
    try:
        if args.command == "init":
            result = init(root)
        elif args.command == "profile-check":
            errors = profile_errors(read_json(root / "profile.json"))
            if errors:
                raise ValueError(" ".join(errors))
            result = {"profile_valid": True}
        else:
            db = connect(root)
            if args.command == "add":
                result = add_job(db, args)
            elif args.command == "list":
                result = [dict(row) for row in db.execute(
                    "SELECT id, company, role, status, updated_at FROM jobs ORDER BY updated_at DESC, id")]
            elif args.command == "report":
                result = report(db, root)
            else:
                job = get_job(db, args.id)
                if args.command == "show":
                    result = {**job, "events": [dict(row) for row in db.execute(
                        "SELECT at, status, note FROM events WHERE job_id = ? ORDER BY id", (args.id,))]}
                elif args.command == "prepare":
                    result = prepare(db, root, job)
                elif args.command == "check":
                    result = check_packet(root, job)
                else:
                    result = set_status(db, root, job, args.status, args.note)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (OSError, ValueError, sqlite3.Error) as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 1
    finally:
        if db is not None:
            db.close()


if __name__ == "__main__":
    sys.exit(main())
