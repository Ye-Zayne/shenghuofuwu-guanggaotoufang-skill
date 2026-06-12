# 发布检查清单

提交或发布新版本前，检查下面几项：

- [ ] `skill/SKILL.md` 的 description 能准确触发生活服务广告投放场景。
- [ ] `skill/agents/openai.yaml` 的展示名称和默认提示词与当前 Skill 一致。
- [ ] `skill/scripts/*.py` 可执行并能显示 `--help`。
- [ ] 新案例包含 `RESULTS.html`、`RESULTS.md`、`manifest.json`。
- [ ] 新案例包含 `99_执行状态.md`，并说明是否停在即梦前。
- [ ] 没有提交 `.mp4`、`.mov`、`.m4v`、`.webm` 等视频大文件。
- [ ] 没有提交 GitHub token、即梦账号、Cookie、API key 或其他密钥。
- [ ] `python3 tools/validate_repo.py` 通过。
- [ ] README 的安装命令仍然有效。

## 推荐提交命令

```bash
python3 tools/validate_repo.py
git status --short
git add .
git commit -m "Improve life service ad director skill"
git push
```

