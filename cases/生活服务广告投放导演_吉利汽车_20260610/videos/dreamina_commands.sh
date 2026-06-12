#!/usr/bin/env bash
set -euo pipefail

ROOT="/Users/zhangye/Documents/Codex/skill/生活服务广告投放导演_吉利汽车_20260610"
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

# 充值后建议先跑 A1 smoke test，成功后再取消后续注释。
run_unit A1 5 "variants/0528_presenter_product/images/storyboard/S01.png" "references/style_refs/ref_0528_presenter_product.mp4" "参考真人产品讲解广告语法：女性主持人面对镜头自然介绍产品，现代家轿旁，底部留字幕区，不出现可读logo、车牌、价格和乱码文字。"

# run_unit A2 5 "variants/0528_presenter_product/images/storyboard/S02.png" "references/style_refs/ref_0528_presenter_product.mp4" "汽车外观B-roll：灯组、前脸、侧身、轮毂细节，光泽质感，轻微推进或横移，不出现车牌和可读logo。"
# run_unit A3 8 "variants/0528_presenter_product/images/storyboard/S03.png" "references/style_refs/ref_0528_presenter_product.mp4" "汽车内饰B-roll：中控、座椅、后排空间、储物，强调家用和舒适，不出现可读UI和价格。"
# run_unit A4 5 "variants/0528_presenter_product/images/storyboard/S04.png" "references/style_refs/ref_0528_presenter_product.mp4" "主持人站车旁自然召唤预约试驾，指向底部CTA区，不出现固定价格，活动以门店实时信息为准。"
# run_unit B1 5 "variants/0529_short_drama_conversion/images/storyboard/S01.png" "references/style_refs/ref_0529_short_drama_conversion.mp4" "短剧投流广告语法：下班通勤低谷，冷色压抑，人群流动，女主疲惫。"
# run_unit B2 5 "variants/0529_short_drama_conversion/images/storyboard/S02.png" "references/style_refs/ref_0529_short_drama_conversion.mp4" "手机消息触发她去看车，眼神从疲惫转为专注，不出现真实UI字。"
# run_unit B3 6 "variants/0529_short_drama_conversion/images/storyboard/S03.png" "references/style_refs/ref_0529_short_drama_conversion.mp4" "她穿黑色西装外套走进汽车展厅，状态变强，银色家轿在背景。"
# run_unit B4 7 "variants/0529_short_drama_conversion/images/storyboard/S04.png" "references/style_refs/ref_0529_short_drama_conversion.mp4" "她坐在驾驶位试驾，状态放松自信，表现开起来答案更清楚。"
# run_unit B5 7 "variants/0529_short_drama_conversion/images/storyboard/S05.png" "references/style_refs/ref_0529_short_drama_conversion.mp4" "黑金汽车转化卡，预约试驾、到店看车、实时活动、门店咨询，底部CTA。不要虚构固定价格。"
