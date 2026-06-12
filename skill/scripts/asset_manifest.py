#!/usr/bin/env python3
"""Build a ViMax-style asset index and consistency checklist."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


GROUPS = {
    "style_refs": ["references/style_refs/*"],
    "characters": ["characters/*", "images/characters/*"],
    "scenes": ["scenes/*", "images/scenes/*"],
    "storyboard": ["images/storyboard/S*.png", "variants/*/images/storyboard/S*.png"],
    "reverse_shots": ["images/reverse_shots/*"],
    "grid_25": ["images/grid_25/*"],
    "video_tasks": ["videos/manifest.json", "videos/manifest.md", "videos/dreamina_commands.sh"],
    "subtitles": ["subtitles/*"],
}


def rel(root: Path, path: Path) -> str:
    return path.relative_to(root).as_posix()


def collect(root: Path) -> dict[str, list[dict[str, object]]]:
    data: dict[str, list[dict[str, object]]] = {}
    for group, patterns in GROUPS.items():
        items = []
        for pattern in patterns:
            for path in sorted(root.glob(pattern)):
                if path.is_file():
                    items.append({
                        "path": rel(root, path),
                        "size": path.stat().st_size,
                        "suffix": path.suffix.lower(),
                    })
        data[group] = items
    return data


def write_reference_selection(root: Path, data: dict[str, list[dict[str, object]]]) -> None:
    lines = [
        "# 参考图选择与复用说明",
        "",
        "本文件采用 ViMax 式参考管理思路：先索引，再选择，再生成视频任务。",
        "",
        "## 风格参考",
    ]
    for item in data.get("style_refs", []):
        lines.append(f"- `{item['path']}`：用于锁定参考视频语法、节奏和镜头风格。")
    lines.extend(["", "## 分镜参考"])
    for item in data.get("storyboard", []):
        lines.append(f"- `{item['path']}`：可作为对应单元的首帧/视觉参考。")
    lines.extend([
        "",
        "## 选择规则",
        "",
        "- 同一单元优先使用该单元专属分镜图。",
        "- 有参考视频时，参考视频只锁风格和镜头语法，不复制具体品牌或物体。",
        "- 正式跑即梦前，先跑 A1 或 B1 smoke test。",
    ])
    (root / "asset_index" / "reference_selection.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_consistency(root: Path, data: dict[str, list[dict[str, object]]]) -> None:
    storyboard_count = len(data.get("storyboard", []))
    style_ref_count = len(data.get("style_refs", []))
    lines = [
        "# 一致性检查清单",
        "",
        f"- 风格参考数量：{style_ref_count}",
        f"- 分镜/关键帧数量：{storyboard_count}",
        "",
        "## 必查项",
        "",
        "- [ ] 人物年龄感、发型、服装是否跨镜头一致",
        "- [ ] 茶饮杯是否保持无品牌或已授权品牌露出",
        "- [ ] 门店环境是否稳定，不混入汽车/无关品类元素",
        "- [ ] 字幕安全区是否保留",
        "- [ ] 转化卡是否避免虚构固定价格",
        "- [ ] 即梦任务是否从一个单元 smoke test 开始",
        "",
        "## 当前建议",
        "",
    ]
    if style_ref_count == 0:
        lines.append("- 缺少风格参考视频，建议补充用户提供的参考视频。")
    if storyboard_count == 0:
        lines.append("- 缺少逐镜头分镜图，生成视频前必须补齐。")
    if style_ref_count and storyboard_count:
        lines.append("- 前置资产已具备基本视频任务准备条件，等待用户确认/充值后再跑即梦。")
    (root / "asset_index" / "consistency_checklist.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_frame_qc(root: Path, data: dict[str, list[dict[str, object]]]) -> None:
    lines = [
        "# 分镜帧 QC",
        "",
        "| 帧 | 状态 | 检查重点 |",
        "|---|---|---|",
    ]
    for item in data.get("storyboard", []):
        path = str(item["path"])
        lines.append(f"| `{path}` | 待人工确认 | 人物/产品/场景/字幕安全区/是否混入无关元素 |")
    if not data.get("storyboard"):
        lines.append("| - | 缺失 | 尚未生成逐镜头分镜图 |")
    (root / "asset_index" / "frame_qc.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("project_dir")
    args = parser.parse_args()
    root = Path(args.project_dir).resolve()
    (root / "asset_index").mkdir(parents=True, exist_ok=True)
    data = collect(root)
    manifest = {
        "project": root.name,
        "root": str(root),
        "groups": data,
        "status": {
            "style_ref_count": len(data.get("style_refs", [])),
            "storyboard_count": len(data.get("storyboard", [])),
            "ready_before_video": bool(data.get("storyboard")) and (root / ".stop_before_video").exists(),
        },
    }
    (root / "asset_index" / "asset_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    write_reference_selection(root, data)
    write_consistency(root, data)
    write_frame_qc(root, data)
    print(root / "asset_index" / "asset_manifest.json")


if __name__ == "__main__":
    main()
