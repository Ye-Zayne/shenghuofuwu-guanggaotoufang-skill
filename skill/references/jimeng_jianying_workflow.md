# 即梦 CLI 与剪映剪辑工作流

This reference is for execution after scripts, shot tables, and visual prompts exist.

## Directory Contract

Use this structure inside the project output directory:

```text
images/
  reference/
  characters/
  scenes/
  storyboard/
  reverse_shots/
  grid_25/
videos/
  jimeng_clips/
  source_broll/
audio/
  bgm/
  voiceover/
jianying_project/
exports/
```

## 即梦 Task Table

`18_即梦批量生成任务表.csv` must include:

```text
task_id,shot_id,type,input_image,prompt,negative_prompt,duration,aspect_ratio,motion,camera,seed,output_path,status
```

Use `aspect_ratio=9:16` by default.

Before video generation, create actual storyboard images:

- `images/storyboard/S01.png` through the final shot.
- `images/reverse_shots/reverse_A.png`, `reverse_B.png`, etc. when dialogue or interaction exists.
- `images/grid_25/visual_board_25.png`.

Prompt-only storyboard files are incomplete delivery. They are only the source instructions for image generation.

Recommended clip duration:

- Hook shots: 2-3s.
- Product/service process: 3-5s.
- Result reveal: 2-4s.
- CTA: 2-3s.

## CLI Execution Policy

Before running generation, check for available commands:

```bash
command -v jimeng
command -v dreamina
command -v seedance
```

If one exists, inspect its help:

```bash
jimeng --help
dreamina --help
seedance --help
```

Then adapt commands to the installed CLI instead of inventing flags.

If the CLI accepts CSV or JSON batch input, prefer batch mode. If it only accepts single jobs, loop over `18_即梦批量生成任务表.csv`.

If authentication, cookies, token, or account state is missing, do not fabricate output. Record the blocker in `99_执行状态.md` and keep all prompts ready to run.

## 剪映 Output

Always create:

- `19_剪映剪辑方案.md`: editorial intent, rhythm, BGM direction, subtitle style, transitions, CTA.
- `20_剪映时间线.csv`: deterministic edit table.
- `subtitles/subtitles.srt`: universal subtitle file.
- `subtitles/subtitles.ass`: styled subtitle file.
- `subtitles/jianying_subtitles.csv`: Jianying-friendly caption table.
- `subtitles/subtitle_report.md`: generation mode, source, and dependency report.
- `exports/auto_cut_preview.mp4`: ffmpeg rough cut preview when local media or storyboard images exist.
- `exports/auto_cut_subtitles.srt`: subtitle file generated from the timeline.
- `exports/auto_edit_report.md`: automatic editing report with used clips, fallbacks, and missing assets.

`20_剪映时间线.csv` columns:

```text
track,start,end,duration,asset_path,asset_type,shot_id,subtitle,voiceover,bgm,sfx,transition,effect,scale,position,notes
```

Track conventions:

- V1: main video clips.
- V2: overlays, product cards, price cards, CTA stickers.
- A1: voiceover.
- A2: BGM.
- A3: SFX.
- T1: subtitles.
- T2: offer/CTA text.

## Jianying Draft Creation

If a Jianying draft CLI, CapCut XML/JSON generator, or local draft-writing script exists, use it to create `jianying_project/`.

If no draft writer exists, still run the local rough-cut path:

```bash
python3 path/to/life-service-ad-director/scripts/auto_edit_preview.py /path/to/project
```

The rough-cut path reads `20_剪映时间线.csv`, uses V1 video rows, creates a 9:16 MP4, writes subtitles, and falls back in this order:

1. Existing `asset_path` video.
2. Matching storyboard image by `shot_id`, such as `images/storyboard/S01.png`.
3. A neutral placeholder slate.

Do not use storyboard contact sheets as shot media unless explicitly invoked with `--allow-contact-sheet-fallback`. Contact-sheet preview videos are not valid ad previews.

Then make the timeline precise enough for a human editor:

- Exact clip order.
- Start/end time in seconds.
- Subtitle text per clip.
- BGM mood and beat notes.
- SFX positions.
- CTA card timing.
- Cover title and first-frame recommendation.

## Auto-Edit QA

Check:

- `exports/auto_cut_preview.mp4` exists and opens.
- Output is 1080x1920 or another valid 9:16 resolution.
- All V1 timeline rows are represented in order.
- Missing final media is listed in `exports/auto_edit_report.md`.
- Subtitles come from `20_剪映时间线.csv`, not improvised text.

## Subtitle Generation Policy

Use:

```bash
python3 path/to/life-service-ad-director/scripts/subtitle_pipeline.py /path/to/project
```

This creates subtitle files from `20_剪映时间线.csv`.

For existing long videos or voiced final cuts, use Whisper mode:

```bash
python3 path/to/life-service-ad-director/scripts/subtitle_pipeline.py /path/to/project --video /path/to/video.mp4 --mode whisper --model small --language zh
```

Bundled open-source reference:

- `vendor/auto-subtitle` from `m1guelpf/auto-subtitle`, MIT licensed.
- It uses OpenAI Whisper + ffmpeg to transcribe and overlay subtitles.
- In this skill, prefer `scripts/subtitle_pipeline.py` because it also exports timeline-based and Jianying-ready subtitles.

## QA Before Delivery

Check:

- 9:16 throughout.
- First 3 seconds contain a clear hook.
- Price/offer does not cover faces or product proof.
- CTA appears in final 3-5 seconds.
- Every generated asset is referenced by the timeline.
- Missing assets are listed in `99_执行状态.md`.
