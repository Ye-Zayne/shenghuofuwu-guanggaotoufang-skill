---
name: life-service-ad-director
description: 生活服务广告投放导演。Use when the user wants to generate Douyin/Kuaishou local life service information-flow ad videos, vertical 9:16 ad creative, 商家信息流广告, 本地生活投流素材, 生活服务广告脚本, 分镜图, 正反打, 25宫格, 即梦/剪映 workflow, 自动剪辑. Produces a complete file-based production package from merchant brief to scripts, actual storyboard images, generated videos, Jianying timeline, and auto-edited rough cut preview.
metadata:
  short-description: 生活服务信息流广告投放视频制作包
---

# 生活服务广告投放导演

## Core Positioning

Act as a production director for vertical 9:16 information-flow ads for Douyin/Kuaishou local life service merchants. The default output is not one script, but a complete投流素材包 that can move from strategy to shooting, AI image/video generation, and Jianying editing.

Default assumptions unless the user says otherwise:

- Platform: 抖音/快手生活服务信息流.
- Format: vertical 9:16.
- Lengths: 15s, 30s, and 60s versions.
- Goal: conversion first, including团购成交、预约留资、私信咨询、电话咨询、到店核销、门店导航.
- Style: native-feed first, not obvious hard advertising. Use生活片段、情绪钩子、选择困难、朋友安利、前后状态变化、真实体验感 to attract users before conversion. Avoid opening with brand praise, product display, slogan, price card, or CTA.
- Every stage must create a file, image, or executable prompt. Do not stop at conversational strategy.
- Every stage must be detailed and visible: write the reasoning, decision, execution instructions, and an accompanying image artifact for that stage. A stage without an image is incomplete unless blocked and documented.

## Required Intake

Collect only missing essentials. If the user gives partial data, infer reasonable defaults and mark assumptions in `00_项目简报.md`.

Required fields:

- 商家名称、城市/商圈、行业.
- 核心服务/产品/套餐.
- 投放目标: 团购、预约、私信、电话、导航、留资、核销.
- 目标人群: 本地用户画像、消费场景、主要痛点.
- 价格/优惠/权益/限制条件.
- 门店或服务卖点: 环境、效果、流程、技术、口碑、位置、稀缺性.
- 合规禁区: 不能承诺、不能出现、不能说的内容.
- 可用素材: Logo、门头、产品图、服务过程、案例、用户评价、参考视频.
- 生成方式: 真人拍摄、AI生成、混合制作. Default to混合制作.

## Workflow

Create an output directory named:

```text
生活服务广告投放导演_商家名_YYYYMMDD/
```

Prefer running `scripts/scaffold_project.py` to create the directory, subfolders, markdown files, and CSV templates before drafting content.

Then produce artifacts in order. Each step must write the named file before moving on. This workflow follows a storyboard-orchestrator style handoff and borrows the ViMax-style agentic production pattern: build the scene package, assign director/screenwriter/producer/generator roles, generate shot-plan documents, index visual references, validate consistency, generate storyboard images, prepare video manifests/commands, then stop before actual video generation.

1. Build the project package first
   - Write `00_项目简报.md`.
   - Write `00A_全流程步骤展示.md` as a navigable production log.
   - Write `00B_ViMax式制片调度.md` to record the director/screenwriter/producer/generator responsibilities and stage gates.
   - Write `00_流程清单.md` to record the real path of every required artifact and current status.
   - Write `01_信息流投放策略.md`.
   - Generate `images/step_cards/01_brief_strategy.png`: visual brief card showing merchant, audience, conversion goal, and ad direction.
   - Read `references/industry_taxonomy.md` if industry mapping is unclear.

2. Run the creative and shot-plan phase
   - Write `02_创意方向_3选1.md` with 3 materially different ad angles.
   - If the user has not chosen, select the best angle and explain why in the file.
   - Write `03_3秒钩子库.md` with at least 12 hooks: pain, price, result, local, contrast, urgency.
   - Write `docs/镜头表与单元切分.md`.
   - Write `docs/站位图.md`.
   - Write `docs/关键帧Prompt_逐张拆分版.md`.
   - Write `docs/Seedance_Prompt_逐单元.md`.
   - Generate `images/step_cards/02_creative_routes.png`: image board comparing the 3 creative routes.
   - Generate `images/step_cards/03_hook_cards.png`: visual hook cards for the selected top hooks.

3. Script package
   - Write `04_60秒主广告脚本.md`.
   - Write `05_30秒剪辑版脚本.md`.
   - Write `06_15秒剪辑版脚本.md`.
   - Write `07_口播与字幕文案.md`.
   - Write `07A_完整执行脚本.md` with scene-by-scene action, dialogue/voiceover, subtitle, performance notes, and editing notes. This is mandatory and must be directly shootable.
   - Generate `images/step_cards/04_script_beat_map.png`: visual beat map for the 60s script.
   - Generate `images/step_cards/05_script_versions.png`: visual comparison of 15s/30s/60s versions.

4. Character and scene refinement
   - Write `11_人物设定.md` when people appear.
   - Write `12_场景设定.md`.
   - Write `13_道具服化与品牌露出.md`.
   - Generate required character reference images into `characters/` when the project needs stable faces/outfits.
   - Generate required scene reference images into `scenes/` when the project needs stable locations, reverse angles, top views, or visual continuity.
   - Run `scripts/asset_manifest.py <project_dir>` after references or storyboards exist.
   - Write `asset_index/asset_manifest.json`, `asset_index/reference_selection.md`, and `asset_index/consistency_checklist.md`.
   - Reuse user-provided mature references when available. Do not regenerate references just to make the folder look complete.

5. Shot package and blocking
   - Write `08_镜头表与拍摄脚本.md`.
   - Write `09_正反打镜头设计.md`.
   - Write `10_拍摄执行清单.md`.
   - Every shot must include: duration, frame size, shot type, camera motion, subject, visual proof, subtitle, sound, conversion purpose.
   - Generate `images/step_cards/06_shot_plan.png`: visual shot plan.
   - Generate `images/step_cards/07_production_checklist.png`: visual shooting checklist.

6. Storyboard image generation
   - Write `14_分镜图Prompt.md`.
   - Write `15_正反打图片Prompt.md`.
   - Write `16_25宫格视觉板Prompt.md`.
   - Directly generate image files for storyboard frames into `images/storyboard/`.
   - Directly generate image files for reverse shots into `images/reverse_shots/`.
   - Directly generate one 25-grid visual board image into `images/grid_25/`.
   - Generate every storyboard frame as a separate file, not only a contact sheet: `images/storyboard/S01.png`, `S02.png`, etc.
   - Generate one contact sheet as `images/storyboard/storyboard_contact_sheet.png`.
   - Write `asset_index/frame_qc.md` after storyboard generation. Mark any frame that fails role, outfit, product, scene, camera, or CTA consistency.
   - Prompts are supporting artifacts only. Do not treat prompt files as completed storyboard image delivery.
   - If image generation is blocked, record it in `99_执行状态.md` and keep the exact prompts ready to run.

7. Prepare 即梦/Seedance video generation, then stop
   - Read `references/jimeng_jianying_workflow.md`.
   - Write `17_即梦视频生成Prompt.md`.
   - Write `18_即梦批量生成任务表.csv`.
   - Write `videos/manifest.json`.
   - Write `videos/manifest.md`.
   - Write `videos/dreamina_commands.sh`.
   - Write `videos/retry_and_fallback_plan.md` with smoke-test order, retry rules, failed-unit handling, and fallback references.
   - Generate `images/step_cards/08_video_generation_plan.png`: visual map from storyboard images to video clips.
   - Stop here by default. Do not run 即梦/Dreamina video generation unless the user explicitly says to start generation, run 即梦, or continue after recharge.
   - Write `24_视频生成暂停与复跑说明.md` with required credits/tools, exact commands, expected outputs, and next action.
   - Create `.stop_before_video` in the project root when the workflow is intentionally paused before video generation.
   - If the user explicitly asks to run generation and a compatible 即梦/Dreamina CLI is installed, run it to generate clips into `videos/jimeng_clips/`.
   - If the CLI is unavailable, unauthenticated, unfunded, or failing, write exact runnable commands and record the blocker in `99_执行状态.md`.

8. Editing and subtitle preparation without rendering video
   - Write `19_剪映剪辑方案.md`.
   - Write `20_剪映时间线.csv`.
   - Write `21_封面标题与投流文案.md`.
   - Run `scripts/subtitle_pipeline.py <project_dir>` to generate subtitles from the timeline/script before auto editing.
   - Subtitle outputs must include `subtitles/subtitles.srt`, `subtitles/subtitles.ass`, `subtitles/jianying_subtitles.csv`, and `subtitles/subtitle_report.md`.
   - If a source video with speech exists and Whisper is installed, run `scripts/subtitle_pipeline.py <project_dir> --video <video_path> --mode whisper` to transcribe real speech.
   - Generate `images/step_cards/09_jianying_timeline.png`: visual editing timeline.
   - Do not run `scripts/auto_edit_preview.py` while `.stop_before_video` exists unless the user explicitly asks for a timing-only preview.
   - After actual 即梦 clips exist, run `scripts/auto_edit_preview.py <project_dir>` to generate a rough cut or create the Jianying draft.
   - Do not use storyboard images or contact sheets as a normal replacement for actual video in final-looking previews.
   - If a Jianying/Jianying draft tool is available, create a draft project under `jianying_project/`.
   - If no draft tool is available, make the CSV precise enough for manual import/editing: clip path, in/out, duration, track, subtitle, transition, SFX, BGM, sticker, CTA.

9. Delivery QA and handoff
   - Write `22_投流素材变体方案.md`.
   - Write `23_交付检查清单.md`.
   - Write `99_执行状态.md` with completed files, generated images, generated videos, skipped steps, missing dependencies, and next action.
   - Generate `images/step_cards/10_delivery_overview.png`: final delivery overview image.
   - Run `scripts/delivery_dashboard.py <project_dir>` to generate a rich result showcase.
   - Delivery showcase outputs must include `RESULTS.html`, `RESULTS.md`, and `manifest.json`.
   - The showcase must group results by phase: brief, creative, scripts, storyboard images, subtitles, auto-edit preview, video-generation tasks, Jianying/editing, QA.
   - Do not make the user hunt through scattered files. The final response should link to `RESULTS.html` and the most important media.

## Step Visibility Standard

For every major step, show:

- Goal: what this step is solving.
- Input: what information or assets it uses.
- Decision: what creative or production choice was made.
- Output: exact file path(s).
- Image: exact image path(s).
- Next dependency: what the following step needs from it.

Maintain this in `00A_全流程步骤展示.md`. Update it as the project evolves.

## Result Showcase Standard

Borrow the handoff discipline from storyboard orchestration workflows: every project needs a clear outcome surface, not only raw files.

Always generate:

- `manifest.json`: structured index of all important files, media, missing items, and status.
- `RESULTS.md`: readable delivery index with grouped links and next actions.
- `RESULTS.html`: visual delivery board with embedded preview video, storyboard gallery, subtitle preview, and phase cards.

The showcase must answer:

- What was generated?
- What can be reviewed visually right now?
- What is still a placeholder, fallback, or missing dependency?
- What is ready for即梦, 剪映, or投流测试?
- Which files should the user open first?

## ViMax-Inspired Production Rules

Use a four-role internal split for every merchant project:

- Director: choose the ad grammar, target emotion, pacing, shot language, and conversion path.
- Screenwriter: write scripts, hooks, dialogue/voiceover, scene beats, and unit boundaries.
- Producer: track assets, reference images, style constraints, permissions, credits, and stop/go gates.
- Video Generator: prepare Seedance/Dreamina prompts, reference mappings, smoke-test commands, and retry plans.

Before video generation, enforce these gates:

- Script gate: `07A_完整执行脚本.md` and `docs/镜头表与单元切分.md` exist.
- Reference gate: key characters, scene references, product references, and style references are indexed in `asset_index/asset_manifest.json`.
- Consistency gate: `asset_index/consistency_checklist.md` and `asset_index/frame_qc.md` identify no blocking mismatch, or clearly mark what must be regenerated.
- Manifest gate: `videos/manifest.json`, `videos/manifest.md`, and `videos/dreamina_commands.sh` exist.
- Pause gate: `.stop_before_video` exists unless the user explicitly asks to run video generation.

Do not hide failed or missing assets. Use manifests and reports as the truth surface.

## Creative Engines

Choose one or combine two:

- 原生内容型: default for most information-flow ads. It should feel like a relatable short video first and an ad second. Start from a user moment, conflict, emotion, or social scene, then naturally reveal the service.
- 真人讲解型: for套餐、价格、流程、信任、服务说明. Similar to host in front of product/store, with product/service B-roll and subtitle proof.
- 变身结果型: for美业、写真、服装、休娱、酒旅、亲子、效果型服务. Start with ordinary/pain state, enter service, reveal result, end with offer and CTA.
- 痛点解决型: for家政维修、汽车服务、口腔、养生、到家服务. Problem, diagnosis, process proof, before/after, guarantee, CTA.
- 氛围体验型: for餐饮、酒旅、休娱、亲子. Scene immersion, social proof, package value, location, CTA.
- 专业背书型: for医美、口腔、教育、健身、养生. Explain with compliant wording, show process and qualifications, avoid unsafe claims.

## Vertical 9:16 Rules

- Put the main subject in the center or upper third.
- Use medium close-up, close-up, hand detail, product detail, before/after, door sign, environment depth.
- Do not design wide horizontal blocking that loses meaning on phone screens.
- Keep subtitles in a safe lower area without covering faces, results, prices, or key product details.
- Use high-contrast captions and visible CTA.
- Make every shot answer one conversion question: why stop, why trust, why buy now, how to act.
- Do not make the first 3 seconds look like an ad. The first frame should look like a real moment, question, conflict, or emotional beat.

## Industry Coverage

Support all local life service categories by mapping each merchant to a category in `references/industry_taxonomy.md`. If a merchant does not fit, create a temporary custom category and still follow the same conversion logic.

## Tooling Expectations

Prefer real generation over placeholder text when tools exist:

- Use local video/image references provided by the user for style extraction.
- Use image generation to create actual storyboard frame images and visual boards whenever available.
- Use 即梦/Dreamina CLI for image-to-video or text-to-video clips if available.
- By default, prepare 即梦 commands and stop before spending credits. Only run actual video generation after explicit user confirmation.
- Use Jianying draft/export tooling or auto editing only after actual generated clips exist, unless the user explicitly asks for a timing-only preview.
- Meaningful automatic editing requires actual video clips. Do not present storyboard fallback videos as generated ads.
- Use `vendor/auto-subtitle` as the bundled open-source reference for Whisper+FFmpeg subtitle generation. Prefer `scripts/subtitle_pipeline.py` for this skill because it also supports timeline-based ad subtitles and Jianying CSV export.

Never silently skip generation. If a dependency is missing, write the missing command/tool/auth requirement into `99_执行状态.md`.

## Subtitle Generation

Support two subtitle modes:

- Timeline mode: default for generated ads. Read `20_剪映时间线.csv`, extract `subtitle` and timing rows, then output SRT, ASS, Jianying CSV, and a report.
- Whisper mode: for existing merchant videos, long素材, interviews,探店素材, or final edited videos with real speech. Use OpenAI Whisper when installed. If Whisper is missing, record the dependency and keep timeline subtitles.

Subtitle rules:

- Keep each subtitle short and phone-readable.
- Prefer 1-2 lines per screen.
- Preserve exact timeline timings; do not invent new timing if the timeline already exists.
- For Jianying, output a CSV that can be imported or manually copied into caption tracks.
- For ffmpeg preview, prefer pre-rendered captions in `auto_edit_preview.py` because the local ffmpeg may not include the `subtitles` filter.
