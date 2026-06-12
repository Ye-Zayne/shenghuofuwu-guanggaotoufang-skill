#!/usr/bin/env python3
"""Validate the public repository package for the life-service ad director skill."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "README.md",
    "SECURITY.md",
    "skill/SKILL.md",
    "skill/agents/openai.yaml",
    "skill/scripts/scaffold_project.py",
    "skill/scripts/subtitle_pipeline.py",
    "skill/scripts/asset_manifest.py",
    "skill/scripts/delivery_dashboard.py",
    "docs/QUICKSTART.md",
    "docs/CASE_INDEX.md",
    "docs/RELEASE_CHECKLIST.md",
]

REQUIRED_CASE_FILES = [
    "RESULTS.html",
    "RESULTS.md",
    "manifest.json",
    "99_执行状态.md",
    "04_60秒主广告脚本.md",
    "07A_完整执行脚本.md",
    "18_即梦批量生成任务表.csv",
    "20_剪映时间线.csv",
    "videos/manifest.md",
    "videos/dreamina_commands.sh",
]

BLOCKED_SUFFIXES = {".mp4", ".mov", ".m4v", ".avi", ".webm"}
SECRET_MARKERS = [
    "github" + "_pat_",
    "gh" + "p_",
    "gh" + "o_",
    "gh" + "u_",
    "gh" + "s_",
    "gh" + "r_",
]


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    sys.exit(1)


def check_required_files() -> None:
    for rel in REQUIRED_FILES:
        if not (ROOT / rel).exists():
            fail(f"missing required file: {rel}")


def check_cases() -> None:
    cases_dir = ROOT / "cases"
    if not cases_dir.exists():
        fail("missing cases/ directory")
    cases = [p for p in cases_dir.iterdir() if p.is_dir()]
    if not cases:
        fail("no case directories found")
    for case in cases:
        for rel in REQUIRED_CASE_FILES:
            if not (case / rel).exists():
                fail(f"{case.name} missing {rel}")


def check_no_blocked_large_media() -> None:
    for path in ROOT.rglob("*"):
        if ".git" in path.parts or not path.is_file():
            continue
        if path.suffix.lower() in BLOCKED_SUFFIXES:
            fail(f"blocked video file committed candidate: {path.relative_to(ROOT)}")
        if path.stat().st_size > 90 * 1024 * 1024:
            fail(f"file exceeds 90MB: {path.relative_to(ROOT)}")


def check_no_obvious_secrets() -> None:
    for path in ROOT.rglob("*"):
        if ".git" in path.parts or not path.is_file():
            continue
        if path.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp", ".gif"}:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for marker in SECRET_MARKERS:
            if marker in text:
                fail(f"possible secret marker {marker!r} in {path.relative_to(ROOT)}")


def check_script_help() -> None:
    scripts = [
        "skill/scripts/scaffold_project.py",
        "skill/scripts/subtitle_pipeline.py",
        "skill/scripts/asset_manifest.py",
        "skill/scripts/delivery_dashboard.py",
        "skill/scripts/auto_edit_preview.py",
    ]
    for rel in scripts:
        result = subprocess.run(
            [sys.executable, str(ROOT / rel), "--help"],
            cwd=ROOT,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
        )
        if result.returncode != 0:
            fail(f"{rel} --help failed: {result.stderr.strip()}")


def main() -> None:
    check_required_files()
    check_cases()
    check_no_blocked_large_media()
    check_no_obvious_secrets()
    check_script_help()
    print("OK: repository package validation passed")


if __name__ == "__main__":
    main()
