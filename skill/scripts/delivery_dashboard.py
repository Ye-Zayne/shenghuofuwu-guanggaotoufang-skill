#!/usr/bin/env python3
"""Build a visual delivery dashboard for a life-service ad project."""

from __future__ import annotations

import argparse
import csv
import html
import json
from pathlib import Path


PHASES = [
    ("brief", "项目简报", ["00_项目简报.md", "00_流程清单.md", "00A_全流程步骤展示.md", "00B_ViMax式制片调度.md", "01_信息流投放策略.md"]),
    ("creative", "创意与镜头骨架", ["02_创意方向_3选1.md", "03_3秒钩子库.md", "docs/镜头表与单元切分.md", "docs/站位图.md", "docs/关键帧Prompt_逐张拆分版.md", "docs/Seedance_Prompt_逐单元.md"]),
    ("scripts", "脚本", ["04_60秒主广告脚本.md", "05_30秒剪辑版脚本.md", "06_15秒剪辑版脚本.md", "07_口播与字幕文案.md", "07A_完整执行脚本.md"]),
    ("shooting", "镜头与拍摄", ["08_镜头表与拍摄脚本.md", "09_正反打镜头设计.md", "10_拍摄执行清单.md"]),
    ("visual", "视觉设定", ["11_人物设定.md", "12_场景设定.md", "13_道具服化与品牌露出.md", "14_分镜图Prompt.md", "15_正反打图片Prompt.md", "16_25宫格视觉板Prompt.md"]),
    ("asset_index", "资产索引与一致性", ["asset_index/asset_manifest.json", "asset_index/reference_selection.md", "asset_index/consistency_checklist.md", "asset_index/frame_qc.md"]),
    ("video", "即梦视频任务准备", ["17_即梦视频生成Prompt.md", "18_即梦批量生成任务表.csv", "videos/manifest.json", "videos/manifest.md", "videos/dreamina_commands.sh", "videos/retry_and_fallback_plan.md", "24_视频生成暂停与复跑说明.md"]),
    ("edit", "剪辑与字幕", ["19_剪映剪辑方案.md", "20_剪映时间线.csv", "21_封面标题与投流文案.md"]),
    ("delivery", "投流交付", ["22_投流素材变体方案.md", "23_交付检查清单.md", "99_执行状态.md"]),
]


def rel(project: Path, path: Path) -> str:
    return path.relative_to(project).as_posix()


def exists(project: Path, name: str) -> dict[str, object]:
    path = project / name
    return {"path": name, "exists": path.exists(), "size": path.stat().st_size if path.exists() else 0}


def read_head(path: Path, limit: int = 900) -> str:
    if not path.exists():
        return ""
    text = path.read_text(encoding="utf-8", errors="ignore")
    return text[:limit].strip()


def list_files(project: Path, pattern: str) -> list[str]:
    return [rel(project, p) for p in sorted(project.glob(pattern)) if p.is_file()]


def csv_count(path: Path) -> int:
    if not path.exists():
        return 0
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return max(sum(1 for _ in csv.reader(f)) - 1, 0)


def build_manifest(project: Path) -> dict[str, object]:
    storyboard = list_files(project, "images/storyboard/S*.png")
    variant_storyboard = list_files(project, "variants/*/images/storyboard/S*.png")
    step_cards = list_files(project, "images/step_cards/*.png")
    subtitles = list_files(project, "subtitles/*")
    exports = list_files(project, "exports/*")
    video_clips = list_files(project, "videos/jimeng_clips/*")
    variants = []
    for variant_dir in sorted((project / "variants").glob("*")) if (project / "variants").exists() else []:
        if not variant_dir.is_dir():
            continue
        preview = variant_dir / "exports" / "auto_cut_preview.mp4"
        frame = variant_dir / "exports" / "preview_frame.png"
        analysis = variant_dir / "STYLE_ANALYSIS.md"
        if preview.exists() or analysis.exists():
            variants.append({
                "id": variant_dir.name,
                "preview_video": rel(project, preview) if preview.exists() else "",
                "preview_frame": rel(project, frame) if frame.exists() else "",
                "analysis": rel(project, analysis) if analysis.exists() else "",
                "storyboard": [rel(project, p) for p in sorted((variant_dir / "images" / "storyboard").glob("S*.png"))],
            })
    phases = [
        {"id": pid, "title": title, "files": [exists(project, f) for f in files]}
        for pid, title, files in PHASES
    ]
    stop_before_video = (project / ".stop_before_video").exists()
    return {
        "project": project.name,
        "root": str(project),
        "status": {
            "stop_before_video": stop_before_video,
            "has_preview_video": (project / "exports/auto_cut_preview.mp4").exists(),
            "storyboard_frame_count": len(storyboard) + len(variant_storyboard),
            "subtitle_segment_count": csv_count(project / "subtitles/jianying_subtitles.csv"),
        "video_clip_count": 0 if stop_before_video else len(video_clips),
            "jimeng_task_count": csv_count(project / "18_即梦批量生成任务表.csv"),
        },
        "phases": phases,
        "media": {
            "preview_video": "" if stop_before_video else ("exports/auto_cut_preview.mp4" if (project / "exports/auto_cut_preview.mp4").exists() else ""),
            "preview_frame": "" if stop_before_video else ("exports/auto_cut_preview_frame24.png" if (project / "exports/auto_cut_preview_frame24.png").exists() else ""),
            "storyboard": storyboard + variant_storyboard,
            "step_cards": step_cards,
            "subtitles": subtitles,
            "exports": [] if stop_before_video else exports,
            "video_clips": [] if stop_before_video else video_clips,
            "variants": [] if stop_before_video else variants,
        },
        "reports": {
            "status": "99_执行状态.md" if (project / "99_执行状态.md").exists() else "",
            "auto_edit": "exports/auto_edit_report.md" if (project / "exports/auto_edit_report.md").exists() else "",
            "subtitle": "subtitles/subtitle_report.md" if (project / "subtitles/subtitle_report.md").exists() else "",
        },
    }


def write_results_md(project: Path, manifest: dict[str, object]) -> None:
    status = manifest["status"]  # type: ignore[index]
    media = manifest["media"]  # type: ignore[index]
    lines = [
        f"# {project.name} 结果看板",
        "",
        "## 优先查看",
        "",
    ]
    if status.get("stop_before_video"):
        lines.extend([
            "- 当前状态：`已在视频生成前暂停`",
            "- 下一步：充值/确认后运行即梦复跑命令。",
            "- 说明文件：`24_视频生成暂停与复跑说明.md`",
        ])
    if media.get("preview_video"):
        lines.append(f"- 自动粗剪预览：`{media['preview_video']}`")
    if media.get("preview_frame"):
        lines.append(f"- 预览帧：`{media['preview_frame']}`")
    lines.extend([
        f"- 逐镜头分镜数量：`{status['storyboard_frame_count']}`",
        f"- 字幕段落数量：`{status['subtitle_segment_count']}`",
        f"- 即梦任务数量：`{status['jimeng_task_count']}`",
        f"- 已下载/生成视频片段数量：`{status['video_clip_count']}`",
        "",
        "## 分阶段文件",
        "",
    ])
    for phase in manifest["phases"]:  # type: ignore[index]
        lines.append(f"### {phase['title']}")
        for item in phase["files"]:
            mark = "x" if item["exists"] else " "
            lines.append(f"- [{mark}] `{item['path']}`")
        lines.append("")
    lines.extend([
        "## 视觉资产",
        "",
        "### 分镜图",
    ])
    for path in media.get("storyboard", []):
        lines.append(f"- `{path}`")
    lines.extend(["", "### 字幕与导出"])
    for path in media.get("subtitles", []):
        lines.append(f"- `{path}`")
    for path in media.get("exports", []):
        lines.append(f"- `{path}`")
    lines.extend(["", "## 风格变体"])
    for item in media.get("variants", []):
        lines.append(f"- `{item['id']}`")
        if item.get("preview_video"):
            lines.append(f"  - 视频：`{item['preview_video']}`")
        if item.get("analysis"):
            lines.append(f"  - 分析：`{item['analysis']}`")
    (project / "RESULTS.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def card(title: str, body: str) -> str:
    return f"<section class='card'><h2>{html.escape(title)}</h2>{body}</section>"


def write_results_html(project: Path, manifest: dict[str, object]) -> None:
    status = manifest["status"]  # type: ignore[index]
    media = manifest["media"]  # type: ignore[index]
    preview_video = media.get("preview_video", "")
    preview_frame = media.get("preview_frame", "")
    storyboards = media.get("storyboard", [])
    step_cards = media.get("step_cards", [])
    variants = media.get("variants", [])

    video_html = ""
    if status.get("stop_before_video"):
        video_html = "<div class='pause'>已在视频生成前暂停。当前交付为脚本、分镜、字幕、即梦任务表与复跑命令；充值后再生成真正视频。</div>"
    elif preview_video:
        video_html = f"<video controls playsinline src='{html.escape(preview_video)}'></video>"
    elif preview_frame:
        video_html = f"<img src='{html.escape(preview_frame)}' alt='preview'>"

    storyboard_html = "".join(
        f"<figure><img src='{html.escape(path)}' alt='{html.escape(Path(path).stem)}'><figcaption>{html.escape(Path(path).stem)}</figcaption></figure>"
        for path in storyboards
    )
    step_html = "".join(
        f"<figure><img src='{html.escape(path)}' alt='{html.escape(Path(path).stem)}'><figcaption>{html.escape(Path(path).stem)}</figcaption></figure>"
        for path in step_cards
    )
    variants_html = "".join(
        "<section class='card'>"
        f"<h2>{html.escape(item['id'])}</h2>"
        + (f"<video controls playsinline src='{html.escape(item['preview_video'])}'></video>" if item.get("preview_video") else "")
        + (f"<p><a href='{html.escape(item['analysis'])}'>STYLE_ANALYSIS.md</a></p>" if item.get("analysis") else "")
        + "<div class='gallery'>"
        + "".join(
            f"<figure><img src='{html.escape(path)}' alt='{html.escape(Path(path).stem)}'><figcaption>{html.escape(Path(path).stem)}</figcaption></figure>"
            for path in item.get("storyboard", [])
        )
        + "</div></section>"
        for item in variants
    )

    phases_html = ""
    for phase in manifest["phases"]:  # type: ignore[index]
        rows = ""
        for item in phase["files"]:
            cls = "ok" if item["exists"] else "miss"
            label = "完成" if item["exists"] else "缺失"
            rows += f"<li class='{cls}'><span>{label}</span><code>{html.escape(item['path'])}</code></li>"
        phases_html += card(str(phase["title"]), f"<ul class='files'>{rows}</ul>")

    status_body = "".join(
        f"<div class='metric'><strong>{html.escape(str(v))}</strong><span>{html.escape(k)}</span></div>"
        for k, v in status.items()
    )
    script_excerpt = html.escape(read_head(project / "07A_完整执行脚本.md", 1200))
    subtitle_excerpt = html.escape(read_head(project / "subtitles/subtitles.srt", 900))
    report_excerpt = html.escape(read_head(project / "99_执行状态.md", 1200))

    doc = f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(project.name)} 结果看板</title>
  <style>
    body {{ margin:0; font-family:-apple-system,BlinkMacSystemFont,"PingFang SC",Arial,sans-serif; background:#f6f7f8; color:#17202a; }}
    header {{ padding:32px 28px; background:#0f766e; color:white; }}
    header h1 {{ margin:0 0 8px; font-size:28px; }}
    header p {{ margin:0; opacity:.9; }}
    main {{ max-width:1180px; margin:0 auto; padding:24px; }}
    .grid {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(260px,1fr)); gap:16px; }}
    .card {{ background:white; border:1px solid #dfe5e8; border-radius:8px; padding:18px; margin-bottom:16px; }}
    .card h2 {{ margin:0 0 12px; font-size:18px; }}
    video {{ width:100%; max-height:760px; background:#111827; border-radius:8px; }}
    img {{ width:100%; border-radius:8px; display:block; }}
    .metrics {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(160px,1fr)); gap:12px; }}
    .metric {{ background:#eef7f5; border:1px solid #cfe7e2; border-radius:8px; padding:14px; }}
    .metric strong {{ display:block; font-size:24px; color:#0f766e; }}
    .metric span {{ font-size:12px; color:#4b5563; }}
    .pause {{ background:#fff7ed; border:1px solid #fed7aa; color:#9a3412; padding:18px; border-radius:8px; line-height:1.7; }}
    .gallery {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(180px,1fr)); gap:12px; }}
    figure {{ margin:0; background:#fff; border:1px solid #e5e7eb; border-radius:8px; padding:8px; }}
    figcaption {{ font-size:12px; color:#4b5563; margin-top:6px; }}
    .files {{ list-style:none; padding:0; margin:0; }}
    .files li {{ display:flex; gap:10px; align-items:center; padding:6px 0; border-bottom:1px solid #f0f2f3; }}
    .files span {{ font-size:12px; min-width:34px; }}
    .files .ok span {{ color:#0f766e; }}
    .files .miss span {{ color:#b45309; }}
    code, pre {{ font-family:ui-monospace,SFMono-Regular,Menlo,monospace; }}
    pre {{ white-space:pre-wrap; background:#111827; color:#e5e7eb; padding:14px; border-radius:8px; max-height:340px; overflow:auto; }}
  </style>
</head>
<body>
  <header>
    <h1>{html.escape(project.name)} 结果看板</h1>
    <p>集中展示视频、分镜、字幕、脚本、任务表与执行状态。</p>
  </header>
  <main>
    {card("优先查看：自动粗剪预览", video_html or "<p>暂无预览视频。</p>")}
    <section class="card"><h2>状态摘要</h2><div class="metrics">{status_body}</div></section>
    <section class="card"><h2>逐镜头分镜图</h2><div class="gallery">{storyboard_html}</div></section>
    <section class="card"><h2>参考风格变体视频</h2><p>根据你给的 5月28日、5月29日 两种参考语法生成。</p></section>
    {variants_html}
    <section class="card"><h2>步骤图 / 流程图</h2><div class="gallery">{step_html}</div></section>
    <div class="grid">{phases_html}</div>
    <section class="card"><h2>完整执行脚本节选</h2><pre>{script_excerpt}</pre></section>
    <section class="card"><h2>字幕节选</h2><pre>{subtitle_excerpt}</pre></section>
    <section class="card"><h2>执行状态节选</h2><pre>{report_excerpt}</pre></section>
  </main>
</body>
</html>
"""
    (project / "RESULTS.html").write_text(doc, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("project_dir")
    args = parser.parse_args()
    project = Path(args.project_dir).resolve()
    manifest = build_manifest(project)
    (project / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    write_results_md(project, manifest)
    write_results_html(project, manifest)
    print(project / "RESULTS.html")


if __name__ == "__main__":
    main()
