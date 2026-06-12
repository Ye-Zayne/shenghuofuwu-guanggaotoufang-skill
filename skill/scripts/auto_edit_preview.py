#!/usr/bin/env python3
"""Create a 9:16 rough-cut preview from a Jianying timeline CSV."""

from __future__ import annotations

import argparse
import csv
import shutil
import subprocess
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


W, H = 1080, 1920
FPS = 30
FONT_CANDIDATES = [
    "/System/Library/Fonts/STHeiti Medium.ttc",
    "/System/Library/Fonts/STHeiti Light.ttc",
    "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
]


def run(cmd: list[str], cwd: Path | None = None) -> None:
    subprocess.run(cmd, check=True, cwd=cwd)


def ffmpeg() -> str:
    path = shutil.which("ffmpeg")
    if not path:
        raise SystemExit("ffmpeg is required for auto editing but was not found.")
    return path


def parse_float(value: str, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def srt_time(seconds: float) -> str:
    ms = int(round(seconds * 1000))
    h, rem = divmod(ms, 3_600_000)
    m, rem = divmod(rem, 60_000)
    s, ms = divmod(rem, 1000)
    return f"{h:02}:{m:02}:{s:02},{ms:03}"


def read_timeline(project: Path) -> list[dict[str, str]]:
    timeline = project / "20_剪映时间线.csv"
    if not timeline.exists():
        raise SystemExit(f"Missing timeline CSV: {timeline}")
    with timeline.open("r", encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    rows.sort(key=lambda r: (parse_float(r.get("start", "0")), r.get("track", "")))
    return rows


def find_storyboard(project: Path, shot_id: str, allow_contact_sheet: bool) -> Path | None:
    if shot_id:
        for name in (f"{shot_id}.png", f"{shot_id}.jpg", f"{shot_id}.jpeg"):
            path = project / "images" / "storyboard" / name
            if path.exists():
                return path
    if not allow_contact_sheet:
        return None
    for name in ("storyboard_contact_sheet.png", "storyboard_native_9grid.png"):
        path = project / "images" / "storyboard" / name
        if path.exists():
            return path
    return None


def make_video_segment(ff: str, src: Path, out: Path, duration: float) -> None:
    vf = (
        f"scale={W}:{H}:force_original_aspect_ratio=decrease,"
        f"pad={W}:{H}:(ow-iw)/2:(oh-ih)/2,"
        f"setsar=1,fps={FPS}"
    )
    run([
        ff,
        "-y",
        "-i",
        str(src),
        "-t",
        f"{duration:.3f}",
        "-vf",
        vf,
        "-an",
        "-c:v",
        "libx264",
        "-pix_fmt",
        "yuv420p",
        str(out),
    ])


def font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    for candidate in FONT_CANDIDATES:
        path = Path(candidate)
        if path.exists():
            return ImageFont.truetype(str(path), size=size)
    return ImageFont.load_default()


def wrap_text(text: str, max_chars: int = 18) -> list[str]:
    if not text:
        return []
    lines: list[str] = []
    current = ""
    for ch in text:
        current += ch
        if len(current) >= max_chars or ch in "，。！？；":
            lines.append(current.strip())
            current = ""
    if current.strip():
        lines.append(current.strip())
    return lines[:3]


def render_image_with_caption(src: Path, out: Path, caption: str) -> None:
    img = Image.open(src).convert("RGB")
    img.thumbnail((W, H), Image.Resampling.LANCZOS)
    canvas = Image.new("RGB", (W, H), (17, 24, 39))
    x = (W - img.width) // 2
    y = (H - img.height) // 2
    canvas.paste(img, (x, y))

    lines = wrap_text(caption)
    if lines:
        draw = ImageDraw.Draw(canvas, "RGBA")
        title_font = font(54)
        line_h = 72
        block_h = line_h * len(lines) + 42
        box_y = H - 310
        draw.rounded_rectangle(
            (74, box_y, W - 74, box_y + block_h),
            radius=28,
            fill=(0, 0, 0, 142),
        )
        for i, line in enumerate(lines):
            bbox = draw.textbbox((0, 0), line, font=title_font)
            tx = (W - (bbox[2] - bbox[0])) // 2
            ty = box_y + 22 + i * line_h
            draw.text((tx + 2, ty + 2), line, font=title_font, fill=(0, 0, 0, 180))
            draw.text((tx, ty), line, font=title_font, fill=(255, 255, 255, 245))
    canvas.save(out)


def make_image_segment(ff: str, src: Path, out: Path, duration: float, caption: str = "") -> None:
    rendered = out.with_suffix(".caption.png")
    render_image_with_caption(src, rendered, caption)
    vf = (
        f"scale={W}:{H}:force_original_aspect_ratio=decrease,"
        f"pad={W}:{H}:(ow-iw)/2:(oh-ih)/2,"
        f"setsar=1,fps={FPS}"
    )
    run([
        ff,
        "-y",
        "-loop",
        "1",
        "-i",
        str(rendered),
        "-t",
        f"{duration:.3f}",
        "-vf",
        vf,
        "-an",
        "-c:v",
        "libx264",
        "-pix_fmt",
        "yuv420p",
        str(out),
    ])


def make_slate(ff: str, out: Path, duration: float) -> None:
    slate = out.with_suffix(".slate.png")
    canvas = Image.new("RGB", (W, H), (17, 24, 39))
    draw = ImageDraw.Draw(canvas)
    f = font(48)
    msg = "缺少镜头素材"
    bbox = draw.textbbox((0, 0), msg, font=f)
    draw.text(((W - (bbox[2] - bbox[0])) // 2, H // 2), msg, font=f, fill=(255, 255, 255))
    canvas.save(slate)
    make_image_segment(ff, slate, out, duration, "")
    return
    run([
        ff,
        "-y",
        "-f",
        "lavfi",
        "-i",
        f"color=c=0x111827:s={W}x{H}:r={FPS}:d={duration:.3f}",
        "-an",
        "-c:v",
        "libx264",
        "-pix_fmt",
        "yuv420p",
        str(out),
    ])


def write_srt(rows: list[dict[str, str]], srt_path: Path) -> None:
    index = 1
    lines: list[str] = []
    for row in rows:
        if not row.get("subtitle"):
            continue
        start = parse_float(row.get("start", "0"))
        end = parse_float(row.get("end", "0"), start + parse_float(row.get("duration", "3"), 3))
        if end <= start:
            end = start + 2
        lines.extend([
            str(index),
            f"{srt_time(start)} --> {srt_time(end)}",
            row["subtitle"],
            "",
        ])
        index += 1
    srt_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("project_dir", help="Project directory containing 20_剪映时间线.csv")
    parser.add_argument(
        "--allow-contact-sheet-fallback",
        action="store_true",
        help="Allow storyboard contact sheets as a last-resort visual fallback. Off by default because it is not a valid shot preview.",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Fail if any V1 row is missing both its video and per-shot storyboard image.",
    )
    args = parser.parse_args()

    project = Path(args.project_dir).resolve()
    exports = project / "exports"
    exports.mkdir(parents=True, exist_ok=True)

    ff = ffmpeg()
    rows = read_timeline(project)
    video_rows = [r for r in rows if r.get("track") == "V1"]

    used: list[str] = []
    missing: list[str] = []
    segments: list[Path] = []

    with tempfile.TemporaryDirectory(prefix="auto_edit_") as tmp_name:
        tmp = Path(tmp_name)
        for i, row in enumerate(video_rows, start=1):
            duration = parse_float(row.get("duration", ""), 3)
            if duration <= 0:
                duration = max(parse_float(row.get("end", "0")) - parse_float(row.get("start", "0")), 3)
            asset = project / row.get("asset_path", "")
            out = tmp / f"seg_{i:03}.mp4"
            if asset.exists():
                make_video_segment(ff, asset, out, duration)
                used.append(f"{row.get('shot_id','')}: video {asset.relative_to(project)}")
            else:
                storyboard = find_storyboard(project, row.get("shot_id", ""), args.allow_contact_sheet_fallback)
                if storyboard:
                    make_image_segment(ff, storyboard, out, duration, row.get("subtitle", ""))
                    used.append(f"{row.get('shot_id','')}: storyboard {storyboard.relative_to(project)}")
                    missing.append(f"{row.get('shot_id','')}: missing video {row.get('asset_path','')}, used storyboard fallback")
                else:
                    if args.strict:
                        raise SystemExit(
                            f"Missing video and per-shot storyboard for {row.get('shot_id','')}. "
                            "Generate actual clips or images/storyboard/Sxx.png before auto editing."
                        )
                    make_slate(ff, out, duration)
                    used.append(f"{row.get('shot_id','')}: placeholder slate")
                    missing.append(f"{row.get('shot_id','')}: missing video/image for {row.get('asset_path','')}")
            segments.append(out)

        concat = tmp / "concat.txt"
        concat.write_text("".join(f"file '{p}'\n" for p in segments), encoding="utf-8")
        no_sub = exports / "auto_cut_preview_nosub.mp4"
        run([ff, "-y", "-f", "concat", "-safe", "0", "-i", str(concat), "-c", "copy", str(no_sub)])

    srt = exports / "auto_cut_subtitles.srt"
    write_srt(rows, srt)
    final = exports / "auto_cut_preview.mp4"
    try:
        subtitle_filter = (
            "subtitles=filename=exports/auto_cut_subtitles.srt:"
            "force_style='Fontsize=18,Outline=2,MarginV=120'"
        )
        run([
            ff,
            "-y",
            "-i",
            "exports/auto_cut_preview_nosub.mp4",
            "-vf",
            subtitle_filter,
            "-c:a",
            "copy",
            "exports/auto_cut_preview.mp4",
        ], cwd=project)
    except subprocess.CalledProcessError:
        shutil.copy2(no_sub, final)
        missing.append("Subtitle burn-in failed; copied no-subtitle preview to auto_cut_preview.mp4")

    report = exports / "auto_edit_report.md"
    report.write_text(
        "# 自动剪辑报告\n\n"
        f"Project: `{project}`\n\n"
        f"Output: `exports/{final.name}`\n\n"
        f"Subtitles: `exports/{srt.name}`\n\n"
        "## Used Assets\n\n"
        + "\n".join(f"- {item}" for item in used)
        + "\n\n## Missing Or Fallbacks\n\n"
        + ("\n".join(f"- {item}" for item in missing) if missing else "- None")
        + "\n\n## Validity Note\n\n"
        + "- A rough cut made from placeholder slates is only a timing preview, not a video ad preview.\n"
        + "- A rough cut made from a contact sheet fallback is not valid unless explicitly requested.\n"
        + "- Generate per-shot storyboard images or final video clips for meaningful auto editing.\n"
        + "\n",
        encoding="utf-8",
    )
    print(final)


if __name__ == "__main__":
    main()
