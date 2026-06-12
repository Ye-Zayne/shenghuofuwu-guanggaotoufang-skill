#!/usr/bin/env bash
set -euo pipefail
ROOT="/Users/zhangye/Documents/Codex/skill/生活服务广告投放导演_喜茶_20260529"
MODEL="seedance2.0fast"
RATIO="9:16"

run_unit() {
  local unit="$1" duration="$2" image="$3" ref_video="$4" prompt="$5"
  dreamina multimodal2video \
    --video "$ROOT/$ref_video" \
    --image "$ROOT/$image" \
    --ratio="$RATIO" \
    --duration="$duration" \
    --model_version="$MODEL" \
    --poll=60 \
    --prompt "$prompt"
}

# 建议充值后先只跑 A1 做 smoke test，成功后再全量。
run_unit A1 5 "variants/0528_presenter_product/images/storyboard/S01.png" "references/style_refs/ref_0528_presenter_product.mp4" "参考真人产品讲解广告语法：女性主持人面对镜头自然口播，茶饮店外，手持无品牌葡萄果茶杯，底部留字幕区，不出现真实logo、车辆、价格和乱码文字。"

# 全量时取消下面注释：
# run_unit A2 5 "variants/0528_presenter_product/images/storyboard/S02.png" "references/style_refs/ref_0528_presenter_product.mp4" "产品B-roll，葡萄果茶杯、冰块、水珠、鲜果感，真实竖屏广告质感，不出现logo和文字。"
# run_unit A3 5 "variants/0528_presenter_product/images/storyboard/S03.png" "references/style_refs/ref_0528_presenter_product.mp4" "取茶台递杯，现代茶饮店环境，真实生活服务广告，镜头轻微推进。"
# run_unit A4 5 "variants/0528_presenter_product/images/storyboard/S04.png" "references/style_refs/ref_0528_presenter_product.mp4" "主持人轻CTA，提示点进附近门店查看实时活动，不出现固定价格。"
# run_unit B1 5 "variants/0529_short_drama_conversion/images/storyboard/S01.png" "references/style_refs/ref_0529_short_drama_conversion.mp4" "短剧低谷开头，疲惫白领，压抑光线，竖屏投流广告质感。"
# run_unit B2 5 "variants/0529_short_drama_conversion/images/storyboard/S02.png" "references/style_refs/ref_0529_short_drama_conversion.mp4" "手机消息触发转折，主角从疲惫转为专注，不出现真实UI文字。"
# run_unit B3 6 "variants/0529_short_drama_conversion/images/storyboard/S03.png" "references/style_refs/ref_0529_short_drama_conversion.mp4" "主角状态跃迁，穿黑西装走出茶饮店，手持无品牌茶杯。"
# run_unit B4 7 "variants/0529_short_drama_conversion/images/storyboard/S04.png" "references/style_refs/ref_0529_short_drama_conversion.mp4" "暖色结果场景，主角与朋友交流，状态自信放松。"
# run_unit B5 7 "variants/0529_short_drama_conversion/images/storyboard/S05.png" "references/style_refs/ref_0529_short_drama_conversion.mp4" "黑金转化卡，附近门店和实时活动CTA，不虚构固定价格。"
