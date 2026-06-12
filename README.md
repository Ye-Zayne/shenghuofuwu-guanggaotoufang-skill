# 生活服务广告投放导演

面向抖音、快手等短视频平台生活服务/本地业务客户的信息流广告导演型 Codex Skill。

该仓库包含：

- `skill/`：生活服务广告投放导演 Skill 本体、自动化脚本、字幕工具、看板工具、素材索引工具。
- `cases/生活服务广告投放导演_喜茶_20260529/`：喜茶案例，停在即梦视频生成前。
- `cases/生活服务广告投放导演_吉利汽车_20260610/`：吉利汽车案例，停在即梦视频生成前。

## 安装到 Codex

克隆仓库后，把 `skill/` 复制到本机 Codex skills 目录：

```bash
mkdir -p ~/.codex/skills/life-service-ad-director
rsync -a --delete skill/ ~/.codex/skills/life-service-ad-director/
```

然后在 Codex 里用下面这种方式触发：

```text
用 $life-service-ad-director 为一家上海火锅店生成 9:16 信息流广告投放素材包，先停在即梦视频生成前。
```

## 快速开始

创建一个新商家项目骨架：

```bash
python3 skill/scripts/scaffold_project.py "某某商家" --root ./work
```

生成字幕包：

```bash
python3 skill/scripts/subtitle_pipeline.py ./work/生活服务广告投放导演_某某商家_YYYYMMDD
```

生成资产索引和结果看板：

```bash
python3 skill/scripts/asset_manifest.py ./work/生活服务广告投放导演_某某商家_YYYYMMDD
python3 skill/scripts/delivery_dashboard.py ./work/生活服务广告投放导演_某某商家_YYYYMMDD
```

更多说明见：

- [快速使用指南](docs/QUICKSTART.md)
- [案例索引](docs/CASE_INDEX.md)
- [发布检查清单](docs/RELEASE_CHECKLIST.md)
- [安全说明](SECURITY.md)

## 工作流

1. 生成项目简报、投放策略、创意方向、3 秒钩子库。
2. 生成 60 秒/30 秒/15 秒脚本、完整执行脚本。
3. 生成镜头表、站位图、关键帧 Prompt、Seedance Prompt。
4. 生成真人分镜图、正反打、25 宫格视觉方向。
5. 生成字幕包、剪映时间线、投流标题与素材变体。
6. 输出即梦批量任务表、manifest、复跑命令。
7. 在视频生成前暂停，等待即梦额度或人工确认。

## 案例说明

两个案例都保留了前置完整交付物，包括：

- `RESULTS.html`
- `RESULTS.md`
- `00_项目简报.md`
- `00A_全流程步骤展示.md`
- `00B_ViMax式制片调度.md`
- `04_60秒主广告脚本.md`
- `07A_完整执行脚本.md`
- `docs/`
- `asset_index/`
- `subtitles/`
- `videos/`
- `variants/*/images/storyboard/`

## 大文件策略

原始参考视频与临时自动粗剪视频未提交到仓库，原因：

- 避免 GitHub 大文件限制和仓库膨胀。
- 避免把外部参考素材误作为可公开素材发布。
- 当前流程按规则停在即梦视频生成前，不提交生成视频。

如需复跑视频生成，请在本地补齐参考视频后，进入案例目录查看：

- `24_视频生成暂停与复跑说明.md`
- `videos/dreamina_commands.sh`
- `videos/manifest.md`

## 仓库自检

提交前可以运行：

```bash
python3 tools/validate_repo.py
```

它会检查 skill 必需文件、案例看板、脚本可执行性，以及是否误提交视频大文件。
