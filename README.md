# Automated Job Application Tracker Skill

面向 Codex 的通用求职申请整理 skill：把手动提供的职位描述（JD）、招聘方备注或申请摘要，自动整理为结构统一、可持续更新的 Obsidian 求职记录。

本仓库同时包含：

- Codex skill 定义与使用参考；
- 一个仅依赖 Python 标准库的命令行工具；
- Obsidian Markdown 与 Bases 数据库生成逻辑；
- 覆盖职位分类、Markdown 渲染、文件命名和写入流程的测试。

> 本仓库只包含公开的 skill、实现和测试，不包含个人邮箱内容、求职追踪数据或用户私有 Vault 导出。

## 功能

- 从文本文件或标准输入读取 JD / profile；
- 接收公司、职位、状态、来源、地点、截止日期、联系人等字段；
- 根据文本关键词推断 `AI/ML`、`Quant`、`Research`、`Data Science`、`Education` 或 `Other` track；
- 生成带 YAML Properties 的 Obsidian Markdown 笔记；
- 写入指定 Obsidian Vault，并可同步生成 `Job Applications.base`；
- 保留原始职位文本，方便后续匹配邮件回复和更新已有记录；
- 支持 Codex 自动调用，也可以直接使用 CLI。

## 环境要求

- Python 3.11+
- 可选：Obsidian（仅在需要写入 Vault 或使用 Bases 视图时需要）

运行时不依赖第三方 Python 包。

## 安装到 Codex

```bash
git clone https://github.com/DengZhiyuan-math/automated-job-application-tracker-skill.git
cd automated-job-application-tracker-skill

python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e .

mkdir -p "$HOME/.codex/skills"
ln -s "$(pwd)/skills/organize-job-applications" \
  "$HOME/.codex/skills/organize-job-applications"
```

重新打开 Codex task 后，可以直接调用：

```text
$organize-job-applications 把这份职位描述整理并记录到我的 Obsidian 求职追踪库。
```

如果目标位置已经存在，请先确认其中没有需要保留的 skill，再自行移除旧链接或目录。

## 安装 CLI

### 从源码安装

```bash
git clone https://github.com/DengZhiyuan-math/automated-job-application-tracker-skill.git
cd automated-job-application-tracker-skill

python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e .
```

安装完成后检查命令：

```bash
manual-job-profile --help
```

也可以不安装，直接从源码运行：

```bash
PYTHONPATH=src python -m hermes.skills.manual_job_profile --help
```

## 快速开始

### 1. 从 JD 文件生成 Markdown

```bash
manual-job-profile \
  --input job.md \
  --company "Harmattan AI" \
  --role "Deep Learning Intern" \
  --status applied \
  --output ./job-notes/harmattan-ai-deep-learning-intern.md
```

### 2. 从剪贴板写入 Obsidian Vault

macOS：

```bash
pbpaste | manual-job-profile \
  --company "Harmattan AI" \
  --role "Deep Learning Intern" \
  --status drafting \
  --vault "$HOME/Obsidian/Main"
```

默认写入：

```text
<vault>/Hermes Job Tracker/Job Applications/
```

同时生成或刷新：

```text
<vault>/Hermes Job Tracker/Job Applications/Job Applications.base
```

如不希望创建 `.base` 文件，添加 `--no-base`。

### 3. 输出到终端

不传 `--vault` 或 `--output` 时，生成的 Markdown 会打印到标准输出：

```bash
manual-job-profile \
  --input job.md \
  --company "Example Labs" \
  --role "Research Engineer"
```

## 输出模式

| 参数 | 结果 |
| --- | --- |
| `--vault <path>` | 写入 Vault 下的目标文件夹，并默认刷新 Bases 文件 |
| `--output <path>` | 写入指定 Markdown 文件 |
| 两者都不传 | 将 Markdown 打印到标准输出 |

当 `--output` 和 `--vault` 同时传入时，笔记写入 `--output` 指定的位置；只要提供了 `--vault` 且未设置 `--no-base`，仍会刷新 Vault 中的 Bases 文件。

## 参数

| 参数 | 说明 | 默认值 |
| --- | --- | --- |
| `--input` | JD / profile 文本文件；不传时从标准输入读取 | 标准输入 |
| `--vault` | Obsidian Vault 根目录 | 无 |
| `--folder` | Vault 内的目标文件夹 | `Hermes Job Tracker/Job Applications` |
| `--output` | 直接指定 Markdown 输出文件 | 无 |
| `--no-base` | 写入 Vault 时不生成 `.base` 文件 | 关闭 |
| `--company` | 公司名称 | `Unknown Company` |
| `--role` | 职位名称 | `Unknown Role` |
| `--status` | 申请状态 | `drafting` |
| `--track` | 手动指定职位方向；不传时从文本推断 | 自动推断 |
| `--source` | 来源，例如 `manual`、`email`、`linkedin` | `manual` |
| `--location` | 工作地点 | `unknown` |
| `--deadline` | 申请或测评截止日期 | `unknown` |
| `--contact` | 招聘方或联系人 | `unknown` |
| `--application-date` | 申请日期 | 当天日期 |
| `--notes` | 写入 Hermes Notes 的初始备注 | 空 |

## 支持的申请状态

```text
drafting
applied
confirmation_received
waiting
recruiter_replied
interview_scheduled
assessment_pending
assessment_submitted
rejected
offer
withdrawn
no_response
```

状态中的空格会被转换为下划线；不在上述列表中的值会导致命令报错。

以下状态会被标记为 `needs_action: true`：

```text
drafting
waiting
recruiter_replied
interview_scheduled
assessment_pending
```

## 生成内容

每条申请记录包含：

- Obsidian YAML Properties；
- 公司、职位、状态、track、日期、来源、地点和联系人；
- `needs_action` 标记；
- `Snapshot`、`Next Action`、`Fit Notes`、`Hermes Notes` 等区块；
- 完整的原始 JD / profile 文本。

默认文件名格式：

```text
YYYY-MM-DD-<company>-<role>.md
```

`Job Applications.base` 提供 `Active`、`Needs Action` 和 `All Applications` 三个表格视图。

## Codex Skill

Skill 入口位于：

```text
skills/organize-job-applications/SKILL.md
```

扩展说明位于：

```text
skills/organize-job-applications/references/manual_job_profile.md
```

将 `skills/organize-job-applications` 保持原结构放入或链接到 `~/.codex/skills/`。skill 会优先调用已安装的 `manual-job-profile` 命令；因此还需要按上面的方式安装 CLI。

生成的 Markdown 仍保留 `Hermes Notes` 和 `hermes/job-tracker` 等兼容字段，避免破坏已有 Obsidian 数据。

## 项目结构

```text
.
├── skills/organize-job-applications/
│   ├── SKILL.md
│   ├── agents/openai.yaml
│   └── references/manual_job_profile.md
├── src/hermes/skills/manual_job_profile.py
├── tests/test_manual_job_profile.py
├── pyproject.toml
└── README.md
```

## 开发与测试

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
```

当前测试覆盖：

- track 推断；
- Markdown 主要区块渲染；
- 默认文件名清理；
- CLI 写入笔记和 Obsidian Bases 文件。

修改实现后，建议同时运行测试并检查：

```bash
PYTHONPATH=src python -m hermes.skills.manual_job_profile --help
```

## 数据与隐私

工具在本地读取和写入文本，不会主动上传 JD、联系人或申请记录。请不要把真实 Vault、邮箱导出、访问令牌或包含个人信息的生成文件提交到公开仓库。

## 维护约定

核心实现位于 `src/hermes/skills/manual_job_profile.py`。如果 README、skill 参考文档与代码行为不一致，以代码和测试为准，并同步更新文档。

## License

项目包元数据声明为 MIT License。
