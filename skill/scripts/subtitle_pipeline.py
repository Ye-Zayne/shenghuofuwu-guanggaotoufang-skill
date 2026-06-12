#!/usr/bin/env python3
"""Generate ad subtitles from a timeline CSV or Whisper transcription."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


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


def ass_time(seconds: float) -> str:
    cs = int(round(seconds * 100))
    h, rem = divmod(cs, 360_000)
    m, rem = divmod(rem, 6_000)
    s, cs = divmod(rem, 100)
    return f"{h}:{m:02}:{s:02}.{cs:02}"


def clean_text(text: str) -> str:
    return " ".join((text or "").replace("\n", " ").split()).strip()


def read_timeline(project: Path) -> list[dict[str, str]]:
    path = project / "20_剪映时间线.csv"
    if not path.exists():
        raise SystemExit(f"Missing timeline file: {path}")
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    rows.sort(key=lambda r: (parse_float(r.get("start", "0")), r.get("track", "")))
    return rows


def timeline_segments(project: Path) -> list[dict[str, object]]:
    rows = read_timeline(project)
    segments: list[dict[str, object]] = []
    seen: set[tuple[float, float, str]] = set()
    for row in rows:
        text = clean_text(row.get("subtitle", ""))
        if not text:
            continue
        start = parse_float(row.get("start", "0"))
        end = parse_float(row.get("end", "0"))
        if end <= start:
            end = start + max(parse_float(row.get("duration", "2"), 2), 1)
        key = (start, end, text)
        if key in seen:
            continue
        seen.add(key)
        segments.append({
            "start": start,
            "end": end,
            "text": text,
            "shot_id": row.get("shot_id", ""),
            "source": "timeline",
        })
    return segments


def whisper_segments(video: Path, model_name: str, language: str | None) -> list[dict[str, object]]:
    try:
        import whisper  # type: ignore
    except Exception as exc:
        raise SystemExit(
            "Whisper mode requires openai-whisper. Install with: "
            "pip install openai-whisper"
        ) from exc
    model = whisper.load_model(model_name)
    kwargs = {}
    if language and language != "auto":
        kwargs["language"] = language
    result = model.transcribe(str(video), **kwargs)
    segments = []
    for seg in result.get("segments", []):
        segments.append({
            "start": float(seg["start"]),
            "end": float(seg["end"]),
            "text": clean_text(seg["text"]),
            "shot_id": "",
            "source": "whisper",
        })
    return segments


def write_srt(segments: list[dict[str, object]], path: Path) -> None:
    lines: list[str] = []
    for i, seg in enumerate(segments, start=1):
        lines.extend([
            str(i),
            f"{srt_time(float(seg['start']))} --> {srt_time(float(seg['end']))}",
            str(seg["text"]),
            "",
        ])
    path.write_text("\n".join(lines), encoding="utf-8")


def write_ass(segments: list[dict[str, object]], path: Path) -> None:
    header = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,STHeiti,64,&H00FFFFFF,&H000000FF,&HAA000000,&H66000000,0,0,0,0,100,100,0,0,3,2,0,2,80,80,180,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    events = []
    for seg in segments:
        text = str(seg["text"]).replace(",", "，")
        events.append(
            f"Dialogue: 0,{ass_time(float(seg['start']))},{ass_time(float(seg['end']))},Default,,0,0,0,,{text}"
        )
    path.write_text(header + "\n".join(events) + "\n", encoding="utf-8")


def write_jianying_csv(segments: list[dict[str, object]], path: Path) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["start", "end", "duration", "text", "shot_id", "track", "style", "notes"])
        for seg in segments:
            start = float(seg["start"])
            end = float(seg["end"])
            writer.writerow([
                f"{start:.3f}",
                f"{end:.3f}",
                f"{end - start:.3f}",
                seg["text"],
                seg.get("shot_id", ""),
                "T1",
                "white_text_black_shadow_bottom_safe",
                "Import or recreate on Jianying subtitle track.",
            ])


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("project_dir")
    parser.add_argument("--mode", choices=["timeline", "whisper"], default="timeline")
    parser.add_argument("--video", help="Video path for Whisper mode")
    parser.add_argument("--model", default="small")
    parser.add_argument("--language", default="zh")
    args = parser.parse_args()

    project = Path(args.project_dir).resolve()
    out_dir = project / "subtitles"
    out_dir.mkdir(parents=True, exist_ok=True)

    if args.mode == "whisper":
        if not args.video:
            raise SystemExit("--video is required for whisper mode")
        segments = whisper_segments(Path(args.video).resolve(), args.model, args.language)
        source = str(Path(args.video).resolve())
    else:
        segments = timeline_segments(project)
        source = str(project / "20_剪映时间线.csv")

    write_srt(segments, out_dir / "subtitles.srt")
    write_ass(segments, out_dir / "subtitles.ass")
    write_jianying_csv(segments, out_dir / "jianying_subtitles.csv")
    (out_dir / "segments.json").write_text(
        json.dumps(segments, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    (out_dir / "subtitle_report.md").write_text(
        "# 字幕生成报告\n\n"
        f"- Mode: `{args.mode}`\n"
        f"- Source: `{source}`\n"
        f"- Segment count: `{len(segments)}`\n"
        "- Outputs:\n"
        "  - `subtitles/subtitles.srt`\n"
        "  - `subtitles/subtitles.ass`\n"
        "  - `subtitles/jianying_subtitles.csv`\n"
        "  - `subtitles/segments.json`\n\n"
        "## Open-source reference\n\n"
        "- Bundled reference: `vendor/auto-subtitle` from `m1guelpf/auto-subtitle`.\n"
        "- Whisper mode requires `openai-whisper` if real video speech transcription is needed.\n",
        encoding="utf-8",
    )
    print(out_dir / "subtitles.srt")


if __name__ == "__main__":
    main()
