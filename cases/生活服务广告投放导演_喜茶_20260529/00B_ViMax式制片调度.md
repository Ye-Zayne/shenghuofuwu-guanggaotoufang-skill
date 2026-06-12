# 00B_ViMax式制片调度

本项目参考 ViMax 的多智能体制片思路，但不直接依赖 ViMax 模型。这里把生活服务广告生产拆成四个角色，保证视频生成前的资产、分镜、参考和命令都是可复核的。

## Director 导演

职责：

- 判断广告语法：真人产品讲解型 / 短剧转化型。
- 锁定竖屏 9:16、信息流节奏、字幕安全区。
- 判断是否停在视频生成前。

本项目决策：

- 参考 `5月28日.mp4`：真人产品讲解型。
- 参考 `5月29日.mp4`：短剧转化型。
- 当前按用户要求停在视频生成前。

## Screenwriter 编剧

职责：

- 生成钩子、脚本、单元边界、台词/旁白。
- 把广告拆成可生成的视频单元。

本项目产物：

- `04_60秒主广告脚本.md`
- `07A_完整执行脚本.md`
- `docs/镜头表与单元切分.md`
- `docs/Seedance_Prompt_逐单元.md`

## Producer 制片

职责：

- 管理参考视频、关键帧、字幕、任务表、即梦额度与暂停状态。
- 确保没有把静态预览误当真实视频。

本项目产物：

- `00_流程清单.md`
- `asset_index/asset_manifest.json`
- `asset_index/reference_selection.md`
- `asset_index/consistency_checklist.md`
- `.stop_before_video`

## Video Generator 视频生成器

职责：

- 生成 Seedance / 即梦任务清单。
- 准备可复跑命令。
- 先 smoke test，再全量生成。

本项目产物：

- `videos/manifest.json`
- `videos/manifest.md`
- `videos/dreamina_commands.sh`
- `videos/retry_and_fallback_plan.md`

## 当前闸门状态

- Script gate：已通过。
- Reference gate：待人工复核资产索引。
- Consistency gate：待人工勾选 `asset_index/consistency_checklist.md`。
- Manifest gate：已生成。
- Pause gate：已开启，等待用户充值后继续。
