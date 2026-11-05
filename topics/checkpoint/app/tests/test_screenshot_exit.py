"""Regression for an observed native screenshot/shutdown lifetime crash."""
import os
from pathlib import Path
import subprocess
import sys


def test_native_screenshot_process_exits_cleanly(tmp_path):
    root=Path(__file__).resolve().parents[1];image=tmp_path/"native.png"
    env=os.environ.copy();env["QT_QPA_PLATFORM"]="offscreen";env["XDG_CACHE_HOME"]=str(tmp_path/"cache")
    result=subprocess.run([sys.executable,"-m","checkpoint.app","--no-setup","--screenshot",str(image),"--screenshot-delay","300"],cwd=root,env=env,capture_output=True,text=True,timeout=20)
    assert result.returncode==0,result.stderr
    assert image.is_file() and image.stat().st_size>10_000
