# 快速使用指南

这个仓库的目标是把一个生活服务商家的投流视频，从简报推进到脚本、分镜图、字幕、即梦任务表、剪映时间线和交付看板。

## 1. 安装 Skill

```bash
mkdir -p ~/.codex/skills/life-service-ad-director
rsync -a --delete skill/ ~/.codex/skills/life-service-ad-director/
```

安装后，在 Codex 中用 `$life-service-ad-director` 触发。

## 2. 推荐提示词

```text
用 $life-service-ad-director 为一家杭州亲子摄影店生成 9:16 生活服务信息流广告投放素材包。
要求：不要一上来像广告，前 3 秒用真实用户痛点吸引；输出 60 秒、30 秒、15 秒脚本；生成分镜图；准备即梦任务表和剪映时间线；视频生成前先停止。
```

## 3. 新建项目骨架

```bash
python3 skill/scripts/scaffold_project.py "杭州亲子摄影店" --root ./work
```

输出目录格式：

```text
生活服务广告投放导演_商家名_YYYYMMDD/
```

## 4. 关键交付物

- `00_项目简报.md`
- `01_信息流投放策略.md`
- `04_60秒主广告脚本.md`
- `07A_完整执行脚本.md`
- `docs/镜头表与单元切分.md`
- `docs/关键帧Prompt_逐张拆分版.md`
- `images/storyboard/`
- `18_即梦批量生成任务表.csv`
- `20_剪映时间线.csv`
- `subtitles/`
- `videos/dreamina_commands.sh`
- `RESULTS.html`

## 5. 停在即梦前

默认规则是：先准备视频生成任务，不直接消耗即梦额度。项目根目录出现 `.stop_before_video` 时，说明当前应停在视频生成前。

继续生成视频前，先看：

- `24_视频生成暂停与复跑说明.md`
- `videos/manifest.md`
- `videos/dreamina_commands.sh`

## 6. 更新结果看板

```bash
python3 skill/scripts/asset_manifest.py ./work/生活服务广告投放导演_商家名_YYYYMMDD
python3 skill/scripts/subtitle_pipeline.py ./work/生活服务广告投放导演_商家名_YYYYMMDD
python3 skill/scripts/delivery_dashboard.py ./work/生活服务广告投放导演_商家名_YYYYMMDD
```

打开 `RESULTS.html` 检查最终交付面板。

