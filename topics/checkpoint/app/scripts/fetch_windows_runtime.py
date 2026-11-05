"""Download the reviewed Windows vendor runtime, checking every recorded hash."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys
import urllib.request

ROOT = Path(__file__).resolve().parents[1]


def main():
    sources = json.loads((ROOT / "design/windows-runtime-sources.json").read_text())
    runtime = ROOT / "build/windows-runtime"
    wheels = ROOT / "build/windows-wheels"
    runtime.mkdir(parents=True, exist_ok=True)
    wheels.mkdir(parents=True, exist_ok=True)
    python = sources["python"]
    target = runtime / "python-embed.zip"
    with urllib.request.urlopen(python["url"], timeout=120) as response:
        target.write_bytes(response.read(32 * 1024 * 1024))
    if hashlib.sha256(target.read_bytes()).hexdigest() != python["sha256"]:
        raise ValueError("Embedded Python checksum mismatch")
    (runtime / "source.json").write_text(json.dumps(python, indent=2))
    # Pin transitive dependencies too, rather than resolving today's latest versions.
    expected = sources["wheels"]
    pins = ["==".join(name.split("-")[:2]) for name in expected]
    requirements = runtime / "vendor-requirements.txt"
    requirements.write_text("\n".join(pins) + "\n")
    subprocess.run([
        sys.executable, "-m", "pip", "download", "--no-deps", "--only-binary=:all:",
        "--platform", "win_amd64", "--python-version", "313",
        "--implementation", "cp", "--abi", "cp313", "--abi", "abi3",
        "--dest", str(wheels), "-r", str(requirements),
    ], check=True)
    actual = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in wheels.glob("*.whl")}
    if actual != expected:
        raise ValueError("Windows wheel names or checksums differ from the reviewed runtime")
    print("Embedded Python and every Windows wheel match the reviewed hashes.")


if __name__ == "__main__":
    main()
