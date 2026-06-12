#!/usr/bin/env bash
set -euo pipefail

ROOT="/Users/zhangye/Documents/Codex/skill/生活服务广告投放导演_喜茶_20260529"

# 参考 5月28日：真人产品讲解型。当前 CLI 在本机静默 EXIT:1，待 dreamina 生成接口恢复后复跑。
dreamina multimodal2video \
  --video "$ROOT/references/style_refs/ref_0528_presenter_product.mp4" \
  --image "$ROOT/variants/0528_presenter_product/images/storyboard/S01.png" \
  --ratio=9:16 \
  --duration=5 \
  --model_version=seedance2.0fast \
  --prompt "参考视频的结构和镜头语法：竖屏信息流，女性主持人面对镜头自然介绍，穿插产品特写和环境 B-roll，字幕安全区留白，节奏像产品讲解广告。请改成现代茶饮生活服务广告：年轻女性主持人在现代茶饮店外自然口播介绍一杯清爽葡萄果茶，穿插无品牌白色茶饮杯、杯壁水珠、取茶台、商场门店环境。不要出现真实logo、不要出现车、不要出现汽车元素、不要出现价格大字，不要生成乱码文字。真实商业广告质感，手机竖屏9:16。"

# 参考 5月29日：短剧转化型。
dreamina multimodal2video \
  --video "$ROOT/references/style_refs/ref_0529_short_drama_conversion.mp4" \
  --image "$ROOT/variants/0529_short_drama_conversion/images/storyboard/S01.png" \
  --ratio=9:16 \
  --duration=5 \
  --model_version=seedance2.0fast \
  --prompt "参考视频的结构和镜头语法：短剧投流广告，低谷开头，趋势触发，主角状态跃迁，最后强转化页。请改成现代茶饮生活服务广告：年轻女性从疲惫低谷开始，朋友邀请她下楼喝一杯，茶饮让她恢复状态，最后出现附近门店和实时活动 CTA。不要出现真实logo，不要虚构固定价格，不要乱码文字。竖屏9:16，真实短剧投流质感。"
