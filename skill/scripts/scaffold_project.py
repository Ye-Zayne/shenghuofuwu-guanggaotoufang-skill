#!/usr/bin/env python3
"""Scaffold a local-life ad production package."""

from __future__ import annotations

import argparse
import csv
from datetime import datetime
from pathlib import Path


MD_FILES = [
    "00_项目简报.md",
    "00_流程清单.md",
    "00A_全流程步骤展示.md",
    "00B_ViMax式制片调度.md",
    "01_信息流投放策略.md",
    "02_创意方向_3选1.md",
    "03_3秒钩子库.md",
    "04_60秒主广告脚本.md",
    "05_30秒剪辑版脚本.md",
    "06_15秒剪辑版脚本.md",
    "07_口播与字幕文案.md",
    "08_镜头表与拍摄脚本.md",
    "09_正反打镜头设计.md",
    "10_拍摄执行清单.md",
    "11_人物设定.md",
    "12_场景设定.md",
    "13_道具服化与品牌露出.md",
    "14_分镜图Prompt.md",
    "15_正反打图片Prompt.md",
    "16_25宫格视觉板Prompt.md",
    "17_即梦视频生成Prompt.md",
    "19_剪映剪辑方案.md",
    "21_封面标题与投流文案.md",
    "22_投流素材变体方案.md",
    "23_交付检查清单.md",
    "24_视频生成暂停与复跑说明.md",
    "99_执行状态.md",
]

DIRS = [
    "images/reference",
    "images/step_cards",
    "images/characters",
    "images/scenes",
    "images/storyboard",
    "images/reverse_shots",
    "images/grid_25",
    "videos/jimeng_clips",
    "videos/source_broll",
    "videos/downloads",
    "docs",
    "characters",
    "scenes",
    "audio/bgm",
    "audio/voiceover",
    "subtitles",
    "asset_index",
    "jianying_project",
    "exports",
]

JIMENG_COLUMNS = [
    "task_id",
    "shot_id",
    "type",
    "input_image",
    "prompt",
    "negative_prompt",
    "duration",
    "aspect_ratio",
    "motion",
    "camera",
    "seed",
    "output_path",
    "status",
]

JIANying_COLUMNS = [
    "track",
    "start",
    "end",
    "duration",
    "asset_path",
    "asset_type",
    "shot_id",
    "subtitle",
    "voiceover",
    "bgm",
    "sfx",
    "transition",
    "effect",
    "scale",
    "position",
    "notes",
]


def safe_name(value: str) -> str:
    return "".join(ch if ch not in r'\/:*?"<>|' else "_" for ch in value).strip() or "未命名商家"


def write_csv(path: Path, columns: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(columns)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("merchant", help="商家名称")
    parser.add_argument("--date", default=datetime.now().strftime("%Y%m%d"))
    parser.add_argument("--root", default=".", help="输出根目录")
    args = parser.parse_args()

    project = Path(args.root) / f"生活服务广告投放导演_{safe_name(args.merchant)}_{args.date}"
    project.mkdir(parents=True, exist_ok=True)

    for dirname in DIRS:
        (project / dirname).mkdir(parents=True, exist_ok=True)

    for filename in MD_FILES:
        path = project / filename
        if not path.exists():
            title = filename.removesuffix(".md")
            path.write_text(f"# {title}\n\n", encoding="utf-8")

    write_csv(project / "18_即梦批量生成任务表.csv", JIMENG_COLUMNS)
    write_csv(project / "20_剪映时间线.csv", JIANying_COLUMNS)

    print(project.resolve())


if __name__ == "__main__":
    main()
